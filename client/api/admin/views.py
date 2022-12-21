from rest_framework import generics , status 
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import (User)
from account.api.serializers import UserSerializer
from client.models import (
    Loan , LoanApplication
)
from client.api.serializers import (
    LoanSerializer , LoanApplicationSerializer ,
) 
from .serializers import (
    AdminLoanApplicationSerializer , AdminLoanSerializer
)
from django.db.models import Sum , F 


class AllCustomersListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().exclude(is_staff=True)


class CustomerRetrieveApiView(generics.RetrieveDestroyAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all().exclude(is_staff=True)
    lookup_field = 'uuid'


class CustomerDisableApiView(generics.GenericAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all().exclude(is_staff=True)

    def get(self, request,uuid, *args, **kwargs):
        try:
            customer = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response({'success':False,'detail':'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        customer.is_active = False
        customer.save()
        return Response({'success':True, 'detail':'Customer disabled'}, status=status.HTTP_200_OK)


class CustomerEnableApiView(generics.GenericAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all().exclude(is_staff=True)

    def get(self, request,uuid, *args, **kwargs):
        try:
            customer = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response({'success':False,'detail':'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        customer.is_active = True
        customer.save()
        return Response({'success':True, 'detail':'Customer enabled'}, status=status.HTTP_200_OK)



class CustomerApplicationListApiView(generics.GenericAPIView): 
    serializer_class = LoanApplicationSerializer 
    queryset = LoanApplication.objects.all() 

    def get(self, request,uuid, *args, **kwargs):
        try:
            customer = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response({'success':False,'detail':'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        applications = LoanApplication.objects.filter(user=customer) 
        serializer = self.serializer_class(applications , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class CustomerLoansListApiView(generics.GenericAPIView): 
    serializer_class = LoanSerializer 
    queryset = Loan.objects.all() 

    def get(self, request,uuid, *args, **kwargs):
        try:
            customer = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response({'success':False,'detail':'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        applications = Loan.objects.filter(user=customer) 
        serializer = self.serializer_class(applications , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)



class AllLoanApplicationApiView(generics.ListAPIView):
    serializer_class = AdminLoanApplicationSerializer
    queryset = LoanApplication.objects.all() 


# APP-20221219225430-2022

class ApplicationDetailApiView(generics.RetrieveAPIView):
    serializer_class = AdminLoanApplicationSerializer
    queryset = LoanApplication.objects.all() 
    lookup_field = 'uuid'


class AllLoanApiView(generics.ListAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()  


class LoanDetailApiView(generics.RetrieveDestroyAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()   
    lookup_field = 'uuid'  





class LoanApplicationSummaryApiView(APIView): 

    def get(self, request, *args, **kwargs):
        total_applications = LoanApplication.objects.all()
        total_applications_count = total_applications.count()
        pending_applications = total_applications.filter(status='pending').count()
        rejected_applications = total_applications.filter(status='rejected').count()
        accepted_applications = total_applications.filter(status='accepted').count()
        summary = {
            'total':total_applications_count,
            'pending':pending_applications,
            'accepted':accepted_applications,
            'rejected': rejected_applications 
        }
        return Response(summary , status=status.HTTP_200_OK)



class LoanSummaryApiView(APIView):     

    def get(self, request, *args, **kwargs):
        total_loan = Loan.objects.all()
        total_loan_count = total_loan.count()
        pending_loan_count = total_loan.filter(status='active').count()
        completed_loan = total_loan.filter(status='completed').count()
        total_loan_amount = Loan.all_loan_total()
        total_loan_paid_amount = Loan.get_total_paid()
        total_loan_remaining_amount = Loan.get_loan_remaining()
        summary = { 
            'total': total_loan_count,
            'active_loan':pending_loan_count,
            'completed': completed_loan,
            'sum_of_total_loan':  total_loan_amount,
            'sum_of_active_loan':  total_loan_remaining_amount, 
            'total_repayment':  total_loan_paid_amount ,  
        } 
        return Response(summary , status=status.HTTP_200_OK) 



class CustomerSummaryApiView(APIView):     

    def get(self, request, *args, **kwargs):
        summary = { 
            'all': User.objects.all().exclude(is_staff=True).count(), 
            'active':User.active_user(),
            'disabled': User.disabled_user(),
        } 
        return Response(summary , status=status.HTTP_200_OK) 