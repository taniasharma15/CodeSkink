# LifeLine Navigator Deployment Guide

This guide provides instructions for deploying LifeLine Navigator in various environments.

## 📋 Deployment Options

1. **Local Development** - For development and testing
2. **Docker Container** - For consistent deployment
3. **Streamlit Cloud** - For easy hosting
4. **Production Server** - For self-hosted deployment

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/lifeline-navigator.git
cd lifeline-navigator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Development Tips
- Use `streamlit run app.py --server.headless=false` to see the server console
- Enable auto-reload with `streamlit run app.py --server.runOnSave=true`
- Use `--server.port=8502` to run on a different port

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the image
docker build -t lifeline-navigator .

# Run with Docker Compose (recommended)
docker-compose up -d

# Or run directly
docker run -d --name lifeline-navigator -p 8501:8501 lifeline-navigator
```

### Production with Nginx
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f lifeline-navigator

# Stop services
docker-compose down
```

### Docker Configuration
The `Dockerfile` includes:
- Multi-stage build for smaller image size
- Non-root user for security
- Health checks
- Environment variables

### Environment Variables
Create a `.env` file:
```env
PYTHONUNBUFFERED=1
PORT=8501
HOST=0.0.0.0
```

## ☁️ Streamlit Cloud Deployment

### Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
5. Configure the app:
   - Main script: `app.py`
   - Requirements file: `requirements.txt`
   - Optional: Environment variables

### Streamlit Cloud Tips
- Set `server.headless=true` in `.streamlit/config.toml`
- Enable `showErrorDetails` for debugging
- Use `gatherUsageStats=false` to disable analytics

## 🖥️ Production Server Deployment

### Requirements
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.11+
- Nginx (for reverse proxy)
- Systemd (for process management)

### Step-by-Step Deployment

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv nginx curl

# Create application user
sudo useradd -m -s /bin/bash lifeline
```

#### 2. Deploy Application
```bash
# Switch to application user
sudo -u lifeline

# Clone repository
cd /home/lifeline
git clone https://github.com/yourusername/lifeline-navigator.git
cd lifeline-navigator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # For production serving
```

#### 3. Configure Nginx
Create `/etc/nginx/sites-available/lifeline-navigator`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Static files
    location /static/ {
        alias /home/lifeline/lifeline-navigator/.streamlit/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Main application
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_read_timeout 86400s;
        proxy_connect_timeout 60s;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/lifeline-navigator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Create Systemd Service
Create `/etc/systemd/system/lifeline-navigator.service`:
```ini
[Unit]
Description=LifeLine Navigator
After=network.target

[Service]
Type=simple
User=lifeline
WorkingDirectory=/home/lifeline/lifeline-navigator
Environment=PATH=/home/lifeline/lifeline-navigator/venv/bin
ExecStart=/home/lifeline/lifeline-navigator/venv/bin/gunicorn --bind 127.0.0.1:8501 --workers 3 --timeout 120 src.ui.app:main
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lifeline-navigator
sudo systemctl start lifeline-navigator
```

### SSL/HTTPS Configuration

#### Using Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl status certbot.timer
```

#### Nginx with SSL
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Other configuration...
}
```

## 🔧 Environment Configuration

### Production Configuration
Update `src/config.py` for production:
```python
# Production settings
DEBUG = False
LOG_LEVEL = "WARNING"
CACHE_TTL = 300  # 5 minutes

# Production data paths
DATA_DIR = Path("/var/lifeline/data")
LOG_DIR = Path("/var/lifeline/logs")
```

### Environment Variables
Create `.env.production`:
```env
DEBUG=false
LOG_LEVEL=WARNING
CACHE_TTL=300
DATA_DIR=/var/lifeline/data
LOG_DIR=/var/lifeline/logs
```

## 📊 Monitoring and Logging

### Application Logging
Configure logging in `src/config.py`:
```python
import logging
from pathlib import Path

# Production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)
```

### Health Checks
Add to your application:
```python
@app.route("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

### Monitoring with Docker
```bash
# Health check
curl http://localhost/health

# View container stats
docker stats lifeline-navigator

# View logs
docker logs lifeline-navigator
```

## 🚀 Performance Optimization

### Docker Performance
```dockerfile
# Use multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
```

### Caching
- Enable browser caching for static files
- Use CDN for global deployment
- Implement Redis for application caching (optional)

### Load Balancing
For high traffic, use load balancing:
```nginx
upstream streamlit {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    location / {
        proxy_pass http://streamlit;
        # ... other configuration
    }
}
```

## 🔄 Backup and Recovery

### Data Backup
```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/lifeline"
mkdir -p $BACKUP_DIR

# Backup data files
cp -r /var/lifeline/data $BACKUP_DIR/data_$DATE

# Backup configuration
cp /etc/nginx/sites-available/lifeline-navigator $BACKUP_DIR/config_$DATE

# Compress
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C $BACKUP_DIR .

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

### Automated Backup
Create a cron job:
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup_script.sh
```

## 🔒 Security Considerations

### File Permissions
```bash
# Set proper permissions
sudo chown -R lifeline:lifeline /home/lifeline/lifeline-navigator
sudo chmod 750 /home/lifeline/lifeline-navigator
```

### Firewall Configuration
```bash
# UFW rules
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Application Security
- Use HTTPS in production
- Implement rate limiting
- Keep dependencies updated
- Use environment variables for sensitive data

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   sudo lsof -i :8501
   
   # Kill process
   sudo kill -9 <PID>
   ```

2. **Permission denied**
   ```bash
   # Fix permissions
   sudo chown -R lifeline:lifeline /home/lifeline/lifeline-navigator
   ```

3. **Nginx configuration error**
   ```bash
   # Test configuration
   sudo nginx -t
   
   # View error log
   sudo tail -f /var/log/nginx/error.log
   ```

### Debug Mode
For debugging, enable detailed error messages:
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

This deployment guide covers various options for deploying LifeLine Navigator. Choose the method that best fits your needs and infrastructure.