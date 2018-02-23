from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashWidget
from django.db import transaction
import datetime
from tickets.models import (Parent, Provider, User)
from tickets.validators import *

class ParentSignUpForm(UserCreationForm):

	first_name = forms.CharField(max_length=30, label='Όνομα')
	last_name = forms.CharField(max_length=30, label='Επώνυμο')
	address = forms.CharField(max_length=30, label='Διεύθυνση')
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

	first_name = forms.CharField(max_length=30, label='Όνομα')
	last_name = forms.CharField(max_length=30, label='Επώνυμο')
	address = forms.CharField(max_length=30, label='Διεύθυνση')
	email = MyEmailField(max_length=30, help_text='example@example.com', label='Email')
	afm = forms.CharField(max_length=30, help_text= 'π.χ. 123456789', label='ΑΦΜ', validators=[RegexValidator(regex="^\d{9}$", message="Παρακαλώ εισάγετε έγκυρο ΑΦΜ (9 ψηφία)")])
	doy = forms.CharField(max_length=30, label='ΔΟΥ')
	lr = forms.CharField(max_length=30, label='Νομικός Εκπρόσωπος')
	adt = forms.CharField(max_length=30, label='Αριθμός Δελτίου Ταυτότητας', validators=[RegexValidator(regex="^\d{6,7}$", message="Παρακαλώ εισάγετε έγκυρο ΑΔΤ (6-7 ψηφία)")])
	site = forms.URLField(max_length=30, required=False, label='Ιστοσελίδα', validators=[URLValidator(message="Παρακαλώ εισάγετε έγκυρη URL")])


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
		provider = Provider.objects.create(user=user, full_name=fn, address=self.cleaned_data['address'], email= user.email,
			afm=self.cleaned_data['afm'], doy=self.cleaned_data['doy'], legal_representative=self.cleaned_data['lr'], adt=self.cleaned_data['adt'], site=(None if _site == None else _site))
		return user



class ProviderEditForm(forms.ModelForm):
	#old_pass = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Τρέχων Κωδικός')
	#old_pass = ReadOnlyPasswordHashWidget(label= ("Pass")),
	address = forms.CharField(max_length=30, required=False, label='Διεύθυνση')
	email = MyEmailField(max_length=30, required=False, help_text='example@example.com', label='Email')
	afm = forms.CharField(max_length=30, required=False, help_text= 'π.χ. 123456789', label='ΑΦΜ', validators=[RegexValidator(regex="^\d{9}$", message="Παρακαλώ εισάγετε έγκυρο ΑΦΜ (9 ψηφία)")])
	doy = forms.CharField(max_length=30, required=False, label='ΔΟΥ')
	lr = forms.CharField(max_length=30, required=False, label='Νομικός Εκπρόσωπος')
	adt = forms.CharField(max_length=30, required=False, label='Αριθμός Δελτίου Ταυτότητας', validators=[RegexValidator(regex="^\d{6,7}$", message="Παρακαλώ εισάγετε έγκυρο ΑΔΤ (6-7 ψηφία)")])
	site = forms.URLField(max_length=30, required=False, label='Ιστοσελίδα', validators=[URLValidator(message="Παρακαλώ εισάγετε έγκυρη URL")])


	class Meta:
		model = User
		fields = ['address', 'email', 'afm', 'doy', 'lr', 'adt', 'site']
		#exclude = ['Password']

	@transaction.atomic
	def save(self, request):
		user = super().save(commit=False)
		#provider = Provider.objects.filter(pk=user).update(address=self.cleaned_data['address'], email= self.cleaned_data['email'],
		#	afm=self.cleaned_data['afm'], doy=self.cleaned_data['doy'], legal_representative=self.cleaned_data['lr'], adt=self.cleaned_data['adt'], site=(None if _site == None else _site))
		_address = self.cleaned_data['address']
		_email = self.cleaned_data['email']
		_afm = self.cleaned_data['afm']
		_doy = self.cleaned_data['doy']
		_lr = self.cleaned_data['lr']
		_adt = self.cleaned_data['adt']
		_site = self.cleaned_data['site']
		temp = Provider.objects.get(pk=request.user)
		provider = Provider.objects.filter(pk=request.user).update(address=(temp.address if _address == "" else _address),
			email=(temp.email if _email == "" else _email), afm=(temp.afm if _afm == "" else _afm), doy=(temp.doy if _doy == "" else _doy), 
			legal_representative=(temp.legal_representative if _lr == "" else _lr), adt=(temp.adt if _adt == "" else _adt), site=(temp.site if _site == "" else _site))

		return user




class BuyCoinsForm(forms.ModelForm):

	card_code = forms.CharField(required = True, label='Κωδικός Κάρτας', validators=[RegexValidator(regex="^\d{16}$", message="Παρακαλώ εισάγετε έγκυρο Kωδικό Κάρτας (16 ψηφία)")])
	card_day = forms.DateField(help_text = 'Η "μερα" δεν έχει σημασία', required = True, label = "Μήνας Λήξης", initial=datetime.date.today)
	card_cvv = forms.CharField(required = True, label = "CVV",  validators=[RegexValidator(regex="^\d{3}$", message="Παρακαλώ εισάγετε έγκυρο Kωδικό Κάρτας (3 ψηφία)")] )
	coins = forms.IntegerField(required = True, label="coins")

	class Meta(UserCreationForm.Meta):
		model = User
		fields = {}

	@transaction.atomic
	def save(self, request):
		user = super().save(commit=False)
		coins2 = self.cleaned_data['coins'] + Parent.objects.get(pk=request.user).coins
		parent = Parent.objects.filter(pk=request.user).update(coins = coins2)
		return user



