from django.urls import path
from . import views

urlpatterns = [
    path('add_person/', views.add_person, name='add_person'),
    path('add_attendees/<int:event_id>/', views.add_attendees, name='add_attendees'),
    path('event/edit_attendee/<int:attendance_id>/', views.remove_attendee, name='edit_attendee'),
    path('event/attendee/remove/<int:attendance_id>/', views.remove_attendee, name='remove_attendee'),
    
]