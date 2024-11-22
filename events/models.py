from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = None  # Remove the username field

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['phone_no']  # No additional fields required


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name

# Person/ Family Model
class Person(models.Model):
    name = models.CharField(max_length=200)
    phone_no = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be 10 digits and numeric."
            )
        ]
    )
    email = models.EmailField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='people')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_person_name_per_user')
        ]

    def __str__(self):
        return self.name


# Invitees to event Model
class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='attendances')
    family_count = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'person'], name='unique_person_name_per_event')
        ]

    def __str__(self):
        return f"{self.person.name} attending {self.event.name}"

