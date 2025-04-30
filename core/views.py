from .forms import AppointmentForm
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required

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
    def get(self, request):
        return render(request, 'dashboard.html')

# views.py
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request, 'appointments/appointment_form_partial.html', {'form': AppointmentForm()})
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    
    template = 'appointments/appointment_form_partial.html' if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else 'appointments/appointment_form.html'
    return render(request, template, {'form': form})