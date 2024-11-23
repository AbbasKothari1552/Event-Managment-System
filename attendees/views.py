from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from events.models import Person,Event, EventAttendance
from .forms import PersonForm, EventAttendanceForm

# Add person
@login_required
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = request.user
            person.save()
            return redirect('dashboard')
    else:
        form = PersonForm()
    return render(request, 'add_person.html', {'form': form})

# add attendies/invitees to event
@login_required
def add_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == 'POST':
        person_id = request.POST['person']
        family_count = int(request.POST['family_count'])
        description = request.POST.get('description', '')
        person = get_object_or_404(Person, id=person_id, created_by=request.user)
        EventAttendance.objects.create(event=event, person=person, family_count=family_count, description=description)
        return redirect('dashboard')
    else:
        people = Person.objects.filter(created_by=request.user)
        form = EventAttendanceForm(user=request.user)
    return render(request, 'add_attendees.html', {'form': form, 'event': event, 'people': people})


@login_required
def remove_attendee(request, attendance_id):
    attendance = get_object_or_404(EventAttendance, id=attendance_id)
    event_id = attendance.event.id
    attendance.delete()
    return redirect('event_detail', event_id=event_id)

