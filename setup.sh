#!/bin/bash
# setup.sh - Setup script for Poll System

echo "=== Poll System Setup ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your settings."
    echo "Then run: source .env"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Setup database
echo "Setting up database..."
python manage.py migrate

# Create superuser if .env has credentials
if [ -f .env ]; then
    source .env
    if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py createsuperuser --noinput \
            --username "$DJANGO_SUPERUSER_USERNAME" \
            --email "$DJANGO_SUPERUSER_EMAIL"
    fi
fi

echo "=== Setup Complete ==="
echo "Run: python manage.py runserver"
echo "API: http://localhost:8000/api/polls/"
echo "Admin: http://localhost:8000/admin/"