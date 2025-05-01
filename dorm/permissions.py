from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import UserRole

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

#         required_permission = getattr(view, 'required_permission', None)
#         if required_permission is None:
#             return False
        
#         user_roles = UserRole.objects.filter(user=request.user, deleted_status=False)
#         for user_role in user_roles:
#             if user_role.role and required_permission in user_role.role.permissions.values_list('permission_name', flat=True):
#                 return True
#         return False
