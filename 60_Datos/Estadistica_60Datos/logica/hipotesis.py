import numpy as np
from scipy import stats as scipy_stats


class PruebaHipotesisZ:
    """
    Prueba Z bilateral para la media con sigma poblacional conocida.

    Contexto del informe:
      Poblacion: N=60, mu=50.65, sigma=25.84
      Muestra hipotetica: n=36, x_barra=55.00
      H0: mu = 50    H1: mu != 50    alpha = 0.05

    Se usa prueba Z porque n >= 30 y sigma es conocida (calculada
    sobre la poblacion completa en la Seccion 5 del informe).
    """

    # Parametros del ejemplo del informe (fijos para reproducir exactamente)
    MU0_DEFECTO     = 50.0
    X_BARRA_DEFECTO = 55.0
    SIGMA_DEFECTO   = 25.84
    N_DEFECTO       = 36
    ALPHA_DEFECTO   = 0.05

    def __init__(
        self,
        mu0: float     = MU0_DEFECTO,
        x_barra: float = X_BARRA_DEFECTO,
        sigma: float   = SIGMA_DEFECTO,
        n: int         = N_DEFECTO,
        alpha: float   = ALPHA_DEFECTO,
    ) -> None:
        self.mu0     = mu0
        self.x_barra = x_barra
        self.sigma   = sigma
        self.n       = n
        self.alpha   = alpha

        self.z_calculado: float = 0.0
        self.z_critico:   float = 0.0
        self.valor_p:     float = 0.0
        self.decision:    str   = ""

    def calcular(self) -> "PruebaHipotesisZ":
        """Calcula el estadistico Z, el valor critico, el valor-p y toma la decision estadistica."""
        self.z_calculado = (self.x_barra - self.mu0) / self.error_estandar
        self.z_critico   = float(scipy_stats.norm.ppf(1 - self.alpha / 2))
        self.valor_p     = float(2 * (1 - scipy_stats.norm.cdf(abs(self.z_calculado))))
        self.decision    = (
            "Se rechaza H\u2080"
            if self.en_region_critica
            else "No se rechaza H\u2080"
        )
        return self

    @property
    def error_estandar(self) -> float:
        """Calcula el error estandar de la media: sigma / raiz(n)."""
        return self.sigma / np.sqrt(self.n)

    @property
    def en_region_critica(self) -> bool:
        """Verifica si el Z calculado esta fuera de los limites de aceptacion (rechaza H0)."""
        return abs(self.z_calculado) > self.z_critico

    @property
    def intervalo_confianza(self) -> tuple:
        """Calcula el intervalo de confianza para la media con nivel (1-alpha)*100%."""
        margen = self.z_critico * self.error_estandar
        return (self.x_barra - margen, self.x_barra + margen)

    # ---- Tabla de conceptos clave ----
    CONCEPTOS = [
        ("Hipotesis estadistica",
         "Afirmacion sobre un parametro poblacional que se verifica con datos muestrales."),
        ("H\u2080 (nula)",
         "Hipotesis de 'no efecto'. Siempre incluye igualdad (=, \u2264 o \u2265). Es la que se pone a prueba."),
        ("H\u2081 (alternativa)",
         "Lo que el investigador quiere demostrar. Determina si la prueba es bilateral o unilateral."),
        ("Error Tipo I (\u03b1)",
         "Rechazar H\u2080 cuando es verdadera. Se controla fijando el nivel de significancia."),
        ("Error Tipo II (\u03b2)",
         "No rechazar H\u2080 cuando es falsa. Se relaciona con la potencia de la prueba (1-\u03b2)."),
        ("Valor-p",
         "Probabilidad de obtener un resultado tan extremo si H\u2080 fuera cierta. Valor-p < \u03b1 \u21d2 rechazar H\u2080."),
        ("Potencia (1-\u03b2)",
         "Probabilidad de rechazar H\u2080 correctamente cuando es falsa (capacidad de deteccion)."),
    ]

    TIPOS_PRUEBA = [
        ("Bilateral (dos colas)", "H\u2081: \u03bc \u2260 \u03bc\u2080",
         "No se tiene direccion esperada del efecto. Se rechaza H\u2080 en ambos extremos."),
        ("Unilateral izquierda",  "H\u2081: \u03bc < \u03bc\u2080",
         "Se espera que el parametro sea menor al valor de referencia."),
        ("Unilateral derecha",    "H\u2081: \u03bc > \u03bc\u2080",
         "Se espera que el parametro sea mayor al valor de referencia."),
    ]
