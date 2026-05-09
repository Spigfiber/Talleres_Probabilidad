import numpy as np

# Los 60 datos aleatorios organizados por filas tal como aparecen en el informe
DATOS_FILAS = {
    "Fila 1": np.array([12, 45, 78, 23, 56, 89, 34, 67, 90, 11], dtype=float),
    "Fila 2": np.array([22, 33, 44, 55, 66, 77, 88, 99, 10, 20], dtype=float),
    "Fila 3": np.array([30, 40, 50, 60, 70, 80, 91, 81, 71, 61], dtype=float),
    "Fila 4": np.array([51, 41, 31, 21, 13, 24, 35, 46, 57, 68], dtype=float),
    "Fila 5": np.array([79, 82, 73, 64, 55, 47, 38, 29, 19,  9], dtype=float),
    "Fila 6": np.array([ 2, 14, 26, 37, 48, 59, 63, 74, 85, 96], dtype=float),
}

N_POBLACION = 60
DATOS_POR_FILA = 10
TOTAL_FILAS = 6


class ConjuntoDatos:
    """
    Almacena los 60 datos aleatorios organizados por fila.
    Solo gestiona el acceso a los datos; los calculos estadisticos
    viven en estadistica.py y frecuencias.py.
    """

    def __init__(self, datos_filas: dict) -> None:
        self.por_fila = {
            nombre: np.array(vals, dtype=float)
            for nombre, vals in datos_filas.items()
        }

    @property
    def valores(self) -> np.ndarray:
        """Devuelve todos los 60 datos como un array plano sin estructura de filas."""
        return np.concatenate(list(self.por_fila.values()))

    @property
    def ordenados(self) -> np.ndarray:
        """Devuelve los 60 datos ordenados de menor a mayor, necesarios para calcular la mediana."""
        return np.sort(self.valores)

    @property
    def cantidad(self) -> int:
        """Devuelve la cantidad total de datos, que siempre es 60."""
        return len(self.valores)

    @property
    def minimo(self) -> float:
        """Devuelve el valor mas pequeño en el conjunto."""
        return float(self.valores.min())

    @property
    def maximo(self) -> float:
        """Devuelve el valor mas grande en el conjunto."""
        return float(self.valores.max())

    @property
    def suma(self) -> float:
        """Devuelve la suma total de todos los 60 datos."""
        return float(self.valores.sum())

    @property
    def suma_por_fila(self) -> dict:
        """Devuelve la suma parcial de los 10 datos en cada una de las 6 filas."""
        return {nombre: float(vals.sum()) for nombre, vals in self.por_fila.items()}

    @property
    def nombres_filas(self) -> list:
        """Devuelve la lista de nombres de las 6 filas de datos."""
        return list(self.por_fila.keys())
