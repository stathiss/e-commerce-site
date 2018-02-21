from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tickets.models import Event
from tickets.serializers import EventSerializer
from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth import login

from tickets.forms import ParentSignUpForm, ProviderSignUpForm
from tickets.models import User

def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def about(request):
    return render(request, 'about.html')

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
        return redirect('/about/')

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
        return redirect('/')


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
