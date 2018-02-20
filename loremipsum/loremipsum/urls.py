from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
