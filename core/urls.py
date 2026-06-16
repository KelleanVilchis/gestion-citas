from . import views
from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(), name='home'), 
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]