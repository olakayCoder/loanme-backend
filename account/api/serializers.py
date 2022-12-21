from rest_framework import serializers
from account.models import User




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)




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
    address = serializers.CharField(allow_blank=True)
    pin = serializers.IntegerField() 


class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField('change_created_at_format')
    phone_verified_at = serializers.SerializerMethodField('change_phone_verified_at_format')
    updated_at = serializers.SerializerMethodField('change_updated_at_format')
    date_of_birth = serializers.SerializerMethodField('change_date_of_birth_format')
    class Meta:
        model = User
        fields = [   
            'uuid','first_name','last_name','email','email_verified','email_verified_at',
            'image','is_active','is_staff','is_admin','created_at','updated_at','deleted_at',
            'date_of_birth','phone','phone_verified','phone_verified_at','verification_completed',
            'marital_status','children','resident_type','rent_per_year','country','state','city',
            'address','lga', 'educational_status','employment_status', 'business_name' , 'monthly_income'
        ]

    
    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y")
    def change_phone_verified_at_format(self , obj ):
        return  obj.phone_verified_at.strftime("%b %d, %Y")
    def change_updated_at_format(self , obj ):
        return  obj.updated_at.strftime("%b %d, %Y")
    def change_date_of_birth_format(self , obj ):
        return  obj.date_of_birth.strftime("%b %d, %Y") 



class AccountSetupBvnSerializer(serializers.Serializer):
    type = serializers.CharField(allow_blank=False)
    number = serializers.IntegerField()







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

