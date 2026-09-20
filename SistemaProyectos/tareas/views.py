from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import RegistroUsuarioForm, ProyectoForm, TareaForm
from .models import Proyecto, Tarea


#------------------------------------Registro usuario-----------------------------------------

#CreateView es una vista vacía
class RegistroUsuarioView(CreateView):

    #Formulario a usar en el template
    form_class = RegistroUsuarioForm

    #Template donde se renderiza el formulario de registro
    template_name = "registration/registro.html"

    #Redirección a template especificado en urls que es login
    success_url = reverse_lazy("login")


#--------------------------------------Proyecto-----------------------------------------

#ListView listará los objetos
#LoginRequiredMixin es una herramienta que condiciona un inicio de sesión para acceder a una vista
#LoginRequiredMixin debe ir antes que listview, ya que debe verificar login primero
class ProyectoListView(LoginRequiredMixin, ListView):

    #Modelo del cual se extraen los campos
    model = Proyecto

    #Template donde se renderiza los campos
    template_name = "tareas/proyecto-list.html"

    #Nombre con el que se envían los datos al template
    context_object_name = "proyectos"

    #Condiciona los proyectos a mostrar por usuario logueado
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


#DetaiView procesa los campos de un proyecto
class ProyectoDetailView(LoginRequiredMixin, DetailView):

    # Modelo del cual se extraen los campos
    model = Proyecto

    #Template donde se renderiza el modelo
    template_name = "tareas/proyecto-detail.html"

    #Nombre con el que se enviaran los datos al template
    context_object_name = "proyecto"

    #Define el nombre con el que viene un valor primary key en la url del proyecto
    #En vistas genericas es pk
    pk_url_kwarg = "id"

    #Condiciona los proyectos a mostrar por usuario logueado
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


#CreateView construye su vista a partir de un formulario
class ProyectoCreateView(LoginRequiredMixin, CreateView):

    #Formulario del template
    form_class = ProyectoForm

    #Template donde se renderiza el formulario de nuevo proyecto
    template_name = "tareas/proyecto-create.html"

    # Redirección a template especificado en urls proyecto_list
    success_url = reverse_lazy("proyecto_list")

    #En la validación del formulario, se asigna al usuario correspondiente al proyecto
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


#En update no se valida el usuario en el formulario, ya que está asignado a un proyecto
class ProyectoUpdateView(LoginRequiredMixin, UpdateView):

    # Modelo del cual se extraen los campos
    model = Proyecto

    # Formulario del template
    form_class = ProyectoForm

    # Template donde se renderiza el formulario
    template_name = "tareas/proyecto-update.html"

    # Define el nombre con el que viene un valor primary key en la url de la tarea
    pk_url_kwarg = "id"

    # Redirección a template especificado en urls proyecto_list
    success_url = reverse_lazy("proyecto_list")

    # Condiciona los proyectos a mostrar por usuario. La consulta trae todos los proyectos
    # Y debido a UpdateView se restringe a solo 1 por el id enviado en la url
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


    # Obtiene los datos a enviar al template y añade el id del proyecto al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proyecto_id"] = self.kwargs["id"]
        return context


#El delete de un proyecto es procesado por DeleteView
class ProyectoDeleteView(LoginRequiredMixin, DeleteView):

    # Modelo del cual se extraen los campos
    model = Proyecto

    # Template donde se renderiza el proyecto a eliminar
    template_name = "tareas/proyecto-delete.html"

    # Define el nombre con el que viene un valor primary key en la url del proyecto
    pk_url_kwarg = "id"

    # Redirección a template especificado en urls proyecto_list
    success_url = reverse_lazy("proyecto_list")

    # Nombre con el que se enviaran los datos al template
    context_object_name = "proyecto"

    # Condiciona los proyectos a mostrar por usuario. La consulta trae todos los proyectos
    # Y debido a DeleteView se restringe a solo 1 por el id enviado en la url
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)


    # Obtiene los datos a enviar al template y añade el id del proyecto al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proyecto_id"] = self.kwargs["id"]
        return context



