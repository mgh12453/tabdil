from django.db import models
from django.contrib.auth.models import User

app_name = 'core'


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='seller')
    balance = models.PositiveIntegerField(default=0, editable=False)

    has_conflict = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.user.username


