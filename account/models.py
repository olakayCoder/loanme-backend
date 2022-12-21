from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin ,BaseUserManager
from django.contrib.auth.models import Group , Permission
# Create your models here.
from uuid import uuid4 
from helpers.options import ModelFieldOptions



def upload_to(instance, filename):
    return 'profiles/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model( email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,email,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(email,password,**extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    !!! ACCOUNT PIN IS THE PASSWORD
    """
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    first_name = models.CharField(max_length=100, null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True) 
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False, help_text=_('Flag to determine if email has been verified'))
    email_verified_at = models.DateTimeField(
        null=True, blank=True,
        help_text=_('The date email was verified')
    )
    image = models.ImageField( 
        upload_to=upload_to , null=True , blank=True ,
        help_text=_(
            "This image will be gotten from the bvn data return"
        ),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(
        null=True, blank=True,
        help_text=_('The date this user account was deleted')
    )
    date_of_birth = models.DateField(null=True , blank=True)
    verification_completed = models.BooleanField(
        default=False,
        help_text=_('Flag that determined if the user has completed all necessary verifications')
    )
    phone = models.CharField( max_length=20, null=False , blank=False )
    phone_verified = models.BooleanField(
        default=False,
        help_text=_('Flag that determined if the phone number has been verified')
    )
    phone_verified_at = models.DateTimeField(
        null=True, blank=True,
        help_text=_('The date phone number was verified')
    )
    marital_status = models.CharField(
        choices=ModelFieldOptions.MARITAL_STATUS , null=True , blank=True, max_length=10,
        help_text=_('The marital status of the user')
    )

    children = models.CharField(max_length=20, choices=ModelFieldOptions.CHILDREN_COUNT ,null=True, blank=True)
    resident_type = models.CharField(max_length=10, choices=ModelFieldOptions.RESIDENT_TYPE , null=True , blank=True)
    rent_per_year  = models.DecimalField(
        null=True, blank=True,
        decimal_places=2, max_digits=10,
        help_text=_('This field is required for a rented apartment') 
    )

    """
    The field that is related to the user address and location starts
    """
    country = models.CharField(max_length=50, null=True , blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    lga = models.CharField(
        max_length=100, null=True, blank=True,
        help_text=_('Local government area of the user location')
    )

    """
    The field that is related to the user educational and employment detail  starts
    """
    educational_status = models.CharField(
        max_length=20, choices=ModelFieldOptions.EDUCATIONAL_STATUS, null=True, blank=True,
        help_text=_('Educational level of the user')
    )
    employment_status = models.CharField(
        max_length=20, choices=ModelFieldOptions.EMPLOYMENT_STATUS, null=True, blank=True,
        help_text=_('Employment status of the user')
    )
    business_name = models.CharField(
        max_length=100, null=True, blank=True,
        help_text=_('The employer name or business name of the user working place')
    )
    monthly_income = models.IntegerField(null=True, blank=True)

    objects= UserManager()

    USERNAME_FIELD ="email" 



    def __str__(self) -> str:
        return self.email


    @classmethod
    def check_email(cls, email:str):
        return cls.objects.filter(email=email).exists()


    @classmethod
    def disabled_user(cls):
        return cls.objects.filter(is_active=False , is_staff=False).count()


    @classmethod
    def active_user(cls):
        return cls.objects.filter(is_active=True , is_staff=False).count()

  

class UserBank(models.Model):
    uuid = models.CharField(max_length=100 ,  null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True , blank=True)
    code = models.IntegerField(null=True , blank=True)
    account_number = models.IntegerField(null=True , blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)





class UserNextOfKin(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    first_name = models.CharField(max_length=100, null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True) 
    email = models.EmailField(unique=True)
    phone = models.CharField( max_length=20, null=False , blank=False )
    country = models.CharField(max_length=50, null=True , blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True),
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

class UserBvn(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=100)
    marital = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    mixing = models.CharField(max_length=100)
    registered_date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=100 , default=uuid4)







class UserCard(models.Model):
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField( 
        max_length=100, null=True , blank=True,
        help_text=_('The authorization code of the card')
    )
    type = models.CharField(
        max_length=100 , null=True , blank=True,
        help_text=_('The type of card used')
    ) 
    start = models.IntegerField(
        null=True , blank=True,
        help_text=_('First six digit of the card')
    )
    last = models.IntegerField(
        null=True , blank=True,
        help_text=_('First six digit of the card')
    )
    account_name = models.CharField(max_length=200, null=True)
    email = models.EmailField( null=True , blank=True)
    is_default = models.BooleanField(default=False)
    is_reusable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Phone(models.Model):
    phone = models.CharField( max_length=20, null=False , blank=False )
    is_verified = models.BooleanField( default=False )
    created_at = models.DateTimeField(auto_now_add=True)  