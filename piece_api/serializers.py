from django.contrib.auth import get_user_model
from rest_framework import serializers
from piece.models import Piece

User = get_user_model()

class PieceSerializer(serializers.ModelSerializer):  
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='slug')
    
    class Meta:
        model = Piece
        fields = ['text', 'user', 'slug', 'created_at']
        read_only_fields = ['slug', 'created_at']
    