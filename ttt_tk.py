#DEPENDENCIAS
import random #PARA ELEGIR EL INICIO CUANDO LA IA JUEGA PRIMERO
import os #PARA BORRAR LA CONSOLA
import sys #PARA IDENTIFICAR LA PLATAFOR
import tkinter as tk #PARA CREAR LA VENTANA DE TKINTER
from tkinter import ttk #PARA CREAR LOS BOTONES DE TKINTER
from tkinter import font #PARA CREAR LA FUENTE DE LOS BOTONES
import time #PARA HACER PAUSAS

#VARIABLE DE DEBUG CONDICIONAL
debug_enabled = True

#CREAMOS LA DICCIONARIO CON LAS POSICIONES Y LES ASIGNAMOS EL VALOR DE VACIO
tablero = {
        'A1': ' ', 'A2': ' ', 'A3': ' ',
        'B1': ' ', 'B2': ' ', 'B3': ' ',
        'C1': ' ', 'C2': ' ', 'C3': ' '
    }
def iniciar_tablero(): #DAMOS VALORES ' ', LIBRES, A TODAS LAS POSICIONES DEL TABLERO
    for vertical in ['A', 'B', 'C']:
        for horizontal in ['1', '2', '3']:
            tablero[vertical+horizontal] = ' '

def crear_tablero():
    tablero_frame_estilo = ttk.Style() #CREAMOS EL ESTILO DEL FRAME, ttk NO PERMITE HACERLO CON BG O FG
    tablero_frame_estilo.theme_use("clam") #USAMOS EL TEMA CLAM
    tablero_frame_estilo.configure("tablero_frame.TFrame", background="black", borderwidth=2, relief="raised") #LO DEFINIMOS Y PONEMOS NOMBRE DE REFERENCIA (HA DE ACABAR CON .TFrame)
    tablero_frame = ttk.Frame(ventana_juego, padding=10, relief="raised", borderwidth=2, style="tablero_frame.TFrame", name="tablero_frame") #CREAMOS EL FRAME CON EL ESTILO CREADO ANTERIORMENTE
    tablero_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=2, pady=2) #LO PONEMOS EN LA VENTANA
    #SETEAMOS LA ZONA DE JUEGO 3X3
    tablero_frame.rowconfigure(0, weight=1) 
    tablero_frame.rowconfigure(1, weight=1) 
    tablero_frame.rowconfigure(2, weight=1)
    tablero_frame.columnconfigure(0, weight=1)
    tablero_frame.columnconfigure(1, weight=1)
    tablero_frame.columnconfigure(2, weight=1)
    #CREAMOS LOS BOTONES DEL TABLERO Y LOS PONEMOS EN EL FRAME
    fuente_boton = ttk.Style()
    fuente_boton_style = font.Font(family="console", size=12, weight="bold")
    fuente_boton.configure("fuente_boton.TButton",background="darkgray", font=fuente_boton_style) #DEFINIMOS LA FUENTE DE LOS BOTONES
    for vertical in ['A', 'B', 'C']:
        for horizontal in ['1', '2', '3']:
            boton = ttk.Button(tablero_frame, text='', command=lambda v=vertical, h=horizontal: jugar_player(v+h), state='disabled', style="fuente_boton.TButton", name=vertical.lower()+horizontal) #CREAMOS EL BOTON CON EL VALOR DEL TABLERO Y LO DESHABILITAMOS
            vert, hori = conversor_posiciones_grid(vertical, horizontal)
            boton.grid(row=vert, column=hori, sticky=tk.NSEW , padx=2, pady=2) #CREAMOS EL BOTON Y LO PONEMOS EN SU POSICIÓN
            tablero[vertical+horizontal] = boton

#CONVERTIMOS LA LETRA EN UN NUMERO Y NUMEROS EMPEZANDO POR 0 PARA QUE FUNCIONE EN EL GRID
def conversor_posiciones_grid(vert, hori):
    if debug_enabled: print('--> conversor_posiciones_grid')
    return(int(ord(vert))-65, int(hori)-1) 