#----------------------------------Tareas------------------------------------------------

class TareaCreateView(LoginRequiredMixin, CreateView):

    # Formulario a usar en el template
    form_class = TareaForm

    # Template donde se renderiza el formulario de nueva tarea
    template_name = "tareas/tarea-create.html"

    # Obtiene los datos a enviar al template y añade el id del proyecto al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proyecto_id"] = self.kwargs["id"]
        return context


    def form_valid(self, form):

        #Se asigna el proyecto al que pertenece una tarea
        #self.kwargs obtiene los valores de parámetros enviados por url
        proyecto = Proyecto.objects.get(id = self.kwargs["id"])
        form.instance.proyecto = proyecto

        #Se aplica la validación del formulario
        return super().form_valid(form)


    #La redirección se hace indicando el nombre de la vista y colocando el id del proyecto
    def get_success_url(self):
        return reverse("proyecto_detail", args=[self.kwargs["id"]])


#En UpdateView no se valida usuario en el formulario, ya está asignado a la tarea
class TareaUpdateView(LoginRequiredMixin, UpdateView):

    # Modelo del cual se extraen los campos
    model = Tarea

    #Formulario a usar en el template
    form_class = TareaForm

    # Template donde se renderiza el formulario de nueva tarea
    template_name = "tareas/tarea-update.html"

    # Define el nombre con el que viene un valor primary key en la url de la tarea
    pk_url_kwarg = "id"

    # Condiciona las tareas a mostrar por usuario. La consulta trae todos los tareas
    # Y debido a UpdateView se restringe a solo 1 por el id enviado en la url
    def get_queryset(self):
        return Tarea.objects.all()


    def get_success_url(self):
        #Se obtiene la tarea editada. Se busca el proyecto asociado y se guarda el id
        tarea = Tarea.objects.get(id = self.kwargs["id"])
        proyecto = tarea.proyecto
        id_proyecto = proyecto.id

        #La redirección se hace a detalles del proyecto
        return reverse("proyecto_detail", args=[id_proyecto])


    def get_context_data(self, **kwargs):
        # Obtiene los datos a enviar al template y se añade el id del proyecto
        context = super().get_context_data(**kwargs)
        tarea = Tarea.objects.get(id=self.kwargs["id"])
        proyecto = tarea.proyecto
        context["proyecto_id"] = proyecto.id

        return context

class TareaDeleteView(LoginRequiredMixin, DeleteView):

    # Modelo del cual se extraen los campos
    model = Tarea

    # Template donde se renderiza el formulario de eliminar tarea
    template_name = "tareas/tarea-delete.html"

    # Define el nombre con el que viene un valor primary key en la url de la tarea
    pk_url_kwarg = "id"

    #Devuelve la tarea a eliminar. Debido a DeleteView se restringe a solo 1
    # Al pasar el id de la tarea a actualizar en la url
    def get_queryset(self):
        return Tarea.objects.all()


    def get_context_data(self, **kwargs):
        # Obtiene los datos a enviar al template y
        # añade el id del proyecto ascoiado y el nombre de la tarea
        context = super().get_context_data(**kwargs)
        tarea = Tarea.objects.get(id=self.kwargs["id"])
        proyecto = tarea.proyecto
        context["proyecto_id"] = proyecto.id
        context["nombre_tarea"] = tarea.nombre

        return context


    def get_success_url(self):
        #Se obtiene la tarea a eliminar. Se busca el proyecto asociado y se guarda el id
        tarea = Tarea.objects.get(id = self.kwargs["id"])
        proyecto = tarea.proyecto
        id_proyecto = proyecto.id

        #La redirección se hace a detalles del proyecto
        return reverse("proyecto_detail", args=[id_proyecto])
