from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse

from ..models import Payment, Booking
from ..serializers import PaymentSerializer
from ..services.chapa_service import initialize_payment, verify_payment

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own payments
        return Payment.objects.filter(booking__user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        booking = serializer.validated_data['booking']
        if booking.user != self.request.user:
            raise serializers.ValidationError("You can only create payments for your own bookings.")
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def initiate_chapa_payment(self, request, pk=None):
        """
        Initiate Chapa payment for the specified payment instance.
        """
        payment = self.get_object()
        
        if payment.status != 'pending':
            return Response(
                {'error': 'Payment has already been processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Prepare payment data for Chapa
            payment_data = {
                'amount': str(payment.amount),
                'currency': payment.currency,
                'email': request.user.email,
                'first_name': request.user.first_name or 'User',
                'last_name': request.user.last_name or str(request.user.id),
                'tx_ref': payment.transaction_id,
                'callback_url': request.build_absolute_uri(
                    reverse('payment-callback', kwargs={'pk': payment.id})
                ),
                'return_url': request.build_absolute_uri('/payments/success/'),
                'customization[title]': 'ALX Travel App',
                'customization[description]': f'Payment for booking #{payment.booking.id}',
            }
            
            # Initialize payment with Chapa
            response = initialize_payment(payment_data)
            
            if response.status_code == 200:
                data = response.json()
                payment.chapa_reference = data.get('data', {}).get('reference')
                payment.metadata['checkout_url'] = data.get('data', {}).get('checkout_url')
                payment.save()
                
                return Response({
                    'checkout_url': payment.metadata['checkout_url'],
                    'reference': payment.chapa_reference,
                    'status': payment.status
                })
            else:
                error_message = response.json().get('message', 'Failed to initialize payment')
                return Response(
                    {'error': error_message},
                    status=response.status_code
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='callback/(?P<pk>[^/.]+)')
    def payment_callback(self, request, pk=None):
        """
        Handle Chapa payment callback.
        This endpoint is called by Chapa after a payment attempt.
        """
        payment = get_object_or_404(Payment, id=pk)
        
        # Verify the payment with Chapa
        try:
            response = verify_payment(payment.transaction_id)
            
            if response.status_code == 200:
                data = response.json()
                status_from_chapa = data.get('data', {}).get('status')
                
                # Update payment status based on Chapa response
                if status_from_chapa == 'success':
                    payment.status = 'successful'
                    payment.booking.status = 'confirmed'
                    payment.booking.save()
                    
                    # TODO: Send confirmation email asynchronously
                    # send_payment_confirmation_email.delay(payment.id)
                    
                elif status_from_chapa in ['failed', 'cancelled']:
                    payment.status = 'failed'
                
                payment.save()
                
                # Redirect to frontend success/failure page
                status_str = 'success' if payment.status == 'successful' else 'failed'
                frontend_url = f"{settings.FRONTEND_URL}/payments/{status_str}/?transaction_id={payment.transaction_id}"
                
                return Response({
                    'status': payment.status,
                    'transaction_id': payment.transaction_id,
                    'redirect_url': frontend_url
                })
            else:
                return Response(
                    {'error': 'Failed to verify payment'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        """
        Manually verify a payment status with Chapa.
        This can be called from the frontend if the callback fails.
        """
        payment = self.get_object()
        
        try:
            response = verify_payment(payment.transaction_id)
            
            if response.status_code == 200:
                data = response.json()
                status_from_chapa = data.get('data', {}).get('status')
                
                # Update payment status based on Chapa response
                if status_from_chapa == 'success' and payment.status != 'successful':
                    payment.status = 'successful'
                    payment.booking.status = 'confirmed'
                    payment.booking.save()
                    payment.save()
                    
                    # TODO: Send confirmation email asynchronously
                    # send_payment_confirmation_email.delay(payment.id)
                
                return Response({
                    'status': payment.status,
                    'transaction_id': payment.transaction_id,
                    'chapa_status': status_from_chapa
                })
            else:
                return Response(
                    {'error': 'Failed to verify payment'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
