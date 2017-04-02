from django.contrib.auth.models import User
from users.models import UserDetails
from datetime import date
from django import forms
from django.forms import widgets
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']


class AdditionalDetails(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea,required=False)
    description.widget.attrs['class'] = 'form-control'
    college = forms.CharField(widget=forms.TextInput,required=False)
    college.widget.attrs['class'] = 'form-control'
    date_of_birth = forms.DateField(widget=forms.DateInput,required=False)
    date_of_birth.widget.attrs['class'] = 'form-control'
    date_of_birth.widget.attrs['placeholder'] = 'YYYY-MM-DD'
    profile_image = forms.FileField(required=False)

    class Meta:
        model = UserDetails
        fields = ['description', 'college', 'date_of_birth', 'profile_image']



