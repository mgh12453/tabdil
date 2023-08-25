from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from logging import getLogger
from core.models import Purchase, Seller

logger = getLogger(__name__)


class AddBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        amount = request.query_params.get('amount')
        seller = request.query_params.get('seller')

        if amount is None or int(amount) <= 0:
            return Response({'error': 'amount is not valid'}, status=400)
        amount = int(amount)

        seller = Seller.objects.get(user__id=int(seller))

        with transaction.atomic():
            try:
                Purchase.objects.create(seller=seller, amount=amount).save()
            except Exception as e:
                logger.error(f'error in saving purchase {e}')
                return Response({'error': 'error in saving purchase'}, status=400)

        return Response({'message': 'purchase created successfully'}, status=200)