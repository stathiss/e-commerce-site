from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	path('about/', views.about, name='about'),
    path('', views.index, name='index'),
    path('api/events/', views.event_list, name='event_list'),
    path('api/events/<int:pk>/', views.event_detail, name='event_detail'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
