from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('check-auth/', views.check_auth, name='check-auth'),
    path('events/', views.user_events_overview, name='user-events'),
]