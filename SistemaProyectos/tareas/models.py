from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
    #Atributos/campos
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    #User es un modelo django. related_name, permite aplicar busqueda inversa usuario.proyectos.all()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proyectos")

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    #Constante que contiene valores posibles del estado de una tarea
    #Cada tupla tiene 2 elementos:
    #El primero se guarda en base de datos y el segundo es lo que ve el usuario.
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("finalizada", "Finalizada"),
    ]

    #Atributos/campos
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(default="pendiente", choices=ESTADOS, max_length=20)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="tareas")

    def __str__(self):
        return self.nombre