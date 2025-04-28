from django.shortcuts import render, redirect
from .models import Appointment, Patient, Doctor
from .forms import AppointmentForm

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})