from config import BARCOS, TAMANO_TABLERO
import random

def crear_tablero():
    return [["_"] * TAMANO_TABLERO for _ in range(TAMANO_TABLERO)]


def mostrar_tablero(tablero, ocultar=False):
    for fila in tablero:
        if ocultar:
            print(" ".join("█" if celda in [b["inicial"] for b in BARCOS.values()] else celda for celda in fila))
        else:
            print(" ".join(fila))


def colocar_barco(tablero, fila, col, nombre_barco, orientacion):
    barco = BARCOS[nombre_barco]
    tamaño = barco["tamaño"]
    inicial = barco["inicial"]

    if orientacion == "H":
        if col + tamaño > TAMANO_TABLERO:
            return False
        for i in range(tamaño):
            if tablero[fila][col + i] != "_":
                return False
        for i in range(tamaño):
            tablero[fila][col + i] = inicial
    elif orientacion == "V":
        if fila + tamaño > TAMANO_TABLERO:
            return False
        for i in range(tamaño):
            if tablero[fila + i][col] != "_":
                return False
        for i in range(tamaño):
            tablero[fila + i][col] = inicial
    else:
        return False

    return True


def colocar_barcos_aleatorios(tablero):
    for nombre in BARCOS:
        colocado = False
        while not colocado:
            fila = random.randint(0, TAMANO_TABLERO - 1)
            col = random.randint(0, TAMANO_TABLERO - 1)
            orientacion = random.choice(["H", "V"])
            colocado = colocar_barco(tablero, fila, col, nombre, orientacion)


def disparar(tablero_objetivo, tablero_disparo, fila, col):
    if tablero_disparo[fila][col] != "_":
        return "repetido"

    if tablero_objetivo[fila][col] in [b["inicial"] for b in BARCOS.values()]:
        tablero_disparo[fila][col] = "X"
        return "acierto"
    else:
        tablero_disparo[fila][col] = "O"
        return "agua"


def disparo_cpu(tablero_objetivo, tablero_disparo, disparos_realizados):
    while True:
        fila = random.randint(0, TAMANO_TABLERO - 1)
        col = random.randint(0, TAMANO_TABLERO - 1)
        if (fila, col) not in disparos_realizados:
            disparos_realizados.add((fila, col))
            resultado = disparar(tablero_objetivo, tablero_disparo, fila, col)
            return fila, col, resultado


def todos_los_barcos_hundidos(tablero_objetivo, tablero_disparo):
    for fila in range(TAMANO_TABLERO):
        for col in range(TAMANO_TABLERO):
            if tablero_objetivo[fila][col] in [b["inicial"] for b in BARCOS.values()] and tablero_disparo[fila][col] != "X":
                return False
    return True