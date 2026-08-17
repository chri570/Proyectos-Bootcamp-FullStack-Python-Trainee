from pathlib import Path

def mostrar_contactos(lista_contactos):
    print(f"{'-' * 38}")
    print(f"{' '*10}LISTA DE CONTACTOS{' '*10}")

    if len(lista_contactos) == 0:
        print("INFO: No hay contactos registrados.")
        print(f"{'-' * 38}")
        return

    for i, (nombre, telefono) in enumerate(lista_contactos.items(), start=1):
        print(f"({i}) Nombre: {nombre} | Teléfono: {telefono}")

    print(f"{'-' * 38}")


def agregar_nuevo_contacto(lista_contactos):
    print(f"{'-' * 38}")
    print(f"{' ' * 10}NUEVO CONTACTO{' ' * 10}")

    #Ingreso y validación de nombre y n°teléfono
    nombre_contacto = validar_nombre()
    numero_telefono = validar_telefono()

    if nombre_contacto.lower() in [nombre.lower() for nombre in lista_contactos]:
        print(f"ERROR: Ya existe un contacto con el nombre ingresado.")
    
    else:
        #Creación de nuevo contacto
        lista_contactos[nombre_contacto] = numero_telefono
        print(f"INFO: Contacto creado con éxito.")

    print(f"{'-' * 38}")


def validar_nombre():
    while True:
        nombre = input("Nombre: ")
        if len(nombre) > 20:
            print("ERROR: El máximo de caracteres permitidos es 20.\n")
        else:
            break
    return nombre


def validar_telefono():
    while True:
        numero = input("Teléfono: ")
        if numero.isdigit():
            #56 612 XXXXXX (11) = 612 XXXXXX (9) longitud teléfono fijo
            #56 9 XXXXXXXX (11) = 9XXXXXXXX (9) longitud teléfono móvil
            if 9 <= len(numero) <= 11:
                break
            else:
                print(f"ERROR: La cantidad de dígitos ingresados no cumplen con el total mínimo o máximo permitidos.\n")

        else:
            print(f"ERROR: Solo se pueden ingresar dígitos.\n")

    return numero


def modificar_contacto(lista_contactos):
    print(f"{'-' * 38}")
    print(f"{' ' * 10}MODIFICAR CONTACTO{' ' * 10}")

    if len(lista_contactos) == 0:
        print("INFO: No hay contactos registrados.")
        print(f"{'-' * 38}")
        return

    mostrar_contactos(lista_contactos)

    while True:
        #Se guarda el número que representa un contacto en el listado de tipo str
        #Se guardan las claves, para modificar el contacto seleccionado
        opciones = [str(i) for i, clave in enumerate(lista_contactos, start=1)]
        claves = [clave for clave in lista_contactos]

        #Guarda el contacto a modificar
        select_contacto = input("Ingrese el número (x) del contacto a modificar: ")

        #Verifica si el contacto está en la lista
        if select_contacto.replace(" ","") in opciones:
            mostrar_opciones_modificacion()
            while True:
                opcion = input("Ingrese opción 1 o 2: ")

                #Validación de opción
                if opcion in ("1", "2"):
                    #Modifica nombre
                    if opcion == "1":
                        nombre_nuevo = validar_nombre()

                        # Si el nombre existe en alguna clave, no se agrega el contacto, saliendo al menú.
                        if nombre_nuevo.lower() in [nombre.lower() for nombre in lista_contactos]:
                            print(f"ERROR: Ya existe un contacto con el nombre ingresado.")

                        else:
                            #No se puede modificar el nombre de la clave directamente
                            #Se crea un nuevo diccionario con el teléfono y se borra el contacto anterior
                            lista_contactos[nombre_nuevo] = lista_contactos[ claves[int(select_contacto) - 1] ]
                            del lista_contactos[ claves[int(select_contacto) - 1] ]
                            print(f"INFO: Nombre modificado con éxito.\n")

                    #Modifica teléfono
                    else:
                        telefono_nuevo = validar_telefono()
                        lista_contactos[ claves[int(select_contacto) - 1] ] = telefono_nuevo
                        print(f"INFO: Teléfono modificado con éxito.")
                    break

                else:
                    print("ERROR: Elija una opción válida.\n")
            break

        else:
            print("ERROR: El nombre del contacto no fue encontrado.\n")

    print(f"{'-' * 38}")


def mostrar_opciones_modificacion():
    print(f"¿Qué desea modificar?")
    print(f"(1) Nombre.")
    print(f"(2) Teléfono.")


def eliminar_contacto(lista_contactos):
    print(f"{'-' * 38}")
    print(f"{' ' * 10}ELIMINAR CONTACTO{' ' * 10}")

    if len(lista_contactos) == 0:
        print("INFO: No hay contactos registrados.")
        print(f"{'-' * 38}")
        return

    mostrar_contactos(lista_contactos)

    #Se guarda el número que representa un contacto en el listado de tipo str
    #Se guardan las claves, para eliminar el contacto seleccionado
    opciones = [str(i) for i, clave in enumerate(lista_contactos, start=1)]
    claves = [clave for clave in lista_contactos]

    while True:
        #Guarda la opción ingresada
        select_contacto = input("Ingrese el número (x) del contacto a eliminar: ")

        if select_contacto.replace(" ","") in opciones:
            #Se convierte select_contacto a tipo int para acceder a la clave
            #y se resta 1 por estar en una lista
            del lista_contactos[ claves[int(select_contacto)-1] ]
            print(f"INFO: Contacto borrado.")
            break

        else:
            print(f"ERROR: Opción no válida.\n")

    print(f"{'-' * 38}")


def cargar_datos():
    agenda = {}

    #Lectura de datos del archivo. Si no existe, lo crea
    if not Path("agenda.txt").is_file():
        with open("agenda.txt", "x") as archivo:
            pass

    else:
        with open("agenda.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                #Crea una lista con 2 elementos, clave y valor, respectivamente. Determinado por el "|"
                contacto = linea.split("|")
                nombre = contacto[0].strip()
                telefono = contacto[1].strip()
                agenda[nombre] = telefono

    return agenda


def guardar_datos(agenda):
    #Escritura/Sobrescritura de datos al archivo
    with open("agenda.txt", "w", encoding="utf-8") as archivo:
        for clave, valor in agenda.items():
            archivo.write(f"{clave} | {valor}\n")
