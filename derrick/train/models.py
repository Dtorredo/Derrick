from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# User model
class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


# Contact model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# Train model
class Train(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# Destination model
class Destination(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Schedule model
class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_station = models.ForeignKey(Destination,related_name="departure_schedules" ,on_delete=models.CASCADE,null=True)
    arrival_station = models.ForeignKey(Destination,related_name="arrival_schedules" ,on_delete=models.CASCADE,null=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    seats = models.JSONField(default=dict, null=True, blank=True)

    def initialize_seats(self,rows=5,columns=4):
        seats = {}
        for row in range(1, rows+1):
            for columns in ['A','B','C','D']:
                seat_number = f"{row}{columns}"
                seats[seat_number] = True
        return seats

    def save(self,*args,**kwargs):
        if not self.seats:
            self.seats = self.initialize_seats(rows=5,columns=4)
        super().save(*args, **kwargs)

    def calculate_total_price(self,number_of_seats):
        return self.price_per_seat * number_of_seats
    def __str__(self):
        return f"{self.train} - {self.departure_station} to {self.arrival_station}"


# Booking model
class Booking(models.Model):
    email = models.EmailField(blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.email}"

