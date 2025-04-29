from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    specialization = models.CharField(max_length=100, verbose_name="Especialidad")
    
    def __str__(self):
        return f"Dr(a). {self.first_name} {self.last_name} ({self.specialization})"
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['last_name', 'first_name']


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