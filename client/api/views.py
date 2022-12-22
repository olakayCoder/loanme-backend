from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,IsAdminUser
)
from dateutil.relativedelta import relativedelta
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from django.forms.models import model_to_dict
from client.models import (
    LoanApplication , Loan  , ScoreCriteriaOption , Offer , LoanOffer , LoanSchedule , LoanRepayment , LoanScoreBoard
)
from django.db.models import Sum , F  
from .serializers import (
    LoanRequestSerializer, LoanSerializer , LoanOfferSerializer,
    LoanOfferAcceptSerializer , LoanApplicationSerializer ,LoanScheduleSerializer,
)
from account.api.serializers import (
    UserSerializer , UserBankSerializer,
    UserCardSerializer
)
from account.models import UserBank , UserCard
from helpers.utils import LoanApplicationScore
from helpers.generators import CustomValuesGenerator
import json
from account.models import User
import random
from datetime import datetime , timedelta
from django.utils import timezone

# from dateutil.relativedelta import relativedelta
# t = datetime.now()
# next_week = timedelta(weeks=1)
# n = t + next_week


class LoanApplicationRetrieveCreateApiView(generics.GenericAPIView):
    serializer_class = LoanRequestSerializer  
    permission_classes = [IsAuthenticated]  
    queryset = Loan.objects.all()

    @swagger_auto_schema(
        operation_description='''
        Customer loan applications history endpoint. 
        ''',
        operation_summary='Get customer loan applications history'
    )
    def get(self, request, *args, **kwargs):
        user = User.objects.get(uuid='ACC-2022122181540-2022') 
        loans = LoanApplication.objects.filter(user=user)
        serializer = self.serializer_class(loans, many=True) 
        return Response(serializer.data , status=status.HTTP_200_OK) 
    


    @swagger_auto_schema(
        operation_description='''
        Customer loan application endpoint. 
        The applicant customer must have completed all necessary CAC verification. eg
        BVN
        Account
        etc.
        ''',
        operation_summary='Apply for loan'
    )
    def post(self, request, *args, **kwargs):
        """
        We start in this view by initializing the score variable for the customer
        then check if the customer has an active loan : if yes return status 400 no  continue
        then create an application object for the customer in the DB.
        Now using the score criteria option stored in the DB 
        check customer application value with the criteria score to give increment point
        then check customer score with the loan offer score range e.i > 70 , < 70 > 60 , < 60 > 50 and < 50.
        If the customer meet the criteria to receive loan, calculate loan offer for customer.
        """
        score = 0
        data = request.data
        user = User.objects.get(id=request.user.id)
        # print(data)  
        # user = User.objects.get(id=1)
        if Loan.objects.filter(user=user, status='active').exists():
            return Response({'success':False, 'detail':'You have an active loan'}, status=status.HTTP_400_BAD_REQUEST)
        app = LoanApplication.objects.create(user=user, data=json.dumps(data))

        # personal info response
        marital_status = data['marital_status']
        children = data['children']
        gender = data['gender']
        personal_score_option = ScoreCriteriaOption.objects.filter(category__name='Personal info')
        # print(ScoreCriteriaOption.get_total_points())
        for val in personal_score_option:
            if marital_status == val.name:
                score += val.points
            if children == val.name:
                score += val.points
            if gender == val.name:
                score += val.points
        # education and employment response
        level_of_education = data['education']
        employment = data[ 'employment']
        educational_employment = ScoreCriteriaOption.objects.filter(category__name='Education and employment')
        for val in educational_employment:
            if level_of_education == val.name:
                score += val.points
            if employment == val.name:
                score += val.points

        # WORK
        work_duration = data['years_at_work']
        work_options = ScoreCriteriaOption.objects.filter(category__name='Work')
        for val in work_options:
            if work_duration == val.name:
                print(work_duration) 
                score += val.points

        # residence
        residence = data['residence']
        year_at_residence = data['years_at_residence']
        residence_option_score = ScoreCriteriaOption.objects.filter(category__name='Residence')
        for val in residence_option_score:
            if residence == val.name:
                score += val.points
            if year_at_residence == val.name:
                score += val.points
        # loan reason
        loan_reason = data['reason']
        loan_reason_option_score = ScoreCriteriaOption.objects.filter(category__name='Loan Reason')
        for val in loan_reason_option_score:
            if loan_reason == val.name:
                score += val.points
        f = ['Performing', 'Non performing']
        crc = f[0] 
        crc = random.choice(f)
        loan_reason_option_score = ScoreCriteriaOption.objects.filter(category__name='CRC')
        for val in loan_reason_option_score:
            if crc == val.name: 
                score += val.points
        amount_requested = int(data['amount'])
        #  checking the amount eligibility of the user using the score
        if score >= 70 :
            eligible_amount = (amount_requested) * 1.00 
        if score <= 70 and score >= 60 :
            eligible_amount = (amount_requested) * 0.70 
        if score <= 60 and score >= 50:
            eligible_amount = (amount_requested) * 0.50 
        if score < 50:
            eligible_amount = (amount_requested) * 0.00
            return Response({'detail':'Not eligible for loan'}, status=status.HTTP_200_OK)
        # calculating loan offer for the user to generate loan offer
        # print(score)  
        # print(crc)
        # loan_offers_list = [] 
        offers = Offer.objects.filter(type='month')
        for offer in offers:
            print(offer)
            offer_amount = eligible_amount
            offer_interest = round( float(eligible_amount * (offer.percentage / 100)) , 2 )
            offer_total_repayment =  round( float(eligible_amount + (eligible_amount * (offer.percentage / 100))) , 2)
            offer_principal = eligible_amount 
            offer_payment_duration = offer.count
            offer_percentage = offer.percentage 
            # !!! todo , change weeks to month using the  from dateutil.relativedelta import relativedelta
            # offer_due_date =  (
            #     (datetime.now()  +  timedelta(weeks=offer_payment_duration)).strftime("%b %d, %Y")
            #     ) 
            offer_due_date = timezone.now()  +  relativedelta(months=offer_payment_duration)
            # (weeks=offer_payment_duration) 
            offer_for_user = LoanOffer.objects.create(
                application=app, 
                period=offer_payment_duration ,
                user=user,
                interest = offer_interest , 
                percentage=offer_percentage, 
                due_date=offer_due_date,  
                principal_amount = offer_principal ,
                total_repayment = offer_total_repayment ,
                offer_amount=offer_amount,   
            )
            print(offer_amount) 
        m = LoanOffer.objects.filter(user=user, application=app)
        for n in m:
            print(n) 
        serializer = LoanOfferSerializer(m , many=True )  
        LoanApplicationScore.score_application(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({'h':'kk'}, status=status.HTTP_201_CREATED)



class LoanRetrieveRequestApiView(generics.GenericAPIView):
    serializer_class = LoanSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='''
        Retrieve a loan detail. 
        ''',
        operation_summary='Get customer loan detail'
    )
    def get(self, request, uuid , *args, **kwargs):
        user = User.objects.get(id=1)  
        loan = Loan.objects.get(user=user)
        serializer = self.serializer_class(loan)        
        return Response(serializer.data , status=status.HTTP_200_OK) 


