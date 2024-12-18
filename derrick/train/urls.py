
from django.contrib import admin
from django.urls import path

from train import views

urlpatterns = [

    path('home/', views.index, name='index'),
    path('schedule/', views.schedule, name='schedule'),

    path('seats/', views.seats, name='seats'),
    path('', views.login, name='loginform'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('messages/', views.message, name='message'),
    path('bookseats/<int:id>',views.book_seats, name='book_seats'),

    path('schedular/', views.schedular, name='schedular'),
    path('booker/<int:id>',views.booker, name='booker'),
    path('confirm/<int:id>',views.check_seats, name='check_seats'),

    path('trainadmin',views.allbookings, name='trainadmin'),

    path('bookings/',views.mybookings, name='mybookings'),

    path('checkbookings/',views.confirm, name='confirm'),

    path('editbooking/<int:id>',views.editbookings, name='editbooking'),

    path('updatebooking/<int:id>',views.updatebookings, name='updatebooking'),

    path('deletebooking/<int:id>',views.deletebooking, name='deletebooking'),
    path('selected/', views.searchbooking,name='searchbooking'),
]
