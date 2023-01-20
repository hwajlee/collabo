# accounts/urls.py
from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    # accounts/singup/
    path('signup/', views.signup, name='signup'),
    # accounts/login/
    path('login/', views.login, name='login'),
    # accounts/logout/
    path('logout/', views.logout, name='logout'),
    # accounts/<username>/profile
    path('<username>/', views.profile, name='profile'),
    # accounts/<username>/follow
    path('<username>/follow/', views.follow, name='follow'),
]