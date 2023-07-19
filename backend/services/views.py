from django.db.models import Prefetch

from rest_framework import viewsets

from clients.models import Client
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    # queryset = Subscription.objects.select_related('client__user')\
    #     .only('client__company_name', 'client__user__email')
    prefetch = Prefetch('client', queryset=Client.objects.select_related('user').only('company_name', 'user__email'))
    queryset = Subscription.objects.prefetch_related('plan', prefetch)
    # queryset = Subscription.objects.select_related('plan').prefetch_related(prefetch)
