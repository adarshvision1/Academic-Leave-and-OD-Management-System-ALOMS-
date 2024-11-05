from django.db import models
from django.contrib.auth.models import User

class ODRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.IntegerField()
    reason = models.TextField()
    file = models.FileField(upload_to='od_files/')
    status = models.CharField(max_length=20, default='Pending')  # Pending, Approved, Denied

class LeaveIntimation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # Pending, Approved, Denied
