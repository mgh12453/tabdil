from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from logging import getLogger
from core.models import Charge

logger = getLogger(__name__)


class ChargePhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        amount = int(request.GET.get('amount'))
        customer_phone_number = request.GET.get('customer_phone_number')

        if amount is None or int(amount) <= 0:
            return Response({'error': 'amount is not valid'}, status=400)
        amount = int(amount)

        if user.seller is None:
            return Response({'error': 'you are not a seller'}, status=400)

        with transaction.atomic():
            if user.seller.balance - amount < 0:
                return Response({'error': 'your balance is not enough'}, status=400)

            try:
                Charge.objects.create(seller=user.seller, amount=amount, customer_phone_number=customer_phone_number).save()
            except Exception as e:
                logger.error(f'error in saving charge {e}')
                return Response({'error': 'error in saving charge'}, status=400)

        return Response({'message': 'charge created successfully'}, status=200)
