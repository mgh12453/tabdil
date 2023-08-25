from .models import Seller, Purchase
from django.db.models.functions import Coalesce
from django.db.models import Sum, IntegerField, BooleanField, Case, When, Value, F
from django.db import transaction


@transaction.atomic
def check_finance_conflicts():
    sellers_with_total_purchase = Seller.objects.annotate(
        total_purchase=Coalesce(Sum('purchase__amount'), 0, output_field=IntegerField())
    )

    sellers_with_conflict = sellers_with_total_purchase.annotate(
        found_conflict=Case(
            When(total_purchase=F('balance'), then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        )
    )

    sellers_with_conflict.filter(has_conflict=False, found_conflict=True).update(has_conflict=True)
