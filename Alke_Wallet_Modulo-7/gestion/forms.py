from django import forms
from .models import Cliente, Cuenta, Transaccion


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        fields = [
            "nombre",
            "email",
            "telefono",
        ]

        #Se especifica el nombre de las etiquetas asociadas a cada field/campo
        #De lo contrario django lo asigna
        labels = {
            "nombre": "Nombre completo",
            "email": "Correo electrónico",
            "telefono": "Teléfono"
        }

        #Especifica el tipo de campo para cada field y aplica bootstrap
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
        }

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta

        fields = [
            "numero",
            "contactos_autorizados",
        ]

        labels = {
            "numero": "Numero de cuenta",
            "contactos_autorizados": "Seleccione las cuentas autorizadas",
        }

        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "contactos_autorizados": forms.CheckboxSelectMultiple(attrs={"class": "list-unstyled mb-3"}),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion

        fields = [
            "tipo",
            "monto",
            "descripcion"
        ]

        labels = {
            "tipo": "Seleccione el tipo de transacción",
            "monto": "Monto",
            "descripcion": "Descripción",
        }

        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }