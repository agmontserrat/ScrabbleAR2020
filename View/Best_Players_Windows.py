from Controller.Generic_Window import Generic_Window
from Model.Generic_Manegement_Files import Generic_Manegement
import os

class Top10(Generic_Window):
    """Clase de la Ventana del Top 10 del juego ScrabbleAr. Es hija de Generic_Window. En ella podemos visualizar los 
    mejores 10  puntajes de cada nivel, y de todos los niveles juntos"""
    def __init__(self,*args,**kwargs):
        super(Top10,self).__init__(*args,**kwargs)
        self.sg = self.get_sg()
        self.name_windows='BEST PLAYERS'
    def initialize_timeout_window(self):
        pass
    def initialize_layout(self):
        super()
        columna = [
            [self.sg.Text('')],
            [self.sg.Text('1º\n2º\n3º\n4º\n5º\n6º\n7º\n8º\n9º\n10º', text_color='white', font=(6))]
        ]
        
        headings = ['  NOMBRE ', '  PUNTAJE ', '  NIVEL ', '  FECHA ']
        values_hardcodeados = [list(player.values()) for player in Generic_Manegement.readJsonFile("top10"+os.sep+"scores.json")["TODOS"]]
        layout = [
            [self.sg.Image(os.getcwd()+'/Static/images/top10.png')],
            [self.sg.Button('TODOS', size=(10,1), button_color = ('black', '#abbf42')), self.sg.Button('FACIL', size=(10,1), button_color=('black', '#F0803C')), self.sg.Button('MEDIO', size=(10,1), button_color=('black', '#F0803C')), self.sg.Button('DIFICIL', size=(10,1), button_color=('black', '#F0803C'))],
            [self.sg.Column(columna), self.sg.Table(values_hardcodeados, headings, select_mode="none", justification= 'center', key='tabla', num_rows=10, max_col_width=20,text_color="white",auto_size_columns=True, font=(6))],
            [self.sg.Button('Atras', font=(18), button_color=('black', 'White'))],
        ]
        return layout  

    def content(self):
        if self.event == "Atras":
            self.stop_loop_main()
        elif self.event in ["TODOS","FACIL","MEDIO","DIFICIL"]:
            values_hardcodeados = [list(player.values()) for player in Generic_Manegement.readJsonFile("top10/scores.json")[self.event][:10]]
            self.windows.FindElement('tabla').Update(values_hardcodeados)
            self.windows.FindElement(self.event).Update(button_color = ('black', '#abbf42'))
            for i in ['TODOS', 'FACIL', 'MEDIO', 'DIFICIL']:
                    if i is not self.event:
                        self.windows.FindElement(i).Update(button_color = ('black', '#F0803C'))

    