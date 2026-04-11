# 🌱 AgroYantra — Farm-to-Table E-Commerce Platform

> Fresh produce directly from Nepali farms to your doorstep.

[![CI](https://github.com/agroyantra/agroyantra-site/actions/workflows/django-ci.yml/badge.svg)](https://github.com/agroyantra/agroyantra-site/actions)

## Overview

**AgroYantra** (अग्रोयन्त्र) is a Django-based e-commerce platform connecting local Nepali farmers directly with consumers — no middlemen, no online payments. All orders use **Cash on Delivery (COD)**.

- 🌐 Domain: [agroyantra.com.np](https://agroyantra.com.np)
- 💳 Payment: Cash on Delivery only
- 🇳🇵 Built for Nepal

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework |
| Frontend | Tailwind CSS (CDN), Vanilla JS |
| Database | SQLite3 |
| Server | Gunicorn + Nginx |
| Images | Pillow |

## Quick Start (Development)

```bash
# 1. Clone
git clone https://github.com/agroyantra/agroyantra-site.git
cd agroyantra-site

# 2. Virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment variables
cp .env.example .env
# Edit .env and set DEBUG=True, ALLOWED_HOSTS=localhost,127.0.0.1

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## App Structure

```
agroyantra-site/
├── ojasecommerce/      # Project config (settings, urls, wsgi)
├── accounts/           # Custom user model, auth
├── categories/         # Product categories
├── products/           # Product catalog, search
├── carts/              # Shopping cart (session-based)
├── orders/             # Orders, COD payment tracking
├── profile/            # User dashboard & profile
├── landing_page/       # Homepage
├── about_us_farm/      # About, Our Farm, Contact
├── backend/            # Staff admin dashboard
├── templates/          # All HTML templates
├── static/             # CSS, JS, images
└── media/              # User-uploaded files
```

## Payment System

**Cash on Delivery only.** No online gateway is integrated.

Order flow:
1. Customer places order → status: **New**
2. Staff reviews & accepts → status: **Accepted**
3. Delivery made, cash collected → status: **Completed**

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full server setup instructions.

Quick summary:
```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=ojasecommerce.settings_prod

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn --config gunicorn.conf.py ojasecommerce.wsgi:application
```

## Admin Access

- Django Admin: `/admin/`
- Staff Dashboard: `/backend/`

## License

MIT © AgroYantra
