from rest_framework import serializers
from .models import User, Property, Booking, Payment, Review, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class PropertySerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    amenities = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        error_messages={'empty': 'At least one amenity must be provided'}
    )
    
    class Meta:
        model = Property
        fields = [
            'id', 'host', 'name', 'description', 'location', 
            'price_per_night', 'max_guests', 'amenities',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_max_guests(self, value):
        if value < 1:
            raise serializers.ValidationError('Maximum guests must be at least 1')
        return value

    def validate(self, data):
        if data.get('max_guests', 1) < 1:
            raise serializers.ValidationError('Maximum guests must be at least 1')
        return data

class BookingSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        source='property',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'property', 'property_id', 'user', 'start_date', 
            'end_date', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'total_price']

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'payment_date']
        read_only_fields = ['id', 'payment_date']

class ReviewSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at']