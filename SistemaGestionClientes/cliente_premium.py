from cliente import Cliente

class ClientePremium(Cliente):

    #Constructor
    def __init__(self, ide, nombre, email, telefono, direccion, descuento, nivel):
        super().__init__(ide, nombre, email, telefono, direccion)

        #Descuento depende del nivel en porcentaje: básico-> 10, medio-> 13, alto-> 16
        if nivel in ("básico", "medio", "alto"):
            self.__nivel = nivel
            match nivel:
                case "básico":
                    if descuento != "10":
                        raise ValueError("Valor no válido en descuento premium básico.")
                case "medio":
                    if descuento != "13":
                        raise ValueError("Valor no válido en descuento premium medio.")
                case "alto":
                    if descuento != "16":
                        raise ValueError("Valor no válido en descuento premium alto.")


            self.__descuento = descuento

        else:
            raise ValueError("Nivel no válido")


    def __str__(self):
        return f"{super().__str__()} | {self.__descuento:<10} | {self.__nivel:<7} | {"":<15}|"

    def get_nivel(self):
        return self.__nivel

    def get_descuento(self):
        return self.__descuento

    def set_nivel(self, nivel):
        if nivel == "medio":
            self.__nivel = nivel
            self.__descuento = "13"

        elif nivel == "alto":
            self.__nivel = nivel
            self.__descuento = "16"

        else:
            raise ValueError("Nivel no válido")