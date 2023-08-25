from django.db import models
from .finance import Purchase
from django.utils.log import logging
from django.db import transaction
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


app_name = 'core'


class Charge(models.Model):
    amount = models.PositiveIntegerField(null=False, blank=False)
    seller = models.ForeignKey('core.Seller', on_delete=models.PROTECT, related_name='charges')
    purchase = models.ForeignKey('core.Purchase', on_delete=models.PROTECT, related_name='charges', null=True, blank=True)
    customer_phone_number = models.CharField(max_length=11, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        try:
            if self.pk is not None:
                logger.warning(f'FATAL: you can not update a charge - {self.__str__()}')
                return super().save(*args, **kwargs)

            self.full_clean()
            self.purchase = Purchase.objects.create(seller=self.seller, amount=-self.amount, type='DBC')
            self.purchase.save()
            return super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f'error in saving charge {e}')
            raise Exception('error in saving charge')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} - {self.seller.user.username} to {self.customer_phone_number}'
