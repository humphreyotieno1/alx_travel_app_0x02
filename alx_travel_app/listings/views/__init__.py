from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..models import Property, Booking, Payment
from ..serializers import PropertySerializer, BookingSerializer, PaymentSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
        'payments': reverse('payment-list', request=request, format=format),
    })

class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'price_per_night', 'max_guests']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at']

    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Automatically set the host to the current user
        """
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure only property owners can update their properties
        """
        property = self.get_object()
        if property.host != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property', 'status', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'created_at']

    def get_queryset(self):
        """
        Filter bookings by user if not admin
        """
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Automatically set the user to the current user
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure only the user who made the booking can update it
        """
        booking = self.get_object()
        if booking.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Cancel a booking instead of deleting it
        """
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        
        if booking.status == 'cancelled':
            return Response(
                {'detail': 'This booking has already been cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
