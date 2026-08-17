from metodos_agenda import mostrar_contactos, agregar_nuevo_contacto, modificar_contacto, eliminar_contacto, \
    cargar_datos, guardar_datos
from textwrap import dedent

agenda = cargar_datos()

while True:
    print(f"BIENVENIDO A AGENDA TELEFÓNICA")
    print(f"¿Qué desea hacer?")
    print(dedent(f"""
        (1) Mostrar contactos.
        (2) Agregar nuevo contacto.
        (3) Modificar contacto.
        (4) Eliminar contacto.
        (5) Salir."""))

    opcion = input("\nSeleccione una opción: ")

    match opcion:
        case "1":
            mostrar_contactos(agenda)
        case "2":
            agregar_nuevo_contacto(agenda)
        case "3":
            modificar_contacto(agenda)
        case "4":
            eliminar_contacto(agenda)
        case "5":
            guardar_datos(agenda)
            print("¡GRACIAS. VUELVE PRONTO!")
            break
        case _:
            print("Opción no válida.\n")
