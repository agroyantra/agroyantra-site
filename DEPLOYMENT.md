# Deployment Guide — AgroYantra

## Server Requirements

- Ubuntu 22.04 LTS
- Python 3.11+
- Nginx
- Certbot (Let's Encrypt SSL)

## Step-by-Step Deployment

### 1. Server Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.11 python3.11-venv python3-pip nginx certbot python3-certbot-nginx -y
```

### 2. Deploy Application

```bash
# Create app directory
sudo mkdir -p /var/www/agroyantra
sudo chown $USER:$USER /var/www/agroyantra

# Clone repo
cd /var/www/agroyantra
git clone https://github.com/agroyantra/agroyantra-site.git .

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
cp .env.example .env
nano .env
```

Set these values:
```
DJANGO_SECRET_KEY=<generate a 50-char random key>
DEBUG=False
ALLOWED_HOSTS=agroyantra.com.np,www.agroyantra.com.np
SERVER_IP=<your server IP>
```

Generate secret key:
```bash
python -c "from django.core.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Django Setup

```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=ojasecommerce.settings_prod

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

sudo mkdir -p /var/www/agroyantra/media
sudo chown -R www-data:www-data /var/www/agroyantra/media
sudo chown -R www-data:www-data /var/www/agroyantra/staticfiles
```

### 5. Gunicorn Service

```bash
sudo cp agroyantra.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable agroyantra
sudo systemctl start agroyantra
sudo systemctl status agroyantra
```

### 6. Nginx Configuration

```bash
sudo cp nginx.conf /etc/nginx/sites-available/agroyantra
sudo ln -s /etc/nginx/sites-available/agroyantra /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. SSL Certificate

```bash
sudo certbot --nginx -d agroyantra.com.np -d www.agroyantra.com.np
```

### 8. Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Updating the Site

```bash
cd /var/www/agroyantra
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart agroyantra
```

## Useful Commands

```bash
# Check logs
sudo journalctl -u agroyantra -f
sudo tail -f /var/log/gunicorn-error.log

# Restart services
sudo systemctl restart agroyantra
sudo systemctl reload nginx

# Django shell
source venv/bin/activate
python manage.py shell
```
