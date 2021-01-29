from abc import ABC,abstractclassmethod
import json
import pickle
import os
from datetime import datetime
class Generic_Manegement(ABC):
    """Clase que nos ayuda con el manejo de archivos en el juego."""
    def __init__(self):
        super().__init__()

    @classmethod
    def readJsonFile(self,nameFile):
        """Función que recibe un nombre de un archivo json y lo abre en caso de que exista."""
        data=''
        try: 
            with open(os.getcwd()+os.sep+"Static"+os.sep+"data"+os.sep+nameFile, encoding="utf-8") as file:
                data=json.load(file)
            return data
        except FileNotFoundError:
            print("No existe o no se pudo localizar el archivo", nameFile)
            exit(1)
            
    @classmethod
    def loadLastGame(self):
        """Función que carga la ultima partida guardada"""
        try:
            with open(os.getcwd()+os.sep+"Static"+os.sep+"data"+os.sep+"ultima_partida.pickle", "rb") as f:
                partida = pickle.load(f)
                f.close()
        except:
            partida = None
        return partida

    @classmethod
    def saveLastGame(self,game):
        """Función que guarda en una archivo pickle los datos de la partida a posponer."""
        try:
            with open(os.getcwd()+os.sep+"Static"+os.sep+"data"+os.sep+"ultima_partida.pickle", 'wb') as archivo:
                pickle.dump(game, archivo)
                archivo.close()
                return True
        except FileNotFoundError:
            print('Hubo un error. No pudimos guardar tu partida. No la podés retomar luego.')
            return False

    @classmethod
    def saveScores(self, nombre, puntos, nivel):
        """Funcion que guarda un nuevo puntaje con el nombre del jugador, nivel y el dia en el que se jugó la partida. 
        En caso de no encontrar el archivo donde debe guardarlo, porque por ejemplo pudo ser borrado, crea uno nuevo.,"""
        now = datetime.now()
        fecha_actual = now.strftime("%d-%m-%Y")
        try:
            partidas = self.readJsonFile("top10"+os.sep+"scores.json")
            puntaje = {
                "jugador": nombre,
                "puntaje": puntos,
                "nivel": nivel,
                "fecha": fecha_actual
            }
            partidas[nivel].append(puntaje)
            partidas["TODOS"].append(puntaje)
            partidas[nivel] = sorted(partidas[nivel], key=lambda x: x["puntaje"], reverse=True)
            partidas["TODOS"] = sorted(partidas["TODOS"], key=lambda x: x["puntaje"], reverse=True)
            with open(os.getcwd()+os.sep+"Static"+os.sep+"data"+os.sep+"top10"+os.sep+"scores.json", "w", encoding="utf-8") as file:
                json.dump(partidas, file, indent=4)
                file.close()
        except FileNotFoundError:
            partidas = {'TODOS': [], 'FACIL': [], 'MEDIO': [], 'DIFICIL': []}
            puntaje = {
                "jugador": nombre,
                "puntaje": puntos,
                "nivel": nivel,
                "fecha": fecha_actual
            }
            partidas[nivel].append(puntaje)
            partidas["TODOS"].append(puntaje)
            partidas[nivel] = sorted(partidas[nivel], key=lambda x: x["puntaje"], reverse=True)
            partidas["TODOS"] = sorted(partidas["TODOS"], key=lambda x: x["puntaje"], reverse=True)
            with open(os.getcwd()+os.sep+"Static"+os.sep+"data"+os.sep+"top10"+os.sep+"scores.json", "w", encoding="utf-8") as file:
                json.dump(partidas, file, indent=4)
                file.close()