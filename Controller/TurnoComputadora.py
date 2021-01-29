from Controller.Jugadas import Jugadas
import itertools as it
from random import choice, randrange
class TurnoComputadora(Jugadas):
    def __init__(self,*args, **kwargs):
        """Esta clase es la encargada de llevar a cabo con el turno de la máquina. """
        super(TurnoComputadora,self).__init__(*args, **kwargs)
    
    def agregar_a_palabra(self, ficha):
        """Agrega una Ficha a la palabra de la computadora"""
        self.palabra.append(ficha)
    
    def formar_lista_de_strings(self):
        """Esta función toma las fichas del atril de la computadora, las agrega a un set y luego permutando los caracteres forma todas las combinaciones posibles.
        Devuelve esos strings creados.
        """
        letras= ''
        for ficha in self.atril:
            if ficha.get_letra() != "RR" and ficha.get_letra() != "LL":
                letras += ficha.get_letra()
        strings = set()
        for i in range(2, len(letras) + 1):
            strings.update((map("".join, it.permutations(letras, i))))
        return strings

    def formar_palabras_validas(self, configuracion):
        """Esta funcion toma los strings creados en formar_lista_de_strings y se asegura de guardar en una lista solo las palabras válidas para lexicon y spelling. 
        Estas son las posibles palabras que la computadora puede jugar.
        Devuelve la lista creada.
        """
        lista_strings = self.formar_lista_de_strings()

        palabras_validas = []
        for pal in lista_strings:
            if "RR" not in pal and "LL" not in pal:
                self.palabrastr = pal
                if self.chequear_palabra(configuracion):
                    palabras_validas.append(self.palabrastr)
        return palabras_validas


    
    def ubicar_palabra(self, window):
        """Esta funcion se asegura de que en la ventana haya un lugar en el que puedan ubicarse las Fichas de la palabra de corrido.
        Elige una orientación al azar.
        Devuelve True si encontró el lugar, y False si no."""
        espacio_vacio= True
        letras_puestas = 0
        posiciones = []
        self.orientacion[0] = True
        self.orientacion[1] = choice([True, False]) #True= Horizontal, False= Vertical
        if self.orientacion[1] == True:
            if window[(7,7)].GetText() == '': #Si nadie puso una ficha y arraca la computadora
                x = 7
                y = 7
            else:
                x = randrange(14)
                if (x + len(self.palabrastr) >= 15):
                    x = x - len(self.palabrastr)
                y = randrange(14)
            while espacio_vacio and (letras_puestas < len(self.palabrastr)):
                if window[(x,y)].GetText() == '':
                    posiciones.append((x,y))
                else:
                    espacio_vacio = False
                x += 1
                letras_puestas += 1
            if espacio_vacio:
                self.palabra_posiciones = posiciones
                self.ocupadas_por_mi.extend(posiciones)
            return espacio_vacio
        else:
            if window[(7,7)].GetText() == '': #Si nadie puso una ficha y arraca la computadora
                x = 7
                y = 7
            else:
                y = randrange(14)
                if (y + len(self.palabrastr) >= 15):
                    y = y - len(self.palabrastr)
                x = randrange(14)
            while espacio_vacio and (letras_puestas<len(self.palabrastr)):
                if window[(x,y)].GetText() == '':
                    posiciones.append((x,y))
                else:
                    espacio_vacio = False
                y += 1
                letras_puestas += 1
            if espacio_vacio:
                self.palabra_posiciones = posiciones
                self.ocupadas_por_mi.extend(posiciones)
            return espacio_vacio
            

    def hacer_palabra(self, configuracion):
        """Esta funcion toma una lista de palabras validas para lexicon y spelling y en el nivel fácil,
         elige una al azar. En los niveles Medio y Dificil, elige la más larga para complicar un poco al jugador y sumar más puntos.
         
         Luego, toma las Fichas de nuestro atril y las pone en la lista que representa nuestra palabra (self.palabra).
         Busca una por una en el atril"""
        palabras = self.formar_palabras_validas(configuracion)
        if palabras:
            if configuracion["Nivel"] == "FACIL":
                self.palabrastr = choice(palabras)
            else:
                palabras.sort(key=lambda pal: len(pal), reverse=True)
                print(palabras)
                self.palabrastr = palabras[0]
               
            
            cant = 0
            while cant < len(self.palabrastr):
                encontre = False
                i = 0
                while i < len(self.atril) and not encontre:
                    if (self.atril[i] != '') and (self.atril[i].get_letra() == self.palabrastr[cant]):
                        self.agregar_a_palabra(self.atril[i])
                        self.atril[i] = ''
                        encontre = True
                    i += 1
                cant += 1
            return True