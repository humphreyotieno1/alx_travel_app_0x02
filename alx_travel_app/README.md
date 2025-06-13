# ALX Travel App - Database Modeling and Seeding

This project implements the database models, serializers, and data seeding for the ALX Travel App.

## Models

1. **Listing**: Represents properties available for booking
2. **Booking**: Records guest bookings for listings
3. **Review**: Stores guest reviews for listings

## Setup

1. Clone the repository
2. Create and activate virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Seed the database: `python manage.py seed`

## API Endpoints

- `/listings/`: List all available properties
- `/listings/<id>/`: Get details of a specific property
- `/bookings/`: List all bookings
- `/bookings/<id>/`: Get details of a specific booking

## Documentation

Access API documentation at `/swagger/` after running the server.