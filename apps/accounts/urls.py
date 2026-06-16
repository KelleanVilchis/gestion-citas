from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('user/registration/', views.UserCreateView.as_view(), name='user_create'),
    path('user/edit/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('user/show/<int:pk>/', views.UserShowView.as_view(), name='user_show'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]