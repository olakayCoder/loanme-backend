from rest_framework import status  , generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import User , Phone 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes,   force_str, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .serializers import (
    SignupPhoneSerializer , SignupPhoneVerifySerializer , SignupSerializer,
    UserSerializer , AccountSetupBvnSerializer , ResetPasswordRequestEmailSerializer,
    ChangePasswordSerializer , SetNewPasswordSerializer , LoginSerializer ,
)
from helpers.utils import INVALID_CODES , create_jwt_pair_for_user
from helpers.options import ModelFieldOptions
from helpers.mailing import MailServices
from helpers.generators import CustomValuesGenerator
from datetime import datetime
import time
from threading import Thread
from drf_yasg.utils import swagger_auto_schema
from client.models import Transaction
from django.contrib.auth import authenticate
from uuid import uuid4

from rest_framework.exceptions import PermissionDenied , NotAuthenticated




class PhoneApiView(generics.GenericAPIView):
    serializer_class = SignupPhoneSerializer

    def post(self,request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            if User.objects.filter(phone=serializer.validated_data['phone']).exists():
                return Response({'success':False,'detail': 'Number already exist'} , status=status.HTTP_400_BAD_REQUEST)
            Phone.objects.create(phone=serializer.validated_data['phone'])
            return  Response({'success':True,'detail': 'Verification code sent to phone number'} , status=status.HTTP_200_OK)
        return Response({'success':False,'detail': 'Number is required'} , status=status.HTTP_400_BAD_REQUEST)



class PhoneVerifyApiView(generics.GenericAPIView):
    serializer_class = SignupPhoneVerifySerializer

    def post(self,request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            if len(str(code)) >= 6 and code not in INVALID_CODES:
                phone = Phone.objects.get(phone=serializer.validated_data['phone'])
                phone.is_verified = True
                phone.save()
                return  Response({'success':True,'detail': 'Phone number verification successfully'} , status=status.HTTP_200_OK)
        return Response({'success':False,'detail': 'Invalid verification code'} , status=status.HTTP_400_BAD_REQUEST)


class UserSignupApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request , *args, **kwarg):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(): 
            phone_verified = Phone.objects.filter(phone=serializer.validated_data['phone'], is_verified=True)

            if phone_verified:
                phone_verified = phone_verified.first()
                phone_verified.delete()

                new_user = User()
                new_user.first_name = serializer.validated_data['first_name']
                new_user.last_name = serializer.validated_data['last_name']
                new_user.email = serializer.validated_data['email']
                new_user.phone = serializer.validated_data['phone'] 
                new_user.phone_verified = True
                new_user.phone_verified_at = datetime.now() 
                new_user.country = serializer.validated_data['country']
                new_user.state = serializer.validated_data['state']
                new_user.city = serializer.validated_data['city']
                new_user.address = serializer.validated_data['address']

                new_user.set_password(str(serializer.validated_data['pin']))
                try:
                    tokens = create_jwt_pair_for_user(new_user)
                    new_user.save()
                    return Response({
                        'success':True,
                        'detail': 'Account created successfully',
                        'tokens': tokens,
                        'user': UserSerializer(new_user).data
                    } , status=status.HTTP_200_OK)
                except:
                    return Response({'success':False,'detail': 'Error occurred creating account'} , status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':False,'detail': 'Error occurred creating account. Try again later'} , status=status.HTTP_400_BAD_REQUEST)



class AccountSetupBvnApiView(generics.GenericAPIView):
    serializer_class = AccountSetupBvnSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            if serializer.validated_data.get('type','BVN') in ModelFieldOptions.KYC_TYPE:
                number = serializer.validated_data['number']
                print(len(str(number)))
                if len(str(number)) != 10 : 
                    response = {'success':False,'detail': 'Invalid  number length'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                time.sleep(5) 
                return Response({'success':False,'detail': 'BVN verification successful'} , status=status.HTTP_200_OK)

        print(CustomValuesGenerator.random_bvn(20))
        response = {'success':False,'detail': 'Invalid credential provided'}
        for error_type , error_msg in serializer.errors.items():
            if error_type == 'type' :
                response.update({'type':'KYC type is required'})
            if error_type == 'number' :
                response.update({'number':'Valid number is required'})
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class AddDebitCardApiView(generics.GenericAPIView):
    serializer_class = AccountSetupBvnSerializer
  
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=1)
        uuidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reference = f'ref_{uuidb64}_{uuid4().hex}' 
        Transaction.objects.create(
            user=user, type='card', amount='50', 
            reference=reference 
        )
        return Response(status=status.HTTP_400_BAD_REQUEST)









class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
  
    @swagger_auto_schema(
        operation_description='Authenticate user',
        operation_summary='Authenticate user'
    )
    def post(self, request ):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True): 
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']
            user = authenticate(email=email , password=password)
            mail = User.check_email(email)
            if user is not None :
                if user.is_active:
                    serializer = UserSerializer(user)
                    tokens = create_jwt_pair_for_user(user)
                    response = {
                        'success': True ,
                        'message': 'Login is successful',
                        "tokens" : tokens , 
                        'user' : serializer.data 
                    }
                    return Response(response , status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied(
                        "Your account is disabled, kindly contact the administrative")
            if mail:
                raise PermissionDenied(
                        "Your account is disabled, kindly contact the administrative")
            return Response({'success': False , 'message': 'Invalid login credential'}, status=status.HTTP_400_BAD_REQUEST)





# !!! PASSWORD MANAGEMENT VIEW START
class ResetPasswordRequestEmailApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestEmailSerializer
    

    @swagger_auto_schema(
        operation_description='Request for password reset using an email account',
        operation_summary='Reset password request'
    )
    def post(self, request):
        email = request.data['email']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(email=email)
                uuidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                Thread(target=MailServices.forget_password_mail, kwargs={
                    'email': user.email ,'token': token , 'uuidb64':uuidb64
                }).start()
                return Response( 
                        {'success':True , 'message': 'Password reset instruction will be sent to the mail' },
                        status=status.HTTP_200_OK
                        )
            except:
                return Response( 
                    {'success':True , 'message': 'Password reset instruction will be sent to the mail' }, 
                    status=status.HTTP_200_OK
                    )
        return Response( 
                    {'success':False , 'message': 'Enter a valid email address' }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )

# This view handle changing of user password on forget password
class SetNewPasswordTokenCheckApi(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer


    @swagger_auto_schema(
        operation_description='Reset password confirm',
        operation_summary='Reset password confirm'
    )
    def post(self, request, token , uuidb64 ):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            password1 = request.data['password1']
            password2 = request.data['password2']
            if password1 != password2 :
                return  Response({'success':False ,'message': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
            if PasswordResetTokenGenerator().check_token(user, token):
                data = request.data
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                user.set_password(serializer.validated_data['password1'])
                user.save() 
                return Response({'success':True , 'message':'Password updated successfully'}, status=status.HTTP_200_OK)
            return Response({'success':False ,'message':'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'success':False ,'message': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)


#  This view handle password update within app ( authenticated user)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer 
    permission_classes = [ IsAuthenticated ] 
    model = User

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    

    @swagger_auto_schema(
        operation_description='Change user password',
        operation_summary='Change user password'
    )
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']
            if password1 != password2 :
                return  Response({'success':False ,'detail': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'success':False ,'detail': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("password2"))
            self.object.save()
            response={
                'success': True,
                'detail': 'Password updated successfully',
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AccountApiView(generics.GenericAPIView):
    serializer_class = UserSerializer



    def get(self,request, *args,**kwargs):
        CustomValuesGenerator.random_bvn() 
        user = User.objects.get(id=1) 
        serializer = self.serializer_class(user)
        return Response(serializer.data, status.HTTP_200_OK) 