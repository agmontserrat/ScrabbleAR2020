from Controller.Jugadas import Jugadas
import PySimpleGUI as sg
import os
from Model.funciones_juego import pos_en_tablero
class TurnoJugador(Jugadas):
    """Esta clase es la encargada de llevar a cabo el turno del Jugador.
    
    ocupadas: lista de tuplas que representan posiciones. Son todas las casillas que han sido ocupadas ya sea por el Jugador o por la Computadora.
    letra_seleccionada: valor booleano que indica si hemos seleccionado una letra de nuestro atril o no.
    letra: int que indica el numero de Ficha del atril que se ha seleccionado.
    letra_actual: Ficha del atril que se ha selecionado.
    turno_de_jugar: valor booleano que indica si al jugador le corresponde jugar o no.
    cambios: int. cantidad de cambios de fichas que se han realizado a lo largo del juego.
    
    """
    def __init__(self,*args, **kwargs):
        super(TurnoJugador,self).__init__(*args, **kwargs)
        self.ocupadas = []
        self.letra_seleccionada= False
        self.letra = ''
        self.letra_actual = ''
        self.turno_de_jugar = None
        self.cambios=0
    
    def incrementar_cambios(self):
        """Esta funcion se ejecuta luego de hacer un cambio de fichas. Incrementa en uno la cantidad de veces que se ha hecho."""
        self.cambios = self.cambios + 1

    def get_cambios(self):
        return self.cambios

    def set_turno_juego(self, value):
        """Esta funcion recibe un valor (True, o False) que indica si el Jugador tiene el turno o no. """
        self.turno_de_jugar = value

    def cambiar_letra_seleccionada(self):
        "Cambia el estado de letra_seleccionada."
        self.letra_seleccionada = not self.letra_seleccionada 
    
    def get_letra_seleccionada(self):
        return self.letra_seleccionada

    def get_letra_actual(self):
        return self.letra_actual
    
    def get_letra(self):
        return self.letra

    def get_atril(self):
        return self.atril

    def get_turno_juego(self):
        return self.turno_de_jugar

    def get_palabrastr(self):
        return self.palabrastr
    
    def get_ocupadas(self):
        return self.ocupadas

    def agregar_a_palabra(self):
        self.palabra.append(self.letra_actual)

    def seleccione_una_letra(self, event):
        """Funcion que se ejecuta cuando seleccionamos una letra de nuestro atril. Cambia el estado de letra_seleccionada a True, y guarda en letra el numero del evento (posicion del atril que fue clickeada),
        en letra_actual la Ficha (objeto) que está en esa posicion del atril, y quita la Ficha del atril."""
        self.cambiar_letra_seleccionada()
        self.letra = event
        self.letra_actual = self.atril[event]
        self.atril[event] = ''  #saco la letra que seleccioné 
    
    def devuelvo_una_letra(self, event):
        """Función que se ejecuta cuando seleccionamos una letra de nuestro atril, pero luego la queremos devolver clickeando nuevamente en ella
        Cambia el estado de letra seleccionada y devuelve al atril la Ficha"""
        self.cambiar_letra_seleccionada()
        self.atril[event] = self.letra_actual

    def armar_palabra_str(self):
        '''
        Usa las Fichas de la palabra y forma el string 
        '''
        pal = []
        for each in self.palabra:
            pal.append(each.get_letra())
        self.palabrastr = ''.join(pal)
    
    def agregar_a_ocupadas(self, posiciones):
        self.ocupadas.extend(posiciones)

    def set_nueva_ocupada(self, posicion):
        """Acá guardamos la nueva casilla que hemos ocupado en todas las listas que necesiten guardar esa información"""
        self.ocupadas.append(posicion)
        self.ocupadas_por_mi.append(posicion)
        self.palabra_posiciones.append(posicion)

    def devolver_todas_las_letras(self, window, posiciones):
        """
        Con las fichas de la palabra no valida, borra las del tablero y las devuelve al atril
        """
        pos = 0
        largo = len(self.palabra)
        for i in range(largo):
            ultima_pos = self.ocupadas.pop()
            self.ocupadas_por_mi.pop()
            pos_en_tablero(ultima_pos, posiciones, window)
            window[ultima_pos].Update('')
            letra = self.palabra.pop()
            sigo = True
            while sigo and pos < 7:
                if window[pos].GetText() == '':
                    window[pos].Update(letra.get_letra(), 
                    image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(letra.get_letra()),
                    image_size=(40, 40), disabled=False)
                    
                    self.atril[pos] = letra
                    sigo = False
                pos = pos + 1
        self.limpiar_palabra()
        self.orientacion = [False, False]
        window['Cambiar'].Update(disabled=False)


    def validar_posicion(self,event):
        '''
        Funcion encargada de chequear que las letras se esten poniendo en la direccion correcta
    	'''
        x, y = self.ocupadas[len(self.ocupadas) - 1]
        if self.orientacion[0]:  # Si la orientacion ya fue definida
            if (event in self.ocupadas):
                return False
            if (self.orientacion[1]):  # Si la orientacion definida es horizontal
                if (event[0] == x and event[1] == y + 1):
                    return True
                else:
                    sg.Popup('Colocar letras horizontalmente de izquierda a derecha')
                    return False
            else:  # Si la orientacion definida es vertical
                if (event[0] == x + 1 and event[1] == y):
                    return True
                else:
                    sg.Popup('Colocar letras verticalmente de arriba a abajo')
                    return False
        else:  # Si la orientacion no fue definida aun
            if (event[0] == x and event[1] == y + 1):  # Si la segunda letra en colocar esta de forma consecutiva y horizontal
                self.orientacion[1] = True
                self.orientacion[0] = True
                return True
            elif (event[0] == x + 1 and event[1] == y):  # Si la segunda letra en colocar esta de forma vertical, consecutiva y descendentemente
                self.orientacion[1] = False
                self.orientacion[0] = True
                return True
            else:  # Si nada de esto pasa, la posicion a la que intenta acceder no es valida
                sg.Popup('Solo se pueden colocar letras de forma consecutiva (horizontal de izquierda a derecha o vertical descendentemente)')
                return False
        print('Posiciones Ocupadas', self.ocupadas)
        print('Ultimos valores', x, y)


