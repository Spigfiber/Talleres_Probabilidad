import numpy as np


# Los tres conglomerados seleccionados con sus 12 promedios academicos cada uno
# La seleccion fue aleatoria: quedaron los semestres II, IV y VI de seis posibles
DATOS_POR_CONGLOMERADO = {
    "Semestre II  (C2)":  np.array([3.2, 2.9, 3.5, 3.8, 2.7, 4.0, 3.0, 3.5, 2.5, 3.9, 3.3, 3.0]),
    "Semestre IV (C4)":  np.array([3.5, 4.0, 3.8, 3.2, 4.3, 3.6, 2.9, 4.0, 3.7, 3.5, 4.1, 3.8]),
    "Semestre VI (C6)":  np.array([4.1, 3.8, 4.5, 4.0, 3.8, 4.3, 3.6, 4.5, 3.9, 4.2, 4.0, 3.7]),
}

# Todos los conglomerados de la poblacion, incluyendo los no seleccionados
TODOS_LOS_CONGLOMERADOS = [
    "Semestre I  (C1)",
    "Semestre II  (C2)",
    "Semestre III (C3)",
    "Semestre IV (C4)",
    "Semestre V  (C5)",
    "Semestre VI (C6)",
]

# Los seleccionados para la muestra
CONGLOMERADOS_SELECCIONADOS = ["Semestre II  (C2)", "Semestre IV (C4)", "Semestre VI (C6)"]

# Parametros generales de la poblacion
ESTUDIANTES_POR_SEMESTRE = 12
TOTAL_SEMESTRES = 6
N_POBLACION = TOTAL_SEMESTRES * ESTUDIANTES_POR_SEMESTRE


class ConjuntoDatos:
    """
    Guarda los promedios academicos de la muestra, organizados por conglomerado.
    Ofrece acceso a los datos completos, por semestre individual y ordenados.
    No hace calculos estadisticos, eso lo manejan otras clases.
    """

    def __init__(self, datos_por_conglomerado: dict) -> None:
        # Guardamos una copia del diccionario para no modificar el original
        self.por_conglomerado = {
            nombre: np.array(vals, dtype=float)
            for nombre, vals in datos_por_conglomerado.items()
        }

    @property
    def valores(self) -> np.ndarray:
        """Todos los promedios de la muestra como un arreglo plano."""
        return np.concatenate(list(self.por_conglomerado.values()))

    @property
    def ordenados(self) -> np.ndarray:
        """Los promedios de menor a mayor, necesarios para calcular la mediana."""
        return np.sort(self.valores)

    @property
    def cantidad(self) -> int:
        """Cuantos estudiantes hay en la muestra (n)."""
        return len(self.valores)

    @property
    def minimo(self) -> float:
        """El promedio mas bajo de toda la muestra."""
        return float(self.valores.min())

    @property
    def maximo(self) -> float:
        """El promedio mas alto de toda la muestra."""
        return float(self.valores.max())

    @property
    def suma(self) -> float:
        """Suma de todos los promedios, necesaria para calcular la media."""
        return float(self.valores.sum())

    @property
    def suma_por_conglomerado(self) -> dict:
        """Suma de promedios de cada semestre seleccionado."""
        return {nombre: float(vals.sum()) for nombre, vals in self.por_conglomerado.items()}

    @property
    def nombres_conglomerados(self) -> list:
        """Nombres de los tres semestres seleccionados."""
        return list(self.por_conglomerado.keys())