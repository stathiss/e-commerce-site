from django.urls import include, path
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from tickets import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProviderEditView.as_view(), name='edit'),
    path('profile/add_event/', views.EventCreateView.as_view(), name='add_event'),
    path('api/events/', views.event_list, name='event_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/events/<int:pk>/', views.event_detail, name='event_detail'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/parent/', views.ParentSignUpView.as_view(), name='parent_signup'),
    path('accounts/signup/provider/', views.ProviderSignUpView.as_view(), name='provider_signup'),
    path('events/', views.EventListView, name='event_list'),
    path('event/<int:pk>', views.EventDetailView, name='event_detail'),
    path('event/<int:pk>/buy', views.EventBuyView, name='event_buy'),
    path('provider/<int:pk>', views.ProviderDetailView, name='provider_detail'),
    path('buy_coins/', views.buy_coins.as_view(), name='buy_coins'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
