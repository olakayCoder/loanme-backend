from django.db.models.signals import post_save , pre_save , post_delete
from django.dispatch import receiver
from uuid import uuid4
from .models import (
   Loan , LoanApplication ,LoanOffer ,LoanRepayment,Offer, Transaction,
   LoanSchedule,LoanScoreBoard , ScoreCriteriaCategory , ScoreCriteriaOption
)
import os
from helpers.utils import get_current_timestamp



@receiver(post_save , sender=Loan)
def user_loan_signal(sender, instance , created , **kwarg):
    if created:
        stamp_time = get_current_timestamp()
        unique_slug = f'LN-{stamp_time}'
        instance.uuid = unique_slug
        instance.save()


 
@receiver(post_save , sender=ScoreCriteriaOption)
def user_score_criteria_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()


@receiver(post_save , sender=ScoreCriteriaCategory)
def user_profile_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()


@receiver(post_save , sender=Offer)
def user_offer_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()





@receiver(post_save , sender=LoanApplication)
def user_loan_application_signal(sender, instance , created , **kwarg):
    if created:
        stamp_time = get_current_timestamp()
        unique_slug = f'APP-{stamp_time}'
        instance.uuid =unique_slug
        instance.save()




@receiver(post_save , sender=LoanSchedule)
def user_loan_schedule_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()





@receiver(post_save , sender=LoanScoreBoard)
def user_loan_score_board_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()





@receiver(post_save , sender=LoanOffer)
def user_loan_offer_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()



@receiver(post_save , sender=LoanRepayment)
def user_loan_repayment_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()




@receiver(post_save , sender=Transaction)
def user_transaction_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()
