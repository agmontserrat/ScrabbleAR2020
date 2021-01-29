# ScrabbleAR 2020
Trabajo final de la materia de Seminario de Lenguajes (Opción Pyhton).
ScrabbleAR es un juego basado en el popular juego Scrabble, en el que se intenta ganar puntos
mediante la construcción de palabras sobre un tablero. En ScrabbleAR se juega contra la
computadora y se redefinen algunas de las reglas del juego original. En particular, respecto a las
palabras a construir, sólo se podrán utilizar palabras clasificadas como adjetivos, sustantivos y
verbos, de acuerdo a cómo se configure el juego.

Alumna: García, Agustina

## Requisitos
  - Python 3.6
  - Pattern3 3.0.0
  - PySimpleGUI
 
 ## Como jugar
 Instalar las librerías necesarias.

 Descargar el contenido del repositorio.
 
 El juego inicia al ejecutar el archivo ScrabbleAR.py.

 Al abrir la aplicación se muestra el menú principal. El jugador puede elegir "Nuevo Juego" para iniciar una partida
 con el nivel Facil predeterminado, "Configuracion" para elegir otro nivel y/o cambiar valores como gusten,
 "Continuar Partida" que si está habilitado es porque tenemos una partida guardada, "Como Jugar" para ver las reglas del juego,
 y "Top 10" para ver los puntajes guardados.


 ## Contenido

 ### Configuración.
 En esta carpeta encontramos el archivo configuracionMain. Aquí podemos configurar nuestro nivel. Al elegir uno, los valores predeterminados de cada nivel
 aparecen. Podemos personalizar nuestra partida cambiando esos valores, pero jugando con el tablero
 del nivel que elegimos.
 Las unicas cosas que no son configurables son las palabras que admite.
 En el nivel Facil se juega con Sustantivos, Adjetivos y verbos. En el medio con Sustantivos y Verbos.
 En el nivel Dificil con UNA de estas tres categorías al azar.

 ### Juego
 Contiene todos los aspectos visuales necesarios paras la partida. El tablero, los atriles, etc.
 Utiliza los archivos juego_funciones.py que tiene las funciones necesarias para el juego, y turno_maquina.py.
 Los tableros de cada nivel tienen casillas con premio y casillas con descuento de puntos.
 Las partidas guardadas estan almacenadas en formato pickle para poder guardar objetos como la bolsa de fichas.
 Si se sobreescribe la partida guardada, esta se pierde.
 ### Top Puntajes
 En este podemos ver los mejores 10 puntajes de cada nivel y ademas los mejores 10 puntajes entre todos los niveles.

 ### Fin de la partida.
 La partida finaliza cuando:
 -El jugador toca el botón "Terminar".
 -No hay suficientes fichas para repartir un atril entero (o sea, hay menos de 7 fichas en la bolsa).
 -La computadora no puede formar ninguna palabra con sus fichas.
 -Se acaba el tiempo de la partida.

