from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from .views.payment_views import PaymentViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename='property')
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel App API",
      default_version='v1',
      description="API documentation for ALX Travel App",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Payment URLs
    path('api/payments/<uuid:payment_id>/initiate-chapa/', 
         PaymentViewSet.as_view({'post': 'initiate_chapa_payment'}), 
         name='initiate-chapa-payment'),
    path('api/payments/callback/<uuid:payment_id>/', 
         PaymentViewSet.as_view({'get': 'payment_callback'}), 
         name='payment-callback'),
]
