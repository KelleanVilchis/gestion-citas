from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('users/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('<int:pk>/', views.AppointmentShowView.as_view(), name='appointment_show'),


    #path('book/', TemplateView.as_view(template_name="appointments/book.html"), name='book'),
    #path('check/', TemplateView.as_view(template_name="appointments/check.html"), name='check'),
    #path('slots/', TemplateView.as_view(template_name="appointments/slots.html"), name='slots'),
]
