from django import forms
from django.contrib.auth.models import User


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
        if User.objects.filter(email='email')[:1] != ['']:
            raise forms.ValidationError('Email are not identical.')
