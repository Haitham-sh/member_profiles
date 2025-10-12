from django.urls import path
from . import views

urlpatterns = [
    path('<int:event_id>/join/', views.join_event, name='join-event'),
    path('<int:event_id>/members/', views.event_members, name='event-members'),
    path('events/<int:event_id>/members/<int:member_id>/role/', views.change_member_role, name='change-role'),
]