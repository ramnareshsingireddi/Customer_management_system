from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
import secrets
import urllib.parse
import requests
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///customer.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Google OAuth & Frontend Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '').strip()
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '').strip()
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback').strip()
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3003').rstrip('/')

# Groq AI Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '').strip()
GROQ_MODEL = os.getenv('GROQ_MODEL', 'qwen/qwen3.8-27b').strip()
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

cors_origins_env = os.getenv('CORS_ORIGINS', '').strip()
if cors_origins_env == '*':
    cors_origins = '*'
elif cors_origins_env:
    cors_origins = [o.strip() for o in cors_origins_env.split(',') if o.strip()]
else:
    cors_origins = [
        'http://localhost:3003',
        'http://localhost:3000',
        'http://localhost:5000',
        'http://localhost:5173'
    ]

if FRONTEND_URL and isinstance(cors_origins, list) and FRONTEND_URL not in cors_origins:
    cors_origins.append(FRONTEND_URL)

CORS(app, origins=cors_origins, supports_credentials=True)


# ==================== Database Models ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='local', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to owned customers with cascade deletion
    customers = db.relationship('Customer', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        if password:
            self.password = generate_password_hash(password)
        else:
            self.password = None
    
    def check_password(self, password):
        if not self.password or not password:
            return False
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'auth_provider': self.auth_provider or 'local',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite index for efficient per-user lookups and unique email per user
    __table_args__ = (
        db.UniqueConstraint('user_id', 'email', name='uq_user_customer_email'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==================== Authentication Routes ====================

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint supporting username or email"""
    try:
        data = request.get_json()
        
        identifier = (data.get('username') or data.get('email') or '').strip() if data else ''
        password = data.get('password') if data else ''
        
        if not identifier or not password:
            return jsonify({'message': 'Missing username/email or password'}), 400
        
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
        
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if not user.password and user.google_id:
            return jsonify({
                'message': 'This account was created with Google. Please use "Continue with Google" to sign in.'
            }), 400
        
        if not user.check_password(password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint supporting username, email, and password"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Missing username or password'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip() or None
        password = data.get('password')
        
        if len(password) < 4:
            return jsonify({'message': 'Password must be at least 4 characters long'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 409
        
        if email and User.query.filter_by(email=email).first():
            return jsonify({'message': 'An account with this email already exists'}), 409
        
        user = User(
            username=username,
            email=email,
            auth_provider='local'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Registration successful',
            'token': access_token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get current authenticated user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/auth/google', methods=['GET', 'POST'])
def google_auth():
    """
    GET: Redirects user to Google OAuth 2.0 consent screen, or returns auth URL
    POST: Exchanges Google ID token or authorization code directly for app JWT
    """
    if request.method == 'GET':
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or 'your-google' in GOOGLE_CLIENT_ID:
            # Informative redirect or JSON if credentials are not configured yet
            msg = 'Google OAuth credentials are not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in backend/.env'
            if request.headers.get('Accept') == 'application/json':
                return jsonify({'message': msg, 'configured': False}), 400
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote(msg)}")
        
        state = secrets.token_urlsafe(16)
        params = {
            'client_id': GOOGLE_CLIENT_ID,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'select_account',
            'state': state
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        
        if request.args.get('format') == 'json' or request.headers.get('Accept') == 'application/json':
            return jsonify({'auth_url': auth_url}), 200
        
        return redirect(auth_url)
    
    # POST handling (direct token or code exchange from client)
    try:
        data = request.get_json() or {}
        id_token_str = data.get('id_token')
        code = data.get('code')
        
        if not id_token_str and not code:
            return jsonify({'message': 'Missing Google id_token or authorization code'}), 400
        
        user_info = None
        
        if id_token_str:
            # Verify ID token cryptographically
            try:
                user_info = google_id_token.verify_oauth2_token(
                    id_token_str, 
                    google_requests.Request(), 
                    GOOGLE_CLIENT_ID
                )
            except Exception as e:
                return jsonify({'message': f'Invalid Google ID token: {str(e)}'}), 401
        elif code:
            # Exchange code for tokens
            token_resp = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_CLIENT_SECRET,
                    'redirect_uri': GOOGLE_REDIRECT_URI,
                    'grant_type': 'authorization_code'
                },
                timeout=10
            )
            if not token_resp.ok:
                return jsonify({'message': 'Failed to exchange authorization code with Google'}), 400
            token_data = token_resp.json()
            if 'id_token' in token_data:
                user_info = google_id_token.verify_oauth2_token(
                    token_data['id_token'],
                    google_requests.Request(),
                    GOOGLE_CLIENT_ID
                )
            elif 'access_token' in token_data:
                profile_resp = requests.get(
                    'https://www.googleapis.com/oauth2/v3/userinfo',
                    headers={'Authorization': f"Bearer {token_data['access_token']}"},
                    timeout=10
                )
                if profile_resp.ok:
                    user_info = profile_resp.json()
        
        if not user_info or not user_info.get('email'):
            return jsonify({'message': 'Unable to retrieve verified Google profile'}), 400
        
        google_id = str(user_info.get('sub'))
        google_email = user_info.get('email').lower().strip()
        google_name = user_info.get('name') or google_email.split('@')[0]
        
        user, token = resolve_google_user(google_id, google_email, google_name)
        return jsonify({
            'message': 'Google authentication successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/auth/google/callback', methods=['GET'])
def google_callback():
    """OAuth 2.0 callback endpoint invoked by Google after user consent"""
    try:
        # Check for error returned by Google
        error = request.args.get('error')
        if error:
            error_desc = request.args.get('error_description') or 'Google authentication was cancelled or failed'
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote(error_desc)}")
        
        code = request.args.get('code')
        if not code:
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote('Authorization code missing from Google response')}")
        
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote('Google OAuth credentials not configured on backend')}")
        
        # Exchange authorization code for tokens
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'redirect_uri': GOOGLE_REDIRECT_URI,
                'grant_type': 'authorization_code'
            },
            headers={'Accept': 'application/json'},
            timeout=10
        )
        
        if not token_response.ok:
            error_msg = 'Failed to exchange authorization code with Google.'
            try:
                err_data = token_response.json()
                if 'error_description' in err_data:
                    error_msg += f" {err_data['error_description']}"
            except Exception:
                pass
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote(error_msg)}")
        
        token_data = token_response.json()
        raw_id_token = token_data.get('id_token')
        access_token_google = token_data.get('access_token')
        user_info = None
        
        # Cryptographically verify ID token if available
        if raw_id_token:
            try:
                user_info = google_id_token.verify_oauth2_token(
                    raw_id_token,
                    google_requests.Request(),
                    GOOGLE_CLIENT_ID
                )
            except Exception as e:
                print(f"ID Token verification warning: {e}")
        
        # Fallback to Google userinfo endpoint if ID token parsing was not available
        if not user_info and access_token_google:
            userinfo_resp = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f"Bearer {access_token_google}"},
                timeout=10
            )
            if userinfo_resp.ok:
                user_info = userinfo_resp.json()
        
        if not user_info or not user_info.get('email'):
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote('Unable to verify Google profile and email')}")
        
        # Validate that email is verified by Google
        if not user_info.get('email_verified', False) and user_info.get('verified_email') is not True:
            return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote('Google email is not verified')}")
        
        google_id = str(user_info.get('sub'))
        google_email = user_info.get('email').lower().strip()
        google_name = user_info.get('name') or google_email.split('@')[0]
        
        user, jwt_token = resolve_google_user(google_id, google_email, google_name)
        
        # Redirect to frontend with JWT token
        return redirect(f"{FRONTEND_URL}/?token={jwt_token}")
        
    except Exception as e:
        return redirect(f"{FRONTEND_URL}/?error={urllib.parse.quote(f'Google OAuth error: {str(e)}')}")


def resolve_google_user(google_id, google_email, google_name):
    """
    Find existing user or safely create/link Google account,
    then issue standard application JWT.
    """
    # 1. Check if user already exists by google_id
    user = User.query.filter_by(google_id=google_id).first()
    
    if not user:
        # 2. Check if user already exists by email (safe linking)
        user = User.query.filter_by(email=google_email).first()
        if user:
            user.google_id = google_id
            if user.auth_provider == 'local':
                user.auth_provider = 'both'
            elif not user.auth_provider:
                user.auth_provider = 'google'
            db.session.commit()
    
    if not user:
        # 3. New user - create account
        # Generate a unique username derived from email or name
        base_username = google_email.split('@')[0].replace('.', '_')
        if len(base_username) > 60:
            base_username = base_username[:60]
        username = base_username
        suffix = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}_{suffix}"
            suffix += 1
        
        user = User(
            username=username,
            email=google_email,
            google_id=google_id,
            auth_provider='google',
            password=None
        )
        db.session.add(user)
        db.session.commit()
    
    # Generate standard application JWT
    jwt_token = create_access_token(identity=str(user.id))
    return user, jwt_token



# ==================== Customer Routes ====================

@app.route('/api/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """Get all customers for the authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        customers = Customer.query.filter_by(user_id=current_user_id).order_by(Customer.created_at.desc()).all()
        return jsonify({
            'customers': [customer.to_dict() for customer in customers]
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/customers/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Get customer by ID scoped strictly to authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user_id).first()
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        return jsonify(customer.to_dict()), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/api/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """Create a new customer for the authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'message': 'Name and email are required'}), 400
        
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        
        # Check if email already exists for THIS user
        if Customer.query.filter_by(user_id=current_user_id, email=email).first():
            return jsonify({'message': 'A customer with this email already exists in your account'}), 409
        
        customer = Customer(
            user_id=current_user_id,
            name=name,
            email=email,
            phone=data.get('phone', '').strip(),
            company=data.get('company', '').strip(),
            address=data.get('address', '').strip()
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer created successfully',
            'customer': customer.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """Update a customer strictly owned by the authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user_id).first()
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data and data['name']:
            customer.name = data['name'].strip()
        if 'email' in data and data['email']:
            new_email = data['email'].strip()
            # Check if new email already exists for another customer of THIS user
            existing = Customer.query.filter_by(user_id=current_user_id, email=new_email).first()
            if existing and existing.id != customer_id:
                return jsonify({'message': 'A customer with this email already exists in your account'}), 409
            customer.email = new_email
        if 'phone' in data:
            customer.phone = str(data['phone'] or '').strip()
        if 'company' in data:
            customer.company = str(data['company'] or '').strip()
        if 'address' in data:
            customer.address = str(data['address'] or '').strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """Delete a customer strictly owned by the authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user_id).first()
        
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({'message': 'Customer deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/customers/search', methods=['GET'])
@jwt_required()
def search_customers():
    """Search customers strictly within the authenticated user's records"""
    try:
        current_user_id = int(get_jwt_identity())
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'customers': []}), 200
        
        customers = Customer.query.filter(
            Customer.user_id == current_user_id,
            (
                (Customer.name.ilike(f'%{query}%')) |
                (Customer.email.ilike(f'%{query}%')) |
                (Customer.company.ilike(f'%{query}%')) |
                (Customer.phone.ilike(f'%{query}%'))
            )
        ).order_by(Customer.created_at.desc()).all()
        
        return jsonify({
            'customers': [customer.to_dict() for customer in customers]
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# ==================== Groq AI Features ====================

@app.route('/api/ai/chat', methods=['POST'])
@jwt_required()
def ai_chat():
    """
    AI Customer Copilot chat endpoint with user-isolated natural language CRUD capabilities.
    Executes database operations scoped strictly to the authenticated user.
    """
    try:
        if not GROQ_API_KEY:
            return jsonify({'message': 'Groq API key is not configured in backend/.env'}), 400
        
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({'message': 'Message is required'}), 400
        
        # Pull live customer records ONLY for the authenticated user
        user_customers = Customer.query.filter_by(user_id=current_user_id).order_by(Customer.created_at.desc()).all()
        customers_context = []
        for c in user_customers:
            customers_context.append({
                'id': c.id,
                'name': c.name,
                'email': c.email,
                'phone': c.phone or '',
                'company': c.company or '',
                'address': c.address or ''
            })
        
        system_prompt = (
            "You are the intelligent AI Copilot and Database Operator for this Customer Management System (CMS).\n"
            "You have complete access to the current authenticated user's customer database and have the power to EXECUTE database operations directly!\n\n"
            "Current User's Customer Records in Database:\n"
            f"{json.dumps(customers_context, indent=2)}\n\n"
            "Instructions:\n"
            "You MUST ALWAYS respond with a strictly valid JSON object matching this schema:\n"
            "{\n"
            "  \"action\": \"create\" | \"update\" | \"delete\" | \"none\",\n"
            "  \"data\": {\n"
            "    \"id\": integer or null (used for update or delete),\n"
            "    \"target_email\": string or null (used to locate customer if id not given),\n"
            "    \"target_name\": string or null (used to locate customer if id not given),\n"
            "    \"name\": string or null (customer name for create or update),\n"
            "    \"email\": string or null (customer email for create or update),\n"
            "    \"phone\": string or null,\n"
            "    \"company\": string or null,\n"
            "    \"address\": string or null\n"
            "  },\n"
            "  \"reply\": \"Clear, helpful message explaining what you did or answering the user's question.\"\n"
            "}\n\n"
            "Action Rules:\n"
            "- When user wants to add/create/register a customer: set action=\"create\", extract all details into data, write a clear reply.\n"
            "- When user wants to update/edit/change a customer's info: set action=\"update\", identify customer by id/email/name, specify new values in data, write a clear reply.\n"
            "- When user wants to delete/remove a customer: set action=\"delete\", identify customer in data, write a clear reply.\n"
            "- When user asks a general question, analysis, or advice: set action=\"none\", data={}, answer the question thoroughly in reply.\n"
            "Return only valid JSON."
        )
        
        messages = [{'role': 'system', 'content': system_prompt}]
        
        # Append recent conversation history (up to last 6 turns)
        for h in history[-6:]:
            role = 'user' if h.get('role') == 'user' else 'assistant'
            if h.get('content'):
                messages.append({'role': role, 'content': str(h.get('content'))})
        
        messages.append({'role': 'user', 'content': user_message})
        
        groq_resp = requests.post(
            GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': GROQ_MODEL,
                'messages': messages,
                'temperature': 0.2,
                'response_format': {'type': 'json_object'},
                'max_tokens': 800
            },
            timeout=25
        )
        
        if not groq_resp.ok:
            err_msg = 'Groq API error'
            try:
                err_data = groq_resp.json()
                if 'error' in err_data:
                    err_msg = err_data['error'].get('message', err_msg)
            except Exception:
                pass
            return jsonify({'message': f'AI Service error: {err_msg}'}), groq_resp.status_code
        
        raw_content = groq_resp.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        parsed = {}
        try:
            parsed = json.loads(raw_content)
        except Exception:
            parsed = {'action': 'none', 'data': {}, 'reply': raw_content}
        
        action = parsed.get('action', 'none')
        action_data = parsed.get('data') or {}
        reply_text = parsed.get('reply') or ''
        
        action_performed = None
        action_details = None
        
        # ======================================================================
        # Execute Database CRUD Operations (Strictly Scoped to Authenticated User)
        # ======================================================================
        if action == 'create':
            name = action_data.get('name', '').strip()
            email = action_data.get('email', '').strip()
            
            if not name:
                name = 'New Customer'
            if not email:
                email = f"{name.lower().replace(' ', '_')}@example.com"
            
            existing = Customer.query.filter_by(user_id=current_user_id, email=email).first()
            if existing:
                reply_text = f"Notice: A customer with email '{email}' already exists in your account ({existing.name} - {existing.company or 'N/A'}). Record was not duplicated."
            else:
                new_customer = Customer(
                    user_id=current_user_id,
                    name=name,
                    email=email,
                    phone=action_data.get('phone') or '',
                    company=action_data.get('company') or '',
                    address=action_data.get('address') or ''
                )
                db.session.add(new_customer)
                db.session.commit()
                action_performed = 'create'
                action_details = new_customer.to_dict()
                reply_text = f"✓ **Created Customer**: **{new_customer.name}** ({new_customer.email}) &bull; Company: {new_customer.company or 'None'} (ID #{new_customer.id}).\n\n{reply_text}"
        
        elif action == 'update':
            target_id = action_data.get('id')
            target_email = action_data.get('target_email') or action_data.get('email')
            target_name = action_data.get('target_name') or action_data.get('name')
            
            target_cust = None
            if target_id:
                target_cust = Customer.query.filter_by(id=int(target_id), user_id=current_user_id).first()
            if not target_cust and target_email:
                target_cust = Customer.query.filter(Customer.user_id == current_user_id, Customer.email.ilike(target_email.strip())).first()
            if not target_cust and target_name:
                target_cust = Customer.query.filter(Customer.user_id == current_user_id, Customer.name.ilike(f"%{target_name.strip()}%")).first()
            
            if target_cust:
                if action_data.get('name'):
                    target_cust.name = action_data['name'].strip()
                if action_data.get('email'):
                    new_email = action_data['email'].strip()
                    duplicate = Customer.query.filter_by(user_id=current_user_id, email=new_email).first()
                    if not duplicate or duplicate.id == target_cust.id:
                        target_cust.email = new_email
                if 'phone' in action_data and action_data['phone'] is not None:
                    target_cust.phone = str(action_data['phone']).strip()
                if 'company' in action_data and action_data['company'] is not None:
                    target_cust.company = str(action_data['company']).strip()
                if 'address' in action_data and action_data['address'] is not None:
                    target_cust.address = str(action_data['address']).strip()
                
                db.session.commit()
                action_performed = 'update'
                action_details = target_cust.to_dict()
                reply_text = f"✓ **Updated Customer**: **{target_cust.name}** (ID #{target_cust.id}).\n\n{reply_text}"
            else:
                reply_text = "Could not find a matching customer in your account to update. Please specify their name or email."
        
        elif action == 'delete':
            target_id = action_data.get('id')
            target_email = action_data.get('target_email')
            target_name = action_data.get('target_name')
            
            target_cust = None
            if target_id:
                target_cust = Customer.query.filter_by(id=int(target_id), user_id=current_user_id).first()
            if not target_cust and target_email:
                target_cust = Customer.query.filter(Customer.user_id == current_user_id, Customer.email.ilike(target_email.strip())).first()
            if not target_cust and target_name:
                target_cust = Customer.query.filter(Customer.user_id == current_user_id, Customer.name.ilike(f"%{target_name.strip()}%")).first()
            
            if target_cust:
                cust_info = target_cust.to_dict()
                db.session.delete(target_cust)
                db.session.commit()
                action_performed = 'delete'
                action_details = cust_info
                reply_text = f"✓ **Deleted Customer**: **{cust_info['name']}** ({cust_info['email']}) from your account.\n\n{reply_text}"
            else:
                reply_text = "Could not find a matching customer in your account to delete. Please specify the exact name or email."
        
        return jsonify({
            'reply': reply_text,
            'action_performed': action_performed,
            'action_details': action_details,
            'model': GROQ_MODEL
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error communicating with AI service: {str(e)}'}), 500


@app.route('/api/ai/draft-email', methods=['POST'])
@jwt_required()
def ai_draft_email():
    """
    Drafts tailored customer outreach emails strictly for customers owned by authenticated user.
    """
    try:
        if not GROQ_API_KEY:
            return jsonify({'message': 'Groq API key is not configured in backend/.env'}), 400
        
        current_user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        customer_id = data.get('customer_id')
        goal = data.get('goal', 'check_in')
        custom_instructions = data.get('notes', '').strip()
        
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user_id).first() if customer_id else None
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        
        goal_prompts = {
            'check_in': 'Draft a friendly, professional quarterly check-in email to see how they are doing and ask if they need support.',
            'proposal': 'Draft a persuasive business proposal or renewal pitch highlighting how our customer success team can deliver greater value.',
            'meeting': 'Draft a concise meeting invitation request proposing a brief 20-minute catch-up call next week.',
            'custom': f'Draft an email tailored to the customer following these specific instructions: {custom_instructions}'
        }
        
        instructions = goal_prompts.get(goal, goal_prompts['check_in'])
        if custom_instructions and goal != 'custom':
            instructions += f"\nAdditional Context / Custom Notes: {custom_instructions}"
        
        system_prompt = (
            "You are a professional enterprise sales and client relationship management specialist. "
            "Your task is to write high-converting, courteous, personalized business emails to clients.\n"
            "Respond strictly in valid JSON format with two keys:\n"
            "\"subject\": \"<concise compelling email subject line>\",\n"
            "\"body\": \"<the full professional email body with greeting, paragraphs, and sign-off placeholders like [Your Name] / [Your Title]>\"\n"
            "Do not wrap in markdown quotes or extra backticks if possible, just pure valid JSON."
        )
        
        user_prompt = (
            f"Customer Profile:\n"
            f"- Name: {customer.name}\n"
            f"- Email: {customer.email}\n"
            f"- Company: {customer.company or 'N/A'}\n"
            f"- Phone: {customer.phone or 'N/A'}\n"
            f"- Address: {customer.address or 'N/A'}\n\n"
            f"Objective:\n{instructions}"
        )
        
        groq_resp = requests.post(
            GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 800
            },
            timeout=25
        )
        
        if not groq_resp.ok:
            return jsonify({'message': 'Failed to generate email draft from AI service'}), groq_resp.status_code
        
        content = groq_resp.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Parse JSON output from content
        parsed = {}
        try:
            cleaned = content
            if cleaned.startswith('```'):
                lines = cleaned.splitlines()
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                cleaned = '\n'.join(lines).strip()
            parsed = json.loads(cleaned)
        except Exception:
            lines = content.splitlines()
            subject = f"Following up with {customer.name} - {customer.company}" if customer.company else f"Following up - {customer.name}"
            body = content
            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line.split(':', 1)[1].strip()
                    body = '\n'.join([l for l in lines if l != line]).strip()
                    break
            parsed = {'subject': subject, 'body': body}
        
        return jsonify({
            'subject': parsed.get('subject', 'Customer Follow-up'),
            'body': parsed.get('body', content),
            'customer': customer.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error drafting email: {str(e)}'}), 500


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'API is running'}), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500


# ==================== Database Initialization & Safe Migration ====================

def init_db():
    """Initialize database, run safe non-destructive migrations, and purge legacy demo data"""
    with app.app_context():
        # 1. Run migrations for schema changes prior to ORM queries
        try:
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            is_postgres = db.engine.dialect.name == 'postgresql'
            
            with db.engine.connect() as conn:
                # Migrate 'users' table
                if 'users' in table_names:
                    user_cols = [c['name'] for c in inspector.get_columns('users')]
                    if 'email' not in user_cols:
                        conn.execute(db.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(120);" if is_postgres else "ALTER TABLE users ADD COLUMN email VARCHAR(120);"))
                    if 'google_id' not in user_cols:
                        conn.execute(db.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(100);" if is_postgres else "ALTER TABLE users ADD COLUMN google_id VARCHAR(100);"))
                    if 'auth_provider' not in user_cols:
                        conn.execute(db.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR(20) DEFAULT 'local';" if is_postgres else "ALTER TABLE users ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local';"))
                    if is_postgres:
                        try:
                            conn.execute(db.text("ALTER TABLE users ALTER COLUMN password DROP NOT NULL;"))
                        except Exception:
                            pass
                    conn.commit()

                # Migrate 'customers' table
                if 'customers' in table_names:
                    cust_cols = [c['name'] for c in inspector.get_columns('customers')]
                    if 'user_id' not in cust_cols:
                        if is_postgres:
                            conn.execute(db.text("ALTER TABLE customers ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE CASCADE;"))
                        else:
                            conn.execute(db.text("ALTER TABLE customers ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE;"))
                        conn.commit()
                        
                        # Assign any existing customer records without user_id to the first legitimate user if one exists
                        first_real_user = conn.execute(db.text("SELECT id FROM users WHERE username != 'demo' ORDER BY id ASC LIMIT 1;")).fetchone()
                        if first_real_user and first_real_user[0]:
                            conn.execute(db.text(f"UPDATE customers SET user_id = {first_real_user[0]} WHERE user_id IS NULL;"))
                            conn.commit()

        except Exception as mig_err:
            print(f"Migration notice: {mig_err}")

        # 2. Ensure all tables are created
        db.create_all()

        # 3. Clean up legacy mock/demo data if present
        try:
            # Remove demo user 'demo'
            legacy_demo_user = User.query.filter_by(username='demo').first()
            if legacy_demo_user:
                # Remove mock customers seeded with demo user
                Customer.query.filter_by(user_id=legacy_demo_user.id).delete()
                db.session.delete(legacy_demo_user)
                db.session.commit()
                print("Purged legacy demo user account.")
            
            # Remove any legacy unassigned sample customers
            sample_emails = ['john@example.com', 'jane@example.com', 'bob@example.com']
            deleted_samples = Customer.query.filter(
                (Customer.user_id.is_(None)) | 
                (Customer.email.in_(sample_emails) & Customer.name.in_(['John Doe', 'Jane Smith', 'Bob Johnson']))
            ).delete(synchronize_session=False)
            if deleted_samples:
                db.session.commit()
                print(f"Purged {deleted_samples} legacy mock customer records.")
        except Exception as cleanup_err:
            db.session.rollback()
            print(f"Cleanup notice: {cleanup_err}")


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug, host='0.0.0.0', port=port)

