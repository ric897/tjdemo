# TJ Demo - Django Authentication App

A Django application with user authentication features, deployed on DigitalOcean App Platform.

## Features

- User registration and login
- User profile management
- Dashboard functionality
- PostgreSQL database integration
- Production-ready deployment configuration

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/ric897/tjdemo.git
cd tjdemo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Deployment

The application is configured for automatic deployment on DigitalOcean App Platform:

- **Repository**: https://github.com/ric897/tjdemo
- **App Platform URL**: https://tjdemo-app-fhlfw.ondigitalocean.app
- **Auto-deploy**: Enabled on push to main branch

### Environment Variables

The following environment variables are configured in DigitalOcean App Platform:

- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Django secret key (generate a secure one)
- `ALLOWED_HOSTS`: App domain
- `DATABASE_URL`: Automatically provided by managed database
- `DB_*`: Database connection details (auto-injected from managed database)

### Database

The app uses a managed PostgreSQL database on DigitalOcean:
- Engine: PostgreSQL 15
- Environment: Development (can be upgraded to production)

## Tech Stack

- **Framework**: Django 5.2.5
- **Database**: PostgreSQL (production) / SQLite (development)
- **Static Files**: WhiteNoise
- **Web Server**: Gunicorn
- **Deployment**: DigitalOcean App Platform
- **CI/CD**: GitHub integration with auto-deploy

## Project Structure

```
tjdemo/
├── authentication/          # Authentication app
│   ├── models.py           # Custom User model
│   ├── views.py            # Authentication views
│   ├── forms.py            # User forms
│   └── templates/          # Authentication templates
├── templates/              # Global templates
├── static/                 # Static files (CSS, JS)
├── tjdemo/                 # Project settings
│   └── settings.py         # Django settings
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version
├── Procfile               # App Platform process config
└── .env.example           # Environment variables template
```