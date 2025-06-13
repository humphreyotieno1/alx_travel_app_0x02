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

## API Documentation

### ALX Travel App API Documentation

#### API Endpoints

##### Properties

- `GET /api/properties/` - List all properties
  - Query parameters:
    - `location` - Filter by location
    - `price_per_night` - Filter by price
    - `max_guests` - Filter by maximum guests
    - `search` - Search in name, description, or location
    - `ordering` - Order results by price or creation date

- `GET /api/properties/{id}/` - Get property details
- `POST /api/properties/` - Create a new property (requires admin authentication)
- `PUT/PATCH /api/properties/{id}/` - Update a property (requires admin authentication)
- `DELETE /api/properties/{id}/` - Delete a property (requires admin authentication)

##### Bookings

- `GET /api/bookings/` - List bookings (returns only user's bookings unless admin)
  - Query parameters:
    - `property` - Filter by property
    - `status` - Filter by booking status
    - `start_date` - Filter by start date
    - `end_date` - Filter by end date
    - `ordering` - Order results by start date or creation date

- `GET /api/bookings/{id}/` - Get booking details
- `POST /api/bookings/` - Create a new booking (requires authentication)
- `PUT/PATCH /api/bookings/{id}/` - Update a booking (requires authentication)
- `DELETE /api/bookings/{id}/` - Cancel a booking (requires authentication)

#### Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by POSTing to `/auth/token/` with email and password
2. Include the token in subsequent requests using the Authorization header:
   ```
   Authorization: Token <your-token>
   ```

#### Documentation

- Swagger UI: `/api/swagger/`
- API Documentation: `/api/docs/`

#### Error Responses

All endpoints return appropriate HTTP status codes:
- 200 OK - Successful request
- 201 Created - New resource created
- 204 No Content - Resource deleted
- 400 Bad Request - Invalid request data
- 401 Unauthorized - Authentication required
- 403 Forbidden - Permission denied
- 404 Not Found - Resource not found
- 405 Method Not Allowed - Invalid HTTP method
- 500 Internal Server Error - Server error

## Documentation

Access API documentation at `/swagger/` after running the server.