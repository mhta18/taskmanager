from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the owner of a task can edit or delete it.
    Others can only view.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner
        return obj.owner == request.user