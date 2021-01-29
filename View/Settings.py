from Controller.Generic_Window import Generic_Window
from Model.Generic_Manegement_Files import Generic_Manegement
from View.GameBoard import Tablero
import os
from string import ascii_uppercase as up
from random import choice

letras = list(up)
letras.extend(["Ñ", "RR", "LL"])
letras = sorted(letras)

tipos = {'Adjetivos': ["/AO", "/JJ", "/AQ", "/DI", "/DT"],
        'Sustantivos':["/NC", "/NCS","/NCP", "/NNS", "/NP", "/NN", "/NNP","/W"],
        'Verbos': ["/VAG", "/VBG", "/VAN", "/MD", "/VAS", "/VMG", "/VMI", "/VB", "/VMM", "/VMN",
        "/VMP", "/VBN", "/VMS", "/VSG", "/VSI", "/VSN", "/VSP","/VSS" ]}


class Configuracion(Generic_Window):
    """This is the gameboard of the proyect(game). First view of the system show the """
    def __init__(self,*args, **kwargs):
        super(Configuracion,self).__init__(*args, **kwargs)
        self.sg = self.get_sg()
        self.name_windows = "Settings"
        self.letras = letras
        self.configuraciones = self.configuraciones_predeterminadas()
        self.config = {"A": {'valor': 1, 'cant': 11},
                 "B": {"valor": 3, 'cant': 3},
                 "C": {"valor": 2, 'cant': 4},
                 "D": {"valor": 2, 'cant': 4},
                 "E": {"valor": 1, 'cant': 11},
                 "F": {"valor": 4, 'cant': 2},
                 "G": {"valor": 2, 'cant': 2},
                 "H": {"valor": 4, 'cant': 2},
                 "I": {"valor": 1, 'cant': 6},
                 "J": {"valor": 6, 'cant': 2},
                 "K": {"valor": 8, 'cant': 1},
                 "L": {"valor": 1, 'cant': 4},
                 "LL": {"valor": 8, 'cant': 1},
                 "M": {"valor": 3, 'cant': 3},
                 "N": {"valor": 1, 'cant': 5},
                 "Ñ": {"valor": 8, 'cant': 1},
                 "O": {"valor": 1, 'cant': 8},
                 "P": {"valor": 3, 'cant': 2},
                 "Q": {"valor": 8, 'cant': 1},
                 "R": {"valor": 1, 'cant': 4},
                 "RR": {"valor": 8, 'cant': 1},
                 "S": {"valor": 1, 'cant': 7},
                 "T": {"valor": 1, 'cant': 4},
                 "U": {"valor": 1, 'cant': 6},
                 "V": {"valor": 4, 'cant': 2},
                 "W": {"valor": 8, 'cant': 1},
                 "X": {"valor": 8, 'cant': 1},
                 "Y": {"valor": 4, 'cant': 1},
                 "Z": {"valor": 10, 'cant': 1},
                 "Posiciones" : { 'Palabrax3': [(0, 0), (1, 1), (0, 14), (1, 13), (14, 14), (13, 13), (14, 0), (13, 1), (9, 5), (9, 9), (5, 9),
                                               (5, 5)],
                                'Letrax2': [(2, 12), (3, 11), (4, 10), (6, 8), (8, 6), (10, 4), (11, 3), (12, 2), (2, 2), (3, 3), (4, 4), (6, 6),(8, 8), (10, 10), (11, 11), (12, 12)],
                                'Palabrax2': [(0, 10), (0, 4), (7, 14), (7, 0), (14, 10), (14, 4)],
                                'Letrax3': [(3, 7), (11, 7), (7, 11), (7, 3)],
                                'Letra-1':  [(2, 5), (2, 9), (5, 12), (9, 12), (12, 9), (12, 5), (9, 2), (5, 2)]
                },
                 'Nivel': 'FACIL',
                 'TipoDePalabra':  [],
                 'Palabras': '',
                 'TiempoTurno': 4,
                 'TiempoJuego': 40,
                 'FilasColumnas': 15
    
                 }

    def initialize_layout(self):
        columna_fichas_1 = [
            [self.get_button(self.letras[j], (3, 1)),
             self.sg.Spin([i for i in range(1, 101)], initial_value=1, key='valor' + self.letras[j], size=(2, 1)),
             self.sg.Spin([i for i in range(5, 101)], initial_value=11, key='cant' + self.letras[j], size=(2, 1))] for j in
            range(0, 10)
        ]
        columna_fichas_2 = [
            [self.get_button(self.letras[j], (3, 1)),
             self.sg.Spin([i for i in range(1, 101)], initial_value=1, key='valor' + self.letras[j], size=(2, 1)),
             self.sg.Spin([i for i in range(5, 101)], initial_value=11, key='cant' + self.letras[j], size=(2, 1))]for j in
            range(10, 20)
        ]
        columna_fichas_3 = [
            [self.get_button(self.letras[j], (3, 1)),
             self.sg.Spin([i for i in range(1, 101)], initial_value=1, key='valor' + self.letras[j], size=(2, 1)),
             self.sg.Spin([i for i in range(5, 101)], initial_value=11, key='cant' + self.letras[j], size=(2, 1))] for j in
            range(20, 29)
        ]
        botones_fichas = [
            self.sg.Column(columna_fichas_1), self.sg.Column(columna_fichas_2), self.sg.Column(columna_fichas_3)
        ]
        layout = [
            [self.sg.Image(os.getcwd()+os.sep+'Static'+os.sep+'images'+os.sep+'configuracion.png')],
            [self.sg.Text('Seleccioná tu nivel!', font=(20), justification='center')],
            [self.get_button('FACIL', (12, 1)),
             self.get_button('MEDIO', (12, 1)),
             self.get_button('DIFICIL',(12, 1))],
            [self.sg.Text('¡Podes personalizar los valores predeterminados del nivel!', font=(14))],
            [self.sg.Text('TIEMPOS', )],
            [self.sg.Text('  Tiempo partida: ',tooltip='Maximo = 60 minutos'), self.sg.Combo(values=(10, 20, 40), key='tiempo_juego', tooltip='Maximo = 60 minutos'), self.sg.Text('minutos')],
            [self.sg.Text('  Tiempo turno: ',tooltip='Maximo = 10 minutos'), self.sg.Combo(values=(1, 2, 4), key='tiempo_turno', tooltip='Maximo = 10 minutos'), self.sg.Text('minutos')],
            [self.sg.Text('    ', )],
            [self.sg.Text('FICHAS (valor - cantidad)')],
             botones_fichas,
            [self.sg.Text('    ', )],
            [self.get_button('Aplicar y jugar!', (12,1), 'listo', disabled=True, ), self.get_button('Cancelar', (12,1)), self.sg.Checkbox('My first Checkbox!', key='tema_inclusivo', default=False)]
        ]
        return layout

    def initialize_timeout_window(self):
        pass
    def validar_parametros(self, valor, tipomax):
        """
        Funcion que controla que nuestro valor sea válido (que no esté vacío, que no sea una letra, que no se salga del rango maximo).

        El valor máximo para las letras (tanto valor como cantidad) es 100.
        El valor maximo para una partida es de 60 (minutos).
        El valor máximo para un turno de una partida es de 10 (minutos)
        """
        valida = False
        try:
            if valor != "":
                if (tipomax > int(valor) > 0):
                    valida = True
            return valida
        except (ValueError):
            return valida


    def configuraciones_predeterminadas(self):
        configuracion = {}
        for each in ['FACIL', 'MEDIO', 'DIFICIL']:
            configuracion[each] = Generic_Manegement.readJsonFile("configuracion"+os.sep+"{}.json".format(each))
        return configuracion
            
    
    def content(self):
        print (self.value)
        if self.event == 'Cancelar':
            self.stop_loop_main()
        elif self.event is 'listo':
            huboError = False
            for i in letras:                                            #REVISIÓN DE QUETODO LO INGRESADO SEA VÁLIDO.
                if self.validar_parametros(self.value['valor' + i], 100):
                    self.config[i]['valor'] = int(self.value['valor' + i])
                else: huboError = True
                if self.validar_parametros(self.value['cant' + i], 100):
                    self.config[i]['cant'] = int(self.value['cant' + i])
                else: huboError= True
            if self.validar_parametros(self.value['tiempo_turno'], 10):
                self.config['TiempoTurno'] = int(self.value['tiempo_turno'])
            else: huboError=True
            if self.validar_parametros(self.value['tiempo_juego'], 60):
                self.config['TiempoJuego'] = int(self.value['tiempo_juego'])
            else: huboError = True
            
            if not huboError:
                self.stop_loop_main()
                Tablero(None, self.config).start()
            else:
                self.sg.popup('No estas ingresando un valor valido en el algún campo! Por favor revisá.')

        if self.event in ['FACIL', 'MEDIO', 'DIFICIL']:
            #Actualizamos los botones
            self.windows[self.event].update(button_color=('black', '#abbf42'))
            for i in ['FACIL', 'MEDIO', 'DIFICIL']:
                if i is not self.event:
                    self.windows[i].update(button_color=('black', '#F0803C'))
                self.windows['listo'].update(disabled=False)
            self.config["Nivel"] = self.configuraciones[self.event]["Nivel"]
            self.config["Posiciones"] = self.configuraciones[self.event]["Posiciones"]
            
            for i in self.letras:
                self.windows['valor'+i].update(self.configuraciones[self.event][i]['valor'])
                self.windows['cant'+i].update(self.configuraciones[self.event][i]['cant'])
            self.windows['tiempo_juego'].update(self.configuraciones[self.event]["TiempoJuego"])
            self.windows['tiempo_turno'].update(self.configuraciones[self.event]["TiempoTurno"])

            if self.event == 'DIFICIL':   #SI ES DIFICIL DEBE ELEGIR UN TEMA AL AZAR
                tipostr= choice(list(tipos))
                self.config['TipoDePalabra'] = tipos[tipostr] 
                self.config['Palabras'] = tipostr
                
            else:                    #SI NO, ELIGE EL QUE LE TOCA
                self.config['TipoDePalabra'] = self.configuraciones[self.event]["TipoDePalabra"]
                self.config['Palabras'] = self.configuraciones[self.event]["Palabras"]
           
