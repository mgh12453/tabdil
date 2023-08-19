from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from logging import getLogger
from core.models import Purchase

logger = getLogger(__name__)


class AddBalance(APIView):
    metadata_class = ['POST']
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.POST.get('amount')
        seller = request.POST.get('seller')

        if amount is None or amount <= 0:
            return Response({'error': 'amount is not valid'}, status=400)

        with transaction.atomic():
            try:
                Purchase.objects.create(seller=seller, amount=amount).save()
            except Exception as e:
                logger.error(f'error in saving purchase {e}')
                return Response({'error': 'error in saving purchase'}, status=400)
