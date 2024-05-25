import secrets, string

from django.forms import ValidationError

def custom_slugify(instance, attempt = 1):
    CODE_CHARACTERS = string.ascii_letters + string.digits
    CODE_LENGTH = 15
    MAX_ATTEMPTS = 5

    # Check if the maximum number of attempts has been reached
    if attempt >= MAX_ATTEMPTS:
        raise ValidationError(f"Failed to generate a unique slug after {MAX_ATTEMPTS} attempts.")

    sender_model = instance.__class__

    slug = ''.join(secrets.choice(CODE_CHARACTERS) for _ in range(CODE_LENGTH))
        
    # Check if the generated slug already exists and recurse if necessary
    if sender_model.objects.filter(slug=slug).exclude(id=instance.id).exists():
        return custom_slugify(instance, attempt + 1)
        
    return slug