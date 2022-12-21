from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import (
    User, UserBank , Phone , UserCard , UserBvn 
)
# Register your models here.



class UserBankInline(admin.StackedInline):
    model = UserBank


class CustomUserAdminConfig(UserAdmin):     
    model = User
    search_fields = ('email', 'first_name',)   
    list_filter = ('email', 'first_name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'first_name','last_name', 'is_active', 'is_staff', 'is_superuser',) 
    fieldsets = (
        (None, {'fields': (
           'uuid','first_name','last_name','email','email_verified','email_verified_at',
            'image','is_admin','deleted_at',  'date_of_birth','phone','phone_verified','phone_verified_at','verification_completed',
            'marital_status','children','resident_type','rent_per_year','country','state','city',
            'address','lga', 'educational_status','employment_status', 'business_name' , 'monthly_income'
            
        )}),   
         
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email' , 'first_name',  'last_name',   'password1','password2' , 'is_active', 'is_staff' )} 
         ),
    )


admin.site.register(User, CustomUserAdminConfig) 
admin.site.register(Phone)          
admin.site.register(UserCard)
admin.site.register(UserBvn)       