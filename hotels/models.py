from django.db import models

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=255)

class RoomType(models.Model):
    SINGLE = "Single"
    DOUBLE = "Double"
    TRIPLE = "Triple"
    QUAD = "Quad"
    
    ROOM_CHOICES = [
        (SINGLE, "Single"),
        (DOUBLE, "Double"),
        (TRIPLE, "Triple"),
        (QUAD, "Quad"),
    ]
    
    name = models.CharField(max_length=10, choices=ROOM_CHOICES)
    base_capacity = models.IntegerField()
    extra_capacity = models.IntegerField()
    total_rooms = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="room_types")

    @property
    def max_capacity(self):
        return self.base_capacity + self.extra_capacity

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=10)

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    rooms_booked = models.IntegerField(default=0)

    class Meta:
        unique_together = ('room', 'check_in', 'check_out')
