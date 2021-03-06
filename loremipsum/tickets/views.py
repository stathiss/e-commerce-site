from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect,render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView
from django.contrib.auth import login
from tickets.models import Event, Provider, Transaction, Parent
from tickets.serializers import EventSerializer
from tickets.filters import EventFilter
from tickets.ticketgen.gen_pdf import gen_pdf_from_tx
from django.core.mail import EmailMessage
from datetime import datetime
from .watermark.watermark import main as watermark

from tickets.forms import ParentSignUpForm, ProviderSignUpForm, ProviderEditForm, BuyCoinsForm, EventCreateForm, EventBuyForm, EventsSearchForm

from tickets.models import User

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def stats_per_month(request):
    if request.user.is_authenticated:
        if request.user.is_provider:
            stats_per_month = {}
            events = Event.objects.filter(provider=request.user.provider)
            for e in events:
                transactions = Transaction.objects.filter(event=e)
                event_name = e.title
                for tx in transactions:
                    tx_cost = tx.total_cost/150
                    tx_amount = tx.amount
                    tx_date = tx.date.strftime("%Y%m")

                    ##Logic
                    if tx_date in stats_per_month:

                        if event_name in stats_per_month[tx_date]:
                            stats_per_month[tx_date][event_name]["total_amount"] += tx_amount
                            stats_per_month[tx_date][event_name]["total_cost"] += tx_cost

                        else:
                            stats_per_month[tx_date][event_name] = { "total_amount": tx_amount, "total_cost": tx_cost }

                    else:
                        stats_per_month[tx_date] = {}
                        stats_per_month[tx_date][event_name] = { "total_amount": tx_amount, "total_cost" : tx_cost }

            return render(request, 'stats_per_month.html', context = { 'stats_per_month' : stats_per_month })




def profile(request):
    if request.user.is_authenticated:
        if request.user.is_provider:
            """ Calculate stats for age types """
            event_types = {}
            events = Event.objects.filter(provider=request.user.provider)
            counter = 0.0
            for e in events:
                event_type = Event.TYPES[int(e.event_type)-1][1]
                tickets_no = (e.capacity - e.availability)
                if event_type in event_types:
                    event_types[event_type]["counter"] += tickets_no
                else:
                    event_types[event_type] = { "counter" : tickets_no, "type": event_type }
                counter += tickets_no
            if counter > 0:
                for t in event_types:
                    event_types[t]["counter"] /= counter
                    event_types[t]["counter"] *= 100
            """ Calculate stats for age ranges """
            event_ranges = {}
            counter = 0.0
            for e in events:
                range_ = 0 if e.age_range == "0005" else 1 if e.age_range == "0609" else 2 if e.age_range == "1012" else 3
                event_range = Event.AGE_RANGES[range_][1]
                tickets_no = (e.capacity - e.availability)
                if event_range in event_ranges:
                    event_ranges[event_range]["counter"] += tickets_no
                else:
                    event_ranges[event_range] = { "counter" : tickets_no, "range": event_range }
                counter += tickets_no
            if counter > 0:
                for r in event_ranges:
                    event_ranges[r]["counter"] /= counter
                    event_ranges[r]["counter"] *= 100

            return render(request, 'profile.html', context = { 'stats_types' : event_types, 'stats_ranges': event_ranges })
        elif request.user.is_parent:
            transactions = Transaction.objects.filter(parent=request.user.parent)
            return render(request, 'profile.html', context = { 'transactions' : transactions })
    return render(request, 'profile.html')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_parent:
            return redirect('/about/')
        else:
            return redirect('/')
    return render(request, 'index.html')

class ParentSignUpView(CreateView):
    model = User
    form_class = ParentSignUpForm
    template_name = '../templates/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = '????????????'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request.POST.get("lat", ""), self.request.POST.get("lng", ""))
        login(self.request, user)
        return redirect('/profile/')

class ProviderSignUpView(CreateView):
    model = User
    form_class = ProviderSignUpForm
    template_name = '../templates/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'provider'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request.FILES)
        login(self.request, user)
        return redirect('/profile/')

def model_form_upload(request):
    if request.method == 'POST':
        form = ProviderSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            img_filepath = Provider.objects.get(pk=user).logo
            print("ImageFieldFile to string is " + str(img_filepath))
            watermark(("/code/loremipsum/" + str(img_filepath)), '/code/loremipsum/tickets/watermark/watermark.png', 128, 128)
            login(request, user)
            return redirect('/profile/')
    else:
        form = ProviderSignUpForm()
    return render(request, '../templates/registration/signup_form.html', {
        'form': form, 'user_type' : '??????????????'
    })


class ProviderEditView(CreateView):
    model = User
    form_class = ProviderEditForm
    template_name = '../templates/registration/edit.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'provider'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request)
        return redirect('/profile/')

