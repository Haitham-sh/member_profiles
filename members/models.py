from django.db import models
from users.models import User
from events.models import Event

class EventMember(models.Model):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('speaker', 'Speaker'),
        ('graduate', 'Graduate'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('participant', 'Participant'),
        ('guest', 'Guest'),
        ('volunteer', 'Volunteer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'event']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"