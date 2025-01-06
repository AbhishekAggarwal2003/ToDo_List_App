from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)  # Deadline for the task

    # Adding priority field
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='Medium',
    )

    def __str__(self):
        return self.todo_name
    
    def time_remaining(self):
        if self.deadline:
            time_remaining = self.deadline - timezone.now()
            return max(timedelta(0), time_remaining)
        return timedelta(0)  # No deadline, no time remaining