from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ClienteForm, CuentaForm, TransaccionForm
from .models import Cliente, Cuenta, Transaccion

#la clase bloquea el acceso a las vistas
#a usuarios no logueados y que no sean staff
#staff permite el acceso al administrador de django
class AccesoPersonalMixin(LoginRequiredMixin, UserPassesTestMixin,):
    def test_func(self):
        return self.request.user.is_staff


#---------------------------------Cliente-----------------------------------------


class ClienteListView(AccesoPersonalMixin, ListView):
    model = Cliente
    template_name = "gestion/lista_clientes.html"
    context_object_name = "clientes"

    def get_queryset(self):
        #Se obtienen todos los clientes registrados, añadiendo a cada registro el conteo de transacciones realizadas
        #en una cuenta y se ordenan de forma ascendente por nombre
        clientes = Cliente.objects.annotate(
            total_movimientos=Count("cuenta__transacciones")
        ).order_by("nombre")

        #Obtiene el valor del input de la barra de búsqueda
        buscar = self.request.GET.get("buscar", "").strip()

        #Filtra el/los clientes de acuerdo al substring que coincida con nombre o email.
        if buscar:
            clientes = clientes.filter(
                Q(nombre__icontains=buscar)
                | Q(email__icontains=buscar)
            )

        return clientes

    #Guarda el valor buscado de la barra de búsqueda y lo añade al contexto para ser usado en el template
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto["buscar"] = self.request.GET.get(
            "buscar", ""
        )

        return contexto


class ClienteDetailView(AccesoPersonalMixin, DetailView):
    model = Cliente
    template_name = "gestion/detalle_cliente.html"
    context_object_name = "cliente"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        #Devuelve la cuenta cuyo cliente sea igual al id/pk recibido en la url.
        #Al usar first se devuelve None cuando no se encuentra una cuenta asociada a un cliente
        cuenta = Cuenta.objects.filter(
            cliente=self.object
        ).first()

        #Se añade la cuenta del cliente al contexto del template
        contexto["cuenta"] = cuenta

        contexto["titulo"] = "Detalle cliente"

        #Guarda los ingresos y egresos asociados a la cuenta solo si existen
        contexto["movimientos"] = cuenta.transacciones.all() if cuenta else []

        return contexto


class ClienteCreateView(AccesoPersonalMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/form_cliente.html"
    success_url = reverse_lazy("lista_clientes")

    #Añade un valor adicional al contexto del template
    extra_context = {
        "titulo": "Crear cliente",
    }

    #Antes de redireccionar se añade un mensaje informativo para el usuario
    def form_valid(self, form):
        respuesta = super().form_valid(form)

        messages.success(
            self.request,
            "Cliente creado correctamente.",
        )

        return respuesta


class ClienteUpdateView(AccesoPersonalMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/form_cliente.html"
    success_url = reverse_lazy("lista_clientes")

    #Añade un valor adicional al contexto del template
    extra_context = {
        "titulo": "Actualizar cliente",
    }

    #Antes de redireccionar se añade un mensaje informativo para el usuario
    def form_valid(self, form):
        respuesta = super().form_valid(form)

        messages.success(
            self.request,
            "Cliente actualizado correctamente.",
        )

        return respuesta


class ClienteDeleteView(AccesoPersonalMixin, DeleteView):
    model = Cliente
    template_name = "gestion/confirmar_eliminar.html"
    context_object_name = "cliente"
    success_url = reverse_lazy("lista_clientes")

    def form_valid(self, form):
        #La eliminación del cliente solo se hace si no tiene una cuenta
        try:
            respuesta = super().form_valid(form)
        except ProtectedError:
            #Se redirecciona a detalle del cliente notificando que el cliente tiene una cuenta
            messages.error(
                self.request,
                "No se puede eliminar un cliente "
                "que tiene una cuenta asociada.",
            )

            return redirect("detalle_cliente", pk=self.object.pk,)

        #Se añade mensaje de eliminación exitosa antes de redireccionar a la url correspondiente.
        messages.success(self.request,"Cliente eliminado correctamente.",)

        return respuesta




#-----------------------------------Cuenta-----------------------------------------


class CuentaCreateView(AccesoPersonalMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = "gestion/form_cuenta.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["id_cliente"] = self.kwargs["pk"]
        contexto["titulo"] = "Crear cuenta"

        return contexto


    def form_valid(self, form):
        try:
            cliente = Cliente.objects.get(pk=self.kwargs["pk"])
            if Cuenta.objects.filter(cliente=cliente).exists():
                raise ValueError
        except ValueError:
            messages.error(self.request, "Cliente solo puede tener UNA cuenta.")
            return redirect("detalle_cliente", pk=self.kwargs["pk"])

        form.instance.cliente = cliente

        # Se añade mensaje de creación de cuenta exitosa antes de redireccionar a la url correspondiente.
        messages.success(self.request, "Cuenta creada correctamente.", )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("detalle_cliente",args=[self.kwargs["pk"]])


class CuentaUpdateView(AccesoPersonalMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = "gestion/form_cuenta.html"


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])
        id_cliente = cuenta.cliente.id

        contexto["id_cliente"] = id_cliente
        contexto["titulo"] = "Actualizar cuenta"

        return contexto


    def form_valid(self, form):
        # Se añade mensaje de creación de cuenta exitosa antes de redireccionar a la url correspondiente.
        messages.success(self.request, "Cuenta eliminada correctamente.", )

        return super().form_valid(form)

    def get_success_url(self):
        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])
        id_cliente = cuenta.cliente.id
        return reverse("detalle_cliente",args=[id_cliente])

class CuentaDeleteView(AccesoPersonalMixin, DeleteView):
    model = Cuenta
    template_name = "gestion/confirmar_eliminar_cuenta.html"
    context_object_name = "cuenta"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])
        id_cliente = cuenta.cliente.id

        contexto["id_cliente"] = id_cliente

        return contexto


    def form_valid(self, form):
        #Para eliminar una cuenta significa que no debe tener transacciones
        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])
        try:
            if cuenta.transacciones.exists():
                raise ValueError
        except ValueError:
            id_cliente = cuenta.cliente.id
            messages.error(self.request, "No se puede eliminar una cuenta que tiene transacciones.")
            return redirect("detalle_cliente", pk=id_cliente)

        # Se añade mensaje de creación de cuenta exitosa antes de redireccionar a la url correspondiente.
        messages.success(self.request, "Cuenta eliminada correctamente.", )

        return super().form_valid(form)

    def get_success_url(self):
        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])

        id_cliente = cuenta.cliente.id

        return reverse("detalle_cliente",args=[id_cliente])



#--------------------------------Transaccion-----------------------------------

class TransaccionCreateView(AccesoPersonalMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = "gestion/crear_transaccion.html"

    def form_valid(self, form):
        form.instance.cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])

        messages.success(self.request, "Transacción creada correctamente.", )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])
        id_cliente = cuenta.cliente.id

        contexto["id_cliente"] = id_cliente

        return contexto

    def get_success_url(self):
        cuenta = Cuenta.objects.get(pk=self.kwargs["pk"])

        id_cliente = cuenta.cliente.id

        return reverse("detalle_cliente", args=[id_cliente])