from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'password','is_vendor']



class VendorForm(forms.ModelForm):
    class Meta:
        model = VendorInformation
        fields = ['menu', 'business_name']