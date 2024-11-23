from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from events.models import Event
 
# Base Page
def base(request):
    return render(request, 'base.html')  


# # User Registration
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
