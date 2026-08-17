class Cliente:

    #Constructor
    def __init__(self, ide, nombre, email, telefono, direccion):
        if ide == "":
            raise ValueError("Id no puede estar vacío.")

        self.__ide = ide
        self.__nombre = self.validar_nombre(nombre)
        self.__email = self.validar_email(email)
        self.__telefono = self.validar_telefono(telefono)
        self.__direccion = self.validar_direccion(direccion)


    #Getters atributos
    def get_ide(self):
        return self.__ide

    def get_nombre(self):
        return self.__nombre

    def get_email(self):
        return self.__email

    def get_telefono(self):
        return self.__telefono

    def get_direccion(self):
        return self.__direccion


    #Setters atributos
    def set_nombre(self):
        nombre = input("Nombre: ")
        self.__nombre = self.validar_nombre(nombre)

    def set_email(self):
        email = input("Email: ")
        self.__email = self.validar_nombre(email)

    def set_telefono(self):
        telefono = input("Teléfono: ")
        self.__telefono = self.validar_telefono(telefono)

    def set_direccion(self):
        direccion = input("Dirección: ")
        self.__direccion = self.validar_direccion(direccion)

    @staticmethod
    def validar_nombre(nombre):
        if nombre == "":
            raise ValueError("Nombre no puede estár vacío.")
        return nombre

    @staticmethod
    def validar_email(email):
        if email == "" or "@" not in email:
            raise ValueError("Correo no tiene @ o está vacío.")
        return email

    @staticmethod
    def validar_telefono(telefono):
        if telefono == "":
            raise ValueError("Teléfono no puede estár vacío.")
        return telefono

    @staticmethod
    def validar_direccion(direccion):
        if direccion == "":
            raise ValueError("Dirección no puede estár vacío.")
        return direccion

    #Devuelve información del cliente
    def __str__(self):
        return f"{self.__ide:<11} | {self.__nombre:<21} | {self.__email:<30} | {self.__telefono:<13} | {self.__direccion:<25}"