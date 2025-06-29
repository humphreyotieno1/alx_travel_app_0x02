# ALX Travel App

A comprehensive travel booking platform built with Django and Django REST framework.

## Features

- User authentication and authorization
- Property listings with search and filtering
- Booking system
- Reviews and ratings
- Admin dashboard

## Prerequisites

- Python 3.8+
- MySQL 5.7+
- pip
- virtualenv (recommended)

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd alx_travel_app_0x02
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```env
   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database
   DB_NAME=alx_travel_app
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=3306
   
   # Security
   CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

### 5. Set up the database

1. Create a MySQL database:
   ```sql
   CREATE DATABASE alx_travel_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Security Best Practices

1. **Never commit sensitive data**
   - Keep `.env` in your `.gitignore`
   - Use `.env.example` as a template

2. **In production**:
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`
   - Use HTTPS
   - Set secure cookie and session settings
   - Use a production-ready database
   - Set up proper file permissions

3. **Regularly update dependencies**
   ```bash
   pip list --outdated
   pip install -U package-name
   ```

## API Documentation

API documentation is available at `/api/docs/` when running the development server.

## Deployment

For production deployment, consider using:
- Gunicorn or uWSGI as application server
- Nginx as reverse proxy
- PostgreSQL for production database
- Redis for caching
- Celery for background tasks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

- `/listings/`: List all available properties
- `/listings/<id>/`: Get details of a specific property
- `/bookings/`: List all bookings
- `/bookings/<id>/`: Get details of a specific booking

## Documentation

Access API documentation at `/swagger/` after running the server.