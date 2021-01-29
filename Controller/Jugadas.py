import PySimpleGUI as sg
from abc import ABC,abstractmethod
import os
from pattern3.text.es import spelling,lexicon, parse

class Jugadas(ABC):
    """Esta clase define las instancias que tiene cualquier turno. Sus clases hijas son TurnoJugador y TurnoComputadora.

    atril: lista con los objetos Ficha de nuestro "atril"
    palabra: lista con los objetos Ficha que forman nuestra palabra a jugar
    palabrastr: string. Acá ponemos nuestra palabra en formato string. Nos sirve para agregarla a la lista de palabras jugadas.
    palabra_posiciones: lista de tuplas que representa las posiciones en las que vamos a ubicar cada una de las Fichas de nuestra palabra
    puntos: int. Representa los puntos que vamos acumulando durante la partida.
    ocupadas_por_mi: lista de tuplas que representan posiciones del tablero. Nos sirve que cada jugador reconozca las posiciones que ha ocupado a la hora de posponer la partida/ cargar una partida vieja.
    orientacion: lista con dos valores booleanos. Si orientacion[0] = false, la orientacion todavía no fue definida. Si orientacion[1] = True, la orientacion definida es horizontal, si es False es vertical.
    
    """
    def __init__(self, bolsa):
        super()
        self.atril = self.inicializar_atril(bolsa)
        self.palabra = [] #FICHAS de la palabra actual
        self.palabrastr = ""
        self.palabra_posiciones = []
        self.puntos = 0
        self.ocupadas_por_mi= []
        self.orientacion= [False, False] # si orientacion[0] = false todavia no definida, = True definida. Si orientacion[1]=True, la orientacion definida es horizontal, si = False, vertical

    def inicializar_atril(self, bolsa):
        """Funcion que inicializa nuestro atril al inicio de la partida. Lo carga con 7 fichas de nuestra Bolsa."""
        atril = []
        for i in range(7):
            ficha = bolsa.sacar_letra()
            atril.append(ficha)  # lista donde estan los objetos de las Fichas
        return atril

    def cargar_atril(self, bolsa):
        """Función que repone nuestro atril. Lo recorre cada vez que terminamos una jugada, y por cada lugar sin Ficha, le agrega una de nuestra Bolsa"""
        if bolsa.suficientes_fichas(): 
            for i in range(7): 
                if self.atril[i] == '':
                    ficha = bolsa.sacar_letra()
                    self.atril[i] = ficha  # lista donde estan los objetos de las Fichas
            return True
        else:
            return False
    
    def limpiar_palabra(self):
        """Elimina todo lo que establecimos en la jugada con respecto a la palabra que chequeamos, para que podamos continuar con una nueva palabra."""
        del self.palabra[:] 
        self.palabrastr = ""
        del self.palabra_posiciones[:]
        self.orientacion= [False, False]

    def get_puntos(self):
        """Devuelve los puntos acumulados a lo largo de la partida"""
        return self.puntos
        
    def get_palabra(self):
        """Devuelve la lista de Fichas que forma nuestra palabra a jugar"""
        return self.palabra

    def get_palabrastr(self):
        """Devuelve el string que representa nuestra palabra a jugar"""
        return self.palabrastr

    def get_atril(self):
        """Devuelve el atril (lista de Fichas)"""
        return self.atril
    
    def get_palabra_posiciones(self):
        """Devuelve las posiciones en las que ubicaremos las Fichas de nuestra palabra"""
        return self.palabra_posiciones

    def get_ocupadas_por_mi(self):
        """Devuelve las posiciones que hemos ocupado a lo largo de nuestra partida. Solo las que ocupamos, no las de nuestro oponente"""
        return self.ocupadas_por_mi
        
    def chequear_palabra(self, configuracion):
        '''Funcion encargada de chequear que la palabra puesta esté en lexicon y spelling.
        Devuelve True si cumple con las condiciones.'''
        valida = False
        if "ñ" in self.palabrastr.lower() and self.palabrastr.lower() in lexicon:
            palabra = parse(self.palabrastr, tokenize=True, tags=True, chunks=False).replace(self.palabrastr, '')
            if palabra in configuracion['TipoDePalabra']:
                valida = True
        elif self.palabrastr.lower() in lexicon and self.palabrastr.lower() in spelling:
            palabra = parse(self.palabrastr, tokenize=True, tags=True, chunks=False).replace(self.palabrastr, '')
            if palabra in configuracion['TipoDePalabra']:
                valida = True
        return valida
    
    def calcular_puntaje(self, posiciones):
        '''Funcion encargada de calcular los puntos de la palabra teniendo en cuenta las posiciones del tablero en la que estan puestas sus fichas.
        Devuelve el total sumado.
        	'''
        largo = len(self.palabra)
        puntos = 0
        mult2 = 0
        mult3 = 0
        for i in range(largo):
            letra = self.palabra[i]
            pos = self.palabra_posiciones[i]
            if pos in posiciones["Letrax2"]:
                puntos += (letra.get_valor() * 2)
            elif pos in posiciones['Letrax3']:
                puntos += (letra.get_valor() * 3)
            elif pos in posiciones['Palabrax3']:
                puntos += letra.get_valor()
                mult3 += 1
            elif pos in posiciones['Palabrax2']:
                puntos += letra.get_valor()
                mult2 += 1
            elif pos in posiciones['Letra-1']:
                puntos += (letra.get_valor() - 1)
            else:
                puntos += letra.get_valor()
        if mult2 != 0:
            for i in range(mult2):
                puntos = puntos * 2
        if mult3 != 0:
            for i in range(mult3):
                puntos = puntos * 3
        self.puntos = self.puntos + puntos
        return puntos