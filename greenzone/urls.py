from django.urls import path
from . import views


urlpatterns = [
    # Login Views
    path('login/', views.user_login, name='login')
]