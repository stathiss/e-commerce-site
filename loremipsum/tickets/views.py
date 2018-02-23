from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tickets.models import Event, Provider
from tickets.serializers import EventSerializer
from django.shortcuts import redirect,render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.contrib.auth import login
from tickets.filters import EventFilter


from tickets.forms import ParentSignUpForm, ProviderSignUpForm, ProviderEditForm, BuyCoinsForm, EventCreateForm

from tickets.models import User

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def profile(request):
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
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
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
        user = form.save()
        login(self.request, user)
        return redirect('/profile/')        


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
        #p = Provider.objects.get(pk=self.model.provider)
        return redirect('/events/')        

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

def EventListView(request):
    query_string = ''
    found_entries = None
    template_name = 'event_list.html'
    home_lat = 37.983810
    home_lon = 23.7275
    found_entries = []
    events = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=events)
    for e in event_filter.qs:
        if get_distance(home_lat, home_lon, e.latitude, e.longitude) <= 5:
            found_entries.append(e)
    return render(request, template_name,
            { 'event_list': found_entries, 'filter': event_filter })
def EventDetailView(request, pk):
    template_name = 'event_detail.html'
    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Δεν υπάρχει τέτοια εκδήλωση")

    Event.objects.filter(pk=e.id).update(hits=(e.hits+1))
    return render(request, template_name, context = { 'event': e })

def ProviderDetailView(request, pk):
    template_name = 'provider_detail.html'
    try:
        p = Provider.objects.get(pk=pk)
        event_list = Event.objects.filter(provider=p)
    except Provider.DoesNotExist:
        raise Http404("Δεν υπάρχει τέτοιος διοργανωτής")
    return render(request, template_name, context = { 'provider': p,
                  'event_list' : event_list})

def EventBuyView(request, pk):
    template_name = 'event_buy.html'
    try:
        e = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Δεν υπάρχει τέτοια εκδήλωση")
    if request.user.is_authenticated:
        if request.user.is_parent:
            return render(request, template_name, context = { 'event': e })
        else:
            return redirect('/accounts/signup/parent')
    else:
        return redirect('/accounts/signup/parent')
