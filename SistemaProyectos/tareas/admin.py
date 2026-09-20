from django.contrib import admin
from .models import Proyecto, Tarea


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "fecha_creacion")

    #usuario es un objeto que pertenece al modelo User y username es un atributo de ese modelo
    #razón por la que se usa __ para acceder al valor.
    search_fields = ("nombre", "usuario__username")
    list_filter = ("usuario__username",)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "estado", "fecha_creacion")
    list_filter = ("estado",)

    #proyecto es un atributo foreign key que pertenece al modelo Proyecto
    search_fields = ("nombre", "proyecto__nombre")
