from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm


UserModel = get_user_model()

"""
class CustomUserCreationForm(BaseUserCreationForm):
    
    class Meta:
        model = UserModel
        fields = ("email",)
        field_classes = {"email": forms.EmailField}
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return email
"""