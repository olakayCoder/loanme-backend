from rest_framework import serializers
from client.models import (
    Loan, LoanApplication , LoanOffer ,LoanRepayment ,LoanSchedule ,LoanScoreBoard
)
from datetime import datetime , timedelta

class LoanRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    gender = serializers.CharField(allow_blank=False)
    date_of_birth = serializers.DateField()
    marital_status = serializers.CharField(allow_blank=False)
    children = serializers.CharField(allow_blank=False)

    education = serializers.CharField(allow_blank=False)
    employment = serializers.CharField(allow_blank=False)
    employer = serializers.CharField(allow_blank=False)
    income = serializers.IntegerField()

    residence = serializers.CharField(allow_blank=False)
    years_at_residence = serializers.CharField(allow_blank=False)
    rent_per_year = serializers.CharField()

    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    bank_name = serializers.CharField(allow_blank=False)
    account_name = serializers.CharField(allow_blank=False)
    account_number = serializers.CharField(allow_blank=False)


    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    reason = serializers.CharField(allow_blank=False)



class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['uuid', 'status','data']      




class LoanScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSchedule
        fields = "__all__"

    



class LoanOfferSerializer(serializers.ModelSerializer):
    due_date = serializers.SerializerMethodField('change_date_format')
    application = LoanApplicationSerializer(read_only=True)   
    class Meta:
        model = LoanOffer
        fields = ['uuid' , 'application', 'period' , 'interest' , 'percentage' , 'total_repayment', 'offer_amount', 'due_date' ]  

    def change_date_format(self , obj ):
        return  obj.due_date.strftime("%b %d, %Y")
     



class LoanOfferAcceptSerializer(serializers.ModelSerializer):
    offer_uuid = serializers.CharField(allow_blank=False)
    class Meta:
        model = LoanOffer
        fields = ['offer_uuid']  


    def change_date_format(self , obj ):
        return  obj.due_date.strftime("%b %d, %Y")



class LoanSerializer(serializers.ModelSerializer):
    offer = LoanOfferSerializer(read_only=True)
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