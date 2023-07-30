# importamos render para mostrar una pagina web
from django.shortcuts import render, redirect, get_object_or_404
# Utilizar clase para crear formularios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Permite guardar usuarios en la DB
from django.contrib.auth.models import User
# Permite utilizar el response
from django.http import HttpResponse
# Utilizar login (cookie)
from django.contrib.auth import login, logout, authenticate
# Para manejar el error IntegrityError
from django.db import IntegrityError
# importar el formulario para ingresar tareas
from .forms import TaskForm
# Acceder al modelo de la base de datos
from .models import Task

# definimos la función para mosntrar eh home
def home(request):
    return render(request, 'home.html')

# Definimos la función para el singup y validar el usuario, contraseña y guardar en la base de datos, primero se deben de realizar las migraciones con <python manage.py migrate>


def singup(request):

    # Si se accede con el método GET se muestra el formulario
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    # Se se accede con el método POST se validan los datos de usuario, contraseña, y guardar en la base de datos
    else:
        # Comprobamos que las contraseñas sen iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                # si las contraseñas coinciden se crea el objeto user con el nombre de usuario y contraseña
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                # Guardamos el usuario en la DB
                user.save()
                # Creamos una sesión para el usuario
                login(request, user)
                # Redireccionamos a la página tasks
                return redirect('tasks')
                # Mostramos el mensaje que se guardó el usuario
                # return HttpResponse('Usuario creado satisfactoriamente')
            except IntegrityError:
                # En caso de que exista el usuario
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya esxiste',
                })
            # Mensaje que indica que las contraseñas son no coinciden
        return render(request, 'singup.html', {
            'form' : UserCreationForm,
            'error' : 'Las contraseñas no coinciden'
        })

def tasks(request):
    # Obtenemos todos los elementos de la DB tasks = Task.objects.all()
    # usamos filter para mostar los datos de un usuarios especifico y que no esten compmletadas
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html',{
        'tasks' : tasks
    })

def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        # Permite rellenar el formulario con los datos guardados
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{
                'task'  : task,
                'form' : form
            })
    else:
        try:
            task = get_object_or_404(Task, pk = task_id, user = request.user)

            form = TaskForm(instance=task)
            return render(request, 'task_detail.html',{
                'task'  : task,
                'form' : form
            })
        except ValueError:
            return render(request, 'task_detail.html', {
                'task' : task,
                'form' : form,
                'error' : "Error actualizando"
            })
        

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form' : TaskForm,
                'error' : 'Proporciona datos validos'
                })
        
def singout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
            )
        if user is None:
            return render(request, 'signin.html', {
                'form' : AuthenticationForm,
                'error' : 'Usuario o contraseña invalido'
            })
        else:
            login(request, user)
            return redirect('tasks')
        