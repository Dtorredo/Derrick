from django.contrib import admin

from train.models import Train, Destination, Schedule,Contact,Booking,User

# Register your models here.
admin.site.register(Train)
admin.site.register(Contact)
admin.site.register(Destination)
admin.site.register(Booking)
admin.site.register(User)
admin.site.register(Schedule)

class ScheduleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.seats:
            obj.seats = obj.initialize_seats(rows=10, cols=4)
        super().save_model(request, obj, form, change)


