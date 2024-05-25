from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from.serializers import PieceSerializer
from piece.models import Piece
from core.permissions import IsOwnerOrReadOnly
from core.pagination import RandomResultsSetPagination
from .permissions import has_update_permissions, has_delete_permissions

# Create your views here.
class PieceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    lookup_field = 'slug'
    permission_classes = [
        IsAuthenticatedOrReadOnly, 
        DjangoModelPermissionsOrAnonReadOnly,
    ]

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            'user': request.user.slug,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class PieceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    lookup_field = 'slug'
    permission_classes = [
        IsAuthenticatedOrReadOnly, 
        DjangoModelPermissionsOrAnonReadOnly,
        IsOwnerOrReadOnly,
    ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "result": serializer.data,
            "perms": {
                "update": has_update_permissions(instance, request),
                "delete": has_delete_permissions(instance, request),
            }
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {
            **request.data,
            'user': request.user.slug,
        }
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class PieceRandomListAPIView(generics.ListAPIView):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    lookup_field = 'slug'
    pagination_class = RandomResultsSetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly, 
        DjangoModelPermissionsOrAnonReadOnly,
        IsOwnerOrReadOnly,
    ]