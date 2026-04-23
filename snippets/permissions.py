from rest_framework import permissions

class isOwnerOrReadOnly(permissions.BasePermission):
    """
    custom permission that only allows owners to edit/delete the view
    """
    def has_object_permission(self, request, view, obj):
        # allow GET, HEAD, or OPTION request for everyone.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner==request.user