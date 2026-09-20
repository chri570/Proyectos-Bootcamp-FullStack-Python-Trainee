from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from tareas.views import RegistroUsuarioView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('tareas.urls')),

    #Por defecto, LoginView busca un template_name="registration/login.html"
    #No es necesario pasarlo como argumento dentro de .as_view()
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
]
