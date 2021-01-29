import os

def pos_en_tablero(posicion, posiciones, window):
    print(posicion)
    print(window)
    if posicion in posiciones["Palabrax2"]:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'palabrax2.png', image_size=(40, 40))
    elif posicion in posiciones["Palabrax3"]:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'palabrax3.png', image_size=(40, 40))
    elif posicion in posiciones["Letrax2"]:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'letrax2.png', image_size=(40, 40))
    elif posicion in posiciones["Letrax3"]:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'letrax3.png', image_size=(40, 40))
    elif posicion in posiciones['Letra-1']:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'letra1.png', image_size=(40, 40))
    else:
        window[posicion].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'vacio.png', image_size=(40, 40)) #
        

def preparar_tablero(window, config, pos):
    """
    Prepara las posiciones especiales del tablero dependiendo de su dificultad
    """
    for x in range(config['FilasColumnas']):
        for y in range(config['FilasColumnas']):
            pos_en_tablero((x,y), pos, window)
    window[7, 7].Update('', image_filename=os.getcwd()+os.sep+"Static"+os.sep+'images'+os.sep+'centro.png', image_size=(40, 40))