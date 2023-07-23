import datetime
import logging
import time

from celery import shared_task


log = logging.getLogger('django.db.backends')


@shared_task()
def set_price_from_plan(plan_instance_id):
    from .models import Subscription, Plan
    log.debug('=============== FROM PLAN ================')

    time.sleep(5)

    plan_instance: Plan = Plan.objects.get(id=plan_instance_id)
    queryset = plan_instance.subscriptions.select_related('service').only('service__price', 'plan_id')

    subscriptions = []
    for i_subscription in queryset:
        new_price = i_subscription.service.price - i_subscription.service.price * plan_instance.discount_percent / 100
        i_subscription.price = new_price
        subscriptions.append(i_subscription)
    Subscription.objects.bulk_update(subscriptions, fields=['price'])


@shared_task()
def set_price_from_service(service_instance_id):
    from .models import Subscription, Service
    log.debug('=============== FROM SERVICE ================')

    time.sleep(10)

    service_instance = Service.objects.get(id=service_instance_id)
    queryset = service_instance.subscriptions.select_related('plan').only('plan__discount_percent', 'service_id')

    subscriptions = []
    for i_subscription in queryset:
        new_price = service_instance.price - service_instance.price * i_subscription.plan.discount_percent / 100
        i_subscription.price = new_price
        subscriptions.append(i_subscription)
    Subscription.objects.bulk_update(subscriptions, fields=['price'])


@shared_task()
def set_comment(service_instance_id):
    from .models import Subscription, Service
    log.debug('=============== FROM SET COMMENT ================')

    service_instance = Service.objects.get(id=service_instance_id)
    queryset = service_instance.subscriptions.all()

    subscriptions = []
    for i_subscription in queryset:
        i_subscription.comment = str(datetime.datetime.now())
        subscriptions.append(i_subscription)

    time.sleep(30)

    Subscription.objects.bulk_update(subscriptions, fields=['comment'])
