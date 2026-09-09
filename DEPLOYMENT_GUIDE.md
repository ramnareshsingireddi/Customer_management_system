# Deployment Guide - Customer Management Application

Complete guide to deploy the Customer Management Application to various platforms.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Heroku Deployment](#heroku-deployment)
3. [AWS Deployment](#aws-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [Railway Deployment](#railway-deployment)
6. [Vercel (Frontend Only)](#vercel-frontend-only)
7. [Production Configuration](#production-configuration)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass
- [ ] JWT_SECRET_KEY changed to strong random value
- [ ] Database credentials secured
- [ ] HTTPS enabled
- [ ] CORS origins configured correctly
- [ ] Environment variables set
- [ ] Database backups configured
- [ ] Error logging enabled
- [ ] Performance optimization complete
- [ ] Security audit passed

### Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS only
- [ ] Configure firewall rules
- [ ] Set up SSL certificates
- [ ] Enable database encryption
- [ ] Configure backup retention
- [ ] Set up monitoring alerts
- [ ] Review access controls

---

## Heroku Deployment

### Easy Deployment with Heroku

Heroku is the easiest option for beginners with built-in PostgreSQL support.

### Step 1: Install Heroku CLI

Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

```bash
# Verify installation
heroku --version
```

### Step 2: Create Heroku Account

Sign up at [heroku.com](https://www.heroku.com)

### Step 3: Login to Heroku

```bash
heroku login
```

### Step 4: Create Heroku App

```bash
# Create app
heroku create your-app-name

# Verify
heroku apps
```

### Step 5: Add PostgreSQL

```bash
# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev --app your-app-name

# Check add-ons
heroku addons --app your-app-name
```

### Step 6: Set Environment Variables

```bash
heroku config:set JWT_SECRET_KEY="your-strong-secret-key" --app your-app-name
heroku config:set FLASK_ENV="production" --app your-app-name
heroku config:set FLASK_DEBUG="False" --app your-app-name

# Verify
heroku config --app your-app-name
```

### Step 7: Create Procfile

Create a `Procfile` in project root:

```
web: gunicorn app:app
release: python app.py
```

### Step 8: Update Requirements

Add gunicorn for production:

```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 9: Deploy

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Add Heroku remote (if not done automatically)
heroku git:remote -a your-app-name

# Push to Heroku
git push heroku main
```

### Step 10: Open Application

```bash
heroku open --app your-app-name
```

### Troubleshooting Heroku

```bash
# View logs
heroku logs --tail --app your-app-name

# Run database migrations
heroku run python app.py --app your-app-name

# SSH into dyno
heroku ps:exec --app your-app-name
```

---

## AWS Deployment

### EC2 + RDS Deployment

More control with AWS infrastructure.

### Step 1: Create EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose Amazon Linux 2 or Ubuntu 20.04 LTS
4. Select t3.micro (free tier eligible)
5. Configure security groups:
   - Allow SSH (22) from your IP
   - Allow HTTP (80) from anywhere
   - Allow HTTPS (443) from anywhere
6. Launch and download key pair (.pem file)

### Step 2: Connect to EC2

```bash
# Make key readable
chmod 400 your-key.pem

# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3
sudo yum install python3 python3-pip -y

# Install PostgreSQL client
sudo yum install postgresql -y

# Install Node.js
curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install nodejs -y
```

### Step 4: Create RDS Database

1. Go to AWS Console → RDS
2. Create Database
3. Choose PostgreSQL
4. Use db.t3.micro (free tier)
5. Set master username and password
6. Disable public accessibility initially
7. Create security group allowing inbound on port 5432
8. Note the endpoint

### Step 5: Clone Project

```bash
# Install git
sudo yum install git -y

# Clone repository
git clone https://github.com/your-username/customer-management-app.git
cd customer-management-app
```

### Step 6: Deploy Backend

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
nano .env
# Enter your RDS endpoint and credentials

# Run tests
python -m pytest

# Start with gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Step 7: Deploy Frontend

```bash
# Navigate to frontend directory
cd customer-app

# Install dependencies
npm install

# Build
npm run build

# Install and start serve
sudo npm install -g serve
serve -s build -l 3000 &
```

### Step 8: Set Up Nginx Reverse Proxy

```bash
# Install Nginx
sudo yum install nginx -y

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure (edit /etc/nginx/nginx.conf)
sudo nano /etc/nginx/nginx.conf
```

Add to `http` block:

```nginx
upstream backend {
    server localhost:5000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 9: SSL Certificate

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot-renew
```

---

## DigitalOcean Deployment

### App Platform (Easiest)

### Step 1: Create GitHub Repository

Push your code to GitHub.

### Step 2: Create DigitalOcean Account

Sign up at [digitalocean.com](https://www.digitalocean.com)

### Step 3: Create App

1. Go to App Platform
2. Click "Create App"
3. Connect GitHub repository
4. Choose branch (main)
5. Configure apps:
   - Backend: Python/Flask
   - Frontend: Node.js/React
6. Add database: PostgreSQL

### Step 4: Set Environment Variables

In App settings:

```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=your-strong-key
FLASK_ENV=production
```

### Step 5: Deploy

Click "Deploy" and wait for build and deploy to complete.

---

## Railway Deployment

### One-Click Deployment

1. Go to [railway.app](https://railway.app)
2. Connect GitHub
3. Select repository
4. Railway auto-detects services
5. Add PostgreSQL plugin
6. Set environment variables
7. Deploy

---

## Vercel (Frontend Only)

### Deploy React to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Build React App

```bash
cd customer-app
npm run build
```

### Step 3: Deploy

```bash
vercel --prod
```

### Step 4: Update API Endpoint

Set environment variable in Vercel:

```
REACT_APP_API_URL=https://your-backend-domain.com/api
```

---

## Production Configuration

### Environment Variables (Production)

Create `.env.production`:

```
# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# Security
JWT_SECRET_KEY=generate-strong-random-key-here
JWT_ACCESS_TOKEN_EXPIRES=86400

# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# CORS
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/app.log
```

### Generate Strong Secret Key

```bash
# Using Python
python -c "import os; print(os.urandom(32).hex())"

# Using OpenSSL
openssl rand -hex 32
```

### Database Backups

```bash
# PostgreSQL backup
pg_dump -U user -h host database_name > backup.sql

# Automated backup (cron job)
# Add to crontab -e:
0 2 * * * pg_dump -U user -h localhost db > /backups/db_$(date +\%Y\%m\%d).sql
```

### SSL/HTTPS Configuration

```bash
# Get free SSL from Let's Encrypt
sudo certbot certonly --standalone -d your-domain.com

# Configure in Nginx
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
```

### Performance Optimization

```python
# Add caching to Flask
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# Use connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "pool_size": 10,
    "max_overflow": 20,
}
```

---

## Monitoring & Maintenance

### Logging Setup

```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    app.logger.addHandler(handler)
```

### Health Checks

Set up monitoring endpoint:

```python
@app.route('/api/health')
def health():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'healthy'}, 200
    except:
        return {'status': 'unhealthy'}, 500
```

### Uptime Monitoring

Services to monitor uptime:
- UptimeRobot
- Pingdom
- New Relic
- Datadog
- CloudWatch

### Performance Monitoring

```bash
# Install APM agent
pip install newrelic

# Configure
newrelic-admin run-program gunicorn app:app
```

### Database Maintenance

```sql
-- Regular maintenance
VACUUM ANALYZE;
REINDEX DATABASE customer_db;

-- Monitor slow queries
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();
```

### Auto-Scaling

Configure auto-scaling based on:
- CPU usage > 70%
- Memory usage > 80%
- Request count > 1000/min

---

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
      
      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          git push https://heroku:$HEROKU_API_KEY@git.heroku.com/your-app.git main
```

---

## Cost Estimation (Monthly)

| Platform | Cost | Tier |
|----------|------|------|
| Heroku | $50+ | Hobby + PostgreSQL |
| AWS | $20-100+ | EC2 + RDS |
| DigitalOcean | $12-50+ | Droplet + Database |
| Railway | $5-50+ | Pay-as-you-go |
| Vercel | $0-50+ | Free + Pro |

---

## Rollback Plan

```bash
# Heroku rollback
heroku releases --app your-app
heroku rollback v5 --app your-app

# GitHub rollback
git revert <commit-hash>
git push origin main
```

---

## Post-Deployment

1. Verify application is running
2. Test all CRUD operations
3. Check logs for errors
4. Monitor performance
5. Set up backups
6. Configure monitoring
7. Document deployment process
8. Brief team on access procedures

---

## Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check backend logs, verify database connection |
| CORS Error | Check CORS_ORIGINS configuration |
| Database Connection Failed | Verify connection string, firewall rules |
| Out of Memory | Increase instance size, optimize queries |
| Slow Performance | Enable caching, optimize queries, add CDN |

---

## Support Resources

- [Heroku Documentation](https://devcenter.heroku.com)
- [AWS Documentation](https://docs.aws.amazon.com)
- [DigitalOcean Docs](https://docs.digitalocean.com)
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)

---

**Last Updated:** 2024
**Version:** 1.0.0
