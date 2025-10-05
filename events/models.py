from django.db import models
from users.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ('graduation', 'Graduation'),
        ('conference', 'Conference'),
        ('meeting', 'Meeting'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_password = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title