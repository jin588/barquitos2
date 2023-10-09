import numpy as np
import random
import os
from funcionesyclases import es_posicion_valida, disparar_jugador, disparar_maquina, marcar_casillas_colindantes, Barco, Tablero

def imprimir_tableros_en_paralelo(tablero1, tablero2):
    print("Tus barcos: \t\t Tus disparos:")
    print("  0 1 2 3 4  \t   0 1 2 3 4 ")
    for i in range(5):
        fila_tablero1 = ' '.join(tablero1[i])
        fila_tablero2 = ' '.join(tablero2[i])
        print(f"{i} {fila_tablero1} \t {i} {fila_tablero2}")

def demo_juego():
    # Crear los tableros
    mi_tablero = Tablero((5,5))
    mi_tablero_disparos = Tablero((5,5))
    tablero_maquina_disparos = Tablero((5,5))
    tablero_maquina = Tablero((5,5))

    # Crear los barcos
    tamaños_barcos = [3,2,1]
    barcos_jugador = []
    barcos_maquina = []

    # Colocar los barcos en los tableros
    for tamaño in tamaños_barcos:
        barco_creado_jugador = False
        barco_creado_maquina = False
        while not barco_creado_jugador:
            barco_jugador = Barco(tamaño)
            if barco_jugador.colocar(mi_tablero):
                barcos_jugador.append(barco_jugador)
                barco_creado_jugador = True
        while not barco_creado_maquina:
            barco_maquina = Barco(tamaño)
            if barco_maquina.colocar(tablero_maquina):
                barcos_maquina.append(barco_maquina)
                barco_creado_maquina = True

    while True:
        acierto = True
        while acierto:
        # Turno del jugador
            fila = int(input("Introduce la fila de tu disparo: "))
            columna = int(input("Introduce la columna de tu disparo: "))
            acierto = disparar_jugador(tablero_maquina, mi_tablero_disparos, fila, columna, barcos_maquina)
            # Limpiar la consola
            os.system('cls' if os.name == 'nt' else 'clear')
             # Imprimir los tableros después de cada disparo
            imprimir_tableros_en_paralelo(mi_tablero.tablero, mi_tablero_disparos.tablero) 

            if all(barco.golpes == barco.tamaño for barco in barcos_maquina):
                print("Braviiisimo !!HAS GANADO!!")
                return

        
        # Turno de la máquina
        acierto = True
        while acierto:
            fila = random.randint(0, 4)
            columna = random.randint(0, 4)
            acierto = disparar_maquina(mi_tablero, tablero_maquina_disparos, fila, columna, barcos_jugador)

             # Limpiar la consola
            os.system('cls' if os.name == 'nt' else 'clear')
             # Imprimir los tableros después de cada disparo
            imprimir_tableros_en_paralelo(mi_tablero.tablero, mi_tablero_disparos.tablero) 

            # Comprobar si alguno de los jugadores ha ganado
        
        if all(barco.golpes == barco.tamaño for barco in barcos_jugador):
            print("GAME OVER")
            break

demo_juego()