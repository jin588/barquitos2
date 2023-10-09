import numpy as np
import random
import os
from funcionesyclases import es_posicion_valida, disparar_jugador, disparar_maquina, imprimir_tableros_en_paralelo, marcar_casillas_colindantes, Barco, Tablero
from variables import TAMAÑOS_BARCOS, TAMAÑO_TABLERO

# creamos los tableros
mi_tablero = Tablero(TAMAÑO_TABLERO)
mi_tablero_disparos = Tablero(TAMAÑO_TABLERO)
tablero_maquina_disparos = Tablero(TAMAÑO_TABLERO)
tablero_maquina = Tablero(TAMAÑO_TABLERO)

barcos_jugador = []
barcos_maquina = []
barcos = barcos_jugador + barcos_maquina

# con este bucle colocamos los barcos en los tableros segun su tamaño y los añadimos a las listas creadas.

for tamaño in TAMAÑOS_BARCOS: #tamaños_barcos nos dice los barcos a colocar en el tablero.
    barco_creado_jugador = False
    barco_creado_maquina = False
    while not barco_creado_jugador: # rellenamos nuestro tablero
        barco_jugador = Barco(tamaño) # creamos un barco de la clase Barco
        if barco_jugador.colocar(mi_tablero):
            barcos_jugador.append(barco_jugador)
            barco_creado_jugador = True
    while not barco_creado_maquina: # rellenamos el tablero de la maquina
        barco_maquina = Barco(tamaño)
        if barco_maquina.colocar(tablero_maquina):
            barcos_maquina.append(barco_maquina)
            barco_creado_maquina = True

# bucle del juego
while True:
    acierto = True
    while acierto: # turno jugador
        fila = int(input("Introduce la fila de tu disparo: "))
        columna = int(input("Introduce la columna de tu disparo: "))
        acierto = disparar_jugador(tablero_maquina, mi_tablero_disparos, fila, columna, barcos_maquina)
        # Limpiar la consola
        os.system('cls' if os.name == 'nt' else 'clear')
        # Imprimir los tableros después de cada disparo
        imprimir_tableros_en_paralelo(mi_tablero.tablero, mi_tablero_disparos.tablero) 

        

    acierto = True
    while acierto: # turno maquina
        fila = random.randint(0, 9)
        columna = random.randint(0, 9)
        acierto = disparar_maquina(mi_tablero, tablero_maquina_disparos, fila, columna, barcos_jugador)
        print("tablero de la maquina")
        print(tablero_maquina)
        os.system('cls' if os.name == 'nt' else 'clear') # limpiar la consola
        imprimir_tableros_en_paralelo(mi_tablero.tablero, mi_tablero_disparos.tablero)

    
    
            
    if all(barco.golpes == barco.tamaño for barco in barcos_jugador):
        print("GAME OVER")
        break
