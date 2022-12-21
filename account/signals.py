from django.db.models.signals import post_save , pre_save , post_delete
from django.dispatch import receiver
from uuid import uuid4
from .models import (
    User , UserBank , UserNextOfKin , UserBvn , UserCard
)
import os
from helpers.utils import get_current_timestamp



@receiver(post_save , sender=User)
def user_profile_signal(sender, instance , created , **kwarg):
    if created:
        stamp_time = get_current_timestamp()
        unique_slug = f'ACC-{stamp_time}'
        instance.uuid = unique_slug
        instance.save()




@receiver(post_save , sender=UserBank)
def user_bank_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()



@receiver(post_save , sender=UserNextOfKin)
def user_next_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()



@receiver(post_save , sender=UserCard)
def user_card_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()



@receiver(post_save , sender=UserBvn)
def user_card_signal(sender, instance , created , **kwarg):
    if created:
        instance.uuid = uuid4().hex
        instance.save()
