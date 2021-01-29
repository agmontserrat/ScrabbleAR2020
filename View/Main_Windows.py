import os
from Controller.Generic_Window import Generic_Window
from View.Best_Players_Windows import Top10
from View.GameBoard import Tablero
from View.Settings import Configuracion
from View.How_To_Play import Reglas
from Model.Generic_Manegement_Files import Generic_Manegement

class Main(Generic_Window):
    """This is the main windows to the proyect(game). First view of the system show the """
    def __init__(self,*args, **kwargs):
        super(Main,self).__init__(*args, **kwargs)
        self.sg = self.get_sg()
        self.name_windows = "Scrabble"
        self.partida_anterior = Generic_Manegement.loadLastGame()
    def initialize_timeout_window(self):
        pass
    def initialize_layout(self):
        self.sg.LOOK_AND_FEEL_TABLE['ScrabbleAr'] = {'BACKGROUND': '#702632',
                                     'TEXT': '#FDE3A7',
                                     'INPUT': '#D9B382',
                                     'TEXT_INPUT': '#2e2e2e',
                                     'SCROLL': '#c7e78b',
                                     'BUTTON': ('black', '#F0803C'),
                                     'PROGRESS': ('#01826B', '#D0D0D0'),
                                     'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                     }
        self.sg.theme("ScrabbleAr")
        layout = [
              [self.sg.Image(os.getcwd()+os.sep+'Static'+os.sep+'images'+os.sep+'SCRABBLE.png')],
                [self.sg.Text('    Bienvenido a SCRABBLEAR', size= (29,1), font=('Terminal', 18))  ],
                [self.get_button("Nuevo Juego",(29, 2))],
                [self.get_button("Continuar Partida", (14, 2), disabled=(self.partida_anterior is None)), self.get_button("Configuracion",(14, 2))],
                [self.get_button("Top 10", (14, 2), ), self.get_button("Cómo Jugar", (14, 2), )],
                [self.get_button("Salir",(29,2), )]
                ]
        return layout

    def content(self) -> None:
        if self.event == "Salir":
            self.stop_loop_main()
        elif self.event == "Top 10":
            self.windows.Hide()
            Top10().start()
            self.windows.un_hide()
        elif self.event == 'Nuevo Juego':
            if self.partida_anterior is not None:
                quiero = self.sg.popup('Tenés una partida vieja guardada. Si continuás la vas a perder. Querés continuar de cualquier manera?', title='Partida guardada', custom_text=("Continuar", "No"))
                if quiero == 'Continuar':
                    Generic_Manegement.saveLastGame(None)
                    self.windows.Hide()
                    Tablero().start() 
                    self.windows.un_hide()
            else:
                self.windows.Hide()
                Tablero().start() 
                self.windows.un_hide()
        elif self.event == 'Configuracion':
            self.windows.Hide()
            Configuracion().start()
            self.windows.un_hide()
        elif self.event == 'Cómo Jugar':
            self.windows.Hide()
            Reglas().start()
            self.windows.un_hide()
        elif self.event == "Continuar Partida":
            if self.partida_anterior is not None:
                self.windows.Hide()
                Tablero(self.partida_anterior).start() 
                self.windows.un_hide()

