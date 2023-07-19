from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    class PlanNameChoices(models.TextChoices):
        full = 'full', 'Full'
        student = 'student', 'Student'
        discount = 'discount', 'Discount'

    plan_type = models.CharField(max_length=30, choices=PlanNameChoices.choices, default=PlanNameChoices.full)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(99)])

    def __str__(self):
        return self.PlanNameChoices[self.plan_type].label


class Subscription(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