class OfferReceiveApproved(generics.GenericAPIView):
    serializer_class = LoanOfferAcceptSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='''
        Accept loan offer. 
        ''',
        operation_summary='Accept a loan offer'
    )
    def post(self, request , *args, **kwargs ):
        user = User.objects.get(id=request.user.id) 
        # user = User.objects.get(id=1) 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            offer = LoanOffer.objects.get(uuid=serializer.validated_data['offer_uuid'])
        except LoanOffer.DoesNotExist:
            return Response({'success':False,'detail':'Offer does not exists'}, status=status.HTTP_404_NOT_FOUND)
        if offer.is_approve :
            return Response({'success':False,'detail':'Offer have been approved already'}, status=status.HTTP_400_BAD_REQUEST)

        application = LoanApplication.objects.get(id=offer.application.id)
        amount_junk = offer.total_repayment / offer.period 
        loan = Loan.objects.create(
            user=user, offer=offer, application=application , 
            amount=offer.total_repayment , due_date=offer.due_date
        ) 
        for period in range(1 , offer.period + 1 ):
            # !!! todo , change weeks to month using the  from dateutil.relativedelta import relativedelta
            date = timezone.now()  +  relativedelta(weeks=period) 
            LoanSchedule.objects.create(
                user=user, amount=amount_junk, 
                loan=loan , offer=offer , date=date 
            )
        offer.is_approve = True
        offer.save()
        application.status = 'accepted'
        application.save()
        other_offer = LoanOffer.objects.filter(application=application)
        for model in other_offer:
            if model.is_approve == False :
                model.delete()
        response = {
            'success':True,
            'detail': 'Money will be transfer to your account shortly'
        }
        return Response( response ,  status=status.HTTP_200_OK)




