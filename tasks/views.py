from django.shortcuts import render
# Utilizar clase para crear formularios
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def helloworld(request):
    return render(request,'singup.html',{
        'form' : UserCreationForm
    })