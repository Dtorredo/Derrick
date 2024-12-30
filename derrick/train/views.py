
import json
from django.http import JsonResponse
import requests

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from reportlab.lib.pagesizes import elevenSeventeen

from train.credentials import LipanaMpesaPpassword, MpesaAccessToken

from train.forms import BookingForm

from train.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth

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
        return redirect('/home', id=id)
    return render(request, 'seats.html',{'schedule':schedule,'seats':available_seats})


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

def pay(request,id):
    selectedBooking = Booking.objects.get(id=id)
    return render(request, 'pay.html',{'selectedBooking': selectedBooking})

#MPESA ACCESS TOKEN

def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


#STK PUSH FUNCTION
def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        booking_id = request.POST['booking_id']
        booking = Booking.objects.get(id=booking_id)
       # booking_id = request.POST['booking_id']
       # amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
       # return HttpResponse(response)

        response_data = response.json()
        #print(response_data)  # Debugging
        code = response_data.get('ResponseCode')
        if code == "0":

        # Save to database
            transaction = Transaction(
            booking_id= booking,
            phone_number=phone,
            amount=1,  # Static amount here, but replace with dynamic if needed
            merchant_request_id=response_data.get('MerchantRequestID'),
            checkout_request_id=response_data.get('CheckoutRequestID'),
            response_code=response_data.get('ResponseCode'),
            response_description=response_data.get('ResponseDescription'),
            customer_message=response_data.get('CustomerMessage'),
            )
            transaction.save()
            return redirect('/success')
        else:
            return redirect('/failed')
    return redirect('/home')


def success(request):
    return render(request, 'paysuccess.html')

def failed(request):
    return render(request, 'payfail.html')

def stkquery(request,id):
    transaction = Transaction.objects.get(id=id)
    access_token = MpesaAccessToken.validated_mpesa_access_token
    headers = {"Authorization": "Bearer %s" % access_token}
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    request = {

            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "CheckoutRequestID": transaction.checkout_request_id,

    }
    response = requests.post(api_url, json=request, headers=headers,)

    response_data = response.json()
    result = response_data.get("ResultCode")

    if result == "1037":
        transaction.transaction_status = "Failed"
        transaction.save()
        return HttpResponse("Timed Out")
    elif result == "0":
        transaction.transaction_status = "Success"
        transaction.save()
        return HttpResponse("Success")
    else:
        transaction.transaction_status = "Failed"
        transaction.save()

def allbookings(request):
    allbookings = Booking.objects.all()
    allschedules = Schedule.objects.all()
    alldestinations = Destination.objects.all()
    alltrains = Train.objects.all()
    allmessages = Contact.objects.all()
    alltransactions = Transaction.objects.all()
    return render(request,'trainadmin.html',{'allbookings':allbookings,'allschedules':allschedules,'alldestinations':alldestinations,'allmessages':allmessages,'alltrains':alltrains, 'alltransactions':alltransactions})
