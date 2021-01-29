from random import shuffle, choice
from Controller.Ficha import Ficha

class Bolsa():
    """
        Crea la bolsa de fichas que vamos a usar durante el juego. 
        Contiene por defecto 101 fichas.
    """
    def __init__(self, listaConfiguracion=''):
        '''Crea la bolsa con fichas'''
        self.bolsa = []
        self.crear_bolsa_de_fichas(listaConfiguracion)
    
    def agregar_a_bolsa(self, ficha, cant):
        '''Añade una cantidad de una ficha especifica a la bolsa.
        	'''
        for i in range(cant):
            self.bolsa.append(ficha)

    def crear_bolsa_de_fichas(self, listaConfiguracion):
        """Crea nuestra Bolsa de Fichas.
        Por cada letra del abecedario, más la Ñ, RR y LL, las agrega dependiendo del 
        valor y la cantidad en la configuración que estamos jugando"""

        from string import ascii_uppercase as up
        import random
        letras = list(up)
        letras.extend(["Ñ", "RR", "LL"])
        letras = sorted(letras)
        for each in letras:
            self.agregar_a_bolsa(Ficha(each, listaConfiguracion[each]['valor']), listaConfiguracion[each]['cant'])
        shuffle(self.bolsa)
        shuffle(self.bolsa)
    
    def sacar_letra(self):
        shuffle(self.bolsa)
        letra = self.bolsa.pop()
        return letra

    def fichas_restantes(self):
        return len(self.bolsa)

    def suficientes_fichas(self):
        return self.fichas_restantes() > 7