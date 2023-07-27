from django.db import models
# Importar user
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creates = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # mostrar el titulo y nombre de quien creó la tarea
    def __str__(self):
        return self.title + ' - ' + self.user.username