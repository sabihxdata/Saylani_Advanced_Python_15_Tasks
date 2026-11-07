''' Task 13 | Booking Conflict Scheduler
Concepts: Datetime, sorting, interval algorithms
Problem: Implement a room booking scheduler. Each booking has room, start datetime, end datetime, and booking ID. Accept bookings only when they do not overlap existing bookings for the same room.
Requirements: Use datetime objects; reject end<=start and duplicate IDs. Adjacent bookings are allowed. Return conflicts for rejected requests.
Sample / expected behavior: Room A: 09:00–10:00 and 10:00–11:00 accepted; 09:30–10:30 rejected.'''


from datetime import datetime


class Booking:
    def __init__(self, booking_id, room, start_time, end_time):
        self.booking_id = booking_id
        self.room = room
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (
            f"ID: {self.booking_id}, "
            f"Room: {self.room}, "
            f"Start: {self.start_time}, "
            f"End: {self.end_time}"
        )


class BookingScheduler:
    def __init__(self):
        self.bookings = []
        self.rejected_bookings = []
        self.booking_ids = set()

    def add_booking(self, booking_id, room, start_time, end_time):

        # Validate datetime objects.
        if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
            reason = "Start and end must be datetime objects"
            self.rejected_bookings.append((booking_id, reason))
            return False

   
        if not booking_id or not room:
            reason = "Booking ID and room cannot be empty"
            self.rejected_bookings.append((booking_id, reason))
            return False

      
        if booking_id in self.booking_ids:
            reason = "Duplicate booking ID"
            self.rejected_bookings.append((booking_id, reason))
            return False

        if end_time <= start_time:
            reason = "End time must be after start time"
            self.rejected_bookings.append((booking_id, reason))
            return False

        for booking in self.bookings:

            if booking.room == room:

                overlap = (
                    start_time < booking.end_time
                    and end_time > booking.start_time
                )

                if overlap:
                    reason = "Booking time conflict"
                    self.rejected_bookings.append((booking_id, reason))
                    return False

        # Accept the booking.
        new_booking = Booking(
            booking_id,
            room,
            start_time,
            end_time
        )

        self.bookings.append(new_booking)
        self.booking_ids.add(booking_id)

        return True

    def show_bookings(self):
        print("\nACCEPTED BOOKINGS")
        print("-" * 60)

        for booking in self.bookings:
            print(booking)

    def show_rejected(self):
        print("\nREJECTED BOOKINGS")
        print("-" * 60)

        for booking_id, reason in self.rejected_bookings:
            print("Booking ID:", booking_id, "| Reason:", reason)



scheduler = BookingScheduler()


def make_time(hour, minute):
    return datetime(2026, 11, 7, hour, minute)



print("TEST 1: VALID BOOKINGS")

print(
    "Booking 1:",
    scheduler.add_booking(
        "B01", "Room A",
        make_time(9, 0),
        make_time(10, 0)
    )
)

print(
    "Booking 2:",
    scheduler.add_booking(
        "B02", "Room A",
        make_time(10, 0),
        make_time(11, 0)
    )
)


print("\nTEST 2: OVERLAPPING BOOKING")

print(
    "Booking 3:",
    scheduler.add_booking(
        "B03", "Room A",
        make_time(9, 30),
        make_time(10, 30)
    )
)

print("\nTEST 3: DIFFERENT ROOM")

print(
    "Booking 4:",
    scheduler.add_booking(
        "B04", "Room B",
        make_time(9, 30),
        make_time(10, 30)
    )
)

print("\nTEST 4: DUPLICATE ID")

print(
    "Booking 4 again:",
    scheduler.add_booking(
        "B04", "Room C",
        make_time(12, 0),
        make_time(13, 0)
    )
)

print("\nTEST 5: INVALID TIME")

print(
    "Booking 5:",
    scheduler.add_booking(
        "B05", "Room A",
        make_time(14, 0),
        make_time(13, 0)
    )
)


scheduler.show_bookings()
scheduler.show_rejected()

print("\nSUMMARY")
print("-" * 60)
print("Accepted:", len(scheduler.bookings))
print("Rejected:", len(scheduler.rejected_bookings))
