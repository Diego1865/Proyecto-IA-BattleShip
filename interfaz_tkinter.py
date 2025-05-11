# interfaz_tkinter.py

import tkinter as tk
from tkinter import messagebox
from logica_juego import (
    crear_tablero, colocar_barcos_aleatorios, disparar, todos_los_barcos_hundidos,
    disparo_cpu
)
from config import TAMANO_TABLERO

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

    def crear_tableros(self):
        for fila in range(TAMANO_TABLERO):
            fila_botones_jugador = []
            fila_botones_computadora = []
            for col in range(TAMANO_TABLERO):
                # Tablero jugador (sólo visual)
                b_j = tk.Label(self.frame_jugador, width=2, height=1, bg="lightblue", relief="ridge", borderwidth=1)
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

    def deshabilitar_tablero(self):
        for fila in self.botones_computadora:
            for btn in fila:
                btn.config(state="disabled")
