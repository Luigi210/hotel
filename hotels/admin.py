from django.contrib import admin
from .models import Hotel, RoomType, Room, Booking

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)
