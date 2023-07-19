from django.db.models import Prefetch, F, QuerySet, Sum

from rest_framework import viewsets

from clients.models import Client
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    # queryset = Subscription.objects.select_related('client__user')\
    #     .only('client__company_name', 'client__user__email')
    prefetch = Prefetch('client', queryset=Client.objects.select_related('user').only('company_name', 'user__email'))
    queryset = Subscription.objects.prefetch_related('plan', prefetch)\
        .annotate(total_price=F('service__price') - F('service__price') * F('plan__discount_percent') / 100)
    # queryset = Subscription.objects.select_related('plan').prefetch_related(prefetch)

    def list(self, request, *args, **kwargs):
        queryset: QuerySet = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_sum'] = queryset.aggregate(total=Sum('total_price')).get('total')
        response.data = response_data

        return response

