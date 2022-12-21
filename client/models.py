from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4 
from django.contrib.auth import get_user_model
from helpers.options import ModelFieldOptions
# Create your models here.
from django.db.models import Sum , F 



User = get_user_model()


class ScoreCriteriaCategory(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 






class ScoreCriteriaOption(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    category = models.ForeignKey(ScoreCriteriaCategory , on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





def is_percentage(value):
    if not isinstance(value, int):
        return False
    if value > 100:
        return False
    return True


class Offer(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    type = models.CharField(max_length=10, choices=ModelFieldOptions.OFFER_TYPE , default='month')
    count = models.IntegerField()
    percentage = models.IntegerField(validators=[is_percentage])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class LoanApplication(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField() 
    status = models.CharField(max_length=10, choices=ModelFieldOptions.LOAN_APPLICATION_STATUS , default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)







class LoanScoreBoard(models.Model):
    uuid = models.CharField(max_length=100 ,  null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey('client.Loan', on_delete=models.CASCADE)
    point = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class LoanOffer(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(LoanApplication , on_delete=models.CASCADE)
    offer = models.OneToOneField(Offer , on_delete=models.SET_NULL , null=True , blank=True )
    period = models.IntegerField(
        help_text=_(''''
        The period that this loan repayment should cover.
        the values are in months eg 3 months , 6 months and 12 months.
        '''
    ))
    interest = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text=_('The interest that is on this loan offer'
    ))
    is_approve = models.BooleanField(default=False)
    # !!! Todd add due_date percentage , principal , total repayment
    percentage = models.IntegerField()
    total_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    offer_amount = models.DecimalField(decimal_places=2, max_digits=10)
    principal_amount = models.DecimalField(decimal_places=2, max_digits=10)
    due_date = models.DateTimeField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






class Loan(models.Model):
    uuid = models.CharField(max_length=100 , default=uuid4, null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.OneToOneField(LoanOffer, on_delete=models.SET_NULL , null=True , blank=True)
    application = models.OneToOneField(LoanApplication , on_delete=models.SET_NULL , null=True , blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=ModelFieldOptions.LOAN_STATUS, default='active' , max_length=10)
    due_date = models.DateField(
        null=True, blank=True,
        help_text=_('The expected date that the loan should be fully paid')
    )
    # data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    @classmethod
    def get_total_paid(cls):
        result  = 0
        for model in cls.objects.all():
            repayments = LoanRepayment.objects.filter(
                        loan=model, payment_status='paid').annotate(
                            sum=F('amount')).aggregate(total_sum= Sum('sum')
                        )
            result += repayments['total_sum']   
        return result


    @classmethod
    def all_loan_total(cls):
        sum = cls.objects.annotate(
            total=Sum(F('amount'))
            ).aggregate(total_price = Sum('total')) 
        return 0 if sum['total_price'] == None else sum['total_price']



    @classmethod
    def get_loan_remaining(cls):
        result = cls.all_loan_total() - cls.get_total_paid()
        return result

 
    





class LoanSchedule(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan = models.ForeignKey(Loan , on_delete=models.CASCADE)
    offer = models.ForeignKey(LoanOffer , on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('loan','Loan'),
        ('card','card'),
    )
    TRANSACTION_STATUS = (
        ('pending','Pending'),
        ('success','Success'),
        ('failed','Failed'),
    )
    uuid = models.CharField(max_length=100 , default=uuid4, null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE , null=True , blank=True)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS , default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






class LoanRepayment(models.Model):
    uuid = models.CharField(max_length=100 , default=uuid4, null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=10, choices=ModelFieldOptions.LOAN_REPAYMENT_TYPE , default='auto')
    payment_status = models.CharField(max_length=10, choices=ModelFieldOptions.LOAN_REPAYMENT_STATUS , default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL ,null=True ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



