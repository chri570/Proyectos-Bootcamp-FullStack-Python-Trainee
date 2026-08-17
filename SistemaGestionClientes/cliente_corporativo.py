from cliente import Cliente

class ClienteCorporativo(Cliente):

    #Constructor
    def __init__(self, ide, nombre, email, telefono, direccion, descuento, empresa):
        super().__init__(ide, nombre, email, telefono, direccion)
        #Descuento sujeto a la empresa
        self.__descuento = self.validar_descuento(descuento)

        if empresa == "":
            raise ValueError("El nombre de la empresa no puede estar vacío.\n")

        self.__empresa = empresa

    def __str__(self):
        return f"{super().__str__()} | {self.__descuento:<10} | {"":<7} | {self.__empresa:<15}|"

    def set_descuento(self):
        descuento = input("Descuento nuevo: ")
        self.__descuento = self.validar_descuento(descuento)

    def get_descuento(self):
        return self.__descuento

    def get_empresa(self):
        return self.__empresa

    @staticmethod
    def validar_descuento(descuento):
        if descuento == "" or not descuento.isdigit():
            raise ValueError("Descuento no puede estar vacío y solo puede contener dígitos.\n")
        return descuento