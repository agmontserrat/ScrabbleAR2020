import PySimpleGUI as sg
from abc import ABC,abstractmethod
import os
#from Magic_Functions import Enviroment

class Generic_Window(ABC):
    """Esta es la clase principal. Todas las implementaciones de ventanas deben ser hijas de esta.
    Esta clase contiene todo lo propio de una ventana estandar."""
    def __init__(self):
        super()
        self.windows = None
        self.layout_content = []
        self.name_windows = ""
        self.sg = sg
        self.event=''
        self.value=''
        self.loop_break=False
        self.timeout=10 
       
    @abstractmethod
    def content(self):
        """Es la funcion principal que debe estar implementada en cada clase hija porque
        aquí esta toda la implementación de la ventana. Todo el comportamiento está dentro de este método."""
        raise NotImplementedError

    @abstractmethod
    def initialize_layout(self):
        """En esta función definimos el layout de nuestra ventana. """
        raise NotImplementedError

    @abstractmethod
    def initialize_timeout_window(self):
        pass

    def get_timeout(self):
        return self.timeout

    def set_timeout(self,timeout):
        self.timeout=timeout

    def get_sg(self):
        return self.sg

    def get_name_windows(self):
        return self.name_windows

    def set_layout(self,layout):
        self.layout_content = layout

    def get_layout(self):
        return self.layout_content

    def stop_loop_main(self):
        #self.windows.Read(timeout=0)
        self.loop_break = True

    def get_loop_main(self):
        return self.loop_break

    def get_button(self, nameButton='', size=(5,5), key= None,  pad=(0.5, 0.5), button_color=('black', '#F0803C'), disabled = False):
        """Esta funcion me retorna un boton generico, en caso de que no se le declaren
        los parametros"""
        if key == None: 
            return self.sg.Button(nameButton, size=size, key=nameButton, pad=pad, button_color= button_color, disabled=disabled)
        else:
            return self.sg.Button(nameButton, size=size, key=key, pad=pad, button_color= button_color, disabled=disabled)
        
    def get_image_button(self, nameButton='', key= '', image_filename='', image_size= (40,40), pad=(0.5, 0.5), button_color=('black', '#F0803C'), disabled = False):
        """Esta funcion me retorna un boton generico en caso de que no se le declaren los parametros, con una imagen. Esta es necesaria especificar."""                                
        return self.sg.Button(nameButton, key=key, image_filename=os.getcwd()+os.sep+"Static"+os.sep+"images"+os.sep+ image_filename, image_size= image_size, pad=pad, button_color= button_color, disabled=disabled)
            

    def loop_main(self):
        self.set_layout(self.initialize_layout())
        layout = [
            [sg.Column(self.get_layout(), element_justification='c')],
        ]
        self.windows = sg.Window(self.get_name_windows(),layout)
        self.initialize_timeout_window()
        while True:
            self.event,self.value = self.windows.Read(timeout=self.timeout)
            
            if self.event == None:
                break
            self.content()
            if self.get_loop_main():
                break

        self.windows.close()

    def start(self) -> None:
        self.loop_main()
        return None