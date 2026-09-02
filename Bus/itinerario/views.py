from django.shortcuts import render, redirect
import json, os


ARCHIVO_JSON = os.path.join(os.path.dirname(__file__), "data", "itinerarios.json")


def cargar_itinerarios():
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_itinerarios(itinerarios):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(
            itinerarios,
            archivo,
            ensure_ascii= False,
            indent = 4
        )

# Create your views here.
def inicio(request):
    itinerarios = cargar_itinerarios()
    return render(request, "index.html", {"itinerarios": itinerarios})

def crear(request):
    if request.method == "POST":
        itinerarios = cargar_itinerarios()

        nuevo_id = max([itinerario["id"] for itinerario in itinerarios], default=0) + 1

        nuevo_itinerario = {
            "id": nuevo_id,
            "nombre_linea": request.POST.get('nombre_linea'),
            "origen": request.POST.get('origen'),
            "destino": request.POST.get('destino'),
            "hora_salida": request.POST.get('hora_salida'),
            "hora_llegada": request.POST.get('hora_llegada'),
            "frecuencia": request.POST.get('frecuencia'),
            "estado": request.POST.get('estado')
        }

        itinerarios.append(nuevo_itinerario)
        guardar_itinerarios(itinerarios)

        return redirect("inicio")
    return render(request, "crear.html")

def detalle(request, id):
    itinerarios = cargar_itinerarios()

    itinerario_encontrado = None

    for i in itinerarios:
        if i["id"] == id:
            itinerario_encontrado = i
            break

    return render(request, "detalle.html", {"itinerario": itinerario_encontrado})

def eliminar(request, id):
    itinerarios = cargar_itinerarios()

    for i in itinerarios:
        if i["id"] == id:
            itinerarios.remove(i)

            break
    guardar_itinerarios(itinerarios)

    return redirect('inicio')