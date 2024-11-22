from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_event/', views.create_event, name='create_event'),
    path('add_person/', views.add_person, name='add_person'),
    path('add_attendance/<int:event_id>/', views.event_attendance, name='event_attendance'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/edit_event/<int:event_id>/', views.event_detail, name='edit_event'),
    path('event/edit_attendee/<int:attendance_id>/', views.remove_attendee, name='edit_attendee'),
    path('event/attendee/remove/<int:attendance_id>/', views.remove_attendee, name='remove_attendee'),
]
