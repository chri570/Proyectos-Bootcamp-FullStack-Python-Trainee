from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import RegistroUsuarioForm, ProyectoForm
from .models import Proyecto, Tarea

#Vistas basadas en clases
#Las basadas en funciones usan render

#CreateView es una vista vacía
class RegistroUsuarioView(CreateView):

    #Formulario a usar en el template
    form_class = RegistroUsuarioForm

    #Template donde se renderiza el formulario de registro
    template_name = "registration/registro.html"

    #Redirección a template especificado en urls
    #En este caso, redirecciona a login nuevamente. Se usa el name no la ruta
    success_url = reverse_lazy("login")


#ListView listará los objetos
#LoginRequiredMixin es una herramienta que condiciona un inicio de sesión para acceder a una vista
#LoginRequiredMixin debe ir antes que listview, ya que debe verificar login primero
class ProyectoListView(LoginRequiredMixin, ListView):

    #Modelo del cual se extraen los campos
    model = Proyecto

    #Template donde se renderiza el modelo
    template_name = "tareas/proyecto-list.html"

    #Es el nombre con el que se enviaran los datos al template
    context_object_name = "proyectos"

    #Condiciona los objetos a mostrar por usuario
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)



class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto

    #Template donde se renderiza el modelo
    template_name = "tareas/proyecto-detail.html"

    #Nombre con el que se enviaran los datos al template
    context_object_name = "proyecto"

    #Define el nombre con el que viene un valor primary key en la url
    pk_url_kwarg = "id"

    #Condiciona los objetos a mostrar por usuario
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)

class ProyectoCreateView(LoginRequiredMixin, CreateView):

    #Formulario del template
    form_class = ProyectoForm

    #Template donde se renderiza el formulario de nuevo proyecto
    template_name = "tareas/proyecto-create.html"

    # Redirección a template especificado en url+s
    # En este caso, a proyecto-list
    success_url = reverse_lazy("proyecto_list")

    #En la validación del formulario, se asigna al usuario correspondiente al proyecto
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

#En update no se valida el usuario en el formulario, ya que está asignado a un proyecto
class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto

    form_class = ProyectoForm

    # Template donde se renderiza el formulario de nuevo proyecto
    template_name = "tareas/proyecto-create.html"

    # Define el nombre con el que viene un valor primary key en la url
    pk_url_kwarg = "id"

    # Redirección a template especificado en url+s
    # En este caso, a proyecto-list
    success_url = reverse_lazy("proyecto_list")

    # Condiciona los objetos a mostrar por usuario
    #Si bien la consulta deberia mostrar todos los proyectos, debido a UpdateView se restringe a solo 1
    #Al pasar el id del proyecto a actualizar en la url
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)

#El delete de un proyecto es procesado por DeleteView
class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto

    # Template donde se renderiza el formulario de nuevo proyecto
    template_name = "tareas/proyecto-create.html"

    # Define el nombre con el que viene un valor primary key en la url
    pk_url_kwarg = "id"

    # Redirección a template especificado en url+s
    # En este caso, a proyecto-list
    success_url = reverse_lazy("proyecto_list")

    context_object_name = "proyecto"

    # Condiciona los objetos a mostrar por usuario
    #Si bien la consulta deberia mostrar todos los proyectos, debido a DeleteView se restringe a solo 1
    #Al pasar el id del proyecto a borrar en la url
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)