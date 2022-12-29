from django.shortcuts import render
from rest_framework import status , generics 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VerifyPaymentSerializer
import requests
from django.conf import settings
from client.models import (
    Transaction , LoanApplication, LoanOffer , Loan
)
from account.models import (
    UserCard , User , UserBvn , 
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.decorators import api_view , permission_classes
# Create your views here.
from helpers.generators import CustomValuesGenerator
import json
import time
from django.http import HttpResponse

class Generate(APIView):

    def get(self, request):
        # CustomValuesGenerator.score_criteria()
        # CustomValuesGenerator.create_offers()
        application = LoanApplication.objects.all().last()
        application_data = json.loads(application.data) 
    
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
        return Response(status=status.HTTP_200_OK)

class VerifyPaymentApiView(generics.GenericAPIView):
    serializer_class = VerifyPaymentSerializer
    permission_classes = [IsAuthenticated]  

    def post(self, request , *args, **kwargs):
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
                    user.is_card = True
                    user.save() 
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
        
        phone = request.data.get('phone', None )
        if phone is None:
            return Response({
                'success':True,
                'detail':'Phone field required'
            },status=status.HTTP_400_BAD_REQUEST)
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




import csv
import xlwt

class ExportDataLoansAsCSVApiView(APIView):


    def get(self , request , *args ,**kwargs):
        users = Loan.objects.all()
        status = self.kwargs.get('user_id',None)
        response = HttpResponse('text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=customers-loans.csv'
        # the csv writer
        writer = csv.writer(response)
        field_names = [
            'UUID','USER','STATUS','AMOUNT','DATE','DUE_DATE'
            ]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in users:
            writer.writerow([
                obj.uuid ,f'{obj.user.first_name } {obj.user.last_name}',
                obj.status , obj.amount , obj.created_at , obj.due_date
                ])
        return response



class ExportDataUsersAsCSVApiView(APIView):


    def get(self , request , *args ,**kwargs):
        users = User.objects.all().exclude(is_staff=True)
        status = self.kwargs.get('user_id',None)
        response = HttpResponse('text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=customers.csv'
        # the csv writer
        writer = csv.writer(response)
        field_names = [   
            'UUID','FIRST_NAME','LAST_NAME','EMAIL','GENDER','IS_ACTIVE','CREATED_AT',
            'DATE_OF_BIRTH','PHONE', 'MARITAL_STATUS','CHILDREN','RESIDENT_TYPE','COUNTRY','STATE','CITY', 
            'ADDRESS1', 'ADDRESS2','EDUCATIONAL_STATUS','EMPLOYMENT_STATUS', 'BUSINESS_NAME' , 'MONTHLY_INCOME'
        ]

        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in users:
            writer.writerow([
                obj.uuid , obj.first_name, obj.last_name , obj.email , obj.gender , obj.is_active , obj.created_at , obj.date_of_birth,
                obj.phone, obj.marital_status, obj.children, obj.resident_type , obj.country , obj.state , obj.city , obj.address1 , obj.address2 ,
                obj.educational_status, obj.employment_status , obj.business_name , obj.monthly_income
                ])
        return response




class ExportDataApplicationsAsCSVApiView(APIView):
    def get(self , request , *args ,**kwargs):
        users = LoanApplication.objects.all()
        status = self.kwargs.get('user_id',None)
        response = HttpResponse('text/csv')
        # force download.
        response['Content-Disposition'] = 'attachment;filename=customers-applications.csv'
        # the csv writer
        writer = csv.writer(response)
        field_names = [   
            'UUID','USER','STATUS','AMOUNT','CREATED_AT',
        ]

        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in users:
            obj_data = json.loads(obj.data)  
            writer.writerow([
                obj.uuid , f'{obj.user.first_name } {obj.user.last_name}', 
                obj.status , obj_data['amount'] , obj.created_at ,
                ])
        return response




class ExportDataExcel(APIView):

    def get(self, request, *args , **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'ID', 'First name', 
            'Lat name','Email' , 
            'Loan amount', 'Repayment amount',
            'Due date','Status' 
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = Loan.objects.all().values_list(
            'uuid', 'user.first_name', 
            'user.last_name','user.email',
            'offer.offer_amount','user.status' ,'due_date'
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(
                    row_num, col_num, 
                    row[col_num], font_style)

        wb.save(response)
        return response





    


    
