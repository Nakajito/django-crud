# importamos render para mostrar una pagina web
from django.shortcuts import render
# Utilizar clase para crear formularios
from django.contrib.auth.forms import UserCreationForm
# Permite guardar usuarios en la DB
from django.contrib.auth.models import User
# Permite utilizar el response
from django.http import HttpResponse



# definimos la función para mosntrar eh home
def home(request):
    return render(request,'home.html')

# Definimos la función para el singup y validar el usuario, contraseña y guardar en la base de datos, primero se deben de realizar las migraciones con <python manage.py migrate>
def singup(request):
    
    # Si se accede con el método GET se muestra el formulario
    if request.method == 'GET':
        return render(request,'singup.html',{
            'form' : UserCreationForm
        })
    # Se se accede con el método POST se validan los datos de usuario, contraseña, y guardar en la base de datos
    else:
        # Comprobamos que las contraseñas sen iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                # si las contraseñas coinciden se crea el objeto user con el nombre de usuario y contraseña
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # Guardamos el usuario en la DB
                user.save()
                # Mostramos el mensaje que se guardó el usuario
                return HttpResponse('Usuario creado satisfactoriamente')
            except:
                # En caso de que exista el usuario
                return HttpResponse('Ya existe el usuario')
            # Mensaje que indica que las contraseñas son no coinciden
        return HttpResponse('No coinciden las contraseñas')
    
