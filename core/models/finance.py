from django.db import models
from django.utils.log import logging
from django.db.models import Sum, F
from django.db import transaction
from django.core.exceptions import ValidationError
from .seller import Seller

logger = logging.getLogger(__name__)
app_name = 'core'


# This model is used to store the purchases of the sellers. all the financial logic is implemented here
class Purchase(models.Model):
    seller = models.ForeignKey('core.Seller', on_delete=models.PROTECT, related_name='purchases')
    amount = models.IntegerField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    extra = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} - {self.seller.user.username}'

    def clean(self):
        new_balance = self.seller.balance + self.amount

        if self.seller.has_conflict:
            raise ValidationError(f'can not save purchase with conflicts: {self.seller} with balance {self.seller.balance}')

        if new_balance < 0:
            raise ValidationError(f'Seller balance is not enough {new_balance} < 0')

    @transaction.atomic
    def save(self, *args, **kwargs):
        try:
            if self.pk is not None:
                logger.warning(f'FATAL: you can not update a purchase - {self.__str__()}')
                return super().save(*args, **kwargs)

            self.full_clean()

            Seller.objects.filter(pk=self.seller.pk).update(balance=F('balance') + self.amount)  # race condition safe
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f'error in saving purchase {e}')
            raise Exception('error in saving purchase')
