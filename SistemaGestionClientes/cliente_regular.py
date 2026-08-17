from cliente import Cliente

class ClienteRegular(Cliente):

    #Constructor
    def __init__(self, ide, nombre, email, telefono, direccion, descuento):
        super().__init__(ide, nombre, email, telefono, direccion)

        self.__descuento = self.validar_descuento(descuento)


    def __str__(self):
        return f"{super().__str__()} | {self.__descuento:<10} | {"":<7} | {"":<15}|"

    def set_descuento(self):
        descuento = input("Descuento nuevo: ")
        self.__descuento = self.validar_descuento(descuento)

    def get_descuento(self):
        return self.__descuento

    @staticmethod
    def validar_descuento(descuento):
        if descuento == "" or not descuento.isdigit():
            raise ValueError("Descuento no puede estar vacío y solo puede contener dígitos.")

        if 5 <= int(descuento) <= 8:
            return descuento

        else:
            raise ValueError("Descuento solo puede ser entre 5% a 8%.")
