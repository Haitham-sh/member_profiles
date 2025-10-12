from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_create, name='event-list-create'),
    path('<int:event_id>/', views.event_detail, name='event-detail'),
    path('search/', views.event_search, name='event-search'),
    path('types/', views.event_types, name='event-types'),
]