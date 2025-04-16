#DEPENDENCIAS
import random #PARA ELEGIR EL INICIO CUANDO LA IA JUEGA PRIMERO
import os #PARA BORRAR LA CONSOLA
import sys #PARA IDENTIFICAR LA PLATAFOR
import tkinter as tk #PARA CREAR LA VENTANA DE TKINTER
from tkinter import ttk #PARA CREAR LOS BOTONES DE TKINTER

#VARIABLE DE DEBUG CONDICIONAL
debug_enabled = True

#CREAMOS LA DICCIONARIO CON LAS POSICIONES Y LES ASIGNAMOS EL VALOR DE VACIO
tablero = {
        'A1': '0', 'A2': '0', 'A3': '0',
        'B1': '0', 'B2': '0', 'B3': '0',
        'C1': '0', 'C2': '0', 'C3': '0'
    }
def iniciar_tablero():
    for vertical in ['A', 'B', 'C']:
        for horizontal in ['1', '2', '3']:
            tablero[vertical+horizontal] = '0'

#DEFINIMOS LOS SIGNOS DE LOS JUGADORES EN UNA VARIABLE TOGGLEABLE
signos_jugadores = ['X', '+']

#DEFINIMOS LAS OPCIONES DE IA O JUGADOR
orden_jugadores = []

#CONTADOR DE JUGADAS
contador_jugadas = 0

#CONTADOR PARTIDAS
contador_partidas = 1

#CREAMOS LA FUNCION QUE LIMPIA LA CONSOLA
def limpiar_consola(): 
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

#LIMPIAMOS UNA ZONA DE LA VENTANA
def limpiar_parrilla(row, column):
    if debug_enabled: print('--> limpiando parrilla')
    for elemento in ventana_juego.winfo_children():
        if elemento.grid_info()['row'] == row and elemento.grid_info()['column'] == column:
            elemento.destroy()

#IMPRIMIR PLANTILLA ORIGINAL
def imprimir_tablero(tablero):
    print(f'Partida {contador_partidas}\n')
    print('  1 2 3')
    print('A', tablero['A1'], tablero['A2'], tablero['A3'])
    print('B', tablero['B1'], tablero['B2'], tablero['B3'])
    print('C', tablero['C1'], tablero['C2'], tablero['C3'])

#CREAMOS LA VENTANA TKINTER
def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Tres en raya")
    ventana.geometry("300x400")
    ventana.title("Tres en raya")
    ventana.configure(bg="black")
    ventana.resizable(False, False)
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=5)
    ventana.columnconfigure(0, weight=1)
    titulo = ttk.Label(ventana, text="Tres en raya", font=("console", 20), background="black", foreground="white")
    titulo.grid(row=0, column=0, sticky="n")
    return ventana

#ACTUALIZADOR DE LABEL EN LA VENTANA
def actualizar_mensaje(texto):
    limpiar_parrilla(1,0)
    if debug_enabled: print('--> actualizando mensaje a: '+texto)
    label = ttk.Label(ventana_juego, text=texto, font=("console", 15), background="black", foreground="white", justify="center")
    label.grid(row=1, column=0)
#CREAMOS LA INTELIGENCIA ARTIFICIAL
def ia():
    #AL CENTRO SI SE PUEDE
    if tablero['B2'] == '0':
        return 'B2'
    #COMPROBAMOS SI NOS PUEDEN GANAR O SI PODEMOS GANAR NOSOTROS
    posible_retorno_linia = jugadas_con_opción_de_linia()
    if ( posible_retorno_linia != None):
        return posible_retorno_linia
    #VEMOS POR DONDE ESTÁ JUGANDO EL RIVAL
    posible_retorno_esquinas = jugadas_de_esquinas()
    if ( posible_retorno_esquinas != None):
        return posible_retorno_esquinas
    #ELEGIMOS AL HAZAR UNA ESQUINA PARA EMPEZAR
    posible_retorno_esquina_libre = esquina_disponible()
    if ( posible_retorno_esquina_libre != None):
        return posible_retorno_esquina_libre
    #ELEGIMOS UNA CRUZ DISPONIBLE COMO ULTIMA OPCION
    return cruz_disponible()

