# ==================== FRONTEND BUILD STAGE ====================
FROM node:18-alpine AS frontend

WORKDIR /app

# Build arguments for Vite environment variables
# Injected at build time during 'docker build --build-arg VITE_API_URL=...'
ARG VITE_API_URL=http://localhost:5000/api
ENV VITE_API_URL=$VITE_API_URL

# Copy package files from frontend directory
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy all frontend source files and configuration
COPY frontend/ ./

# Build the Vite application (bakes VITE_API_URL into the generated dist/ folder)
RUN npm run build

# ==================== PRODUCTION STAGE ====================
FROM node:18-alpine

WORKDIR /app

# Copy built frontend assets from builder stage
COPY --from=frontend /app/dist ./dist

# Install serve to serve static files
RUN npm install -g serve

# Expose default port
ENV PORT=3003
EXPOSE 3003

# Run the application using serve listening on dynamic Render $PORT or default 3003
CMD ["sh", "-c", "serve -s dist -l ${PORT:-3003}"]

