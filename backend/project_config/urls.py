from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from services.views import SubscriptionViewSet


router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
]
