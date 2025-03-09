from django.urls import path
from .views import get_room_allocations

urlpatterns = [
  path('api/hotels/<int:hotel_id>/allocations/', get_room_allocations, name='room_allocations'),
]