#EVALUA TODAS LAS JUGADAS QUE PUEDAN HACER LINIA
def jugadas_con_opción_de_linia():
    if debug_enabled: print('--> checkeando jugada de linia')
    for leter in ['A', 'B', 'C']:
        if (tablero[leter+'1'] == tablero[leter+'2'] != '0' and tablero[leter+'3'] == '0'):
            return leter+'3'
        elif (tablero[leter+'1'] == tablero[leter+'3'] != '0' and tablero[leter+'2'] == '0'):
            return leter+'2'
        elif (tablero[leter+'2'] == tablero[leter+'3'] != '0' and tablero[leter+'1'] == '0'):
            return leter+'1'
    for number in ['1', '2', '3']:
        if (tablero['A'+number] == tablero['B'+number] != '0' and tablero['C'+number] == '0'):
            return 'C'+number
        elif (tablero['A'+number] == tablero['C'+number] != '0' and tablero['B'+number] == '0'):
            return 'B'+number
        elif (tablero['B'+number] == tablero['C'+number] != '0' and tablero['A'+number] == '0'):
            return 'A'+number
    if (tablero['A1'] == tablero['B2'] != '0' and tablero['C3'] == '0'):
        return 'C3'
    elif (tablero['A1'] == tablero['C3'] != '0' and tablero['B2'] == '0'):
        return 'B2'
    elif (tablero['B2'] == tablero['C3'] != '0' and tablero['A1'] == '0'):
        return 'A1'
    elif (tablero['A3'] == tablero['B2'] != '0' and tablero['C1'] == '0'):
        return 'C1'
    elif (tablero['A3'] == tablero['C1'] != '0' and tablero['B2'] == '0'):
        return 'B2'
    elif (tablero['B2'] == tablero['C1'] != '0' and tablero['A3'] == '0'):
        return 'A3'
    #SI NO HAY JUGADAS CON OPCION DE LINEA SEGUIMOS AL SIGUIENTE PASO
    return None

#EVALUA JUGADAS EN ESQUINAS
def jugadas_de_esquinas():
    if debug_enabled: print('--> checkeando jugada de esquinas')
    if (tablero['A1'] != '0' and tablero['A3'] == '0'):
        return 'A3'
    elif (tablero['A1'] != '0' and tablero['C1'] == '0'):
        return 'C1'
    elif (tablero['A3'] != '0' and tablero['C3'] == '0'):
        return 'C3'
    elif (tablero['A3'] != '0' and tablero['A1'] == '0'):
        return 'A1'
    elif (tablero['C1'] != '0' and tablero['C3'] == '0'):
        return 'C3'
    elif (tablero['C1'] != '0' and tablero['A1'] == '0'):
        return 'A1'
    elif (tablero['C3'] != '0' and tablero['A3'] == '0'):
        return 'A3'
    elif (tablero['C3'] != '0' and tablero['C1'] == '0'):
        return 'C1'
    #SI NO HAY JUGADAS EN ESQUINAS SEGUIMOS AL SIGUIENTE PASO
    return None

#ELEGIMOS UNA ESQUINA LIBRE
def esquina_disponible():
    if debug_enabled: print('--> checkeando esquinas')
    jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
    if debug_enabled: print('--> jugada: '+jugada+' tablero: '+tablero[jugada])
    jugadas_probadas = []
    while tablero[jugada] != '0' and len(jugadas_probadas) < 3:
        jugadas_probadas.append(jugada)
        if debug_enabled: print('--> jugadas_probadas: '+str(jugadas_probadas))
        jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
        if debug_enabled: print('--> jugada: '+jugada+' tablero: '+tablero[jugada])
        while jugada in jugadas_probadas:
            jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
            if debug_enabled: print('--> jugada in jugadas_probadas: jugada: '+jugada+' tablero: '+tablero[jugada])
            if debug_enabled: print('--> jugadas_probadas: '+str(len(jugadas_probadas))+'-'+str(jugadas_probadas))
    #VERIFICAMOS QUE HAY JUGANA Y SI NO PASAMOS AL SIGUINTE PASO
    if tablero[jugada] == '0':
        return jugada
    else:
        return None

#ELEGIMOS UNA CRUZ DISPONIBLE
def cruz_disponible():
    if debug_enabled: print('--> checkeando cruces')
    jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
    jugadas_probadas = []
    while tablero[jugada] != '0' and len(jugadas_probadas) < 3:
        jugadas_probadas.append(jugada)
        jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
        while jugada in jugadas_probadas:
            jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
     #VERIFICAMOS QUE HAY JUGANA Y SI NO PASAMOS AL SIGUINTE PASO
    if tablero[jugada] == '0':
        return jugada
    else:
        return None

#EVALUA SI HAY TABLAS
def evaluar_tablas():
    if debug_enabled: print('--> checkeando tablas')
    for espacio in tablero:
        if tablero[espacio] == '0':
            return False
    return True

#ORDENAMOS LA IA Y EL JUGADOR
def orden_ia_jugador():
    if debug_enabled: print('--> ordenando IA y jugador')
    orden_jugadores.clear()
    if random.choice([True, False]):
        orden_jugadores.append('IA')
        orden_jugadores.append('P')
        print('La IA empieza')
    else:
        orden_jugadores.append('P')
        orden_jugadores.append('IA')
        print('El jugador empieza')

#CREAMOS EL OBJETO DE LA VENTANA DE JUEGO
ventana_juego = crear_ventana()

