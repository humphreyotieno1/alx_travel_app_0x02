from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, Booking
from .serializers import PropertySerializer, BookingSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
    })

class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    
    Methods:
    - GET: List all properties or retrieve a specific property
    - POST: Create a new property (requires authentication)
    - PUT/PATCH: Update a property (requires authentication)
    - DELETE: Delete a property (requires authentication)
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'price_per_night', 'max_guests']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at']

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        """Automatically set the host to the current user"""
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        """Ensure only property owners can update their properties"""
        instance = self.get_object()
        if instance.host != self.request.user:
            raise PermissionDenied('You can only update your own properties')
        serializer.save()

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    
    Methods:
    - GET: List all bookings or retrieve a specific booking
    - POST: Create a new booking (requires authentication)
    - PUT/PATCH: Update a booking (requires authentication)
    - DELETE: Cancel a booking (requires authentication)
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property', 'status', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'created_at']

    def get_queryset(self):
        """Filter bookings by user if not admin"""
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user to the current user"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the user who made the booking can update it"""
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied('You can only update your own bookings')
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Cancel a booking instead of deleting it"""
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            raise PermissionDenied('You can only cancel your own bookings')
        instance.status = 'canceled'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
