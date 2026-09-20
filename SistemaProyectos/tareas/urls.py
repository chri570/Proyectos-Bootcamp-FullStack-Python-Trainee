from django.urls import path
from .views import *

urlpatterns = [
    path("proyecto/lista", ProyectoListView.as_view(), name="proyecto_list"),
    path("proyecto/detalle/<int:id>", ProyectoDetailView.as_view(), name="proyecto_detail"),
    path("proyecto/nuevo", ProyectoCreateView.as_view(),name = "proyecto_create"),
    path("proyecto/actualizar/<int:id>", ProyectoUpdateView.as_view(), name="proyecto_update"),
    path("proyecto/borrar/<int:id>", ProyectoDeleteView.as_view(), name="proyecto_delete"),
    path("proyecto/<int:id>/tarea_nueva", TareaCreateView.as_view(), name="tarea_create"),
    path("proyecto/tarea_actualizar/<int:id>", TareaUpdateView.as_view(), name="tarea_update"),
    path("proyecto/tarea_delete/<int:id>", TareaDeleteView.as_view(), name="tarea_delete"),
]