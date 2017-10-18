from django.forms import ModelForm
from django import forms
from .models import (
    Idea,
    Profile,
    )
from django.utils import html
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IdeaForm(ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name',
            'style': 'margin-top: 20px;',
        }))
    overview = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Provide an overview of your idea',
            'style': 'resize:none;'
        }))
    description = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter a detailed description of your idea',
            'style': 'resize:none;'
        }))

    class Meta:
        model = Idea
        # don't include votes because it is not editable
        fields = ('name', 'overview', 'description')


    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '' 
        self.fields['overview'].label = ''
        self.fields['description'].label = ''

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name',
            'style': 'margin-top: 20px;',
        }))
    contact_email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }))
    subject = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
        }))
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'What would you like to say?',
            'style': 'resize:none;'
        }))

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = '' 
        self.fields['contact_email'].label = ''
        self.fields['subject'].label = ''
        self.fields['content'].label = ''

# registration form
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('website', 'bio', 'phone', 'city', 'country')

