import numpy as np
import random
import time
import os

def es_posicion_valida(tablero, fila, columna): # para colocar los barcos
    for dx in range(-1, 2): # rango -1,1 de las filas
        for dy in range(-1, 2):
            if 0 <= fila + dx < tablero.tamaño[0] and 0 <= columna + dy < tablero.tamaño[1]: # verifica si la coordenada esta dentro del tablero.
                if tablero.tablero[fila + dx][columna + dy] != ",": # verifica que la coordenada tiene otro barco
                    return False # si no esta dentro del tablero o la coordinada esta ocupada vuelve a empezar.
    return True # la posicion es valida.

def marcar_casillas_colindantes(tablero, fila, columna):
    for dx in range(-1, 2): 
        for dy in range(-1, 2):
            if 0 <= fila + dx < tablero.tamaño[0] and 0 <= columna + dy < tablero.tamaño[1]:
                if tablero.tablero[fila + dx][columna + dy] == ",":
                    tablero.tablero[fila + dx][columna + dy] = "X" # marca con X las casillas colindantes de los barcos.  jugabilidad.


def disparar_jugador(tablero_maquina, mi_tablero_disparos, fila, columna, barcos_maquina): # mis disparos
    acierto = False 
    if tablero_maquina.tablero[fila][columna] in ["N", "S", "E", "W"]: # impactamos
        tablero_maquina.tablero[fila][columna] = "O" 
        mi_tablero_disparos.tablero[fila][columna] = "O"
        for barco in barcos_maquina: # recorremos los barcos de la maquina 
            if (fila, columna) in barco.posicion:
                barco.golpes += 1 # anotamos el impacto.
                acierto = True
                print("Tocado")
                time.sleep(1)

                if barco.golpes == barco.tamaño: # verificamos si los impactos son igual al tamaño del barco
                    for pos in barco.posicion:
                        marcar_casillas_colindantes(mi_tablero_disparos, *pos)
                        marcar_casillas_colindantes(tablero_maquina, *pos)
                    print("Tocado y hundido!!")
                    time.sleep(1)
    else: # fallamos
        tablero_maquina.tablero[fila][columna] = "X"
        mi_tablero_disparos.tablero[fila][columna] = "X"
        print("aguita")
        time.sleep(1)
    return acierto
        
def disparar_maquina(mi_tablero, tablero_maquina_disparos, fila, columna, barcos_jugador):
    acierto = False 
    if mi_tablero.tablero[fila][columna] in ["N", "S", "E", "W"]: # verifica si el disparo da en n, s ...
        mi_tablero.tablero[fila][columna] = "O"
        tablero_maquina_disparos.tablero[fila][columna] = "O"
        for barco in barcos_jugador:
            if (fila, columna) in barco.posicion:
                barco.golpes += 1
                acierto = True 
                if barco.golpes == barco.tamaño:
                    for pos in barco.posicion:
                        marcar_casillas_colindantes(tablero_maquina_disparos, *pos)
                        marcar_casillas_colindantes(mi_tablero, *pos)
    else:
        mi_tablero.tablero[fila][columna] = "X"
        tablero_maquina_disparos.tablero[fila][columna] = "X"
        return acierto
    
def imprimir_tableros_en_paralelo(tablero1, tablero2):
    print("Tus barcos: \t\t Tus disparos:")
    print("  0 1 2 3 4 5 6 7 8 9 \t   0 1 2 3 4 5 6 7 8 9")
    for i in range(10): # ejecutamos 10 veces este veces
        fila_tablero1 = ' '.join(tablero1[i])# coge la primera fila del tablero y la convierte en una cadena, con " " usando .join
        fila_tablero2 = ' '.join(tablero2[i]) 
        print(f"{i} {fila_tablero1} \t {i} {fila_tablero2}") 




class Barco:
    def __init__(self, tamaño): # metodo constructor de barcos.
        self.tamaño = tamaño # tamaño del barco
        self.orientacion = random.choice(["N","S","E","W"]) # orientacion random del barco.
        self.posicion = [] # en esta lista añadiremos las coordenadas del barco
        self.golpes = 0 
    def colocar(self,tablero): # metodo para colocar los barcos.
            fila = random.randint(0, tablero.tamaño[0]-1) 
            columna = random.randint(0, tablero.tamaño[1]-1)
            if self.orientacion == "E" and columna + self.tamaño < tablero.tamaño[1]: # verificamos que cabe a la derecha (este)
                if all(es_posicion_valida(tablero, fila, columna + i) for i in range(self.tamaño)): #verificamos que esten vacias las casillas.
                    for i in range(self.tamaño): # este bucle se ejecuta por cada casilla que ocupa el barco.
                        tablero.tablero[fila][columna + i] = "E" 
                        self.posicion.append((fila, columna + i)) 
                    return True # el barco se ha colocado
            elif self.orientacion == "W" and columna - self.tamaño >= 0:
                if all(es_posicion_valida(tablero, fila, columna - i) for i in range(self.tamaño)):
                    for i in range(self.tamaño):
                        tablero.tablero[fila][columna - i] = "W"
                        self.posicion.append((fila, columna - i))
                    return True
            elif self.orientacion == "N" and fila - self.tamaño >= 0:
                if all(es_posicion_valida(tablero, fila - i, columna) for i in range(self.tamaño)):
                    for i in range(self.tamaño):
                        tablero.tablero[fila - i][columna] = "N"
                        self.posicion.append((fila - i, columna))
                    return True
            elif self.orientacion == "S" and fila + self.tamaño < tablero.tamaño[0]:
                if all(es_posicion_valida(tablero, fila + i, columna) for i in range(self.tamaño)):
                    for i in range(self.tamaño):
                        tablero.tablero[fila + i][columna] = "S"
                        self.posicion.append((fila + i, columna))
                    return True

class Tablero:
    def __init__(self, tamaño=(10,10)): # metodo constructo de tableros.
        self.tamaño = tamaño
        self.tablero = self.crear_tablero() # guardamos la matriz de crear_tablero, para que cada objeto de la clase Tablero tenga su matriz propia.

    def crear_tablero(self): # creamos la matriz que representa los tableros de juego.
        return np.full(self.tamaño, ",") 
    
    def __str__(self): # este metodo convierte objetos en cadenas.
        numeros = [str(i) for i in range(self.tamaño[0] )] # creamos una lista con los valores de las columnas 
        tablero_str = '  ' + ' '.join(numeros) + '\n' # convertimos la lista de numeros de las columnas en una cadena de texto separa por " "
        for i in range(self.tamaño[0]): # recorremos cada fila y la convertimos en _str
            fila_str = str(i).rjust(2) + ' ' + ' '.join(self.tablero[i]) + '\n' 
            tablero_str += fila_str # añádimos la cadena de la fila a la cadena del tablero.
        return tablero_str # devuelve la cadena de texto del tablero completa.