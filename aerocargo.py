"""Funciones puras para auditar una matriz de carga de una aeronave."""


def _es_numero(valor):
    """Indica si valor es numerico, excluyendo booleanos."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_matrices(cargas, capacidades):
    """Valida dimensiones, regularidad y valores de ambas matrices."""
    if not isinstance(cargas, (list, tuple)) or not isinstance(capacidades, (list, tuple)):
        return False
    if len(cargas) < 2 or len(cargas) != len(capacidades):
        return False
    if not isinstance(cargas[0], (list, tuple)) or len(cargas[0]) < 2:
        return False

    columnas = len(cargas[0])
    for fila_cargas, fila_capacidades in zip(cargas, capacidades):
        if not isinstance(fila_cargas, (list, tuple)) or not isinstance(fila_capacidades, (list, tuple)):
            return False
        if len(fila_cargas) != columnas or len(fila_capacidades) != columnas:
            return False
        for peso, capacidad in zip(fila_cargas, fila_capacidades):
            if not _es_numero(peso) or not _es_numero(capacidad):
                return False
            if peso < 0 or capacidad <= 0:
                return False
    return True


def calcular_ocupacion(cargas, capacidades):
    """Devuelve (matriz_porcentajes, coordenadas_sobrecargadas)."""
    if not validar_matrices(cargas, capacidades):
        raise ValueError("Las matrices de cargas y capacidades no son validas.")

    porcentajes = []
    sobrecargas = []
    for i in range(len(cargas)):
        fila_porcentajes = []
        for j in range(len(cargas[i])):
            porcentaje = cargas[i][j] / capacidades[i][j] * 100.0
            fila_porcentajes.append(porcentaje)
            if porcentaje > 100.0:
                sobrecargas.append((i, j))
        porcentajes.append(fila_porcentajes)
    return porcentajes, sobrecargas


def evaluar_balance(cargas, tolerancia):
    """Devuelve (pesos_por_fila, desbalance_lateral, balance_aprobado)."""
    if not _es_numero(tolerancia) or tolerancia < 0:
        raise ValueError("La tolerancia debe ser un numero mayor o igual a cero.")
    if not isinstance(cargas, (list, tuple)) or len(cargas) < 2:
        raise ValueError("La matriz de cargas debe tener al menos dos filas.")
    if not isinstance(cargas[0], (list, tuple)) or len(cargas[0]) < 2:
        raise ValueError("La matriz de cargas debe tener al menos dos columnas.")

    columnas = len(cargas[0])
    pesos_por_fila = []
    peso_izquierdo = 0
    peso_derecho = 0
    mitad = columnas // 2

    for fila in cargas:
        if not isinstance(fila, (list, tuple)) or len(fila) != columnas:
            raise ValueError("La matriz de cargas debe ser regular.")
        if any(not _es_numero(peso) or peso < 0 for peso in fila):
            raise ValueError("Todos los pesos deben ser numericos y no negativos.")
        pesos_por_fila.append(sum(fila))
        peso_izquierdo += sum(fila[:mitad])
        inicio_derecha = mitad if columnas % 2 == 0 else mitad + 1
        peso_derecho += sum(fila[inicio_derecha:])

    desbalance = abs(peso_izquierdo - peso_derecho)
    return pesos_por_fila, desbalance, desbalance <= tolerancia


def extraer_submatriz_critica(porcentajes, k, p):
    """Extrae la ventana k x p contigua con mayor promedio de ocupacion.

    En caso de empate conserva la primera ventana encontrada, recorriendo
    de arriba hacia abajo y de izquierda a derecha.
    """
    if not isinstance(k, int) or isinstance(k, bool) or not isinstance(p, int) or isinstance(p, bool):
        raise ValueError("k y p deben ser numeros enteros.")
    if k <= 0 or p <= 0:
        raise ValueError("k y p deben ser mayores que cero.")
    if not isinstance(porcentajes, (list, tuple)) or not porcentajes:
        raise ValueError("La matriz de porcentajes no puede estar vacia.")
    if not isinstance(porcentajes[0], (list, tuple)) or not porcentajes[0]:
        raise ValueError("La matriz de porcentajes debe ser bidimensional.")

    filas = len(porcentajes)
    columnas = len(porcentajes[0])
    for fila in porcentajes:
        if not isinstance(fila, (list, tuple)) or len(fila) != columnas:
            raise ValueError("La matriz de porcentajes debe ser regular.")
        if any(not _es_numero(valor) for valor in fila):
            raise ValueError("Los porcentajes deben ser numericos.")
    if k > filas or p > columnas:
        raise ValueError("La ventana no puede ser mayor que la matriz.")

    mejor_promedio = None
    mejor_fila = 0
    mejor_columna = 0
    for i in range(filas - k + 1):
        for j in range(columnas - p + 1):
            suma = 0
            for x in range(i, i + k):
                for y in range(j, j + p):
                    suma += porcentajes[x][y]
            promedio = suma / (k * p)
            if mejor_promedio is None or promedio > mejor_promedio:
                mejor_promedio = promedio
                mejor_fila = i
                mejor_columna = j

    submatriz = [
        list(fila[mejor_columna:mejor_columna + p])
        for fila in porcentajes[mejor_fila:mejor_fila + k]
    ]
    return submatriz
