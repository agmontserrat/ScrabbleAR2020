from Controller.Generic_Window import Generic_Window
from Model.Generic_Manegement_Files import Generic_Manegement
import os

class Reglas(Generic_Window):
    """Esta es la ventana de las reglas del juego. """
    def __init__(self,*args, **kwargs):
        super(Reglas,self).__init__(*args, **kwargs)
        self.sg = self.get_sg()
        self.name_windows = "Cómo Jugar"
        self.reglas = {"Facil": "En este nivel podes usar cualquier tipo de palabra (sustantivos, adjetivos, y verbos).\nPara comenzar el juego, se presiona el botón “Iniciar”.\nDe forma aleatoria, se decide quién empieza a jugar: la computadora o vos.\nCon tus fichas debes formar palabras con 2 letras o más, horizontalmente (las letras ubicadas de izquierda a derecha) o verticalmente (en orden descendente) sobre el tablero.\nEn la primera jugada, una de las letras deberá estar situada en el cuadro de “inicio del juego” (el centro).\nMoves tus fichas apretando en ellas sobre el atril, y luego apretando sobre la casilla del tablero\n  en la que la querés colocar.\nLuego de colocar tu palabra debes chequear si es válida, con el botón 'CHEQUEAR'.\nEn caso de no poder formar palabras, podes cambiar todas o algunas de tus fichas con el boton 'CAMBIAR FICHAS'.\nEl juego termina cuando:\n     -el jugador en turno no puede completar sus siete (7) fichas luego de      una jugada,dado que no hay más fichas en la bolsa de fichas.\n     -se acabó el tiempo de la partida.\n     -se presionó el botón “TERMINAR” partida.'",
              "Medio": "En este nivel podes usar sustantivos y verbos.\n\nPara comenzar el juego, se presiona el botón “Iniciar”.\nDe forma aleatoria, se decide quién empieza a jugar: la computadora o vos.\nCon tus fichas debes formar palabras con 2 letras o más, horizontalmente (las letras ubicadas de izquierda a derecha) o verticalmente (en orden descendente) sobre el tablero.\nEn la primera jugada, una de las letras deberá estar situada en el cuadro de “inicio del juego” (el centro).\nMoves tus fichas apretando en ellas sobre el atril, y luego apretando sobre la casilla del tablero\n  en la que la querés colocar.\nLuego de colocar tu palabra debes chequear si es válida, con el botón 'CHEQUEAR'.\nEn caso de no poder formar palabras, podes cambiar todas o algunas de tus fichas con el boton 'CAMBIAR FICHAS'.\nEl juego termina cuando:\n     -el jugador en turno no puede completar sus siete (7) fichas luego de      una jugada,dado que no -hay más fichas en la bolsa de fichas.\n     -se acabó el tiempo de la partida.\n     -se presionó el botón “TERMINAR” partida.')",
            "Dificil": "En este nivel se elige una categoría de las tres al azar.\n\nPara comenzar el juego, se presiona el botón “Iniciar”.\nDe forma aleatoria, se decide quién empieza a jugar: la computadora o vos.\nCon tus fichas debes formar palabras con 2 letras o más, horizontalmente (las letras ubicadas de izquierda a derecha) o verticalmente (en orden descendente) sobre el tablero.\nEn la primera jugada, una de las letras deberá estar situada en el cuadro de “inicio del juego” (el centro).\nMoves tus fichas apretando en ellas sobre el atril, y luego apretando sobre la casilla del tablero\n  en la que la querés colocar.\nLuego de colocar tu palabra debes chequear si es válida, con el botón 'CHEQUEAR'.\nEn caso de no poder formar palabras, podes cambiar todas o algunas de tus fichas con el boton 'CAMBIAR FICHAS'.\n  El juego termina cuando:\n     -el jugador en turno no puede completar sus siete (7) fichas luego de      una jugada,dado que no hay más fichas en la bolsa de fichas.\n     -se acabó el tiempo de la partida.\n     -se presionó el botón “TERMINAR” partida.'"
            }
    def initialize_timeout_window(self):
        pass
    def initialize_layout(self):
        layout_Reglas = [#OJOOOOOOOOOOO CAMBIASTE - ACAAAAA
            [self.sg.Image(os.getcwd()+os.sep+'Static'+os.sep+'images'+os.sep+'reglas.png')],
            [self.get_button("Facil", (16, 2)), self.get_button("Medio", (16, 2)), self.get_button("Dificil", (16, 2))],
            [self.sg.Multiline("Seleccione un nivel", key="nivel", disabled=True, size=(60, 10))],
            [self.sg.Text('CASILLAS ESPECIALES',font=("Fira Code Medium", 14))],
            [self.sg.Text('  Estas afectan tu puntuación')],
            [self.get_image_button('', (2,1), image_filename='palabrax2.png'), self.sg.Text('Palabra x2'), self.get_image_button('', (2, 1), image_filename='palabrax3.png'), self.sg.Text('Palabra x3')],
            [self.get_image_button('', (2,1), image_filename='letrax2.png'), self.sg.Text('Letra x2'), self.get_image_button('', (2,1), image_filename='letrax3.png'), self.sg.Text('Letra x3'), self.get_image_button('', (2,1), image_filename='bombita.png'), self.sg.Text('Letra -1')],
            [self.get_button("Volver", (8, 2), button_color=("black", "#FA8072"))]
            ]
        return layout_Reglas

    def content(self):
        if self.event  is "Volver":
            self.stop_loop_main()
        elif self.event in ["Facil", "Medio", "Dificil"]:
            print(self.event)
            self.windows[self.event].update(button_color=('black', '#95C623'))
            self.windows['nivel'].update(self.reglas[self.event])
            for i in ["Facil", "Medio", "Dificil"]:
                if i is not self.event:
                    self.windows[i].update(button_color=('black', '#F0803C'))
