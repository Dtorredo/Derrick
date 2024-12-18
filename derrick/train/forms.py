from django import forms
from train.models import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'