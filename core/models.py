from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.last_name} ({self.specialization})"

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    STATUS_CHOICES = [
        ('S', 'Scheduled'),
        ('C', 'Completed'),
        ('N', 'No Show'),
        ('X', 'Cancelled'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    
    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date_time}"