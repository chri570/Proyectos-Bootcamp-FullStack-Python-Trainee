from django.urls import path
from .views import *

urlpatterns = [
    path("proyecto/lista", ProyectoListView.as_view(), name="proyecto_list"),
    path("proyecto/detalle/<int:id>", ProyectoDetailView.as_view(), name="proyecto_detail"),
    path("proyecto/nuevo", ProyectoCreateView.as_view(),name = "proyecto_create"),
    path("proyecto/actualizar/<int:id>", ProyectoUpdateView.as_view(), name="proyecto_update"),
    path("proyecto/borrar/<int:id>", ProyectoDeleteView.as_view(), name="proyecto_update"),
]