class EventCreateView(CreateView):
    model = User
    form_class = EventCreateForm
    template_name = '../templates/registration/add_event.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'provider'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request, self.request.POST.get("lat", ""), self.request.POST.get("lng", ""))
        return redirect('/events/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '?? ?????????????? ?????? ???????????? ????????????????!')
            return redirect('change_password')
        else:
            messages.error(request, '???????????????? ?????????????????? ???? ???????????? ?????? ?????????????????????? ????????????????.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, '../templates/registration/change_password.html', {'form': form})

class buy_coins(CreateView):
    model = User
    form_class = BuyCoinsForm
    template_name = 'buy_coins.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(self.request)
        #login(self.request, user)
        return redirect('/profile/')


@api_view(['GET', 'POST'])
def event_list(request, format=None):
    """
    List all events or create a new one.
    """
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk, format=None):
    """
    Retrieve, update or delete an event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Distance between two points with the Haversine formula
https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
"""
def get_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

class EventListView(FormView):
    form_class = EventsSearchForm
    template_name = 'event_list.html'

    def get(self, request, **kwargs):
        return event_search(request, None)

    def form_valid(self, form, **kwargs):
        token = form.save(self.request)
        return event_search(self.request, token)


def event_search(request, term):
    """ Athens centre coordinates : """
    home_lat = 37.983810
    home_lon = 23.7275
    if request.user.is_authenticated and request.user.is_parent:
        home_lat = request.user.parent.latitude
        home_lon = request.user.parent.longitude
    from elasticsearch_dsl import DocType, Text, Date, Search

    found_entries = []
    results = None
    events = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=events)
    if term: # elastic
        s = Search().filter('match', title=term)
        response = s.execute(ignore_cache=True)
        results = set()
        response = response.to_dict()
        for r in response['hits']['hits']:
            results.add(Event.objects.get(pk=r['_id']))
    else: #filter
        results = event_filter.qs

    for e in results:
        if get_distance(home_lat, home_lon, e.latitude, e.longitude) <= 5:
            found_entries.append(e)
    return render(request, EventListView.template_name,
            { 'event_list': found_entries, 'filter': event_filter, 'location': { 'lon' : home_lon, 'lat': home_lat}, 'search_form': EventListView.form_class })

def EventDetailView(request, pk):
    template_name = 'event_detail.html'
    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("?????? ?????????????? ???????????? ????????????????")

    Event.objects.filter(pk=e.id).update(hits=(e.hits+1))
    return render(request, template_name, context = { 'event': e })

def ProviderDetailView(request, pk):
    template_name = 'provider_detail.html'
    try:
        p = Provider.objects.get(pk=pk)
        event_list = Event.objects.filter(provider=p)
    except Provider.DoesNotExist:
        raise Http404("?????? ?????????????? ?????????????? ??????????????????????")
    return render(request, template_name, context = { 'provider': p,
                  'event_list' : event_list})

class EventBuyView(FormView):
    form_class = EventBuyForm
    template_name = 'event_buy.html'
    success_url = '/buy/success'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        try:
            e = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404("?????? ?????????????? ???????????? ????????????????")
        if request.user.is_authenticated:
            if request.user.is_parent:
                new_balance = request.user.parent.coins - e.cost
                return render(request, self.template_name, context = { 'event': e, 'new_balance' : new_balance, 'form': self.form_class })
            else:
                return redirect('/accounts/signup/parent/')
        else:
            return redirect('/accounts/signup/parent/')
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    def form_valid(self, form, **kwargs):
        pk = self.kwargs['pk']
        e = Event.objects.get(pk=pk)
        result = form.save(self.request, e.cost)
        if result is None:
            return render(self.request, 'buy_failure.html', context = { 'reason': "?????? ?????????????? ???? ???????????????? ?????? ?????? ?????????? ?????? ??????????"})
        elif result is False:
            return redirect('/events/')
        else:
            import datetime
            amount = 0
            if e.cost > 0:
                amount = result/e.cost
            if e.availability - amount < 0:
                return render(self.request, 'buy_failure.html', context = { 'reason': "?????? ???????????????? ???????????? ?????????????????? ?????? ???????? ???? ??????????????????????????" })
            new_balance = self.request.user.parent.coins - result
            if new_balance < 0:
                return render(self.request, 'buy_failure.html', context = { 'reason': "?????? ?????????????? ???? ???????????????? ?????? ?????? ?????????? ?????? ??????????"})
            Parent.objects.filter(pk=self.request.user).update(coins=new_balance)
            Event.objects.filter(pk=pk).update(availability=(e.availability - amount))
            t = Transaction.objects.create(event=e,parent=self.request.user.parent,date=datetime.datetime.now(),amount=amount,total_cost = result)
            ##TODO add pdfcreate
            gen_pdf_from_tx(t)
            email = EmailMessage()
            email.subject = '???? ?????????????????? ?????? - Lorem Ipsum'
            email.body = '???????????????????????? ?????? ?????? ??????????????????????!'
            email.to = [Parent.objects.get(pk=self.request.user).email, ]
            email.attach_file('/code/loremipsum/tickets/ticketgen/receipt.pdf')
            email.send()
            return render(self.request, 'buy_success.html', context = { 'transaction': t, 'new_balance' : new_balance })
