from rest_framework import serializers
from account.models import User , UserBank , UserCard
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class LoginSerializer( TokenObtainPairSerializer , serializers.Serializer ):
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        cus = UserSerializer(user).data  
        # Add custom claims
        token['data'] = cus
        # ...
 
        return token




class SignupPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(allow_blank=True)

    

class SignupPhoneVerifySerializer(serializers.Serializer):
    code = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)
    state = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    address_1 = serializers.CharField(allow_blank=True)
    address_2 = serializers.CharField(allow_blank=True)
    pin = serializers.IntegerField() 


class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField('change_created_at_format')
    # phone_verified_at = serializers.SerializerMethodField('change_phone_verified_at_format')
    updated_at = serializers.SerializerMethodField('change_updated_at_format')
    # date_of_birth = serializers.SerializerMethodField('change_date_of_birth_format') 
    class Meta:
        model = User
        fields = [   
            'uuid','first_name','last_name','email','email_verified','email_verified_at',
            'image','gender','is_active','is_staff','is_admin','created_at','updated_at','deleted_at',
            'date_of_birth','phone','phone_verified','phone_verified_at','verification_completed',
            'marital_status','children','resident_type','rent_per_year','country','state','city', 'is_card','is_bvn','is_bank',
            'address1', 'address2','lga', 'educational_status','employment_status', 'business_name' , 'monthly_income'
        ]

    
    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y")
    def change_phone_verified_at_format(self , obj ):
        if obj.phone_verified_at:
            return  obj.phone_verified_at.strftime("%b %d, %Y")
        return None
    def change_updated_at_format(self , obj ):
        return  obj.updated_at.strftime("%b %d, %Y")
    def change_date_of_birth_format(self , obj ):
        if obj.date_of_birth:
            return  obj.date_of_birth.strftime("%b %d, %Y") 
        return None



class AccountSetupBvnSerializer(serializers.Serializer):
    type = serializers.CharField(allow_blank=False)
    number = serializers.IntegerField()




class UserBankSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField('change_created_at_format')
    updated_at = serializers.SerializerMethodField('change_updated_at_format')
    class Meta:
        model = UserBank
        fields = ['uuid','user','name','code','account_number','account_name','created_at','updated_at']

    def change_updated_at_format(self , obj ):
        return  obj.updated_at.strftime("%b %d, %Y")

    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y")

    
    extra_kwargs = {
            'uuid':{'read_only' : True},  
            'user':{'read_only' : True},  
            'created_at':{'read_only' : True}, 
            'updated_at':{'read_only' : True}, 
        }



class UserCardSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField('change_created_at_format')
    updated_at = serializers.SerializerMethodField('change_updated_at_format')
    class Meta:
        model = UserCard
        fields = [
            'uuid','user','code','type','start',
            'last', 'is_default','account_name',
            'created_at', 'updated_at'
        ]

    def change_updated_at_format(self , obj ):
        return  obj.updated_at.strftime("%b %d, %Y")

    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y")

    
    extra_kwargs = {
            'uuid':{'read_only' : True},  
            'user':{'read_only' : True},  
            'created_at':{'read_only' : True}, 
            'updated_at':{'read_only' : True}, 
        }



"""
!!! USER PASSWORD MANAGEMENT SERIALIZER START
"""
class ResetPasswordRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields =  ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=1,max_length=30, write_only=True , style={'input-type': 'password'} )
    password2 = serializers.CharField(min_length=1,max_length=30, write_only=True , style={'input-type': 'password'} )
    
    class Meta:
        fields = ['password', 'password2']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True , style={'input-type': 'password'} )
    password1 = serializers.CharField(required=True , style={'input-type': 'password'} )
    password2 = serializers.CharField(required=True , style={'input-type': 'password'} )

