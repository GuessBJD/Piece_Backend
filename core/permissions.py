from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Custom permission class to only allow owners of an object to edit it

    def has_object_permission(self, request, view, obj):
        # Check if the request method is a safe method (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Return True if the object's owner is the same as the requesting user
        return obj.user == request.user