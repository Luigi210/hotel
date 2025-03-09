from django.shortcuts import render

from django.db.models import Sum
from django.utils.dateparse import parse_date

from .models import Booking, Hotel, Room, RoomType
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

def get_available_rooms(hotel, check_in, check_out):
    available_rooms = {}

    for room_type in hotel.room_types.all():
        booked_rooms = Booking.objects.filter(
            room__room_type=room_type,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).aggregate(Sum('rooms_booked'))['rooms_booked__sum'] or 0

        available_rooms[room_type.name] = {
            "room_type": room_type,
            "available": max(0, room_type.total_rooms - booked_rooms)
        }
    return available_rooms

@api_view(['GET'])
def get_room_allocations(request, hotel_id):
    guests = int(request.GET.get('guests', 0))
    check_in = parse_date(request.GET.get('check_in'))
    check_out = parse_date(request.GET.get('check_out'))
    
    if not (check_in and check_out and check_in < check_out):
        return Response({'error': 'Invalid dates'}, status=400)
    
    hotel = Hotel.objects.prefetch_related('room_types').get(id=hotel_id)
    available_rooms = get_available_rooms(hotel, check_in, check_out)
    combinations = []

    def find_combinations(remaining_guests, allocation, room_types, available_rooms, combinations):
        if remaining_guests < 0:
            return

        if remaining_guests == 0:
            total_capacity = sum(
                available_rooms[room_type]["room_type"].base_capacity * count
                for room_type, count in allocation.items()
            )

            if total_capacity > 0:
                combinations.append({
                    "combination": allocation.copy(),
                    "total_capacity": total_capacity
                })
            return

        for room_type in room_types:
            room_info = available_rooms[room_type]
            max_capacity = room_info["room_type"].base_capacity
            max_rooms = room_info["available"]

            for count in range(max_rooms + 1):
                allocation[room_type] = count
                find_combinations(
                    remaining_guests - (count * max_capacity),
                    allocation,
                    room_types[1:],
                    available_rooms,
                    combinations
                )
                allocation[room_type] = 0

    combinations = []
    find_combinations(guests, {}, list(available_rooms.keys()), available_rooms, combinations)
    return Response(combinations)
    # return Response(available_rooms)
