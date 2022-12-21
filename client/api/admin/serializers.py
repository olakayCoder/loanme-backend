from rest_framework import serializers
from client.models import (
    LoanApplication , Loan
)
from client.api.serializers import LoanOfferSerializer
from account.api.serializers import (
    UserSerializer
)







 


class AdminLoanApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True ) 
    created_at = serializers.SerializerMethodField('change_created_at_format')
    class Meta:
        model = LoanApplication
        fields = ['uuid', 'status','data','created_at', 'user'] 

    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y") 



class AdminLoanSerializer(serializers.ModelSerializer):
    offer = LoanOfferSerializer(read_only=True)    
    user = UserSerializer(read_only=True)
    due_date = serializers.SerializerMethodField('change_date_format')
    created_at = serializers.SerializerMethodField('change_created_at_format')
    updated_at = serializers.SerializerMethodField('change_updated_at_format')
    class Meta:
        model = Loan
        fields = ["uuid","user",'offer','amount','status','due_date','created_at','updated_at']


    def change_date_format(self , obj ):
        return  obj.due_date.strftime("%b %d, %Y")

    def change_created_at_format(self , obj ):
        return  obj.created_at.strftime("%b %d, %Y") 

    def change_updated_at_format(self , obj ):
        return  obj.updated_at.strftime("%b %d, %Y")




