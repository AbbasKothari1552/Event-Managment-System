from django import forms
from events.models import Person, EventAttendance

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
        fields = ['person', 'invitees_count', 'family_count', 'description']
        widgets = {
            'person': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'invitees_count': forms.Select(attrs={  # Add custom widget here
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['person'].queryset = Person.objects.filter(created_by=user)
