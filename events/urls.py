from django.urls import path
from . import views

urlpatterns = [
    path('create_event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/edit_event/<int:event_id>/', views.event_detail, name='edit_event'),
    path('send_invitation/<int:attendance_id>/<int:event_id>', views.send_invitations, name='send_invitation'),
    path('send_invitation/<int:event_id>', views.send_invitations, name='send_all_invitation'),
    path('invitation/', views.view_invitations, name='invitation'),
    path('accept_invitation/<int:attendance_id>/<int:event_id>', views.accept_invitation, name='accept_invitation'),
    path('decline_invitation/<int:attendance_id>/<int:event_id>', views.decline_invitation, name='decline_invitation'),
]
