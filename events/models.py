from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Venue Model
class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# EventDate Model
class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='event_dates', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.event.name} - {self.date} at {self.time}"

# Enrollment Model (New)
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.event.name}"




