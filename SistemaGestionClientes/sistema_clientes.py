from cliente_regular import ClienteRegular
from cliente_premium import ClientePremium
from cliente_corporativo import ClienteCorporativo
from pathlib import Path
from datetime import datetime
import csv

class SistemaClientes:

    #Constructor
    def __init__(self):
        self.__lista_clientes = []

    @staticmethod
    def mostrar_tipo_cliente():
        print(f"\n{'-' * 19}")
        print(f"| {'TIPO DE CLIENTE': <16}|")
        print(f"{'-' * 19}")
        print(f"|{'(1) Regular': <17}|")
        print(f"|{'(2) Premium': <17}|")
        print(f"|{'(3) Corporativo' :<17}|")
        print(f"{'-' * 19}")

    @staticmethod
    def mostrar_opciones_modificacion():
        print(f"\n{'-' * 24}")
        print(f"| {'OPCIONES A MODIFICAR': <21}|")
        print(f"{'-' * 24}")
        print(f"|{'(1) Nombre': <22}|")
        print(f"|{'(2) Email': <22}|")
        print(f"|{'(3) Teléfono': <22}|")
        print(f"|{'(4) Dirección': <22}|")
        print(f"|{'(5) Tipo de cliente': <22}|")
        print(f"{'-' * 24}")

    @staticmethod
    def campos_cliente():
        #Campos en común para todos los clientes
        ide = input("Ingrese identificador: ")
        nombre = input("Ingrese nombre: ")
        email = input("Ingrese email: ")
        telefono = input("Ingrese teléfono: ")
        direccion = input("Ingrese dirección: ")

        return ide, nombre, email, telefono, direccion

    def agregar_cliente(self):
        self.mostrar_tipo_cliente()

        #Selección de opción
        tipo_cliente = input("Ingrese una opción entre 1 a 3: ")

        #Validación opción
        try:
            match tipo_cliente:
                case "1":
                    #Creación cliente regular. Por defecto, descuento 5%
                    ide, nombre, email, telefono, direccion = self.campos_cliente()
                    cliente = ClienteRegular(ide, nombre, email, telefono, direccion, "5")

                case "2":
                    #Creación cliente premium. Por defecto, nivel básico y descuento 10%
                    ide, nombre, email, telefono, direccion = self.campos_cliente()
                    cliente = ClientePremium(ide, nombre, email, telefono, direccion, "16", "alto")

                case "3":
                    #Creación cliente corporativo
                    ide, nombre, email, telefono, direccion = self.campos_cliente()
                    descuento = input("Ingrese descuento para el corporativo: ")
                    empresa = input("Ingrese el nombre de la empresa: ")
                    cliente = ClienteCorporativo(ide, nombre, email, telefono, direccion, descuento, empresa)

                case _:
                    raise ValueError("Opción inválida. Intente otra vez.\n")

            #Añade cliente a la lista
            self.__lista_clientes.append(cliente)
            self.guardar_actividad("Agregación de cliente.")
            print(f"Cliente creado con éxito.\n")

        except ValueError as error:
            self.guardar_actividad("Error al crear cliente.")
            print(error)

        finally:
            print("Redirigiendo...")

    def mostrar_clientes(self):
        self.guardar_actividad("Revisión lista clientes.")
        print(f"\n{'-' * 164}")
        print(f"|{" "* 72}{"LISTA DE CLIENTES"}{" " * 73}|")
        print(f"{'-' * 164}")

        #Listado de clientes
        print(f"|{"":<6} | {"id":<11} | {"Nombre":<21} | {"Email":<30} | {"Teléfono":<13} | {"Dirección":<25} | {"Descuento":<10} | {"Premium":<7} | {"Empresa":<15}|")
        print(f"{'-' * 164}")
        for i, cliente in enumerate(self.__lista_clientes, start=1):
            print(f"|({i:>4}) | {cliente.__str__()}")

        print(f"{'-' * 164}\n")


    def modificar_cliente(self):
        print(f"\n{'-' * 24}")
        print(f"MODIFICAR CLIENTE")
        print(f"{'-' * 24}")

        if len(self.__lista_clientes) == 0:
            print(f"*** Sin datos ***\n")

        else:
            self.mostrar_clientes()

            #Selección cliente
            opcion = input("Selecciona el número del cliente a modificar: ")

            #Validación cliente elegido
            try:
                if not opcion.replace(" ", "").isdigit():
                    raise ValueError("La opción solo puede ser un número.\n")

                elif int(opcion) > len(self.__lista_clientes) or int(opcion) == 0:
                    raise ValueError("Opción inválida. Intente otra vez.\n")

                else:
                    #Guarda el índice del objeto seleccionado
                    indice = int(opcion) - 1
                    self.mostrar_opciones_modificacion()

                    #Guarda el campo a modificar
                    campo = input("Ingrese la opción del campo a modificar: ")

                    #Validación del campo a modificar
                    match campo:
                        case "1":
                            #Nombre
                            self.__lista_clientes[indice].set_nombre()
                        case "2":
                            #Email
                            self.__lista_clientes[indice].set_email()
                        case "3":
                            #Teléfono
                            self.__lista_clientes[indice].set_telefono()
                        case "4":
                            #Dirección
                            self.__lista_clientes[indice].set_direccion()
                        case "5":
                            #Tipo de cliente. Se actualizan de la siguiente forma:
                            #Opción regular, solo para regular y modifica descuento
                            #Opción premium:
                            #Si el cliente es regular, se actualiza a premium nivel básico.
                            #Si el cliente ya es premium, actualiza su nivel, básico->medio o medio->alto
                            #Opción corporativo, solo para corporativo y modifica descuento

                            self.mostrar_tipo_cliente()

                            #Guarda el tipo de cliente
                            tipo_cliente = input("Ingrese la opción del tipo de cliente al cual actualizar: ")

                            #Validación tipo cliente
                            match tipo_cliente:
                                case "1":
                                    #Cliente regular solo puede modificar su descuento
                                    if not isinstance(self.__lista_clientes[indice], ClienteRegular):
                                        raise TypeError("Un cliente Premium o Corporativo no puede cambiar a Regular.\n")

                                    #Modifica porcentaje
                                    self.__lista_clientes[indice].set_descuento()

                                case "2":
                                    #Modificar cliente premium solo nivel
                                    if isinstance(self.__lista_clientes[indice], ClienteCorporativo):
                                        raise TypeError("Un cliente Corporativo no puede cambiar a Premium.\n")

                                    if isinstance(self.__lista_clientes[indice], ClienteRegular):
                                        #Cliente regular se convierte a premium básico
                                        #Se debe instanciar un nuevo objeto premiun con los datos del regular
                                        #Debe ubicarse en el índice donde fue encontrado, eliminar y agregar el nuevo

                                        cliente = ClientePremium(self.__lista_clientes[indice].get_ide(),
                                                                 self.__lista_clientes[indice].get_nombre(),
                                                                 self.__lista_clientes[indice].get_email(),
                                                                 self.__lista_clientes[indice].get_telefono(),
                                                                 self.__lista_clientes[indice].get_direccion(),
                                                                 10,
                                                                 "básico")

                                        #Elimina el cliente regular
                                        del self.__lista_clientes[indice]

                                        #Añade al mismo cliente con la categoría nueva en la posición que ocupaba antes
                                        self.__lista_clientes.insert(indice, cliente)

                                    else: #Pertenece a Cliente Premium
                                        #Si el nivel es alto, lanza error
                                        if self.__lista_clientes[indice].get_nivel() == "alto":
                                            raise ValueError("Un cliente premium de nivel alto, no se puede modificar más.\n")

                                        #Solo modifica nivel y porcentaje de básico->medio y medio->alto

                                        #cliente básico sube a nivel medio
                                        elif self.__lista_clientes[indice].get_nivel() == "básico":
                                            self.__lista_clientes[indice].set_nivel("medio")

                                        else:#cliente medio sube a nivel alto
                                            self.__lista_clientes[indice].set_nivel("alto")


                                case "3":
                                    #Modificar cliente corporativo solo descuento
                                    if not isinstance(self.__lista_clientes[indice], ClienteCorporativo):
                                        raise TypeError("Un cliente Regular o Premium no puede cambiar a Corporativo\n")

                                    #Modifica porcentaje
                                    self.__lista_clientes[indice].set_descuento()

                                case _:
                                    raise ValueError("Opción inválida. Intente otra vez.\n")

                        case _:
                            raise ValueError("Opción inválida.\n")

                    self.guardar_actividad("Modifición de datos a cliente.")
                    print("Campo modificado con éxito.\n")


            except TypeError as error:
                self.guardar_actividad("Conversión de datos no válida.")
                print(error)

            except ValueError as error:
                self.guardar_actividad("Fallo al modificar datos cliente.")
                print(error)

            finally:
                print("Redirigiendo...\n")


    def eliminar_cliente(self):
        print(f"\n{'-' * 24}")
        print(f"ELIMINAR CLIENTE")
        print(f"{'-' * 24}")

        if len(self.__lista_clientes) == 0:
            print(f"*** Sin datos ***\n")

        else:
            self.mostrar_clientes()

            #Selección cliente
            opcion = input("Ingrese el número del cliente a eliminar: ")

            #Validación selección
            try:
                if not opcion.replace(" ", "").isdigit():
                    raise ValueError("La opción solo puede ser un número.\n")
                elif int(opcion) > len(self.__lista_clientes):
                    raise ValueError("Opción inválida. Intente otra vez.\n")

                #Eliminación cliente seleccionado
                del self.__lista_clientes[int(opcion)-1]
                self.guardar_actividad("Eliminación de cliente.")

            except ValueError as error:
                self.guardar_actividad("Fallo al eliminar cliente.")
                print(error)

            finally:
                print("Redirigiendo...\n")


    def menu_principal(self):
        while True:
            #Menú
            print(f"BIENVENIDO A SC 1.0")
            print(f"¿Qué desea hacer?")
            print(f"{'-' * 24}")
            print(f"|{'(1) Agregar cliente': <22}|")
            print(f"|{'(2) Modificar cliente': <22}|")
            print(f"|{'(3) Eliminar cliente': <22}|")
            print(f"|{'(4) Mostrar clientes': <22}|")
            print(f"|{'(5) Salir': <22}|")
            print(f"{'-' * 24}")

            #Selección de opción
            opcion = input("Ingrese una opción entre 1 a 5: ")

            #Validación de opción
            try:
                match opcion:
                    case "1":
                        self.agregar_cliente()
                    case "2":
                        self.modificar_cliente()
                    case "3":
                        self.eliminar_cliente()
                    case "4":
                        self.mostrar_clientes()
                    case "5":
                        self.guardar_datos_clientes()
                        break
                    case _:
                        raise ValueError("Opción inválida. Intente otra vez.\n")
            except ValueError as error:
                print(error)

    def cargar_datos_clientes(self):
        self.guardar_actividad("Carga datos al sistema.")
        cliente = ""

        if not Path("clientes.csv").is_file():
            with open("clientes.csv", "x") as archivo:
                pass

        else:
            with open("clientes.csv", "r", newline="", encoding="utf-8") as archivo:
                lector = csv.reader(archivo, delimiter=";")

                for linea in lector:
                    #Es un cliente regular
                    if len(linea) == 6:
                        cliente = ClienteRegular(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5])

                    #Cliente premium y corporativo son 7 campos
                    elif len(linea) == 7:
                        #Es un cliente regular
                        if linea[6] in ("básico", "medio", "alto"):
                            cliente = ClientePremium(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5], linea[6])

                        #Es un cliente corporativo
                        else:
                            cliente = ClienteCorporativo(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5], linea[6])

                    if cliente != "":
                        self.__lista_clientes.append(cliente)
                        cliente = ""

    def guardar_datos_clientes(self):
        self.guardar_actividad("Guardado de datos del sistema.")
        with open("clientes.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            for cliente in self.__lista_clientes:
                if isinstance(cliente, ClienteRegular):
                    escritor.writerow((cliente.get_ide(), cliente.get_nombre(), cliente.get_email(), cliente.get_telefono(),
                                       cliente.get_direccion(), cliente.get_descuento()))
                elif isinstance(cliente, ClientePremium):
                    escritor.writerow(
                        (cliente.get_ide(), cliente.get_nombre(), cliente.get_email(), cliente.get_telefono(),
                         cliente.get_direccion(), cliente.get_descuento(), cliente.get_nivel()))

                else: #ClienteCorporativo
                    escritor.writerow(
                        (cliente.get_ide(), cliente.get_nombre(), cliente.get_email(), cliente.get_telefono(),
                         cliente.get_direccion(), cliente.get_descuento(), cliente.get_empresa()))

    @staticmethod
    def guardar_actividad(mensaje):
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open("actividad.log", "a", encoding="utf-8") as archivo:
            archivo.write(f"Fecha: {fecha} | Acción: {mensaje}\n")

sistema_clientes = SistemaClientes()
sistema_clientes.cargar_datos_clientes()
sistema_clientes.menu_principal()