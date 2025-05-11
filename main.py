from logica_juego import (
    crear_tablero,
    mostrar_tablero,
    colocar_barcos_aleatorios,
    disparar,
    disparo_cpu,
    todos_los_barcos_hundidos
)
from config import TAMANO_TABLERO
import os

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_coordenadas():
    while True:
        try:
            fila = int(input("Fila (0-9): "))
            col = int(input("Columna (0-9): "))
            if 0 <= fila < TAMANO_TABLERO and 0 <= col < TAMANO_TABLERO:
                return fila, col
            else:
                print("Coordenadas fuera de rango.")
        except ValueError:
            print("Entrada inválida, escribe un número.")


def main():
    limpiar_pantalla()
    print("=== ¡Bienvenido a BattleShip! ===\n")

    # Tableros del jugador
    tablero_jugador = crear_tablero()
    disparos_recibidos_jugador = crear_tablero()

    # Tableros de la computadora
    tablero_computadora = crear_tablero()
    disparos_recibidos_computadora = crear_tablero()
    disparos_cpu_hechos = set()

    print("Colocando barcos aleatoriamente...\n")
    colocar_barcos_aleatorios(tablero_jugador)
    colocar_barcos_aleatorios(tablero_computadora)

    turno = 0

    while True:
        limpiar_pantalla()
        print(f"--- Turno {turno + 1} ---")
        print("\nTu tablero:")
        mostrar_tablero(tablero_jugador)

        print("\nDisparos realizados a la computadora:")
        mostrar_tablero(disparos_recibidos_computadora, ocultar=True)

        print("\nEs tu turno de disparar.")
        fila, col = pedir_coordenadas()
        resultado = disparar(tablero_computadora, disparos_recibidos_computadora, fila, col)

        if resultado == "acierto":
            print("💥 ¡Impacto!")
        elif resultado == "agua":
            print("Agua...")
        elif resultado == "repetido":
            print("Ya habías disparado ahí.")
            input("Presiona Enter para continuar...")
            continue

        if todos_los_barcos_hundidos(tablero_computadora, disparos_recibidos_computadora):
            print("\n¡Felicidades! ¡Has ganado la batalla!")
            break

        print("\nTurno de la computadora...")
        fila_cpu, col_cpu, resultado_cpu = disparo_cpu(tablero_jugador, disparos_recibidos_jugador, disparos_cpu_hechos)

        if resultado_cpu == "acierto":
            print(f"💥 La computadora te dio en ({fila_cpu}, {col_cpu})")
        else:
            print(f"💨 La computadora falló en ({fila_cpu}, {col_cpu})")

        if todos_los_barcos_hundidos(tablero_jugador, disparos_recibidos_jugador):
            print("\n ¡La computadora ha ganado! Mejor suerte la próxima.")
            break

        input("\nPresiona Enter para el siguiente turno...")
        turno += 1


if __name__ == "__main__":
    main()