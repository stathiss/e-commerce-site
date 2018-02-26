from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashWidget
from django.db import transaction
import datetime
from tickets.models import (Parent, Provider, User, Event)
from tickets.validators import *
from django.contrib.admin import widgets


class ParentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Όνομα')
    last_name = forms.CharField(max_length=30, label='Επώνυμο')
    address = forms.CharField(max_length=30, label='Διεύθυνση')
    email = MyEmailField(max_length=30, help_text='example@example.com', label='Email')
    lat = forms.CharField(widget=forms.HiddenInput())
    lon = forms.CharField(widget=forms.HiddenInput())

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, lat, lng):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        fn = user.first_name + ' ' + user.last_name
        user.latitude = self.cleaned_data['lat']
        user.longitude = self.cleaned_data['lon']
        user.address = self.cleaned_data['address']
        user.is_parent = True
        user.save()
        parent = Parent.objects.create(user=user, latitude = user.latitude, longitude = user.longitude, full_name=fn, email=user.email, address=self.cleaned_data['address'])
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
	logo = forms.ImageField()


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
		provider = Provider.objects.create(user=user, logo=self.cleaned_data['logo'], full_name=fn, address=self.cleaned_data['address'], email= user.email,
			afm=self.cleaned_data['afm'], doy=self.cleaned_data['doy'], legal_representative=self.cleaned_data['lr'], adt=self.cleaned_data['adt'], site=("" if _site == "" else _site))
		return user



class ProviderEditForm(forms.ModelForm):
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

	@transaction.atomic
	def save(self, request):
		user = super().save(commit=False)
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

class EventCreateForm(forms.ModelForm):

	AGE_RANGES = (
			( "0005", "0-5"),
			( "0609", "6-9"),
			( "1012", "10-12"),
			( "1314", "13-14"),
			)

	TYPES = (
			( "1", "Παιδικά θέατρα"),
			( "2", "Συναυλίες"),
			( "3", "Παιδότοποι"),
			( "4", "Πάρτυ"),
			( "5", "Εκπαιδευτικές εκδρομές/εκδηλώσεις"),
			( "6", "Αθλητικές δραστηριότητες"),
			( "7", "Πάρκα αναψυχής"),
			( "8", "Παιδικές κατασκηνώσεις"),
			)

	title = forms.CharField(max_length=50, label='Τίτλος Εκδήλωσης', required=True)
	event_date = forms.SplitDateTimeField(help_text='\n Μορφή ημερομηνίας: YYYY-MM-DD, Μορφή ώρας: HH:MM:SS', label='Ημερομηνία και ώρα Εκδήλωσης', required=True)
	date_added = forms.DateField(help_text='Μορφή ημερομηνίας: YYYY-MM-DD', initial=datetime.date.today, label='Ημερομηνία Δημιουργίας Εκδήλωσης', required=True)
	capacity = forms.IntegerField(min_value=1, label='Χωρητικότητα Εκδήλωσης', required=True)
	location = forms.CharField(max_length=100, label='Διεύθυνση Εκδήλωσης', required=True)
	age_range = forms.ChoiceField(choices=AGE_RANGES, initial="0005", label='Ηλικιακό Εύρος Εκδήλωσης', required=True)
	event_type = forms.ChoiceField(choices=TYPES, initial="1", label='Είδος Εκδήλωσης', required=True)
	cost = forms.IntegerField(min_value=0, label='Κόστος Εκδήλωσης (Σε Coins)', required=True)


	class Meta:
		model = User
		fields = ['title', 'event_date', 'date_added', 'capacity', 'location', 'age_range', 'event_type', 'cost']

	@transaction.atomic
	def save(self, request, lat, lng):
		event = super().save(commit=False)
		event.title = self.cleaned_data['title']
		event.event_date = self.cleaned_data['event_date']
		event.date_added = self.cleaned_data['date_added']
		event.capacity = self.cleaned_data['capacity']
		event.latitude = lat
		event.longitude = lng
		event.location = self.cleaned_data['location']
		event.age_range = self.cleaned_data['age_range']
		event.event_type = self.cleaned_data['event_type']
		event.cost = self.cleaned_data['cost']
		temp = Provider.objects.get(pk=request.user)
		event.hits = 0
		event.availability = self.cleaned_data['capacity']

		event = Event.objects.create(location = self.cleaned_data['location'], latitude = lat, longitude=lng, title=self.cleaned_data['title'], event_date = self.cleaned_data['event_date'], date_added = self.cleaned_data['date_added'], capacity = self.cleaned_data['capacity'], age_range = self.cleaned_data['age_range'], event_type = self.cleaned_data['event_type'], cost = self.cleaned_data['cost'], hits = 0, availability = self.cleaned_data['capacity'], provider=temp)
		return event





class BuyCoinsForm(forms.ModelForm):

	card_code = forms.CharField(required = True, label='Κωδικός Κάρτας', validators=[RegexValidator(regex="^\d{16}$", message="Παρακαλώ εισάγετε έγκυρο Kωδικό Κάρτας (16 ψηφία)")])
	card_year = forms.ChoiceField(required = True, label = "Έτος Λήξης", choices = (
		(1, ("2018")),
		(2, ("2019")),
		(3, ("2020")),
		(4, ("2021")),
		(5, ("2022"))))
	card_month = forms.ChoiceField(required = True, label = "Μήνας Λήξης", choices = (
		(1, ("1")),
		(2, ("2")),
		(3, ("3")),
		(4, ("4")),
		(5, ("5")),
		(6, ("6")),
		(7, ("7")),
		(8, ("8")),
		(9, ("9")),
		(10, ("10")),
		(11, ("11")),
		(12, ("12"))))
	card_cvv = forms.CharField(required = True, label = "CVV",  validators=[RegexValidator(regex="^\d{3}$", message="Παρακαλώ εισάγετε έγκυρο Kωδικό Κάρτας (3 ψηφία)")] )
	coins = forms.ChoiceField(required = True, label = "Ποσό Αγοράς σε €", choices = (
		(1, ("5")),
		(2, ("10")),
		(3, ("20")),
		(4, ("50"))))

	class Meta(UserCreationForm.Meta):
		model = User
		fields = {}

	@transaction.atomic
	def save(self, request):
		user = super().save(commit=False)
		print (self.cleaned_data['coins'])
		coins1 = self.cleaned_data['coins']
		print (coins1)
		if coins1 == "1":
			coins2 = 750
		elif coins1 == "2":
			coins2 = 1500
		elif coins1 == "3":
			coins2 = 3075
		else:
			coins2 = 7650
		coins2 += Parent.objects.get(pk=request.user).coins
		parent = Parent.objects.filter(pk=request.user).update(coins = coins2)
		return user

class EventBuyForm(forms.Form):
    amount = forms.IntegerField(required=True, label="Ποσότητα")

    @transaction.atomic
    def save(self, request, cost):
        if 'buy' in request.POST:
            amount = self.cleaned_data['amount']
            if amount * cost > request.user.parent.coins:
                return None
            else:
                return amount * cost
        else: #User cancelled purchase
            return False


class EventsSearchForm(forms.Form):
    token = forms.CharField(required=True, label="Ελεύθερη αναζήτηση")

    @transaction.atomic
    def save(self, request):
        return self.cleaned_data['token']
