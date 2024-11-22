from django.contrib import admin
from .models import CustomUser, Event, Person, EventAttendance

admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Person)
admin.site.register(EventAttendance)
