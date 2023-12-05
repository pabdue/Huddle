from django.db import models
from django.utils import timezone

# Create your models here.
class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)  # Note: In practice, use a more secure way to store passwords (e.g., Django's built-in password hashing)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HuddleGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Account, related_name='huddle_groups')

    def __str__(self):
        return self.name
    
class Task(models.Model):
    huddle_group = models.ForeignKey(HuddleGroup, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    people_assigned = models.TextField(max_length=100)
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class HuddleGroupMembers(models.Model):
    huddlegroup = models.ForeignKey(HuddleGroup, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['huddlegroup', 'account']