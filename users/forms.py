from django.contrib.auth.models import User

from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

