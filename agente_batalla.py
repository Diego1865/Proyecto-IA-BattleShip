import random
from config import TAMANO_TABLERO

class AgenteBattleship:
    def __init__(self):
        self.disparos_realizados = set()
        self.en_caceria = True
        self.objetivos_pendientes = []

    def siguiente_disparo(self, tablero_objetivo, tablero_disparo):
        if self.en_caceria:
            return self.modo_caceria(tablero_objetivo, tablero_disparo)
        else:
            return self.modo_direccion(tablero_objetivo, tablero_disparo)

    def modo_caceria(self, tablero_objetivo, tablero_disparo):
        while True:
            fila = random.randint(0, TAMANO_TABLERO - 1)
            col = random.randint(0, TAMANO_TABLERO - 1)
            if (fila, col) not in self.disparos_realizados:
                self.disparos_realizados.add((fila, col))
                resultado = self.evaluar_disparo(tablero_objetivo, tablero_disparo, fila, col)
                if resultado == "acierto":
                    self.en_caceria = False
                    self.objetivos_pendientes = self.vecinos_validos(fila, col, tablero_disparo)
                return fila, col, resultado

    def modo_direccion(self, tablero_objetivo, tablero_disparo):
        while self.objetivos_pendientes:
            fila, col = self.objetivos_pendientes.pop(0)
            if (fila, col) in self.disparos_realizados:
                continue
            self.disparos_realizados.add((fila, col))
            resultado = self.evaluar_disparo(tablero_objetivo, tablero_disparo, fila, col)
            if resultado == "acierto":
                self.objetivos_pendientes += self.vecinos_validos(fila, col, tablero_disparo)
            else:
                if not self.objetivos_pendientes:
                    self.en_caceria = True
            return fila, col, resultado

        self.en_caceria = True
        return self.modo_caceria(tablero_objetivo, tablero_disparo)

    def evaluar_disparo(self, tablero_objetivo, tablero_disparo, fila, col):
        if tablero_objetivo[fila][col] in ["A", "B", "C", "S", "F"]:
            tablero_disparo[fila][col] = "X"
            return "acierto"
        else:
            tablero_disparo[fila][col] = "O"
            return "agua"

    def vecinos_validos(self, fila, col, tablero_disparo):
        vecinos = []
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nf, nc = fila + df, col + dc
            if 0 <= nf < TAMANO_TABLERO and 0 <= nc < TAMANO_TABLERO:
                if tablero_disparo[nf][nc] == "_":
                    vecinos.append((nf, nc))
        return vecinos