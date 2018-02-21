from django.core.validators import (RegexValidator, URLValidator, EmailValidator)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

class MyEmailField(forms.CharField):
    default_validators = [EmailValidator(message="Παρακαλώ εισάγετε έγκυρο e-mail")]
    description = _("Email address")

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs['max_length'] = kwargs.get('max_length', 254)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # We do not exclude max_length if it matches default as we want to change
        # the default in future.
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # As with CharField, this will cause email validation to be performed
        # twice.
        defaults = {
            'form_class': forms.EmailField,
        }
        defaults.update(kwargs)

        return super().formfield(**defaults)