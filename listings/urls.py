from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename='property')
router.register(r'bookings', views.BookingViewSet, basename='booking')

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
    path('properties/', views.PropertyList.as_view(), name='property-list'),
    path('properties/<uuid:pk>/', views.PropertyDetail.as_view(), name='property-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<uuid:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('bookings/', views.BookingList.as_view(), name='booking-list'),
    path('bookings/<uuid:pk>/', views.BookingDetail.as_view(), name='booking-detail'),
]