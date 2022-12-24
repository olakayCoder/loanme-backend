from django.shortcuts import render
from rest_framework import status , generics 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VerifyPaymentSerializer
import requests
from django.conf import settings
from client.models import Transaction , LoanApplication
from account.models import UserCard , User , UserBvn
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.decorators import api_view , permission_classes
# Create your views here.
from helpers.generators import CustomValuesGenerator
import json
import time

class Generate(APIView):

    def get(self, request):
        # CustomValuesGenerator.score_criteria()
        # CustomValuesGenerator.create_offers()
        application = LoanApplication.objects.all().last()
        application_data = json.loads(application.data) 
        # print(application_data.__first_name) 
    
        application_data['last_name'] 
        application_data['email'] 
        application_data['gender'] 
        application_data['phone'] 
        application_data['date_of_birth'] 
        application_data['marital_status'] 
        application_data['children'] 
        application_data['education'] 
        application_data['employment'] 
        application_data['income']  
        application_data['employer']  
        application_data['years_at_work']  
        application_data['residence']  
        application_data['years_at_residence']  

        print(application_data['children']  )
        return Response(status=status.HTTP_200_OK)

class VerifyPaymentApiView(generics.GenericAPIView):
    serializer_class = VerifyPaymentSerializer
    permission_classes = [IsAuthenticated]  

    def post(self, request , *args, **kwargs):
        print(request.user)   
        user = User.objects.get(id=request.user.id) 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        type = serializer.validated_data['type']
        reference = serializer.validated_data['reference'] 
        match(type):
            case 'success':
                url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
                headers = {'authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY }' }
                
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
                            type=response['data']['authorization']['card_type'], 
                            code=response['data']['authorization']['authorization_code'],
                            start=response['data']['authorization']['bin'], 
                            last=response['data']['authorization']['last4'],
                            bank=response['data']['authorization']['bank'],
                            exp_month=response['data']['authorization']['exp_month'],
                            exp_year=response['data']['authorization']['exp_year'],
                            signature=response['data']['authorization']['signature'],
                            account_name=response['data']['authorization']['account_name'],
                            is_reusable=response['data']['authorization']['reusable']
                        )
                    else:
                        UserCard.objects.create(
                            user=user,
                            email = user.email , 
                            is_default = True , 
                            type=response['data']['authorization']['card_type'], 
                            code=response['data']['authorization']['authorization_code'],
                            start=response['data']['authorization']['bin'], 
                            last=response['data']['authorization']['last4'],
                            bank=response['data']['authorization']['bank'],
                            exp_month=response['data']['authorization']['exp_month'],
                            exp_year=response['data']['authorization']['exp_year'],
                            signature=response['data']['authorization']['signature'],
                            account_name=response['data']['authorization']['account_name'],
                            is_reusable=response['data']['authorization']['reusable']
                        )
                    return Response({ 'success':True, 'detail':'Payment successful updated'}, status=status.HTTP_200_OK)
            case 'failed' :
                payment = Transaction.objects.get(reference=reference )
                payment.status = 'failed'
                payment.save()
                return Response({ 'success':True, 'detail':'Payment successful updated'}, status=status.HTTP_200_OK)
            case _:
                return Response({ 'success':True, 'detail':'Payment successful updated'}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'detail':'Invalid reference type'}, status=status.HTTP_400_BAD_REQUEST)







class VerifyEmailApiView(APIView):
    def post(self, request ):
        email = request.data['email']
        user = User.objects.filter(email=email).exists()
        if user :
            return Response({
                'success':True,
                'detail':'Email already exist'
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def verify_phone(request):
    bvn = request.data['bvn']
    user = User.objects.get(id=request.user.id) 
    num = str(bvn)
    v = num.count('7')
    if v > 2 :
        return Response({
            'success':True,
            'detail':'Bvn already exist'
        },status=status.HTTP_400_BAD_REQUEST)
    user.is_bvn = True
    user.save() 
    return Response(status=status.HTTP_200_OK) 

class VerifyPhoneApiView(APIView):
    def post(self, request ):
        phone = request.data['phone']
        user = User.objects.filter(phone=phone).exists()
        if user :
            return Response({
                'success':True,
                'detail':'Phone already exist'
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def verify_bvn(request):
    bvn = request.data['bvn']
    user = User.objects.get(id=request.user.id) 
    num = str(bvn)
    v = num.count('7')
    if v > 2 :
        return Response({
            'success':True,
            'detail':'Bvn already exist'
        },status=status.HTTP_400_BAD_REQUEST)
    user.is_bvn = True
    user.save() 
    time.sleep(3)
    return Response(status=status.HTTP_200_OK) 




class VerifyBvnApiView(generics.GenericAPIView):  
    
    def post(self, request ):
        bvn = request.data['bvn']
        # user = User.objects.filter(bvn=bvn).exists()
        num = str(bvn)
        v = num.count('7')
        if v > 2 :
            return Response({
                'success':True,
                'detail':'Phone already exist'
            },status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK) 