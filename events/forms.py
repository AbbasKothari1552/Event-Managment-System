from django import forms
from .models import Event


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




    
