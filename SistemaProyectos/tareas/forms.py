from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Proyecto, Tarea

#UserCreationForm tiene un formulario con los campos username,password1(contraseña),
#password2(confirmación) incorporado
class RegistroUsuarioForm(UserCreationForm):
    #email se crea, ya que en UserCreationForm no viene incorporado
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

#forms.ModelForm es un formulario vacío, cuyos campos dependen del modelo en que se basen
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion"]

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["nombre", "descripcion", "estado"]