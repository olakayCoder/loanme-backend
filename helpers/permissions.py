from rest_framework import permissions
from account.models import User


permissions.IsAdminUser

class IsStudentParent(permissions.DjangoModelPermissions):


    def has_permission(self, request, view):
        return request.user.is_verified
     
    def has_object_permission(self, request, view, obj):
        if obj.parent == None :
            return False
        return bool(request.user and request.user.is_authenticated  and request.user == obj.parent.user)
  

