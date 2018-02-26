from django.urls import include, path
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from tickets import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProviderEditView.as_view(), name='edit'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('profile/add_event/', views.EventCreateView.as_view(), name='add_event'),
    path('profile/stats/', views.stats_per_month, name='stats_per_month'),
    path('api/events/', views.event_list, name='event_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/events/<int:pk>/', views.event_detail, name='event_detail'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/parent/', views.ParentSignUpView.as_view(), name='parent_signup'),
    path('accounts/signup/provider/', views.model_form_upload, name='provider_signup'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>', views.EventDetailView, name='event_detail'),
    path('event/<int:pk>/buy', views.EventBuyView.as_view(), name='event_buy'),
    path('provider/<int:pk>', views.ProviderDetailView, name='provider_detail'),
    path('buy_coins/', views.buy_coins.as_view(), name='buy_coins'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
