from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser
from django import forms
from .models import Event, Person, EventAttendance


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your email'
        })
    )
    
    phone_no = forms.CharField(
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your phone number'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = CustomUser  # Assuming you have a User model imported
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Password and Confirm Password do not match"
            )
        
        return cleaned_data

# Event form
class EventForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter event name'
        })
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
    )

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
    )

    venue = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter event venue'
        })
    )

    description = forms.CharField(
        max_length=500,
        required=False, 
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter event description',
            'rows': 4
        })
    )

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'venue', 'description']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data



# Person form
class PersonForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter full name'
        })
    )

    phone_no = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter phone number'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter email address'
        })
    )

    class Meta:
        model = Person
        fields = ['name', 'phone_no', 'email']

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.created_by and Person.objects.filter(name=name, created_by=self.created_by).exists():
            raise forms.ValidationError("A person with this name already exists for this user.")
        return name
    
# Event invitees attendance form
class EventAttendanceForm(forms.ModelForm):
    family_count = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Number of family members'
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Additional notes',
            'rows': 3
        })
    )

    class Meta:
        model = EventAttendance
        fields = ['person', 'family_count', 'description']
        widgets = {
            'person': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['person'].queryset = Person.objects.filter(created_by=user)