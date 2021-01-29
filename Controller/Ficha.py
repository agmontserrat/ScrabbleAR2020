import PySimpleGUI as sg

class Ficha():
    """
       Clase que crea una ficha. Se inicializa con una letra mayúscula y un integer que representa
       su valor.
    """

    def __init__(self, letra, valor):
        self.letra = letra.upper()
        self.valor = valor

    def get_letra(self):
        # Devuelve la letra de la ficha.
        return self.letra

    def get_valor(self):
        # Devuelve el valor de la letra.
        return self.valor
