import re
import secrets, string
from django.contrib.auth import get_user_model
from django.forms import ValidationError

User = get_user_model()

def custom_user_slugify(email, attempts = 1):
    CODE_CHARACTERS = string.ascii_letters + string.digits
    CODE_LENGTH = 4
    MAX_ATTEMPTS = 5

    if attempts > MAX_ATTEMPTS:
        raise ValidationError(f"Failed to generate a unique username after {MAX_ATTEMPTS} attempts.")

    extracted_username = ""

    match = re.match(r"([^@]+)@[^@]+\.[^@]+", email)

    if match:
        extracted_username = match.group(1)
    
    suffix = ''.join(secrets.choice(CODE_CHARACTERS) for _ in range(CODE_LENGTH))
    slug = f"{extracted_username}_{suffix}"

    if User.objects.filter(slug=slug).exists():
        return custom_user_slugify(email, attempts + 1)

    return slug
