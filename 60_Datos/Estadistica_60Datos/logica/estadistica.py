import numpy as np
from scipy import stats as scipy_stats
from .datos import ConjuntoDatos


class MedidasCentralizacion:
    """
    Calcula media, mediana y moda sobre los 60 datos aleatorios.
    El conjunto es unimodal: solo el 55 se repite (dos veces).
    Media (50.65) y mediana (50.5) son casi identicas, lo que indica
    una distribucion practicamente simetrica.
    """

    def __init__(self, conjunto: ConjuntoDatos) -> None:
        self.conjunto = conjunto
        self.media: float = 0.0
        self.mediana: float = 0.0
        self.moda = None
        self.veces_moda: int = 0
        self.posicion_baja: float = 0.0
        self.posicion_alta: float = 0.0
        self.tabla_frecuencias: dict = {}

    def calcular(self) -> "MedidasCentralizacion":
        """Calcula la media, mediana y moda del conjunto de datos."""
        self.calcular_media()
        self.calcular_mediana()
        self.calcular_moda()
        return self

    def calcular_media(self) -> None:
        """Calcula el promedio de todos los datos sumando y dividiendo entre n."""
        self.media = self.conjunto.suma / self.conjunto.cantidad

    def calcular_mediana(self) -> None:
        """Encuentra el valor central de los datos ordenados.
        Con n par, promedia los dos valores del medio."""
        n = self.conjunto.cantidad
        ordenados = self.conjunto.ordenados
        self.posicion_baja = float(ordenados[n // 2 - 1])
        self.posicion_alta = float(ordenados[n // 2])
        self.mediana = (self.posicion_baja + self.posicion_alta) / 2.0

    def calcular_moda(self) -> None:
        """Encuentra el valor que mas veces aparece en el conjunto.
        Puede haber una o varias modas (unimodal o multimodal)."""
        valores, conteos = np.unique(self.conjunto.valores, return_counts=True)
        self.tabla_frecuencias = dict(zip(valores.tolist(), conteos.tolist()))
        maximo_conteo = int(conteos.max())
        ganadores = valores[conteos == maximo_conteo]
        if len(ganadores) == 1:
            self.moda = float(ganadores[0])
        else:
            self.moda = [float(v) for v in ganadores]
        self.veces_moda = maximo_conteo

    @property
    def es_multimodal(self) -> bool:
        return isinstance(self.moda, list)

    @property
    def moda_texto(self) -> str:
        if self.es_multimodal:
            return "  y  ".join(str(int(m)) for m in self.moda)
        return str(int(self.moda)) if self.moda == int(self.moda) else str(self.moda)


class MedidasDispersion:
    """
    Calcula rango, varianza poblacional y desviacion estandar.
    Con datos entre 2 y 99, el rango es 97 y sigma aprox 25.84,
    lo que da un CV aprox 51%, indicando alta variabilidad relativa.
    """

    def __init__(self, conjunto: ConjuntoDatos, media: float) -> None:
        self.conjunto = conjunto
        self.media = media
        self.rango: float = 0.0
        self.suma_cuadrados: float = 0.0
        self.varianza: float = 0.0
        self.desviacion: float = 0.0

    def calcular(self) -> "MedidasDispersion":
        """Calcula rango, varianza, desviacion estandar y coeficiente de variacion."""
        datos = self.conjunto.valores.astype(float)
        n = self.conjunto.cantidad
        self.rango = self.conjunto.maximo - self.conjunto.minimo
        self.suma_cuadrados = float((datos ** 2).sum())
        self.varianza = self.suma_cuadrados / n - self.media ** 2
        self.desviacion = float(np.sqrt(self.varianza))
        return self

    @property
    def coeficiente_variacion(self) -> float:
        """Mide la variabilidad relativa en porcentaje (desviacion / media * 100).
        Valores altos indican que los datos estan muy dispersos."""
        return (self.desviacion / self.media) * 100.0

    def intervalo_sigma(self, k: int) -> tuple:
        """Calcula el intervalo (media +/- k*sigma) para k desviaciones estandar."""
        return (self.media - k * self.desviacion, self.media + k * self.desviacion)

    def conteo_en_intervalo(self, k: int) -> int:
        """Cuenta cuantos datos caen dentro del intervalo sigma definido por k."""
        bajo, alto = self.intervalo_sigma(k)
        datos = self.conjunto.valores
        return int(((datos >= bajo) & (datos <= alto)).sum())


class FormaDistribucion:
    """
    Analiza asimetria y curtosis de los 60 datos.

    OPTIMIZACION: el estimador KDE (gaussian_kde) se construye una sola vez
    en _estimador_kde() y se reutiliza en todas las llamadas a densidad_kde().
    Antes se instanciaba un estimador nuevo en cada llamada, lo cual era la
    operacion mas cara del modulo al evaluar 500 puntos con scipy cada vez.
    """

    UMBRAL_SESGO    = 0.05
    UMBRAL_CURTOSIS = 0.5

    def __init__(
        self,
        conjunto: ConjuntoDatos,
        media: float,
        mediana: float,
        desviacion: float,
    ) -> None:
        self.conjunto   = conjunto
        self.media      = media
        self.mediana    = mediana
        self.desviacion = desviacion
        self.asimetria: float = 0.0
        self.curtosis:  float = 0.0
        self._kde = None          # se construye una sola vez en el primer uso

    def calcular(self) -> "FormaDistribucion":
        """Calcula el coeficiente de asimetria (sesgo) y curtosis de los datos."""
        datos = self.conjunto.valores
        self.asimetria = float(scipy_stats.skew(datos, bias=True))
        self.curtosis  = float(scipy_stats.kurtosis(datos, bias=True))
        return self

    # ------------------------------------------------------------------ #
    #  KDE con lazy init: se instancia una vez y se reutiliza             #
    # ------------------------------------------------------------------ #
    def _estimador_kde(self):
        """Devuelve el estimador KDE, construyendolo solo la primera vez."""
        if self._kde is None:
            self._kde = scipy_stats.gaussian_kde(
                self.conjunto.valores, bw_method="silverman"
            )
        return self._kde

    def densidad_kde(self, rango_x: np.ndarray) -> np.ndarray:
        """Evalua la densidad sobre rango_x reutilizando el estimador cacheado."""
        return self._estimador_kde()(rango_x)

    def curva_normal(self, rango_x: np.ndarray) -> np.ndarray:
        """Calcula los valores de la curva normal teorica para comparar con los datos."""
        return scipy_stats.norm.pdf(rango_x, loc=self.media, scale=self.desviacion)

    def puntos_qq(self) -> tuple:
        """Genera los puntos para un grafico Q-Q (Quantile-Quantile) para comparar con la normal."""
        (teoricos, observados), (pendiente, intercepto, r) = scipy_stats.probplot(
            self.conjunto.valores
        )
        return teoricos, observados, pendiente, intercepto, float(r)

    @property
    def diferencia_media_mediana(self) -> float:
        """Devuelve la diferencia (media menos mediana) para evaluar el sesgo."""
        return self.media - self.mediana

    @property
    def etiqueta_asimetria(self) -> str:
        """Devuelve una descripcion textual del tipo de asimetria segun el coeficiente calculado."""
        if self.asimetria > self.UMBRAL_SESGO:
            return "Positiva (cola a la derecha)"
        if self.asimetria < -self.UMBRAL_SESGO:
            return "Negativa (cola a la izquierda)"
        return "Aproximadamente simetrica"

    @property
    def etiqueta_curtosis(self) -> str:
        """Devuelve una descripcion textual del tipo de curtosis segun el coeficiente calculado."""
        if self.curtosis > self.UMBRAL_CURTOSIS:
            return "Leptocurtica (pico pronunciado)"
        if self.curtosis < -self.UMBRAL_CURTOSIS:
            return "Platicurtica (distribucion aplanada)"
        return "Mesocurtica (similar a la normal)"