#DEFINIMOS LOS SIGNOS DE LOS JUGADORES EN UNA VARIABLE TOGGLEABLE
signos_jugadores = ['X', 'O']

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

#CIERRA LA VENTANA Y ACABA CON LA EJECUCIÓN
def salir_del_juego():
    if debug_enabled: print('--> cerrando ventana')
    ventana_juego.destroy()
    exit()

#ACTIVAR TODOS LOS BOTONES
def activar_botones():
    if debug_enabled: print('--> activando botones')
    for elemento in ventana_juego.winfo_children():
        if elemento.grid_info()['row'] == 2 and elemento.grid_info()['column'] == 0:
            for botones_del_frame in elemento.winfo_children():
                botones_del_frame["state"]='enabled'

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
    titulo.grid(row=0, column=0, sticky=tk.N)
    ventana.protocol("WM_DELETE_WINDOW", salir_del_juego) #AL PULSAR LA X DE LA VENTANA SE CERRARA EL JUEGO
    return ventana

#ACTUALIZADOR DE LABEL EN LA VENTANA
def actualizar_mensaje(texto):
    limpiar_parrilla(1,0)
    if debug_enabled: print('--> actualizando mensaje a: '+texto)
    label = ttk.Label(ventana_juego, text=texto, font=("console", 15), background="black", foreground="white", justify="center")
    label.grid(row=1, column=0)

#ACTUALIZADOR DE BOTON EN LA VENTANA
def poner_signo_en_boton(boton, signo):
    boton_a_cambiar = ventana_juego.nametowidget('.tablero_frame.'+boton) #OBTENEMOS EL BOTON DEL TABLERO
    boton_a_cambiar["text"] = signo #CAMBIAMOS EL TEXTO DEL BOTON

#CREAMOS LA INTELIGENCIA ARTIFICIAL
def ia():
    #AL CENTRO SI SE PUEDE
    if tablero['B2'] == ' ':
        jugada_ia = 'B2'
    else:
        print('>>>'+tablero['B2']+'<<<')
        #COMPROBAMOS SI NOS PUEDEN GANAR O SI PODEMOS GANAR NOSOTROS
        posible_retorno_linia = jugadas_con_opción_de_linia()
        if ( posible_retorno_linia != None):
            jugada_ia = posible_retorno_linia
        else:
            #VEMOS POR DONDE ESTÁ JUGANDO EL RIVAL
            posible_retorno_esquinas = jugadas_de_esquinas()
            if ( posible_retorno_esquinas != None):
                jugada_ia = posible_retorno_esquinas
            else:
                #ELEGIMOS AL HAZAR UNA ESQUINA PARA EMPEZAR
                posible_retorno_esquina_libre = esquina_disponible()
                if ( posible_retorno_esquina_libre != None):
                    jugada_ia = posible_retorno_esquina_libre
                else:
                    #ELEGIMOS UNA CRUZ DISPONIBLE COMO ULTIMA OPCION
                    jugada_ia = cruz_disponible()
    return jugada_ia

