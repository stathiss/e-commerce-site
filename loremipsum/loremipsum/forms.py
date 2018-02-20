from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.forms import SetPasswordField, PasswordField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Full Name')
    address = forms.CharField(max_length=30, label='Address')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.address = self.cleaned_data['address']
        user.save()