# interfaz_tkinter.py

import tkinter as tk
from tkinter import messagebox
from logica_juego import (
    crear_tablero, colocar_barcos_aleatorios, disparar, todos_los_barcos_hundidos,
    disparo_cpu,colocar_barco
)
from config import BARCOS,TAMANO_TABLERO

class BattleshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval")

        # Crear tableros
        self.tablero_jugador = crear_tablero()
        self.tablero_computadora = crear_tablero()
        self.disparos_jugador = crear_tablero()
        self.disparos_computadora = crear_tablero()
        self.disparos_cpu_realizados = set()

        colocar_barcos_aleatorios(self.tablero_jugador)
        colocar_barcos_aleatorios(self.tablero_computadora)

        # Crear marcos de los tableros
        self.frame_jugador = tk.Frame(self.root)
        self.frame_computadora = tk.Frame(self.root)
        self.frame_jugador.grid(row=0, column=0, padx=10, pady=10)
        self.frame_computadora.grid(row=0, column=1, padx=10, pady=10)

        # Mostrar botones
        self.botones_jugador = []
        self.botones_computadora = []
        self.crear_tableros()

        self.barcos_disponibles = list(BARCOS.keys())  # Del config
        self.barco_actual = tk.StringVar()
        self.barco_actual.set(self.barcos_disponibles[0])

        self.orientacion = tk.StringVar()
        self.orientacion.set("H")

        self.barcos_colocados = []

        # Crear menú superior
        self.crear_menu_colocacion()

    def crear_tableros(self):
        for fila in range(TAMANO_TABLERO):
            fila_botones_jugador = []
            fila_botones_computadora = []
            for col in range(TAMANO_TABLERO):
                # Tablero jugador (sólo visual)
                b_j = tk.Button(self.frame_jugador, width=2, height=1, bg="lightblue", relief="ridge", borderwidth=1, command=lambda f=fila, c=col: self.colocar_barco_jugador(f, c))
                b_j.grid(row=fila, column=col)
                if self.tablero_jugador[fila][col] != "_":
                    b_j.config(bg="blue")  # Mostrar barcos
                fila_botones_jugador.append(b_j)

                # Tablero computadora (clickeable)
                b_c = tk.Button(self.frame_computadora, width=2, height=1, command=lambda f=fila, c=col: self.jugador_dispara(f, c))
                b_c.grid(row=fila, column=col)
                fila_botones_computadora.append(b_c)

            self.botones_jugador.append(fila_botones_jugador)
            self.botones_computadora.append(fila_botones_computadora)

    def crear_menu_colocacion(self):
        frame_menu = tk.Frame(self.root)
        frame_menu.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(frame_menu, text="Barco:").pack(side="left", padx=5)
        menu_barco = tk.OptionMenu(frame_menu, self.barco_actual, *self.barcos_disponibles)
        menu_barco.pack(side="left")

        tk.Label(frame_menu, text="Orientación:").pack(side="left", padx=5)
        menu_orientacion = tk.OptionMenu(frame_menu, self.orientacion, "H", "V")
        menu_orientacion.pack(side="left")

    def colocar_barco_jugador(self, fila, col):
        if len(self.barcos_colocados) == len(BARCOS):
            return  # Ya terminó

        nombre = self.barco_actual.get()
        orientacion = self.orientacion.get()

        if nombre in self.barcos_colocados:
            messagebox.showinfo("Ya colocado", f"Ya colocaste el {nombre}.")
            return

        exito = colocar_barco(self.tablero_jugador, fila, col, nombre, orientacion)
        if exito:
            self.barcos_colocados.append(nombre)
            self.actualizar_tablero_jugador()
            if len(self.barcos_colocados) == len(BARCOS):
                messagebox.showinfo("¡Listo!", "Todos los barcos han sido colocados. ¡Comienza la batalla!")
                self.iniciar_juego()
        else:
            messagebox.showerror("Error", "No se pudo colocar el barco ahí.")

    def actualizar_tablero_jugador(self):
        for fila in range(TAMANO_TABLERO):
            for col in range(TAMANO_TABLERO):
                valor = self.tablero_jugador[fila][col]
                if valor != "_":
                    self.botones_jugador[fila][col].config(bg="blue", state="disabled")


    def jugador_dispara(self, fila, col):
        resultado = disparar(self.tablero_computadora, self.disparos_jugador, fila, col)

        if resultado == "repetido":
            messagebox.showinfo("Ya disparaste ahí", "Prueba otra coordenada.")
            return

        btn = self.botones_computadora[fila][col]
        if resultado == "acierto":
            btn.config(text="X", bg="red", state="disabled")
        elif resultado == "agua":
            btn.config(text="O", bg="white", state="disabled")

        if todos_los_barcos_hundidos(self.tablero_computadora, self.disparos_jugador):
            messagebox.showinfo("¡Victoria!", "¡Has hundido toda la flota enemiga!")
            self.deshabilitar_tablero()
            return

        # Turno de la CPU
        fila_cpu, col_cpu, resultado_cpu = disparo_cpu(self.tablero_jugador, self.disparos_computadora, self.disparos_cpu_realizados)
        b_cpu = self.botones_jugador[fila_cpu][col_cpu]
        if resultado_cpu == "acierto":
            b_cpu.config(bg="red")
        else:
            b_cpu.config(bg="white")

        if todos_los_barcos_hundidos(self.tablero_jugador, self.disparos_computadora):
            messagebox.showinfo("Derrota", "La computadora ha hundido toda tu flota...")
            self.deshabilitar_tablero()

    def iniciar_juego(self):
        colocar_barcos_aleatorios(self.tablero_computadora)  # Barcos del CPU

    def deshabilitar_tablero(self):
        for fila in self.botones_computadora:
            for btn in fila:
                btn.config(state="disabled")
