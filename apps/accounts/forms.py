from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
        }

class AppUserChangeForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500'}),
        }



class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'class':'input'})
        )
    password = forms.CharField(
        label='Password',
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class':'input'}),
    )