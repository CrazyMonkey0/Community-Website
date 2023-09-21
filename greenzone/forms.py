from django import forms
from django.contrib.auth.models import User
import re
from .models import Profile

# login form
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# form registraion
class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # Checking whether these passwords are identical
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords are not identical.')
        return cd['password2']

    # checking if there is an account with the same email address
    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']):
            raise forms.ValidationError('The email already exists.')
        elif  re.match(\
        r"^([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9\.]+[A-Za-z0-9])@([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9-\.]+[A-Za-z0-9])\.[A-Za-z]+$" \
            , cd['email']):
            raise forms.ValidationError('The email is incorrect.')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
