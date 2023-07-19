from rest_framework import serializers

from .models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    plan = PlanSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'client_name', 'email', 'plan', 'total_price')

    # def get_total_price(self, obj):
    #     obj: Subscription
    #     return obj.service.price - obj.service.price * obj.plan.discount_percent / 100

    def get_total_price(self, obj):
        return obj.total_price
