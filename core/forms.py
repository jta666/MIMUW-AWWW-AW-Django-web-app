from django import forms
from .models import CompilationOption, File, Directory

class CompilationOptionForm(forms.ModelForm):
    class Meta:
        model = CompilationOption
        fields = ['standard', 'optimization', 'processor']

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = '__all__'
        exclude = ('owner', )


from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, CreateView
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'
        exclude = ('is_available', 'compiled_content', 'owner', )

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]        