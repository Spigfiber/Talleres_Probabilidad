import numpy as np
import pandas as pd
from .datos import ConjuntoDatos


class DistribucionFrecuencias:
    """
    Construye la tabla de frecuencias para los 60 datos aleatorios.
    Aplica Sturges: k = 1 + 3.322 * log10(60) = 6.907 ≈ 7
    Amplitud: A = ceil(97 / 7) = 14
    Inicio: xmin = 2
    Intervalos resultantes: [2,16), [16,30), [30,44), [44,58), [58,72), [72,86), [86,100)
    """

    def __init__(self, conjunto: ConjuntoDatos) -> None:
        self.conjunto = conjunto
        self.tabla: pd.DataFrame | None = None
        self.k: int = 0
        self.k_exacto: float = 0.0
        self.amplitud: float = 0.0
        self.rango: float = 0.0
        self.inicio: float = 0.0

    def calcular(self) -> "DistribucionFrecuencias":
        """Aplica la regla de Sturges para calcular intervalos y construir la tabla de frecuencias."""
        self.rango = self.conjunto.maximo - self.conjunto.minimo
        """k se redondea al entero mas cercano (6.907 → 7).
        A se redondea al entero superior: ceil(97/7) = 14.
        Se empieza desde xmin = 2.
        """
        self.rango = self.conjunto.maximo - self.conjunto.minimo
        self.k_exacto = 1 + 3.322 * np.log10(self.conjunto.cantidad)
        self.k = int(np.round(self.k_exacto))

        amplitud_cruda = self.rango / self.k
        self.amplitud = float(np.ceil(amplitud_cruda))   # 13.857 → 14

        self.inicio = float(self.conjunto.minimo)         # = 2
        self.tabla = self.construir_tabla()
        return self

    def construir_tabla(self) -> pd.DataFrame:
        """Construye la tabla con intervalos, frecuencias absolutas y relativas acumuladas."""
        datos = self.conjunto.valores
        n = self.conjunto.cantidad
        filas = []

        for i in range(self.k):
            lb = self.inicio + i * self.amplitud
            ub = lb + self.amplitud
            es_ultimo = i == self.k - 1

            if es_ultimo:
                mascara = (datos >= lb) & (datos <= ub)
            else:
                mascara = (datos >= lb) & (datos < ub)

            fi = int(mascara.sum())
            marca = (lb + ub) / 2.0
            etiqueta = f"[{int(lb):2d},{int(ub):4d})"

            filas.append({
                "Intervalo": etiqueta,
                "lb": lb,
                "ub": ub,
                "mi": marca,
                "fi": fi,
            })

        df = pd.DataFrame(filas)
        df["Fi"]  = df["fi"].cumsum()
        df["fri"] = df["fi"] / n
        df["Fri"] = df["Fi"] / n
        return df

    @property
    def indice_modal(self) -> int:
        """Devuelve el indice del intervalo que tiene la mayor frecuencia."""
        return int(self.tabla["fi"].idxmax())

    @property
    def clase_modal(self) -> str:
        """Devuelve el intervalo (clase) que tiene mayor frecuencia."""
        return str(self.tabla.loc[self.indice_modal, "Intervalo"])

    @property
    def frecuencia_modal(self) -> int:
        """Devuelve la mayor frecuencia encontrada (cantidad de datos en la clase modal)."""
        return int(self.tabla["fi"].max())

    def datos_del_intervalo(self, indice: int) -> list:
        """Extrae y ordena todos los datos que pertenecen a un intervalo especifico."""
        fila = self.tabla.iloc[indice]
        datos = self.conjunto.valores
        es_ultimo = indice == self.k - 1
        if es_ultimo:
            mascara = (datos >= fila["lb"]) & (datos <= fila["ub"])
        else:
            mascara = (datos >= fila["lb"]) & (datos < fila["ub"])
        return sorted(int(v) for v in datos[mascara].tolist())
