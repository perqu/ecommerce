from rest_framework.permissions import BasePermission

class HasGroupPermission(BasePermission):
    """
    Custom permission to check if the user belongs to a specific group.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        required_groups = getattr(view, 'required_groups', [])
        return request.user.groups.filter(name__in=required_groups).exists()
