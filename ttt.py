#DEPENDENCIAS
import random #PARA ELEGIR EL INICIO CUANDO LA IA JUEGA PRIMERO
import os #PARA BORRAR LA CONSOLA
import sys #PARA IDENTIFICAR LA PLATAFORMA

#VARIABLE DE DEBUG CONDICIONAL
debug_enabled = False

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

#IMPRIMIR PLANTILLA ORIGINAL
def imprimir_tablero(tablero):
    print(f'Partida {contador_partidas}\n')
    print('  1 2 3')
    print('A', tablero['A1'], tablero['A2'], tablero['A3'])
    print('B', tablero['B1'], tablero['B2'], tablero['B3'])
    print('C', tablero['C1'], tablero['C2'], tablero['C3'])

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


def consultar_repetir():
    global game_on, contador_jugadas, contador_partidas, jugadores
    if debug_enabled: print('--> consultando repetir')
    repetir = input('¿Quieres jugar de nuevo? (s/n): ').lower()
    while repetir not in ['s', 'n']:
        repetir = input('¿Quieres jugar de nuevo? (s/n): ').lower()
    if repetir == 'n':
        game_on = False
    else:
        iniciar_tablero()
        if jugadores == '1':
            orden_ia_jugador()
        contador_jugadas = 0
        contador_partidas += 1

#PREGUNTAMOS NUMERO DE JUGADORES
jugadores = input('¿Cuantos jugadores? (0, 1 o 2): ')
while jugadores not in ['0', '1', '2']:
    jugadores = input('¿Cuantos jugadores? (0, 1 o 2): ')
if jugadores == '0':
    print('Modo PROFESOR FALKEN INICIANDO...')
    orden_jugadores.append('IA')
    orden_jugadores.append('IA')
elif jugadores == '1':
    print('Modo SOLO INICIANDO...')
    orden_ia_jugador()
else:
    print('Modo VS INICIANDO...')
    orden_jugadores.append('P')
    orden_jugadores.append('P')

#PULSAMOS CUALQUIER TECLAR PARA EMPEZAR
input('Pulsa cualquier tecla para empezar')

#LIMPIAMOS
limpiar_consola()

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
        consultar_repetir()
    elif (evaluar_tablas()):
        print('Tablas')
        if jugadores != '0':
            consultar_repetir()
        else:
            contador_jugadas = 0
            contador_partidas += 1
    #INCREMENTAMOS JUGADA
    contador_jugadas += 1
