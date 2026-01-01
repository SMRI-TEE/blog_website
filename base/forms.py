from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # userform lie use garna lie
from django import forms
from base.models import Category


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        
# to decorate django builtin form, we can use cripsy forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category 
        fields = '__all__'
        

