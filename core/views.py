from functools import wraps
from django.http import HttpResponseForbidden
from core.models import *
from .forms import *
from django.db.models import Q
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required, login_required

@login_not_required
def login_view(request):
    # Obtener la url de redirección
    next_url = request.GET.get('next') or request.POST.get('next')  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            # Redirigir a la url de redirección o a la página de inicio
            return redirect(next_url if next_url else 'dashboard')
        
        return render(request, 'login.html', {
            'error': 'Credenciales inválidas',
            'next': next_url  #Preservar la url de redirección
        })
    
    return render(request, 'login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('login')

class DashboardView(View):
    allowed_roles = ['ADMIN', 'MANAGEMENT', 'DOCTOR', 'ATTENDANT']
    def get(self, request):
        return render(request, 'dashboard.html')
    
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@role_required(['ADMIN', 'MANAGEMENT', 'DOCTOR', 'ATTENDANT'])
def appointment_register(request):
    if request.method == 'POST':
        form = AppointmentRegister(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request, 'appointments/appointment_register.html', {'form': AppointmentRegister()})
            return redirect('dashboard')
        else:
            pass
    else:
        form = AppointmentRegister()
    
    template = 'appointments/appointment_register.html' if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else None
    
    return render(request, template, {'form': form})

@role_required(['ADMIN', 'MANAGEMENT', 'DOCTOR'])
def patient_register(request):
    if request.method == 'POST':
        form = PatientRegister(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request, 'patients/patient_register.html', {'form': PatientRegister()})
            return redirect('dashboard')
    else:
        form = PatientRegister()
    
    # Determinar la plantilla a usar basado en el tipo de solicitud
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        template = 'patients/patient_register.html'
    else:
        None
    
    return render(request, template, {'form': form})

@role_required(['ADMIN', 'MANAGEMENT', 'DOCTOR', 'ATTENDANT'])
def patient_list(request):
    query = request.GET.get('q', '')
    print("Search Query:", query)  # Debugging line

    patients = Patient.objects.all()
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    print("Patients Found:", patients.count())  # Debugging line
    return render(request, 'patients/patient_list.html', {'patients': patients})

@role_required(['ADMIN', 'MANAGEMENT'])
def patient_remove(request, pk):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=pk)
        patient.delete()
    return redirect('patient_list')

@role_required(['ADMIN', 'MANAGEMENT','ATTENDANT'])
def doctor_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.select_related('user').all()
    
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'search_query': query
    })

@role_required(['ADMIN', 'MANAGEMENT'])
def doctor_remove(request, pk):
    if request.method == 'POST':
        doctor = Doctor.objects.get(pk=pk)
        doctor.delete()
    return redirect('doctor_list')