import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.contrib.auth.models import Group, Permission
from .models import MyUser
from .utils import custom_user_slugify

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=MyUser)
def MyUser_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.slug == None or instance.slug == '':
        try:
            instance.slug = custom_user_slugify(instance.email)
            instance.save()
        except ValidationError as e:
            logger.error(f"Failed to generate a unique slug: {e}")

@receiver(post_save, sender=MyUser)
def MyUser_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if not Group.objects.filter(name__iexact="Piece_General_Permission"):
            group = Group.objects.create(name="Piece_General_Permission")
            permissions = Permission.objects.filter(codename__in=["add_piece", "change_piece", "delete_piece", "view_piece"])
            group.permissions.set(permissions)
        instance.groups.add(Group.objects.get(name="Piece_General_Permission"))