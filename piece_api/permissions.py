
def is_owner(instance, request):
    return instance.user == request.user

def has_update_permissions(instance, request):
    return (request.user.has_perm('piece.change_piece') and is_owner(instance, request))

def has_delete_permissions(instance, request):
    return (request.user.has_perm('piece.delete_piece') and is_owner(instance, request))