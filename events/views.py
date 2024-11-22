from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .models import Event, Person, EventAttendance
from .forms import RegistrationForm,EventForm, PersonForm, EventAttendanceForm



# Base Page
def base(request):
    return render(request, 'base.html')  


# User Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome, user")
            return redirect('dashboard')
        else:
            messages.error(request, "Soemthing went wrong, olease try again")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

# User logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('base')


# Dashboard
@login_required
def dashboard(request):
    events = Event.objects.filter(created_by=request.user)
    return render(request, 'dashboard.html', {'events': events})


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
def event_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == 'POST':
        person_id = request.POST['person']
        family_count = int(request.POST['family_count'])
        description = request.POST.get('description', '')
        person = get_object_or_404(Person, id=person_id, created_by=request.user)
        EventAttendance.objects.create(event=event, person=person, family_count=family_count, description=description)
        return redirect('dashboard')
    else:
        print("Current user:", request.user)
        people = Person.objects.filter(created_by=request.user)
        print(people)
        form = EventAttendanceForm(user=request.user)
    return render(request, 'event_attendance.html', {'form': form, 'event': event, 'people': people})

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
def remove_attendee(request, attendance_id):
    attendance = get_object_or_404(EventAttendance, id=attendance_id)
    event_id = attendance.event.id
    attendance.delete()
    return redirect('event_detail', event_id=event_id)
