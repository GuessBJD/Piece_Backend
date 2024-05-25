from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

# Create your models here.
class Piece(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, null=False, blank=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text

from .signals import *