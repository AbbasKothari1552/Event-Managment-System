from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Event, EventAttendance, Person
from .forms import EventForm
from attendees.forms import EventAttendanceForm
from django.utils.timezone import now



# Create new event
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_attendances = EventAttendance.objects.filter(event=event)
    
    if request.method == 'POST':
        form = EventAttendanceForm(request.POST, event=event)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.event = event
            attendance.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventAttendanceForm(user=request.user)
    
    context = {
        'event': event,
        'event_attendances': event_attendances,
        'form': form
    }
    return render(request, 'event_detail.html', context)


@login_required
def invitation(request):
    return render(request, 'invitation.html')

@login_required
def send_invitations(request, attendance_id=None, event_id=None):
    """
    Handles sending invitations for single or bulk requests and updates the model fields.
    :param request: HttpRequest object
    :param attendance_id: ID of EventAttendance for single invite
    :param event_id: ID of Event for bulk invites
    :return: JsonResponse or redirect
    """
    if attendance_id:
        # Single invite
        attendance = get_object_or_404(EventAttendance, id=attendance_id)
        if attendance.invite_status == 'PENDING':
            attendance.invite_status = 'SENT'
            attendance.invite_sent_at = now()
            attendance.save()
            message = f"Invitation sent to {attendance.person.name} for event {attendance.event.name}."
            
        else:
            message = f"Invitation for {attendance.person.name} was already sent."
        return redirect('event_detail', event_id=attendance.event.id)

    elif event_id:
        # Bulk invites
        event = get_object_or_404(Event, id=event_id)
        pending_attendees = EventAttendance.objects.filter(event=event, invite_status='PENDING')
        if not pending_attendees.exists():
            return redirect('event_detail', event_id=event.id)
        # Update all pending invitees
        for attendance in pending_attendees:
            attendance.invite_status = 'SENT'
            attendance.invite_sent_at = now()
            attendance.save()

        return redirect('event_detail', event_id=event.id)

    else:
        return redirect('invitation')
    

@login_required
def view_invitations(request):
    """
    Displays all invitations for the logged-in user based on their email.
    """
    # Get the logged-in user's email
    user_email = request.user.email
    
    # Fetch EventAttendance records where the person's email matches the logged-in user's email
    invitations = EventAttendance.objects.filter(person__email=user_email).exclude(invite_status='PENDING')
    
    return render(request, 'invitation.html', {'invitations': invitations})

@login_required
def accept_invitation(request, attendance_id=None, event_id=None):
    pass

@login_required
def decline_invitation(request, attendance_id=None, event_id=None):
    pass

