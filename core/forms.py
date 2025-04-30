from django import forms
from .models import Appointment

class AppointmentRegister(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PatientRegister(forms.ModelForm):
    class Meta:
        model = Appointment.patient.field.related_model
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }