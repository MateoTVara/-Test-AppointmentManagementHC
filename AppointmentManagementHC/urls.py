"""
URL configuration for AppointmentManagementHC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('appointments/register/', views.appointment_register, name='appointment_register'),
    path('patients/list/', views.patient_list, name='patient_list'),
    path('patients/register/', views.patient_register, name='patient_register'),
    path('patients/remove/<int:pk>/', views.patient_remove, name='patient_remove'),
    path('doctors/list/', views.doctor_list, name='doctor_list'),
    path('doctors/remove/<int:pk>/', views.doctor_remove, name='doctor_remove'),
]
