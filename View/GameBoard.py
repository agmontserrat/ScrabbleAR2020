from Controller.Generic_Window import Generic_Window
import os
import pickle
from Model import funciones_juego
from random import shuffle, choice
from Controller.TurnoComputadora import TurnoComputadora
from Controller.TurnoJugador import TurnoJugador
from Controller.Bolsa import Bolsa
from Model.Generic_Manegement_Files import Generic_Manegement
from Model.funciones_juego import preparar_tablero

class Tablero(Generic_Window):
    """Este es el tablero del juego. Es una clase hija de Generic_Window. """
    def __init__(self,continuar = None, configuracion = Generic_Manegement.readJsonFile("configuracion"+os.sep+"FACIL.json"), *args, **kwargs):
        """
        Parametros:
            continuar: representa la partida que se pospuso en alguna partida anterior. Si no nos llega la partida, por defecto se toma que vale None.
            configuracion: la configuracion con la que estamos jugando. Si no recibimos nada, por defecto jugamos con la configuracion del nivel Fácil.

        Variables de instancia:
        partida: (si se carga) es el contenido del archivo que guardó la ultima partida que fue pospuesta.
        iniciar: valor booleano que vale True cuando la partida ha iniciado, y False si la partida no ha comenzado.
        time: El tiempo que nos queda para jugar la partida.
        timeTurno: El tiempo que tenemos de turno para jugar.
        bolsa: la Bolsa de Fichas necesaria para cargar los atriles.    
        jugador: instancia de TurnoJugador
        computadora: instancia de TurnoComputadora
        config: la configuracion del juego.
        posiciones: las posiciones especiales del tablero.
        lista_palabras_jugadas: lista que va a contener las palabras que hemos jugado a lo largo del juego junto con los valores del puntaje que sumó.
            """
        super(Tablero,self).__init__(*args, **kwargs)
        self.sg = self.get_sg()
        self.name_windows = "Gameboard"
        if continuar == None:
            self.iniciar = False
            self.time = configuracion["TiempoJuego"] * 60
            self.timeTurno = configuracion['TiempoTurno'] * 60
            self.timeTurno = configuracion['TiempoTurno'] * 60
            self.bolsa = Bolsa(configuracion)
            self.jugador = TurnoJugador(self.bolsa)
            self.computadora = TurnoComputadora(self.bolsa)
            self.config = configuracion 
            self.posiciones = self.configuracion_pero_con_tuplas(self.config["Posiciones"])
            self.lista_palabras_jugadas = [] 
        else:
            self.partida = continuar
            self.iniciar = True
            self.time = continuar["TiempoTurno"] * 60
            self.timeTurno = continuar['TiempoTurno'] * 60
            self.bolsa = continuar["Bolsa"]
            self.jugador = continuar["Jugador"]
            self.computadora = continuar ["Computadora"]
            self.config = continuar["Config"]
            self.posiciones = continuar["posiciones"]
            self.lista_palabras_jugadas = continuar["lista"]        
        

    def configuracion_pero_con_tuplas(self, config):
        """Este metodo esta hecho ya que necesitamos las posiciones convertidas en tuplas, y al guardarlas en un archivo Json las tenemos como listas. """
        posiciones =  {"Palabrax3": [],  "Letrax2": [],  "Palabrax2": [], "Letrax3":[], "Letra-1": []}
        for clave in config:
            for each in config[clave]:
                posiciones[clave].append(tuple(each))
        return posiciones

    def cargar_aspectos_partida(self):
        """Al cargar una partida que fue guardada, ubica todo lo que debe verse en el tablero."""
        preparar_tablero(self.windows, self.config, self.posiciones)
        for each in self.partida["fichas_en_tablero_Computadora"]:
            self.windows[each].Update(self.partida["fichas_en_tablero_Computadora"][each], image_filename= os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}compu.png'.format(self.partida["fichas_en_tablero_Computadora"][each]), 
                            image_size=(40, 40) )
        for each in self.partida["fichas_en_tablero_Jugador"]:
            self.windows[each].Update(self.partida["fichas_en_tablero_Jugador"][each], image_filename= os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.partida["fichas_en_tablero_Jugador"][each]), 
                            image_size=(40, 40) )
        self.windows['nombreTurno'].Update("JUGADOR")
        self.windows['cont_fichas'].Update(len(self.bolsa.fichas_restantes()))
        self.windows['INICIAR'].update(disabled=True)
        for i in ['Pasar', 'Chequear', 'Cambiar', 'Sacar']:
            self.windows[i].update(disabled = False)
        for i in range(7): 
            self.windows[i].update(self.jugador.get_atril()[i].get_letra(), image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_atril()[i].get_letra()),
                image_size=(40, 40), disabled=False)
        self.windows['PuntosComputadora'].update(self.computadora.get_puntos())
        self.windows['PuntosJugador'].update(self.jugador.get_puntos())
    
    
    def terminar_partida(self):
        """Función que se ejecuta al terminar una partida, ya sea porque se acabaron el tiempo o las fichas, o porque apretamos el botón "Terminar" 
        
        Nos muestra los puntajes finales y dependiendo de ellos, nos informa si ganamos, empatamos o perdimos.
        Si ganamos, nos da la opcion de guardar nuestro puntaje.
        Luego cierra el juego.
        """
        layout_fin_partida = [[self.sg.Text("Terminó el juego! \nTu puntaje: {}\nPuntaje Computadora: {}\n".format(self.jugador.get_puntos(), self.computadora.get_puntos()), font=(20))]]

        if (self.computadora.get_puntos() < self.jugador.get_puntos()):
            layout_fin_partida += [[self.sg.Image(os.getcwd()+os.sep+'Static'+os.sep+'images'+os.sep+'calaverita.png'), self.sg.Text('¡Ganaste!')]]
            layout_fin_partida += [[self.sg.Text('Querés guardar tu puntaje? Ingresá tu nombre')]]
            layout_fin_partida += [[self.sg.InputText()]]
            layout_fin_partida += [[self.sg.Submit(), self.sg.Cancel()]]
            window = self.sg.Window('Guardar Puntaje', layout_fin_partida)
            event, values = window.read()
            nombre_jugador = values[0]
            if event is 'Submit':
                Generic_Manegement.saveScores(nombre_jugador, self.jugador.get_puntos(), self.config['Nivel'])
            window.close()
        elif self.jugador.get_puntos() < self.computadora.get_puntos():
            layout_fin_partida += [[self.sg.Image(os.getcwd()+os.sep+'Static'+os.sep+'images'+os.sep+'calaverita.png'), self.sg.Text('¡Perdiste!', font= (30))]]
            layout_fin_partida += [[self.sg.Text('No pasa nada. La proxima vas a ganar! Seguí jugando.')]]
            window = self.sg.Window('Guardar Puntaje', layout_fin_partida)
            event, values = window.read()
            window.close()
        else:
            layout_fin_partida += [[self.sg.Text('¡No lo puedo creer! Fue un empate.')]]
            layout_fin_partida += [[self.sg.Text('Jugá de nuevo para ganarle esta vez.!')]]
            window = self.sg.Window('Guardar Puntaje', layout_fin_partida)
            event, values = window.read()
            window.close()
        self.stop_loop_main()

    def posponer_partida(self):
        juego = {
            "TiempoJuego": (self.time // 60),
            "TiempoTurno": int(self.timeTurno // 60),
            "Bolsa": self.bolsa,
            "Jugador": self.jugador,
            "Computadora": self.computadora,
            "Config": self.config,
            "posiciones": self.posiciones,
            "lista": self.lista_palabras_jugadas,
            "fichas_en_tablero_Computadora": {},
            "fichas_en_tablero_Jugador": {}
        }
        for each in self.jugador.get_ocupadas_por_mi():
            juego["fichas_en_tablero_Jugador"][tuple(each)] = self.windows[each].GetText()
        
        for each in self.computadora.get_ocupadas_por_mi():
          
            juego["fichas_en_tablero_Computadora"][tuple(each)] = self.windows[each].GetText()
        
       
        
        salir = self.sg.PopupOKCancel('Se guardará la partida. Querés continuar?')
        if salir == 'OK':
            if Generic_Manegement.saveLastGame(juego):
                self.sg.popup('Partida guardada con exito!')
            else:
                self.sg.popup('No se pudo guardar la partida.')
        self.stop_loop_main()
        
    def update_timer(self):
        if self.time > 0:
            self.windows.FindElement('tiempoPartida').Update("{:02d}:{:02d}".format(self.time//60,self.time%60))
            self.time-=1
        else:
            self.terminar_partida()
    
    def update_timer_turno(self):
        if self.timeTurno > 0 and self.jugador.get_turno_juego():
            self.windows.FindElement('tiempoTurno').Update("{:02d}:{:02d}".format(self.timeTurno//60,self.timeTurno%60))
            self.timeTurno-=1
        else:
            self.jugador.set_turno_juego(False)
            self.jugador.devolver_todas_las_letras(self.windows, self.posiciones)
            self.windows.FindElement('tiempoTurno').Update("{:02d}:{:02d}".format(0,0))
            self.timeTurno = self.config['TiempoTurno'] * 60
            self.windows['nombreTurno'].update('COMPUTADORA!  ')

    def initialize_timeout_window(self):
        self.timeout = 1000

    def cambiar_fichas_window(self):
        """Esta es la ventana del cambio de fichas. Podes clickear sobre las que queres cambiar y 
        apretar "listo", o podes cambiarlas todas con la opcion "cambiar las 7" """

        columna = [[self.sg.Text("Clickeá sobre las fichas que querés intercambiar")]]
        columna +=[[self.get_button(self.jugador.get_atril()[i].get_letra(), (4, 2), i, button_color=('black', '#F0803C')) for i in range(7)]]
        columna +=[[self.get_button("Cambiar las 7", (12,1), 'todas'), self.get_button("Listo",(12,1)), self.get_button('Cancelar',(12,1))]]
        layout_fichas = [[self.sg.Column(columna, element_justification='c')]]
        windowFichas = self.sg.Window("Cambio de fichas", layout_fichas)
        
        a_cambiar = []
        while True:
            event, values = windowFichas.read()
            if event is 'Cancelar' or event is None:
                windowFichas.close()
                return False
            elif event is 'todas' and not a_cambiar:
                if self.bolsa.fichas_restantes() >= 7:
                    for i in range(7):
                        nueva_letra = self.bolsa.sacar_letra()
                        self.bolsa.agregar_a_bolsa(self.jugador.get_atril()[i], 1)
                        self.jugador.get_atril()[i] = nueva_letra
                        self.windows[i].update(self.jugador.get_atril()[i].get_letra(), image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_atril()[i].get_letra()), image_size=(40, 40))
                    windowFichas.close()
                    self.windows['corazon{}'.format(self.jugador.get_cambios() + 1)].Update(image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'corazonvacio.png', image_size=(42, 42))
                    return True
            elif event in range(7):
                if event not in a_cambiar:
                    a_cambiar.append(event)
                    windowFichas[event].update(button_color=('black', '#abbf42'))
                else:
                    windowFichas[event].update(button_color=('black', '#F0803C'))
                    a_cambiar.remove(event)
            elif event is "Listo":
                for each in a_cambiar:
                    nueva_letra = self.bolsa.sacar_letra()
                    self.bolsa.agregar_a_bolsa(self.jugador.get_atril()[each], 1)
                    self.jugador.get_atril()[each] = nueva_letra
                    self.windows[each].update(self.jugador.get_atril()[each].get_letra(),
                                        image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_atril()[each].get_letra()),
                                        image_size=(40, 40))
                    self.windows['corazon{}'.format(self.jugador.get_cambios() + 1)].Update(image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'corazonvacio.png', image_size=(42, 42))
                self.sg.popup('Listo! Las cambiaste con exito.\nEste fue tu cambio número {}'.format(self.jugador.get_cambios() + 1))
                windowFichas.close()
                return True
    
    def actualizar_lista(self, palabra, puntos):
        datos_pal = ['{}: {} puntos'.format(palabra, puntos)]
        self.lista_palabras_jugadas.append(datos_pal)
        self.windows['lista_puntos'].Update(self.lista_palabras_jugadas)

    def initialize_layout(self):
        tablero_juego = [
            [self.get_button('', (4,2), (i, j), button_color=('black', '#ebebeb')) for j in range(self.config['FilasColumnas'])] for i
            in range(self.config['FilasColumnas'])]  # MATRIZ TABLERO
    
        atril_compu = [self.get_button('?', (4, 2), i, button_color=('black', '#8CB336'), disabled=True) for i in range(7, 14)]
        mi_atril = [self.get_button('', (4, 2), j, disabled=True) for j in range(7)]
        
        botones_turno = [
                [self.get_button('Chequear', (12, 1), disabled=True), 
                self.get_button('Cambiar', (12, 1), disabled=True), 
                self.get_button('Quitar fichas', (12, 1), 'Sacar', disabled=True)]
            ]
        columna3 = [atril_compu] + [[self.sg.Text('Fichas de la compu',font=(20))]]
        columna3 += [[self.sg.Image(os.getcwd()+'/Static/images/puntoscompu.png', key='imagenpuntosc'), self.sg.Text('---', key='PuntosComputadora', font=(20), size=(10, 1))]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('TURNO', size=(10, 1), font=(20))], [self.sg.Text('-------------------', key='nombreTurno')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Text('')]]
        columna3 += [[self.sg.Image(os.getcwd()+'/Static/images/puntosjugador3.png', key='imagenpuntos'), self.sg.Text('---', key='PuntosJugador', font=(20), size=(10, 1))]]
        columna3 += [
            [self.sg.Image(os.getcwd()+'/Static/images/cambiarfichas.png', key='cambiarfichas'),
            self.get_image_button('', 'corazon3', 'corazon.png', (42,42), button_color=("black", "#702632")),
            self.get_image_button('', 'corazon2', 'corazon.png', (42,42), button_color=("black", "#702632")),
            self.get_image_button('', 'corazon1', 'corazon.png', (42,42), button_color=("black", "#702632"))
            ]#os.getcwd()+'/Static/images/corazon.png'
        ]
        columna3 += [[self.sg.Text('Fichas del jugador', font=(20))]] + [mi_atril]
        columna3 += botones_turno

        columna2 = [x for x in tablero_juego]

        columna1 = [
            [self.sg.Text('')],
            [self.sg.Text("Fichas restantes: {}".format('000'), key='cont_fichas', font=(20))],
            [self.sg.Text("Nivel - {}".format(self.config['Nivel']), key='nivel', font=(20))],
            [self.sg.Text('Categoria de palabras:\n{}'.format(self.config['Palabras']), key='pal', font=(20))],
            [self.sg.Text('Tiempo: ', size=(15, 1),font=(20)), self.sg.Text(key='tiempoPartida', size=(7, 1),font=(20))],
            [self.sg.Text('Tiempo Turno', size=(15, 1),font=(20)), self.sg.Text(key='tiempoTurno', size=(7, 1), font=(20))],
            [self.sg.Text('')],
            [self.sg.Text("Palabras jugadas: ", font=(20))],
            [self.sg.Listbox(self.lista_palabras_jugadas, size=(26, 11), key='lista_puntos', pad=(0.5, 0.5))],
            [self.get_button('INICIAR', (28, 1) )],
            [self.get_button('Pasar Turno', (28, 1), 'Pasar', disabled=True)],
            [self.get_button('Salir', (28, 1))],
            [self.get_button("TERMINAR", (14, 1)), self.get_button("POSPONER", (13, 1))]
        ]

        frame_layout = [[self.sg.Frame('Datos del juego', columna1, font='Any 12', title_color='#FFF2EB')]]

        layout = [
            [self.sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
            [self.sg.Column(frame_layout, element_justification='l'), 
            self.sg.Column(columna2, element_justification='c'),
            self.sg.Column(columna3, element_justification='l')]]

        if self.iniciar:
            self.cargar_aspectos_partida()

        return layout
    
    def content(self):
        if self.event == 'Salir':
            self.sg.Popup("Estas seguro/a de que querés salir?")
            self.stop_loop_main()
        


        if self.event is "INICIAR":
            self.iniciar = True
            self.windows['INICIAR'].update(disabled=True)
            for i in ['Pasar', 'Chequear', 'Cambiar', 'Sacar']:
                self.windows[i].update(disabled = False)
            for i in range(7): 
                self.windows[i].update(self.jugador.get_atril()[i].get_letra(), image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_atril()[i].get_letra()),
                                 image_size=(40, 40), disabled=False)
            self.windows["cont_fichas"].update("Fichas restantes: {}".format(self.bolsa.fichas_restantes()))
            self.jugador.set_turno_juego(choice([True, False]))
            preparar_tablero(self.windows, self.config, self.posiciones)
          

        """"determina si se inicia la instancia del juego"""  
        if self.iniciar:
            evento = self.event
            self.update_timer()
            self.update_timer_turno()


            if self.jugador.get_turno_juego():
    
                if self.event in range(7): 
                    if not self.jugador.get_letra_seleccionada(): #apretaste un boton del atril 
                        self.jugador.seleccione_una_letra(self.event) 
                        path = os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}compu.png'.format(self.jugador.get_letra_actual().get_letra())
                        self.windows.FindElement(evento).Update('', image_filename=path, 
                                         image_size=(40, 40))  # COLOR SELECCIONADA 
                    
                    elif self.jugador.get_letra_seleccionada() and self.windows[self.event].GetText() == '':
                        self.jugador.devuelvo_una_letra(self.event)
                        self.windows[evento].update(self.jugador.get_letra_actual().get_letra(),
                                            image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                            image_size=(40, 40))  # COLOR SIN SELECCIONAR
               
                
                elif type(self.event) == tuple:
                    if self.jugador.get_letra_seleccionada(): #Si tenemos una letra seleccionada y la queremos poner en el tablero

                        if len(self.jugador.get_ocupadas()) < 1 and self.event != (7,7): #Si es la primera de la partida
                            self.sg.popup('Tenes que empezar en el centro del tablero!')

                        elif len(self.jugador.get_palabra()) < 1: #Si es mi primer letra. Ahí es cuando deshabilito el boton Cambiar.
                            self.windows[self.event].Update(self.jugador.get_letra_actual().get_letra(),
                                                        image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                        image_size=(40, 40))
                            self.windows['Cambiar'].Update(disabled=True)
                            self.jugador.set_nueva_ocupada(self.event)
                            self.jugador.agregar_a_palabra()
                            self.jugador.cambiar_letra_seleccionada()
                            self.windows[self.jugador.get_letra()].Update(disabled=True,
                                                image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                image_size=(40, 40))
                        else:
                            if self.event in (self.jugador.get_ocupadas()):
                                self.sg.Popup('Acá no podés :(')  
                                self.windows[self.jugador.get_letra()].Update(self.jugador.get_letra_actual().get_letra(), disabled=False,
                                                    image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                    image_size=(40, 40))
                                self.jugador.devuelvo_una_letra(self.jugador.get_letra())
                            else:
                                if self.jugador.validar_posicion(self.event):
                                    self.windows[self.event].Update(self.jugador.get_letra_actual().get_letra(),
                                                        image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                        image_size=(40, 40)) # Me posiciono y escribo la letra
                                    self.windows[self.jugador.get_letra()].Update(disabled=True,
                                                image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                image_size=(40, 40))
                                    self.jugador.set_nueva_ocupada(self.event)
                                    self.jugador.agregar_a_palabra()
                                    self.jugador.cambiar_letra_seleccionada()
                                else:
                                    self.jugador.devuelvo_una_letra(self.jugador.get_letra())
                                    self.windows[self.jugador.get_letra()].Update(self.jugador.get_letra_actual().get_letra(), disabled=False,
                                                        image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_letra_actual().get_letra()),
                                                        image_size=(40, 40))
                                    


                elif self.event in ['Chequear', 'Cambiar', 'Pasar', 'Sacar']:
                    if self.event is 'Chequear':
                        if (len(self.jugador.get_palabra()) > 1):
                            self.jugador.armar_palabra_str()
                            if self.jugador.chequear_palabra(self.config):
                                self.sg.Popup('Bien! Es válida :)')
                                self.actualizar_lista(self.jugador.get_palabrastr(), self.jugador.calcular_puntaje(self.posiciones))
                                self.windows['PuntosJugador'].update(self.jugador.get_puntos())
                                if not (self.jugador.cargar_atril(self.bolsa)):
                                    self.sg.popup("No quedan más fichas en la bolsa de fichas!\nNo podemos continuar jugando :(")
                                    self.terminar_partida()
                                for i in range(7): 
                                    self.windows[i].update(self.jugador.get_atril()[i].get_letra(), image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}.png'.format(self.jugador.get_atril()[i].get_letra()),
                                    image_size=(40, 40), disabled=False)
                                self.jugador.limpiar_palabra()
                                self.jugador.set_turno_juego(False)
                            else:
                                self.sg.Popup('La palabra no es valida! :(')
                                self.jugador.devolver_todas_las_letras(self.windows, self.posiciones)
                            self.windows['Cambiar'].Update(disabled=False)
                        elif len(self.jugador.get_palabra()) == 1:
                            self.sg.Popup('La palabra debe tener mas de una letra!')


                    if self.event is 'Pasar':
                        seguro = self.sg.popup_yes_no('Estas seguro de que querés pasar el turno?')
                        if seguro == 'Yes':
                            self.jugador.set_turno_juego(False)
                            self.update_timer_turno()


                    if self.event is 'Cambiar':
                        if self.jugador.get_cambios()  < 3:
                            self.cambiar_fichas_window()
                            self.jugador.incrementar_cambios()
                            self.jugador.set_turno_juego(False)
                            self.update_timer_turno()
                        else:
                            self.sg.popup('Lamentablemente solo podes hacer 3 cambios de fichas :(')
                    
                    if self.event is 'Sacar':
                        self.jugador.devolver_todas_las_letras(self.windows, self.posiciones)
                
                elif self.event in ['TERMINAR','POSPONER']:
                    if self.event is 'TERMINAR':
                        terminar = self.sg.popup_ok_cancel('Estás por terminar la partida!')
                        if terminar is 'OK':
                            self.terminar_partida()
                    elif self.event is 'POSPONER':
                        self.posponer_partida()

            if self.jugador.get_turno_juego() == False: 
                if self.computadora.hacer_palabra(self.config):
                    while not (self.computadora.ubicar_palabra(self.windows)):
                        self.computadora.ubicar_palabra(self.windows)

                    if (self.computadora.get_palabra()) and (self.computadora.get_palabra_posiciones()):
                        for i in range(0, len(self.computadora.get_palabra_posiciones())):
                            self.computadora.get_palabra()[i].get_letra()
                            self.windows.FindElement(self.computadora.get_palabra_posiciones()[i]).Update(self.computadora.get_palabra()[i].get_letra(), 
                                image_filename= os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'{}compu.png'.format(self.computadora.get_palabra()[i].get_letra()), 
                                image_size=(40, 40))
                        self.jugador.agregar_a_ocupadas(self.computadora.get_palabra_posiciones())
                        self.actualizar_lista(self.computadora.get_palabrastr(), self.computadora.calcular_puntaje(self.posiciones))
                        if not (self.computadora.cargar_atril(self.bolsa)):
                            self.sg.popup("No quedan más fichas en la bolsa de fichas!\nNo podemos continuar jugando :(")
                            self.terminar_partida()
                        self.windows.FindElement('PuntosComputadora').Update(self.computadora.get_puntos())
                        self.windows.FindElement('cont_fichas').Update(value="Fichas restantes: {}".format(self.bolsa.fichas_restantes()))
                        self.computadora.limpiar_palabra()
                        self.jugador.set_turno_juego(True)
                else:
                    self.sg.popup_ok('La compu no puede formar una palabra. No quiere jugar más.')  
                    self.terminar_partida()          
            
        
        
