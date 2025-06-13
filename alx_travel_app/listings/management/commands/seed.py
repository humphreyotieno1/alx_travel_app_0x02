import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from listings.models import User, Property, Booking, Payment, Review, Message
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample Airbnb data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        self.delete_data()
        self.stdout.write('Creating users...')
        self.create_users()
        self.stdout.write('Creating properties...')
        self.create_properties()
        self.stdout.write('Creating bookings...')
        self.create_bookings()
        self.stdout.write('Creating payments...')
        self.create_payments()
        self.stdout.write('Creating reviews...')
        self.create_reviews()
        self.stdout.write('Creating messages...')
        self.create_messages()
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))

    def delete_data(self):
        Message.objects.all().delete()
        Review.objects.all().delete()
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Property.objects.all().delete()
        User.objects.all().delete()

    def create_users(self):
        users = [
            {
                'id': uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
                'email': 'john@example.com',
                'password': make_password('password123'),
                'phone_number': '+1234567890',
                'role': 'guest'
            },
            {
                'id': uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f23456789012'),
                'email': 'jane@example.com',
                'password': make_password('password123'),
                'phone_number': '+2345678901',
                'role': 'host'
            },
            {
                'id': uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234'),
                'email': 'michael@example.com',
                'password': make_password('password123'),
                'phone_number': '+3456789012',
                'role': 'guest'
            },
            {
                'id': uuid.UUID('d4e5f6a7-b8c9-0123-defc-456789012345'),
                'email': 'sarah@example.com',
                'password': make_password('password123'),
                'phone_number': '+4567890123',
                'role': 'host'
            },
            {
                'id': uuid.UUID('e5f6a7b8-c9d0-1234-efab-567890123456'),
                'email': 'admin@example.com',
                'password': make_password('admin123'),
                'phone_number': '+5678901234',
                'role': 'admin'
            }
        ]
        
        for user_data in users:
            User.objects.create(**user_data)

    def create_properties(self):
        properties = [
            {
                'id': uuid.UUID('f6a7b8c9-d0e1-2345-fbaf-678901234567'),
                'host': User.objects.get(id=uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f23456789012')),
                'name': 'Beachfront Villa',
                'description': 'Luxurious villa with stunning ocean views',
                'location': 'Miami, FL',
                'price_per_night': 299.99
            },
            {
                'id': uuid.UUID('a7b8c9d0-e1f2-3456-fbfa-789012345678'),
                'host': User.objects.get(id=uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f23456789012')),
                'name': 'Mountain Cabin',
                'description': 'Cozy cabin in the mountains',
                'location': 'Aspen, CO',
                'price_per_night': 149.99
            },
            {
                'id': uuid.UUID('b8c9d0e1-f2a3-4567-ebca-890123456789'),
                'host': User.objects.get(id=uuid.UUID('d4e5f6a7-b8c9-0123-defc-456789012345')),
                'name': 'Downtown Loft',
                'description': 'Modern loft in the heart of the city',
                'location': 'New York, NY',
                'price_per_night': 199.99
            },
            {
                'id': uuid.UUID('c9d0e1f2-a3b4-5678-cfab-901234567890'),
                'host': User.objects.get(id=uuid.UUID('d4e5f6a7-b8c9-0123-defc-456789012345')),
                'name': 'Country Cottage',
                'description': 'Charming cottage in the countryside',
                'location': 'Nashville, TN',
                'price_per_night': 129.99
            }
        ]
        
        for property_data in properties:
            Property.objects.create(**property_data)

    def create_bookings(self):
        bookings = [
            {
                'id': uuid.UUID('d0e1f2a3-b4c5-6789-afcd-012345678901'),
                'property': Property.objects.get(id=uuid.UUID('f6a7b8c9-d0e1-2345-fbaf-678901234567')),
                'user': User.objects.get(id=uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890')),
                'start_date': datetime(2023, 6, 15).date(),
                'end_date': datetime(2023, 6, 20).date(),
                'total_price': 1499.95,
                'status': 'confirmed'
            },
            {
                'id': uuid.UUID('e1f2a3b4-c5d6-7890-abcd-123456789012'),
                'property': Property.objects.get(id=uuid.UUID('a7b8c9d0-e1f2-3456-fbfa-789012345678')),
                'user': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'start_date': datetime(2023, 7, 1).date(),
                'end_date': datetime(2023, 7, 5).date(),
                'total_price': 599.96,
                'status': 'confirmed'
            },
            {
                'id': uuid.UUID('f2a3b4c5-d6e7-8901-efac-234567890123'),
                'property': Property.objects.get(id=uuid.UUID('b8c9d0e1-f2a3-4567-ebca-890123456789')),
                'user': User.objects.get(id=uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890')),
                'start_date': datetime(2023, 8, 10).date(),
                'end_date': datetime(2023, 8, 15).date(),
                'total_price': 999.95,
                'status': 'pending'
            },
            {
                'id': uuid.UUID('a3b4c5d6-e7f8-9012-bcad-345678901234'),
                'property': Property.objects.get(id=uuid.UUID('c9d0e1f2-a3b4-5678-cfab-901234567890')),
                'user': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'start_date': datetime(2023, 9, 20).date(),
                'end_date': datetime(2023, 9, 25).date(),
                'total_price': 649.95,
                'status': 'confirmed'
            }
        ]
        
        for booking_data in bookings:
            Booking.objects.create(**booking_data)

    def create_payments(self):
        payments = [
            {
                'id': uuid.UUID('b4c5d6e7-f8a9-0123-fdab-456789012345'),
                'booking': Booking.objects.get(id=uuid.UUID('d0e1f2a3-b4c5-6789-afcd-012345678901')),
                'amount': 1499.95,
                'payment_method': 'credit_card'
            },
            {
                'id': uuid.UUID('c5d6e7f8-a9b0-1234-acdb-567890123456'),
                'booking': Booking.objects.get(id=uuid.UUID('e1f2a3b4-c5d6-7890-abcd-123456789012')),
                'amount': 599.96,
                'payment_method': 'paypal'
            },
            {
                'id': uuid.UUID('d6e7f8a9-b0c1-2345-bdac-678901234567'),
                'booking': Booking.objects.get(id=uuid.UUID('a3b4c5d6-e7f8-9012-bcad-345678901234')),
                'amount': 649.95,
                'payment_method': 'stripe'
            }
        ]
        
        for payment_data in payments:
            Payment.objects.create(**payment_data)

    def create_reviews(self):
        reviews = [
            {
                'id': uuid.UUID('e7f8a9b0-c1d2-3456-facd-789012345678'),
                'property': Property.objects.get(id=uuid.UUID('f6a7b8c9-d0e1-2345-fbaf-678901234567')),
                'user': User.objects.get(id=uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890')),
                'rating': 5,
                'comment': 'Amazing experience! The views were incredible.'
            },
            {
                'id': uuid.UUID('f8a9b0c1-d2e3-4567-bcde-890123456789'),
                'property': Property.objects.get(id=uuid.UUID('a7b8c9d0-e1f2-3456-fbfa-789012345678')),
                'user': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'rating': 4,
                'comment': 'Very cozy place. Perfect for our weekend getaway.'
            },
            {
                'id': uuid.UUID('a9b0c1d2-e3f4-5678-cdaf-901234567890'),
                'property': Property.objects.get(id=uuid.UUID('c9d0e1f2-a3b4-5678-cfab-901234567890')),
                'user': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'rating': 5,
                'comment': 'Absolutely loved the cottage. Very peaceful and relaxing.'
            }
        ]
        
        for review_data in reviews:
            Review.objects.create(**review_data)

    def create_messages(self):
        messages = [
            {
                'id': uuid.UUID('b0c1d2e3-f4a5-6789-acfc-012345678901'),
                'sender': User.objects.get(id=uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890')),
                'recipient': User.objects.get(id=uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f23456789012')),
                'message_body': 'Hi, is the villa available for early check-in?'
            },
            {
                'id': uuid.UUID('c1d2e3f4-a5b6-7890-cfea-123456789012'),
                'sender': User.objects.get(id=uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f23456789012')),
                'recipient': User.objects.get(id=uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890')),
                'message_body': 'Yes, you can check in at 1pm instead of 3pm.'
            },
            {
                'id': uuid.UUID('d2e3f4a5-b6c7-8901-adcd-234567890123'),
                'sender': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'recipient': User.objects.get(id=uuid.UUID('d4e5f6a7-b8c9-0123-defc-456789012345')),
                'message_body': 'Is the loft pet-friendly?'
            },
            {
                'id': uuid.UUID('e3f4a5b6-c7d8-9012-fedc-345678901234'),
                'sender': User.objects.get(id=uuid.UUID('d4e5f6a7-b8c9-0123-defc-456789012345')),
                'recipient': User.objects.get(id=uuid.UUID('c3d4e5f6-a7b8-9012-cdef-345678901234')),
                'message_body': 'Sorry, we do not allow pets in the loft.'
            }
        ]
        
        for message_data in messages:
            Message.objects.create(**message_data)