#EVALUA TODAS LAS JUGADAS QUE PUEDAN HACER LINIA
def jugadas_con_opción_de_linia():
    if debug_enabled: print('--> checkeando jugada de linia')
    for leter in ['A', 'B', 'C']:
        if (tablero[leter+'1'] == tablero[leter+'2'] != ' ' and tablero[leter+'3'] == ' '):
            return leter+'3'
        elif (tablero[leter+'1'] == tablero[leter+'3'] != ' ' and tablero[leter+'2'] == ' '):
            return leter+'2'
        elif (tablero[leter+'2'] == tablero[leter+'3'] != ' ' and tablero[leter+'1'] == ' '):
            return leter+'1'
    for number in ['1', '2', '3']:
        if (tablero['A'+number] == tablero['B'+number] != ' ' and tablero['C'+number] == ' '):
            return 'C'+number
        elif (tablero['A'+number] == tablero['C'+number] != ' ' and tablero['B'+number] == ' '):
            return 'B'+number
        elif (tablero['B'+number] == tablero['C'+number] != ' ' and tablero['A'+number] == ' '):
            return 'A'+number
    if (tablero['A1'] == tablero['B2'] != ' ' and tablero['C3'] == ' '):
        return 'C3'
    elif (tablero['A1'] == tablero['C3'] != ' ' and tablero['B2'] == ' '):
        return 'B2'
    elif (tablero['B2'] == tablero['C3'] != ' ' and tablero['A1'] == ' '):
        return 'A1'
    elif (tablero['A3'] == tablero['B2'] != ' ' and tablero['C1'] == ' '):
        return 'C1'
    elif (tablero['A3'] == tablero['C1'] != ' ' and tablero['B2'] == ' '):
        return 'B2'
    elif (tablero['B2'] == tablero['C1'] != ' ' and tablero['A3'] == ' '):
        return 'A3'
    #SI NO HAY JUGADAS CON OPCION DE LINEA SEGUIMOS AL SIGUIENTE PASO
    return None

#EVALUA JUGADAS EN ESQUINAS
def jugadas_de_esquinas():
    if debug_enabled: print('--> checkeando jugada de esquinas')
    if (tablero['A1'] != ' ' and tablero['A3'] == ' '):
        return 'A3'
    elif (tablero['A1'] != ' ' and tablero['C1'] == ' '):
        return 'C1'
    elif (tablero['A3'] != ' ' and tablero['C3'] == ' '):
        return 'C3'
    elif (tablero['A3'] != ' ' and tablero['A1'] == ' '):
        return 'A1'
    elif (tablero['C1'] != ' ' and tablero['C3'] == ' '):
        return 'C3'
    elif (tablero['C1'] != ' ' and tablero['A1'] == ' '):
        return 'A1'
    elif (tablero['C3'] != ' ' and tablero['A3'] == ' '):
        return 'A3'
    elif (tablero['C3'] != ' ' and tablero['C1'] == ' '):
        return 'C1'
    #SI NO HAY JUGADAS EN ESQUINAS SEGUIMOS AL SIGUIENTE PASO
    return None

#ELEGIMOS UNA ESQUINA LIBRE
def esquina_disponible():
    if debug_enabled: print('--> checkeando esquinas')
    jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
    if debug_enabled: print('--> jugada: '+jugada+' tablero: '+tablero[jugada])
    jugadas_probadas = []
    while tablero[jugada] != ' ' and len(jugadas_probadas) < 3:
        jugadas_probadas.append(jugada)
        if debug_enabled: print('--> jugadas_probadas: '+str(jugadas_probadas))
        jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
        if debug_enabled: print('--> jugada: '+jugada+' tablero: '+tablero[jugada])
        while jugada in jugadas_probadas:
            jugada = random.choice(['A1', 'A3', 'C1', 'C3'])
            if debug_enabled: print('--> jugada in jugadas_probadas: jugada: '+jugada+' tablero: '+tablero[jugada])
            if debug_enabled: print('--> jugadas_probadas: '+str(len(jugadas_probadas))+'-'+str(jugadas_probadas))
    #VERIFICAMOS QUE HAY JUGANA Y SI NO PASAMOS AL SIGUINTE PASO
    if tablero[jugada] == ' ':
        return jugada
    else:
        return None

#ELEGIMOS UNA CRUZ DISPONIBLE
def cruz_disponible():
    if debug_enabled: print('--> checkeando cruces')
    jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
    jugadas_probadas = []
    while tablero[jugada] != ' ' and len(jugadas_probadas) < 3:
        jugadas_probadas.append(jugada)
        jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
        while jugada in jugadas_probadas:
            jugada = random.choice(['A2', 'B1', 'B3', 'C2'])
     #VERIFICAMOS QUE HAY JUGANA Y SI NO PASAMOS AL SIGUINTE PASO
    if tablero[jugada] == ' ':
        return jugada
    else:
        return None

