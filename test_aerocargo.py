"""Pruebas unitarias para AeroCargo-Matrix (biblioteca unittest)."""

import unittest

from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


class PruebasAeroCargo(unittest.TestCase):
    def test_validacion_correcta_matriz_minima(self):
        self.assertTrue(validar_matrices([[0, 10], [20, 30]], [[1, 10], [20, 30]]))

    def test_validacion_rechaza_casos_invalidos(self):
        self.assertFalse(validar_matrices([[1, 2]], [[2, 2]]))
        self.assertFalse(validar_matrices([[1, 2], [3]], [[2, 2], [2, 2]]))
        self.assertFalse(validar_matrices([[1, -2], [3, 4]], [[2, 2], [2, 2]]))
        self.assertFalse(validar_matrices([[1, 2], [3, 4]], [[2, 0], [2, 2]]))
        self.assertFalse(validar_matrices([[1, 2], [3, 4]], [[2, 2], [2, 2], [2, 2]]))

    def test_ocupacion_y_sobrecargas(self):
        ocupacion, sobrecargas = calcular_ocupacion(
            [[50, 120], [0, 200]], [[100, 100], [50, 200]]
        )
        self.assertEqual(ocupacion, [[50.0, 120.0], [0.0, 100.0]])
        self.assertEqual(sobrecargas, [(0, 1)])

    def test_balance_columnas_pares(self):
        filas, desbalance, aprobado = evaluar_balance([[10, 20], [30, 40]], 20)
        self.assertEqual(filas, [30, 70])
        self.assertEqual(desbalance, 20)
        self.assertTrue(aprobado)

    def test_balance_columnas_impares_omite_centro(self):
        filas, desbalance, aprobado = evaluar_balance([[10, 999, 20], [30, 999, 40]], 20)
        self.assertEqual(filas, [1029, 1069])
        self.assertEqual(desbalance, 20)
        self.assertTrue(aprobado)

    def test_submatriz_critica(self):
        matriz = [[10, 20, 30], [40, 100, 110], [50, 120, 130]]
        self.assertEqual(extraer_submatriz_critica(matriz, 2, 2), [[100, 110], [120, 130]])

    def test_ventana_igual_a_matriz(self):
        matriz = [[10, 20], [30, 40]]
        self.assertEqual(extraer_submatriz_critica(matriz, 2, 2), matriz)

    def test_ventana_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            extraer_submatriz_critica([[10, 20], [30, 40]], 3, 2)


if __name__ == "__main__":
    unittest.main()
