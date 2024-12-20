from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions') 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
     
