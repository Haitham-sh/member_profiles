from django.urls import path
from . import views

urlpatterns = [
    path('<int:event_id>/join/', views.join_event, name='join-event'),
    path('<int:event_id>/members/', views.event_members, name='event-members'),
]