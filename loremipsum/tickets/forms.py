from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from tickets.models import (Parent, Provider, User)
from tickets.validators import *

class ParentSignUpForm(UserCreationForm):

	first_name = forms.CharField(max_length=30, label='First Name')
	last_name = forms.CharField(max_length=30, label='Last Name')
	address = forms.CharField(max_length=30, label='Address')
	email = MyEmailField(max_length=30, help_text='example@example.com', label='Email')

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		fn = user.first_name + ' ' + user.last_name
		#up = user.parent
		user.address = self.cleaned_data['address']
		user.is_parent = True
		user.save()
		#up.save()
		parent = Parent.objects.create(user=user, full_name=fn, email=user.email, address=self.cleaned_data['address'])
		return user

class ProviderSignUpForm(UserCreationForm):

	first_name = forms.CharField(max_length=30, label='First Name')
	last_name = forms.CharField(max_length=30, label='Last Name')
	address = forms.CharField(max_length=30, label='Διεύθυνση')
	email = MyEmailField(max_length=30, help_text='example@example.com', label='Email')
	afm = forms.CharField(max_length=30, help_text= 'π.χ. 123456789', label='ΑΦΜ', validators=[RegexValidator(regex="^\d{9}$", message="Παρακαλώ εισάγετε έγκυρο ΑΦΜ (9 ψηφία)")])
	doy = forms.CharField(max_length=30, label='ΔΟΥ')
	lr = forms.CharField(max_length=30, label='Νομικός Εκπρόσωπος')
	adt = forms.CharField(max_length=30, label='Αριθμός Δελτίου Ταυτότητας', validators=[RegexValidator(regex="^\d{6,7}$", message="Παρακαλώ εισάγετε έγκυρο ΑΔΤ (6-7 ψηφία)")])
	site = forms.URLField(max_length=30, required=False, label='WebSite', validators=[URLValidator(message="Παρακαλώ εισάγετε έγκυρη URL")])


	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		fn = user.first_name + ' ' + user.last_name
		user.is_provider = True
		user.save()
		_site = self.cleaned_data['site']
		parent = Provider.objects.create(user=user, full_name=fn, address=self.cleaned_data['address'], email= user.email,
			afm=self.cleaned_data['afm'], doy=self.cleaned_data['doy'], legal_representative=self.cleaned_data['lr'], adt=self.cleaned_data['adt'], site=(None if _site == None else _site))
		return user


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Full Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    address = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
       	up = user.parent
       	up.address = self.cleaned_data['address']
       	#up.full_name = self.cleaned_data['full_name']
       	user.save()
       	up.save()
