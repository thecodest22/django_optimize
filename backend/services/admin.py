from django.contrib import admin

from .models import Service, Plan, Subscription


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name']

    def get_queryset(self, request):
        return Subscription.objects.select_related('client', 'service', 'plan')

    @staticmethod
    @admin.display(description='Name')
    def name(obj: Subscription):
        return f'{obj.service} / {obj.plan}'
