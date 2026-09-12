"""Demostracion completa de AeroCargo-Matrix."""

from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


def mostrar_matriz(matriz, sufijo=""):
    for fila in matriz:
        valores = "  ".join(f"{valor:8.2f}{sufijo}" for valor in fila)
        print(f"[ {valores} ]")


def main():
    # Cada fila va de proa a popa; cada columna, de izquierda a derecha.
    cargas = [
        [400, 550, 300, 350],
        [450, 700, 600, 400],
        [300, 350, 450, 300],
    ]
    capacidades = [
        [500, 500, 500, 500],
        [500, 600, 500, 500],
        [500, 500, 500, 500],
    ]
    tolerancia = 200
    k, p = 2, 2

    print("=" * 62)
    print("AEROCARGO-MATRIX: AUDITORIA DE DISTRIBUCION DE CARGA")
    print("=" * 62)

    if not validar_matrices(cargas, capacidades):
        print("ERROR: las matrices no cumplen los requisitos.")
        return
    print("\nVALIDACION: matrices validas.")

    porcentajes, sobrecargas = calcular_ocupacion(cargas, capacidades)
    print("\nPORCENTAJES DE OCUPACION")
    mostrar_matriz(porcentajes, "%")
    print("\nCeldas sobrecargadas (fila, columna):", sobrecargas or "Ninguna")

    pesos_fila, desbalance, aprobado = evaluar_balance(cargas, tolerancia)
    print("\nDISTRIBUCION LONGITUDINAL")
    for indice, peso in enumerate(pesos_fila):
        print(f"Fila {indice}: {peso:.2f} kg")
    print("\nBALANCE LATERAL")
    print(f"Desbalance: {desbalance:.2f} kg")
    print(f"Tolerancia: {tolerancia:.2f} kg")
    print("Estado:", "APROBADO" if aprobado else "RECHAZADO")

    critica = extraer_submatriz_critica(porcentajes, k, p)
    promedio = sum(sum(fila) for fila in critica) / (k * p)
    print(f"\nSUBMATRIZ CRITICA {k} x {p}")
    mostrar_matriz(critica, "%")
    print(f"Promedio de ocupacion: {promedio:.2f}%")
    print("=" * 62)


if __name__ == "__main__":
    main()