class UserLoanListApiView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer 

    @swagger_auto_schema(
        operation_description='''
        Customer loans history endpoint. 
        ''',
        operation_summary='Get customer loans history'
    )
    def get(self, request, *args, **kwargs):
        # user = User.objects.get(id=request.user.id) 
        user = User.objects.get(id=1)  
        loans = Loan.objects.filter(user=user)
        serializer = self.serializer_class(loans, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK) 



class LoanScheduleListApiView(generics.ListAPIView):
    queryset = LoanSchedule.objects.all() 
    serializer_class = LoanScheduleSerializer  

    @swagger_auto_schema(
        operation_description='''
        Customer loans history endpoint. 
        ''',
        operation_summary='Get customer loans history'
    )
    def get(self, request, uuid , *args, **kwargs):
        # user = User.objects.get(id=request.user.id) 
        user = User.objects.get(id=1)
        try:
            loan = Loan.objects.get(uuid=uuid)
        except Loan.DoesNotExist:
            return  Response({'success':False, 'detail':'Loan does not exist'}, status=status.HTTP_404_NOT_FOUND)
        loan_schedules = LoanSchedule.objects.filter(loan=loan)
        serializer = self.serializer_class(loan_schedules, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK) 


class OutStandingLoanListApiView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer 
    # permission_classes = [IsAuthenticated,IsAdminUser]

       

    @swagger_auto_schema(
        operation_description='''
        Retrieve customer active loan detail. 
        ''',
        operation_summary='Get customer active loan detail'
    )    
    def get(self, request, *args, **kwargs):
        # CustomValuesGenerator.create_offers()
        # CustomValuesGenerator.score_criteria()
        # user = User.objects.get(id=request.user.id)
        user = User.objects.get(id=1) 
        loan = Loan.objects.filter(status='active', user=user)
        serializer = self.serializer_class(loan, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK) 





class CustomersListApiView(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer 
    # permission_classes = [IsAuthenticated,IsAdminUser]


    # @permission_classes([IsAuthenticated])
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)





class UserBankListApiView(generics.ListAPIView):
    queryset = UserBank.objects.all()
    serializer_class = UserBankSerializer 
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        bank = UserBank.objects.filter(user=user)
        serializer = self.serializer_class(bank, many=True).data
        return Response(serializer , status=status.HTTP_200_OK)


class UserCardListApiView(generics.ListAPIView):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer
    permission_classes = [IsAuthenticated]  


    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        card = UserCard.objects.filter(user=user)
        serializer = self.serializer_class(card , many=True).data
        return Response(serializer , status=status.HTTP_200_OK)





class UserLoansApiView(generics.ListAPIView):
    queryset = Loan.objects.all() 
    serializer_class = LoanSerializer 
    permission_classes = [IsAuthenticated]  


    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        card = Loan.objects.filter(user=user)  
        serializer = self.serializer_class(card , many=True).data
        return Response(serializer , status=status.HTTP_200_OK)



class UserLoanRemainingApiView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = UserCardSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        # getting all loan sum
        all_loan_sum = 0
        sum = Loan.objects.filter(user=user).annotate(
            total=Sum(F('amount'))
            ).aggregate(total_price = Sum('total')) 
        all_loan_sum =  0 if sum['total_price'] == None else sum['total_price']
        paid_loan  = 0
        # getting total paid loan for user 
        for model in Loan.objects.filter(user=user):
            repayments = LoanRepayment.objects.filter(
                        loan=model, payment_status='paid').annotate(
                            sum=F('amount')).aggregate(total_sum= Sum('sum')
                        )
            paid_loan += repayments['total_sum']   
        
        loan_debt = all_loan_sum - paid_loan 
        
        response = {
            'success': True,
            'detail':'Loan debt retrieve',
            'debt':loan_debt
        }
        if loan_debt == 0 :
            response.update({
                'hasActiveLoan':False
            })
        else:
            response.update({
                'hasActiveLoan':True
            })
        return Response(response, status=status.HTTP_200_OK)

