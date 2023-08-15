from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm


#   If you want to use this solution you need the login.html file in templates/greenzone
#   and uncommenting LoginForm in forms.py
# Login form support
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('The authentication was successful.')
#                 else:
#                     return HttpResponse('The account is blocked')
#             else:
#                 return HttpResponse('Invalid credentials.')
#     else:
#         form = LoginForm()
#
#     return render(request, 'greenzone/login.html',
#                   {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'greenzone/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'greenzone/register.html',
                  {'user_form': user_form})


# View to display main panel to user
@login_required
def dashboard(request):
    return render(request,
                  'greenzone/dashboard.html',
                  {'section': 'dashboard'})