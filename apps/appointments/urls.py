from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AppointmentShowView,
)

app_name = 'appointments'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('<int:pk>/', AppointmentShowView.as_view(), name='appointment_show'),
]
