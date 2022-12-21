from django.shortcuts import render
from rest_framework import status , generics 
from rest_framework.response import Response
from .serializers import VerifyPaymentSerializer
import requests
from django.conf import settings
from client.models import Transaction
from account.models import UserCard , User
# Create your views here.


class VerifyPaymentApiView(generics.GenericAPIView):
    serializer_class = VerifyPaymentSerializer


    def post(self, request ,_args, **kwargs):
        user = User.objects.get(id=1)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        type = serializer.validated_data['type']
        reference = serializer.validated_data['reference']
        match(type):
            case 'success':
                # url = f'https://api.paystack.co/transaction/verify/:{reference}'                
                url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
                headers = {
                    {'authorization': f'Bearer { settings.PAYSTACK_SECRET_KEY }' }
                }
                r = requests.get(url , headers=headers)
                response = r.json()
                if response['data']['status'] == 'success':
                    amount = response['data']['amount'] 
                    # update the status of ref transaction success
                    payment = Transaction.objects.get(reference=reference )
                    payment.status = 'success'
                    payment.amount = amount
                    payment.save()
                    #  save the card for subsequent use
                    if UserCard.objects.filter(user=user).count():
                        UserCard.objects.create(
                            user=user,
                            email = user.email , 
                            type=response['data']['card_type'], 
                            code=response['data']['authorization_code'],
                            start=response['data']['bin'], 
                            last=response['data']['last4'],
                            account_name=response['data']['account_name'],
                            is_reusable=response['data']['reusable']
                        )
                    else:
                        UserCard.objects.create(
                            user=user,
                            email = user.email , is_default=True,
                            type=response['data']['card_type'], 
                            code=response['data']['authorization_code'],
                            start=response['data']['bin'], 
                            last=response['data']['last4'],
                            account_name=response['data']['account_name'],
                            is_reusable=response['data']['reusable']
                        )
                    return Response({ 'success':True, 'detail':'Payment successful updated'}, status=status.HTTP_200_OK)
            case 'failed' :
                payment = Transaction.objects.get(reference=reference )
                payment.status = 'failed'
                payment.save()
                return Response({ 'success':True, 'detail':'Payment successful updated'}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'detail':'Invalid reference type'}, status=status.HTTP_400_BAD_REQUEST)