from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('check-auth/', views.check_auth, name='check-auth'),
    path('events/', views.user_events_overview, name='user-events'),
    path('profile/picture/', views.UploadProfilePictureView.as_view(), name='upload-profile-picture'),
    path('profile/picture/delete/', views.delete_profile_picture, name='delete-profile-picture'),
]