import numpy as np
from scipy import stats as scipy_stats
from .datos import ConjuntoDatos

## Este modulo contiene las clases que calculan las medidas estadisticas
class MedidasCentralizacion:
    """
    Calcula media, mediana y moda sobre los promedios academicos de la muestra.
    El caso de la moda es especial aqui porque la distribucion es bimodal
    (dos valores con la misma frecuencia maxima).
    """

    UMBRAL_SESGO = 0.05
# El umbral de sesgo se usa para interpretar si la media y la mediana son
# suficientemente diferentes como para decir que la distribucion esta sesgada.
    def __init__(self, conjunto: ConjuntoDatos) -> None:
        self.conjunto = conjunto
        self.media: float = 0.0
        self.mediana: float = 0.0
        self.moda = None
        self.veces_moda: int = 0
        self.posicion_baja: float = 0.0
        self.posicion_alta: float = 0.0
        self.tabla_frecuencias: dict = {}
# La moda puede ser un numero o una lista de numeros si hay empate entre varios valores.
    def calcular(self) -> "MedidasCentralizacion":
        """Ejecuta los tres calculos y devuelve self para poder encadenar llamadas."""
        self.calcular_media()
        self.calcular_mediana()
        self.calcular_moda()
        return self
# La media es sensible a valores extremos, la mediana no. Si la media es mucho mayor que la mediana, la distribucion esta sesgada a la derecha (cola hacia los valores altos).
    def calcular_media(self) -> None:
        """Media: suma de todos los promedios dividida entre el numero de estudiantes."""
        self.media = self.conjunto.suma / self.conjunto.cantidad
