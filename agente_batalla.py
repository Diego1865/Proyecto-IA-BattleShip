import random
from config import TAMANO_TABLERO, BARCOS

class AgenteBattleship:
    def __init__(self):
        self.disparos_realizados = set()
        self.en_caceria = True
        self.objetivos_pendientes = []
        self.aciertos_actuales = []
        self.direccion_confirmada = None
        self.barcos_restantes = {v["inicial"]: v["tamaño"] for v in BARCOS.values()}

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
                    self.aciertos_actuales = [(fila, col)]
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
                self.aciertos_actuales.append((fila, col))
                if len(self.aciertos_actuales) >= 2 and not self.direccion_confirmada:
                    self.direccion_confirmada = self.detectar_direccion()
                if self.direccion_confirmada:
                    self.extender_en_direccion(tablero_disparo)
                else:
                    self.objetivos_pendientes += self.vecinos_validos(fila, col, tablero_disparo)
            else:
                if not self.objetivos_pendientes:
                    self.resetear_caceria()
            return fila, col, resultado

        self.resetear_caceria()
        return self.modo_caceria(tablero_objetivo, tablero_disparo)

    def evaluar_disparo(self, tablero_objetivo, tablero_disparo, fila, col):
        celda = tablero_objetivo[fila][col]
        if celda in self.barcos_restantes:
            tablero_disparo[fila][col] = "X"

            # ¿El barco fue hundido?
            hundido = True
            for f in range(TAMANO_TABLERO):
                for c in range(TAMANO_TABLERO):
                    if tablero_objetivo[f][c] == celda and tablero_disparo[f][c] != "X":
                        hundido = False
                        break
                if not hundido:
                    break

            if hundido:
                self.barcos_restantes.pop(celda, None)
                self.resetear_caceria()
            else:
                self.en_caceria = False  # Aún quedan partes del barco por encontrar
            return "acierto"
        else:
            tablero_disparo[fila][col] = "O"
            return "agua"

    def vecinos_validos(self, fila, col, tablero_disparo):
        vecinos = []
        for df, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nf, nc = fila + df, col + dc
            if 0 <= nf < TAMANO_TABLERO and 0 <= nc < TAMANO_TABLERO:
                if tablero_disparo[nf][nc] == "_":
                    vecinos.append((nf, nc))
        return vecinos

    def detectar_direccion(self):
        if len(self.aciertos_actuales) < 2:
            return None
        (f1, c1), (f2, c2) = self.aciertos_actuales[-2:]
        if f1 == f2:
            return (0, 1) if c2 > c1 else (0, -1)
        elif c1 == c2:
            return (1, 0) if f2 > f1 else (-1, 0)
        return None

    def extender_en_direccion(self, tablero_disparo):
        if not self.direccion_confirmada:
            return
        df, dc = self.direccion_confirmada
        for base in self.aciertos_actuales:
            for signo in [1, -1]:
                nf, nc = base[0] + df * signo, base[1] + dc * signo
                if 0 <= nf < TAMANO_TABLERO and 0 <= nc < TAMANO_TABLERO:
                    if tablero_disparo[nf][nc] == "_" and (nf, nc) not in self.disparos_realizados:
                        self.objetivos_pendientes.append((nf, nc))

    def resetear_caceria(self):
        self.en_caceria = True
        self.aciertos_actuales.clear()
        self.direccion_confirmada = None