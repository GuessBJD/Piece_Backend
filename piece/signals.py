import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import ValidationError
from .models import Piece
from core.utils import custom_slugify

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Piece)
def piece_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.slug == "" or instance.slug == None:
        try:
            instance.slug = custom_slugify(instance)
        except ValidationError as e:
            logger.error(f"Failed to generate a unique slug: {e}")