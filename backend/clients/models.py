from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
