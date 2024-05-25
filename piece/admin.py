from django.contrib import admin
from .models import Piece

# Register your models here.
@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_at')