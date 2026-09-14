from django.contrib import admin
from .models import Proyecto, Tarea

# Register your models here.
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "fecha_creacion")

    #username es un atributo foreign key que pertenece al modelo User
    #y para mostrar un campo específico se utiliza __ y su nombre
    search_fields = ("nombre", "usuario__username")

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "estado", "fecha_creacion")
    list_filter = ("estado",)

    #proyecto es un atributo foreign key que pertenece al modelo Proyecto
    search_fields = ("nombre", "proyecto__nombre")