#DEFINIMOS COMO GLOBAL LOS JUGADORES
jugadores = '0'
#PREGUNTAMOS NUMERO DE JUGADORES
evaluador_preguntador_jugadores = tk.StringVar()
def comprobar_jugadores(*args):
    if evaluador_preguntador_jugadores.get() in ['0', '1', '2']: #COMRPROBAMOS EL VALOR ESTÉ EN 0, 1 O 2
        jugadores = evaluador_preguntador_jugadores.get() #ASIGNAMOS EL VALOR ESCRITO A LOS JUGADORES
        if debug_enabled: print('--> jugadores: '+jugadores)
        if jugadores == '0':
            if debug_enabled: print('Modo PROFESOR FALKEN INICIANDO...')
            actualizar_mensaje('Modo PROFESOR FALKEN\nINICIANDO...')
            orden_jugadores.append('IA')
            orden_jugadores.append('IA')
        elif jugadores == '1':
            if debug_enabled: print('Modo SOLO INICIANDO...')
            actualizar_mensaje('Modo SOLO\nINICIANDO...')
            orden_ia_jugador()
        else:
            if debug_enabled: print('Modo VS INICIANDO...')
            actualizar_mensaje('Modo VS\nINICIANDO...')
            orden_jugadores.append('P')
            orden_jugadores.append('P')
    else:
        if debug_enabled: print('Error: Solo puedes elegir 0, 1 o 2 jugadores')
        evaluador_preguntador_jugadores.set('') #LIMPIA EL TEXTO DEL ENTRY
def preguntar_jugadores():  
    evaluador_preguntador_jugadores.trace_add("write", comprobar_jugadores) #ASIGNAMOS LA FUNCION A LA VARIABLE DE ENTRADA
    preguntador_jugadores_entry = ttk.Entry(ventana_juego, width=5, font=("console", 15), justify="center",textvariable=evaluador_preguntador_jugadores) #CREAMOS EL ENTRY PARA PREGUNTAR JUGADORES Y RELACIONA ASOCIA LA FUNCIÓN
    preguntador_jugadores_texto = ttk.Label(ventana_juego, text="¿Cuantos jugadores? (0, 1 o 2): ", font=("console", 15), background="black", foreground="white")
    preguntador_jugadores_texto.grid(row=1, column=0, sticky="n")
    preguntador_jugadores_entry.grid(row=1, column=0, sticky="s")
    preguntador_jugadores_entry.focus() #PONE EL FOCO EN EL ENTRY
preguntar_jugadores()

#PULSAMOS CUALQUIER TECLAR PARA EMPEZAR
input('Pulsa cualquier tecla para empezar')

#INICIAMOS EL JUEGO
iniciar_tablero()
game_on = True

#INICIAMOS EL JUEGO
while game_on or evaluar_tablas():
    #SI VENIMOS DE TABLAS, LIMPIAMOS EL TRABLERO
    if evaluar_tablas():
        iniciar_tablero()
    
    #IMPRIMIMOS EL TABLERO
    imprimir_tablero(tablero)

    #PEDIMOS JUGADA
    jugada_correcta = False
    if orden_jugadores[contador_jugadas % 2] == 'P':
        jugada = input('Introduce la jugada '+signos_jugadores[contador_jugadas % 2]+' (A1, B2, C3): ').upper()

        #VALIDAMOS JUGADA
        while jugada_correcta == False:
            if len(jugada) != 2 or jugada[0] not in 'ABC' or jugada[1] not in '123':
                print('Jugada imposible')
                jugada = input('Introduce la jugada '+signos_jugadores[contador_jugadas % 2]+' (A1, B2, C3): ').upper()
            elif tablero[jugada] != '0':
                print('Jugada imposible')
                jugada = input('Introduce la jugada '+signos_jugadores[contador_jugadas % 2]+' (A1, B2, C3): ').upper()
            else:
                jugada_correcta = True
    else:
        jugada = ia()
        print('La IA ha jugado: '+jugada)
    
    #LIMPIAMOS
    limpiar_consola()

    #ASIGNAMOS JUGADA AL TABLERO
    tablero[jugada] = signos_jugadores[contador_jugadas % 2]

    #INCREMENTAMOS JUGADA
    contador_jugadas += 1

    #VALIDAMOS SI HAY GANADOR
    if (tablero['A1'] == tablero['A2'] == tablero['A3'] != '0' or
        tablero['B1'] == tablero['B2'] == tablero['B3'] != '0' or
        tablero['C1'] == tablero['C2'] == tablero['C3'] != '0' or
        tablero['A1'] == tablero['B1'] == tablero['C1'] != '0' or
        tablero['A2'] == tablero['B2'] == tablero['C2'] != '0' or
        tablero['A3'] == tablero['B3'] == tablero['C3'] != '0' or
        tablero['A1'] == tablero['B2'] == tablero['C3'] != '0' or
        tablero['A3'] == tablero['B2'] == tablero['C1'] != '0'):
        print('El jugador '+signos_jugadores[contador_jugadas % 2]+' ha ganado')
        game_on = False
    elif (evaluar_tablas()):
        print('Tablas')
        if jugadores != '0':
            repetir = input('¿Quieres jugar de nuevo? (s/n): ').lower()
            while repetir not in ['s', 'n']:
                repetir = input('¿Quieres jugar de nuevo? (s/n): ').lower()
            if repetir == 'n':
                game_on = False
            else:
                if jugadores == '1':
                    orden_ia_jugador()
                contador_jugadas = 0
                contador_partidas += 1
        else:
            contador_jugadas = 0
            contador_partidas += 1
