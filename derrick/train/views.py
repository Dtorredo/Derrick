from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from reportlab.lib.pagesizes import elevenSeventeen
from train.forms import BookingForm

from train.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request,"YOLO.html")

def schedule(request):
    return render(request, 'train.html')

def seats(request):
    return render(request,'Seats.html')

def login(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')


def register_user(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]


        if not first_name or not last_name or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            email=email,
            password=password,
        )
        user.save()
        messages.success(request, 'Registration successful!')
        return redirect('/login')
    else:
        return render(request, 'index.html')


def login_user(request):
    if request.method == "POST":
        if User.objects.filter(
                email=request.POST['email'],
                password=request.POST['password'],
        ).exists():
            user = User.objects.get(
                email=request.POST['email'],
                password=request.POST['password'],
            )
            return render(request, 'YOLO.html', {'user': user})
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def logout_user(request):
    return render(request, 'index.html')

def message(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        message = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        message.save()
        return redirect('/home')
    else:
        return render(request,'contact.html')


def booker(request,id):
    schedule = Schedule.objects.get(id=id)
    return render(request, 'bookseat.html', {'schedule': schedule})

def book_seats(request, id):
    schedule = Schedule.objects.get(id=id)

    if request.method == "POST":
        name = request.POST["name"]
        number_of_seats = int(
            request.POST["number_of_seats"]
        )
        total_price = schedule.calculate_total_price(number_of_seats)

        booking = Booking(
            user=name,
            schedule=schedule,
            number_of_seats=number_of_seats,
            total_price=total_price,
        )
        booking.save()

        return render(request, 'bookseat.html',{'schedule':schedule,'total_price':total_price})
    else:
        return redirect('/home')



def schedular(request):
    schedule = Schedule.objects.all()
    return render(request,'schedule.html',{'schedule':schedule})


def check_seats(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    available_seats = schedule.seats
    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")
        number_of_seats = len(selected_seats)
        email = request.POST["email"]

        if number_of_seats == 0:
            messages.error(request, 'No seats available.')
            return render(request,'seats.html',{'schedule':schedule,'seats':available_seats})

        for seat in selected_seats:
            if not available_seats.get(seat,False):
                messages.error(request, f"Seat {seat} not available.")
                return render(request,'seats.html',{'schedule':schedule,'seats':available_seats})

        for seat in selected_seats:
            available_seats[seat] = False

        schedule.seats = available_seats
        schedule.save()

        total_price = schedule.price_per_seat * number_of_seats

        booking = Booking.objects.create(
            email = email,
            schedule = schedule,
            number_of_seats = number_of_seats,
            total_price = total_price,
        )
        messages.success(request, f"Booking Successful! You have booked {number_of_seats} seats." )
        return redirect('/schedule', id=id)
    return render(request, 'seats.html',{'schedule':schedule,'seats':available_seats})

def allbookings(request):
    allbookings = Booking.objects.all()
    allschedules = Schedule.objects.all()
    alldestinations = Destination.objects.all()
    alltrains = Train.objects.all()
    allmessages = Contact.objects.all()
    return render(request,'trainadmin.html',{'allbookings':allbookings,'allschedules':allschedules,'alldestinations':alldestinations,'allmessages':allmessages,'alltrains':alltrains})

def mybookings(request):
    return render(request,'authorize.html')
#This is what we will define in the action, we need a page to render
def confirm(request):
    if request.method == "POST":
        if User.objects.filter(
                email=request.POST['email'],
                #password=request.POST['password'],
        ).exists():
            user = User.objects.get(
                email=request.POST['email'],
                #password=request.POST['password'],
            )
            bookings = Booking.objects.filter(email=user.email)
            return render(request, 'bookings.html', {'bookings': bookings})
        else:
            return render(request, 'bookseat.html')
    else:
        return render(request, 'bookseat.html')


def editbookings(request,id):
    edit_bookings = Booking.objects.get(id=id)
    return render(request,'editbooking.html',{'edit_bookings':edit_bookings})

def updatebookings(request,id):
    updatebooking = Booking.objects.get(id=id)
    form = BookingForm(request.POST, instance=updatebooking)
    if form.is_valid():
        form.save()
        return redirect('/checkbookings')
    else:
        return render(request, 'YOLO.html')

def deletebooking(request, id):
    clientbooking = Booking.objects.get(id=id)
    clientbooking.delete()
    return redirect('/bookings')

def searchbooking(request):
    

    if request.method=="POST":
        if Schedule.objects.filter(
                departure_station=request.POST['departure_station'],
                arrival_station=request.POST['arrival_station']
        ).exists():
            choseBooking = Schedule.objects.get(
                departure_station=request.POST['departure_station'],
                arrival_station=request.POST['arrival_station']
            )



        return render(request,'selected.html',{'bookings': choseBooking})
            