#EVALUA SI HAY TABLAS
def evaluar_tablas():
    if debug_enabled: print('--> Evaluando tablas')
    for espacio in tablero:
        if tablero[espacio] == ' ':
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
        jugar_player(ia()) #LA IA JUEGA PRIMERO
    else:
        orden_jugadores.append('P')
        orden_jugadores.append('IA')
        print('El jugador empieza')

#CREAMOS EL OBJETO DE LA VENTANA DE JUEGO
ventana_juego = crear_ventana()

#DEFINIMOS COMO GLOBAL LOS JUGADORES
jugadores = ' '
#PREGUNTAMOS NUMERO DE JUGADORES
evaluador_preguntador_jugadores = tk.StringVar()
def comprobar_jugadores(_jugadores):
    global jugadores
    jugadores = _jugadores
    if debug_enabled: print('--> jugadores: '+str(jugadores))
    if jugadores == 0:
        if debug_enabled: print('Modo PROFESOR FALKEN INICIANDO...')
        actualizar_mensaje('Modo PROFESOR FALKEN')
        orden_jugadores.append('IA')
        orden_jugadores.append('IA')
    elif jugadores == 1:
        if debug_enabled: print('Modo SOLO INICIANDO...')
        actualizar_mensaje('Modo SOLO')
        orden_ia_jugador()
    else:
        if debug_enabled: print('Modo VS INICIANDO...')
        actualizar_mensaje('Modo VS')
        orden_jugadores.append('P')
        orden_jugadores.append('P')
        time.sleep(3)
        actualizar_mensaje("TURNO DE X")
    activar_botones() #ACTIVAMOS LOS BOTONES DEL TABLERO
def preguntar_jugadores():  
    preguntador_jugadores_button_0 = ttk.Button(ventana_juego, text='0', command=lambda: comprobar_jugadores(0), name="preguntador_jugadores_button_0") #CREAMOS EL BOTON DE 0
    preguntador_jugadores_button_1 = ttk.Button(ventana_juego, text='1', command=lambda: comprobar_jugadores(1), name="preguntador_jugadores_button_1") #CREAMOS EL BOTON DE 1
    preguntador_jugadores_button_2 = ttk.Button(ventana_juego, text='2', command=lambda: comprobar_jugadores(2), name="preguntador_jugadores_button_2") #CREAMOS EL BOTON DE 2
    preguntador_jugadores_texto = ttk.Label(ventana_juego, text="¿Cuantos jugadores?", font=("console", 15), background="black", foreground="white")
    preguntador_jugadores_texto.grid(row=1, column=0, sticky=tk.N)
    preguntador_jugadores_button_0.grid(row=1, column=0, sticky=tk.SW)
    preguntador_jugadores_button_1.grid(row=1, column=0, sticky=tk.S)
    preguntador_jugadores_button_2.grid(row=1, column=0, sticky=tk.SE)
preguntar_jugadores()

#PREGUNTAR REPETIR PARTIDA
def repetir_partida(que_hacer):
    global game_on, jugadores, contador_jugadas, contador_partidas
    if debug_enabled: print('--> preguntando repetir partida: '+que_hacer)
    
    if jugadores != 0:
        if que_hacer == 'n':
            game_on = False
        else:
            
            if jugadores == 1:
                orden_ia_jugador()
            contador_jugadas = 0
            contador_partidas = 0
    else:
        contador_jugadas = 0
        contador_partidas += 1

