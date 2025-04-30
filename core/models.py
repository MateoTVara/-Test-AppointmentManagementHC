from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador del Sistema'),
        ('MANAGEMENT', 'Personal Administrativo'),
        ('DOCTOR', 'Médico'),
        ('ATTENDANT', 'Personal de Atención'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name="Rol",
        default='ATTENDANT'
    )
    
    # Add these to resolve the conflict
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="core_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions",
        related_query_name="user",
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="Usuario asociado"
    )
    specialization = models.CharField(max_length=100, verbose_name="Especialidad")
    
    def __str__(self):
        return f"Dr(a). {self.user.get_full_name()} ({self.specialization})"
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['user__last_name', 'user__first_name']


class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    date_of_birth = models.DateField(verbose_name="Fecha de nacimiento")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),  # Better for searches
        ]


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE,
        verbose_name="Paciente",
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE,
        verbose_name="Médico",
    )
    date_time = models.DateTimeField(verbose_name="Fecha y hora")
    reason = models.TextField(
        verbose_name="Motivo de la cita",
        help_text="Describe el motivo de la cita médica."
    )
    
    STATUS_CHOICES = [
        ('S', 'Programada'),
        ('C', 'Completada'),
        ('N', 'No Presentado'),
        ('X', 'Cancelada'),
    ]
    status = models.CharField(
        max_length=1, 
        choices=STATUS_CHOICES, 
        default='S',
        verbose_name="Estado"
    )
    
    def __str__(self):
        return f"{self.patient} con {self.doctor} el {self.date_time}"
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-date_time']  # Most recent first
        indexes = [
            models.Index(fields=['date_time']),  # Faster date filtering
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date_time'],
                name='unique_doctor_timeslot',
                violation_error_message="El médico ya tiene una cita programada en este horario"
            ),
        ]