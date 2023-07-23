import logging

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .tasks import set_price_from_plan, set_price_from_service, set_comment


log = logging.getLogger('django.db.backends')


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.name

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._price = instance.price
        return instance

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.price != getattr(self, '_price', None):
            set_price_from_service.delay(self.id)
            set_comment.delay(self.id)


class Plan(models.Model):
    class PlanNameChoices(models.TextChoices):
        full = 'full', 'Full'
        student = 'student', 'Student'
        discount = 'discount', 'Discount'

    plan_type = models.CharField(max_length=30, choices=PlanNameChoices.choices, default=PlanNameChoices.full)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(99)])

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__discount_percent = self.discount_percent

    def __str__(self):
        return self.PlanNameChoices[self.plan_type].label

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._discount_percent = instance.discount_percent
        return instance

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.discount_percent != getattr(self, '_discount_percent', None):
            set_price_from_plan.delay(self.id)


class Subscription(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(99)])
    comment = models.CharField(max_length=50, blank=True, default='')

    # Технически можно и так, но это плохой подход, т.к., если поменяется, например, процент скидки у первичной модели,
    # то автоматического пересчета не будет происходить
    # def save(self, *args, save_model=True, **kwargs):
    #     if save_model:
    #         set_price.delay(self.id)
    #
    #     super().save(*args, **kwargs)
