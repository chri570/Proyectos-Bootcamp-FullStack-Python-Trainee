from django.urls import path
from .views import (ClienteCreateView, ClienteDeleteView, ClienteDetailView, ClienteListView, ClienteUpdateView,
                    CuentaCreateView, CuentaUpdateView, CuentaDeleteView, TransaccionCreateView)

urlpatterns = [
    path("", ClienteListView.as_view(), name="lista_clientes"),
    path("clientes/crear/", ClienteCreateView.as_view(), name="crear_cliente"),
    path("clientes/<int:pk>/", ClienteDetailView.as_view(), name="detalle_cliente"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="editar_cliente"),
    path("clientes/<int:pk>/eliminar/", ClienteDeleteView.as_view(), name="eliminar_cliente"),
    path("clientes/<int:pk>/crear_cuenta", CuentaCreateView.as_view(), name="crear_cuenta"),
    path("clientes/actualizar_cuenta/<int:pk>", CuentaUpdateView.as_view(), name="actualizar_cuenta"),
    path("clientes/eliminar_cuenta/<int:pk>", CuentaDeleteView.as_view(), name="eliminar_cuenta"),
    path("clientes/crear_transacción/<int:pk>", TransaccionCreateView.as_view(), name="crear_transaccion"),
]