def preguntar_repetir_partida():
    fuente_repetir_partida = ttk.Style()
    fuente_repetir_partida_style = font.Font(family="console", size=8)
    fuente_repetir_partida.configure("fuente_repetir_partida.TButton",background="gray", font=fuente_repetir_partida_style) #DEFINIMOS LA FUENTE DE LOS BOTONES
    preguntador_repetir_partida_boton_si = ttk.Button(ventana_juego, text='SI', command=lambda: repetir_partida('s'), style="fuente_repetir_partida.TButton", name="botton_repetir_partida_si") #CREAMOS EL BOTON DE SI
    preguntador_repetir_partida_boton_no = ttk.Button(ventana_juego, text='NO', command=lambda: repetir_partida('n'), style="fuente_repetir_partida.TButton", name="botton_repetir_partida_no") #CREAMOS EL BOTON DE NO
    preguntador_repetir_partida_label = ttk.Label(ventana_juego, text="¿Volver a jugar: ", font=("console", 12), background="black", foreground="white")
    preguntador_repetir_partida_label.grid(row=1, column=0, sticky=tk.N)
    preguntador_repetir_partida_boton_si.grid(row=1, column=0, sticky=tk.SE)
    preguntador_repetir_partida_boton_no.grid(row=1, column=0, sticky=tk.SW)

#PINTAMOS EL TABLERO EN LA VENTANA
crear_tablero()

#INICIAMOS EL JUEGO
iniciar_tablero()
game_on = True

#EJECUTAMOS LA JUGADA
def jugar_player(jugada_boton=None):
    global contador_jugadas, game_on, jugadores, orden_jugadores, tablero, contador_partidas
    if game_on:
        #PEDIMOS JUGADA
        jugada_correcta = False
        if orden_jugadores[contador_jugadas % 2] == 'P':
            jugada = jugada_boton
            #PINTAMOS EL SIGNO EN EL BOTON
            poner_signo_en_boton(jugada_boton.lower(), signos_jugadores[contador_jugadas % 2])
        else:
            jugada = ia()
            print('La IA ha jugado: '+jugada)
            #PINTAMOS EL SIGNO EN EL BOTON
            poner_signo_en_boton(jugada.lower(), signos_jugadores[contador_jugadas % 2])
        #ASIGNAMOS JUGADA AL TABLERO
        tablero[jugada] = signos_jugadores[contador_jugadas % 2]
        #VALIDAMOS SI HAY GANADOR
        if (tablero['A1'] == tablero['A2'] == tablero['A3'] != ' ' or
            tablero['B1'] == tablero['B2'] == tablero['B3'] != ' ' or
            tablero['C1'] == tablero['C2'] == tablero['C3'] != ' ' or
            tablero['A1'] == tablero['B1'] == tablero['C1'] != ' ' or
            tablero['A2'] == tablero['B2'] == tablero['C2'] != ' ' or
            tablero['A3'] == tablero['B3'] == tablero['C3'] != ' ' or
            tablero['A1'] == tablero['B2'] == tablero['C3'] != ' ' or
            tablero['A3'] == tablero['B2'] == tablero['C1'] != ' '):
            limpiar_parrilla(1,0) #LIMPIAMOS LA ZONA DE MENSAJE
            actualizar_mensaje('El jugador '+signos_jugadores[contador_jugadas % 2]+' ha ganado') #INFORMAMOS DE QUIEN HA GANADO
            game_on = False
        elif (evaluar_tablas()):
            limpiar_parrilla(1,0) #LIMPIAMOS LA ZONA DE MENSAJE
            actualizar_mensaje('Tablas') #INFORMAMOS DE LAS TABLAS
            time.sleep(3) #ESPERAMOS PARA MOSTRAR LA OPCIÓN DE HACER OTR JUAGADA
            limpiar_parrilla(1,0) #LIMPIAMOS LA ZONA DE MENSAJE
            preguntar_repetir_partida() #PREGUNTAMOS SI QUIERE VOLVER A JUGAR
        #INCREMENTAMOS JUGADA
        contador_jugadas += 1
        if orden_jugadores[contador_jugadas % 2] != 'P': jugar_player() #SI ES TURNO DE LA IA, LLAMAMOS A LA FUNCIÓN PARA QUE JUEGUE

#MANTENEMOS LA VENTANA ABIERTA
ventana_juego.mainloop()