# La mediana es el valor central de los datos ordenados. Para n par, es el promedio de los dos valores centrales.
    def calcular_mediana(self) -> None:
        """
        Para n par, la mediana es el promedio de los valores en las posiciones
        n/2 y n/2 mas uno. Con n igual a 36 son las posiciones 18 y 19.
        """
        n = self.conjunto.cantidad
        ordenados = self.conjunto.ordenados
        self.posicion_baja = float(ordenados[n // 2 - 1])
        self.posicion_alta = float(ordenados[n // 2])
        self.mediana = (self.posicion_baja + self.posicion_alta) / 2.0
# La moda es el valor que mas se repite. En este caso hay un empate entre 3.8 y 4.0, ambos con frecuencia 4.
    def calcular_moda(self) -> None:
        """
        Busca los valores con mayor frecuencia. Si hay empate entre varios
        valores los guarda todos como una lista (distribucion multimodal).
        En este informe los datos son bimodales: 3.8 y 4.0 empatan en frecuencia.
        """
        valores, conteos = np.unique(
            np.round(self.conjunto.valores, 2), return_counts=True
        )
        self.tabla_frecuencias = dict(zip(valores.tolist(), conteos.tolist()))
        maximo_conteo = int(conteos.max())
        ganadores = valores[conteos == maximo_conteo]
        if len(ganadores) == 1:
            self.moda = float(ganadores[0])
        else:
            self.moda = [float(v) for v in ganadores]
        self.veces_moda = maximo_conteo
# La diferencia entre media y mediana se interpreta como un indicador de sesgo.
    @property
    def es_bimodal(self) -> bool:
        """Indica si la distribucion tiene mas de una moda."""
        return isinstance(self.moda, list)
# La representacion textual de la moda muestra todos los valores ganadores separados por "y" si hay empate.
    @property
    def moda_texto(self) -> str:
        """Representacion textual de la moda, lista para mostrar en pantalla."""
        if self.es_bimodal:
            return "  y  ".join(str(m) for m in self.moda)
        return str(self.moda)

# La diferencia entre media y mediana se interpreta como un indicador de sesgo. 
# Si la media es mucho mayor que la mediana, la distribucion esta sesgada a la derecha (cola hacia los valores altos). 
# Si la media es mucho menor que la mediana, la distribucion esta sesgada a la izquierda (cola hacia los valores bajos). 
# Si la media y la mediana son aproximadamente iguales, la distribucion es simetrica.
class MedidasDispersion:
    """
    Calcula rango, varianza poblacional y desviacion estandar sobre
    los promedios academicos. Con datos en escala 0 a 5 los valores
    son mucho mas pequenos que en el informe anterior, pero la
    interpretacion es la misma.
    """

    def __init__(self, conjunto: ConjuntoDatos, media: float) -> None:
        self.conjunto = conjunto
        self.media = media
        self.rango: float = 0.0
        self.suma_cuadrados: float = 0.0
        self.varianza: float = 0.0
        self.desviacion: float = 0.0

    def calcular(self) -> "MedidasDispersion":
        """Calcula todas las medidas de dispersion y devuelve self."""
        datos = self.conjunto.valores.astype(float)
        n = self.conjunto.cantidad

        self.rango = self.conjunto.maximo - self.conjunto.minimo
        self.suma_cuadrados = float((datos ** 2).sum())

        # Varianza poblacional con formula computacional
        self.varianza = self.suma_cuadrados / n - self.media ** 2
        self.desviacion = float(np.sqrt(self.varianza))
        return self

    @property
    def coeficiente_variacion(self) -> float:
        """CV en porcentaje: que tan dispersos estan los datos respecto a la media."""
        return (self.desviacion / self.media) * 100.0

    def intervalo_sigma(self, k: int) -> tuple:
        """Intervalo de media menos k sigmas hasta media mas k sigmas."""
        return (self.media - k * self.desviacion, self.media + k * self.desviacion)

    def conteo_en_intervalo(self, k: int) -> int:
        """Cuantos promedios reales caen dentro del intervalo de k sigmas."""
        bajo, alto = self.intervalo_sigma(k)
        datos = self.conjunto.valores
        return int(((datos >= bajo) & (datos <= alto)).sum())

# Esta clase representa el procedimiento de muestreo por conglomerados aplicado en este informe.
class FormaDistribucion:
    """
    Analiza si la distribucion de promedios esta sesgada y si es
    mas puntiaguda o aplanada que una normal.
    En este informe el sesgo es negativo porque los semestres avanzados
    tienen mejores notas pero hay pocos estudiantes con notas muy bajas
    que jalan la media hacia abajo.
    """

    UMBRAL_SESGO = 0.05
    UMBRAL_CURTOSIS = 0.5

    def __init__(
        self,
        conjunto: ConjuntoDatos,
        media: float,
        mediana: float,
        desviacion: float,
    ) -> None:
        self.conjunto = conjunto
        self.media = media
        self.mediana = mediana
        self.desviacion = desviacion
        self.asimetria: float = 0.0
        self.curtosis: float = 0.0

    def calcular(self) -> "FormaDistribucion":
        """Calcula asimetria y curtosis de exceso para la muestra."""
        datos = self.conjunto.valores
        self.asimetria = float(scipy_stats.skew(datos, bias=True))
        self.curtosis = float(scipy_stats.kurtosis(datos, bias=True))
        return self

    @property
    def diferencia_media_mediana(self) -> float:
        """Negativa indica sesgo a la izquierda (cola hacia los valores bajos)."""
        return self.media - self.mediana

    @property
    def etiqueta_asimetria(self) -> str:
        if self.asimetria > self.UMBRAL_SESGO:
            return "Positiva (cola a la derecha)"
        if self.asimetria < -self.UMBRAL_SESGO:
            return "Negativa (cola a la izquierda)"
        return "Aproximadamente simetrica"

    @property
    def etiqueta_curtosis(self) -> str:
        if self.curtosis > self.UMBRAL_CURTOSIS:
            return "Leptocurtica (pico pronunciado)"
        if self.curtosis < -self.UMBRAL_CURTOSIS:
            return "Platicurtica (distribucion aplanada)"
        return "Mesocurtica (similar a la normal)"

    def densidad_kde(self, rango_x: np.ndarray) -> np.ndarray:
        """Densidad empirica suavizada con KDE gaussiano (ancho de banda Silverman)."""
        estimador = scipy_stats.gaussian_kde(self.conjunto.valores, bw_method="silverman")
        return estimador(rango_x)

    def curva_normal(self, rango_x: np.ndarray) -> np.ndarray:
        """Normal de referencia con la misma media y sigma que la muestra."""
        return scipy_stats.norm.pdf(rango_x, loc=self.media, scale=self.desviacion)

    def puntos_qq(self) -> tuple:
        """Cuantiles teoricos y observados para el grafico QQ."""
        (teoricos, observados), (pendiente, intercepto, r) = scipy_stats.probplot(
            self.conjunto.valores
        )
        return teoricos, observados, pendiente, intercepto, float(r)