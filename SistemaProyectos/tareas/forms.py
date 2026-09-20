from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Proyecto, Tarea

#UserCreationForm tiene un formulario con los campos username, password1(contraseña),
#password2(confirmación) incorporado
class RegistroUsuarioForm(UserCreationForm):
    #email se crea, ya que en UserCreationForm no viene incorporado
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega estilo bootstrap a los campos con for
        for nombre, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        #Modifica el texto ayuda del formulario
        self.fields["username"].help_text = "Requerido. Máximo 150 caracteres."
        self.fields["email"].help_text = "Requerido. Debe incluir @."

#forms.ModelForm es un formulario vacío, cuyos campos dependen del modelo en que se basen
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion"]

        #Permite aplicar estilos bootstrap a campos seleccionados
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'blank':True}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["nombre", "descripcion", "estado"]

        #Permite aplicar estilos bootstrap a campos seleccionados
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'blank':True}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }