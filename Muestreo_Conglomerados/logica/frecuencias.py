import numpy as np
import pandas as pd
from .datos import ConjuntoDatos


class DistribucionFrecuencias:
    """
    Construye la tabla de frecuencias para los promedios academicos.
    El informe usa un punto de inicio en 2.4 y amplitud 0.4 para obtener
    limites limpios en la escala de notas. Aqui replicamos ese mismo criterio
    pero tambien calculamos automaticamente si el usuario cambia los datos.
    """

    # En el informe la amplitud se redondea a 0.4 para tener limites mas legibles
    AMPLITUD_MINIMA = 0.1

    def __init__(self, conjunto: ConjuntoDatos) -> None:
        self.conjunto = conjunto
        self.tabla: pd.DataFrame | None = None
        self.k: int = 0
        self.k_exacto: float = 0.0
        self.amplitud: float = 0.0
        self.rango: float = 0.0
        self.inicio: float = 0.0

    def calcular(self) -> "DistribucionFrecuencias":
        """
        Aplica Sturges para k y redondea la amplitud a un decimal limpio.
        El informe usa redondeo hacia abajo para k (6.17 queda en 6) y
        redondea la amplitud a 0.4 partiendo desde 2.4 para tener limites
        limpios en la escala de notas de 0 a 5.
        """
        self.rango = self.conjunto.maximo - self.conjunto.minimo
        self.k_exacto = 1 + 3.322 * np.log10(self.conjunto.cantidad)

        # El informe usa el entero mas cercano hacia abajo (floor), no ceil
        self.k = int(np.floor(self.k_exacto))

        amplitud_cruda = self.rango / self.k
        # Redondeamos al multiplo de 0.1 mas cercano hacia arriba para limites limpios
        self.amplitud = round(np.ceil(amplitud_cruda / 0.1) * 0.1, 1)

        # El inicio se coloca justo por debajo del minimo para incluirlo en el primer intervalo
        self.inicio = round(np.floor(self.conjunto.minimo / self.amplitud) * self.amplitud, 2)

        self.tabla = self.construir_tabla()
        return self

    def construir_tabla(self) -> pd.DataFrame:
        """
        Crea los intervalos, cuenta cuantos promedios caen en cada uno
        y calcula las cuatro frecuencias: fi, Fi, fri y Fri.
        """
        datos = self.conjunto.valores
        n = self.conjunto.cantidad
        filas = []

        for i in range(self.k):
            lb = round(self.inicio + i * self.amplitud, 2)
            ub = round(lb + self.amplitud, 2)
            es_ultimo = i == self.k - 1

            if es_ultimo:
                mascara = (datos >= lb) & (datos <= ub)
            else:
                mascara = (datos >= lb) & (datos < ub)

            fi = int(mascara.sum())
            marca = round((lb + ub) / 2.0, 2)
            etiqueta = f"[{lb:.1f}, {ub:.1f})"

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
        """Posicion del intervalo con mayor frecuencia absoluta."""
        return int(self.tabla["fi"].idxmax())

    @property
    def clase_modal(self) -> str:
        """Etiqueta del intervalo modal."""
        return str(self.tabla.loc[self.indice_modal, "Intervalo"])

    @property
    def frecuencia_modal(self) -> int:
        """Cuantos datos tiene el intervalo modal."""
        return int(self.tabla["fi"].max())

    def datos_del_intervalo(self, indice: int) -> list:
        """Lista ordenada de promedios que pertenecen al intervalo indicado."""
        fila = self.tabla.iloc[indice]
        datos = self.conjunto.valores
        es_ultimo = indice == self.k - 1
        if es_ultimo:
            mascara = (datos >= fila["lb"]) & (datos <= fila["ub"])
        else:
            mascara = (datos >= fila["lb"]) & (datos < fila["ub"])
        return sorted(round(v, 2) for v in datos[mascara].tolist())