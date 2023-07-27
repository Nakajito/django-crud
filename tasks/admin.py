from django.contrib import admin
# importar modelos que creamos
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('creates', )
    
# Register your models here.
admin.site.register(Task, TaskAdmin)