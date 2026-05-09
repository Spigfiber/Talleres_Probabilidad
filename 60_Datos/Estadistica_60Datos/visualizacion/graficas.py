import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from scipy import stats as scipy_stats

from logica.estadistica import MedidasCentralizacion, MedidasDispersion, FormaDistribucion
from logica.frecuencias import DistribucionFrecuencias
from logica.datos import ConjuntoDatos
from logica.hipotesis import PruebaHipotesisZ
from .estilos import Paleta


class GraficasEstadisticas:
    """
    Crea todas las figuras matplotlib del analisis de los 60 datos.

    OPTIMIZACIONES aplicadas:
    1. x_continuo y y_kde se calculan UNA SOLA VEZ en __init__ y se
       reutilizan en histograma, poligono, ojivas, kde_vs_normal y dashboard.
       Antes cada metodo llamaba a forma.densidad_kde() por separado,
       provocando que gaussian_kde evaluara 500 puntos multiples veces.

    2. Cada figura se guarda en self._cache la primera vez que se construye.
       Las llamadas siguientes (p. ej. al volver a una pestana) devuelven
       directamente el objeto Figure ya existente sin recalcular nada.
       El histograma tiene dos entradas de cache (abs y relativa) porque
       el toggle puede generar ambas versiones.
    """

    ALPHA = 0.15

    def __init__(
        self,
        conjunto: ConjuntoDatos,
        centralizacion: MedidasCentralizacion,
        dispersion: MedidasDispersion,
        frecuencias: DistribucionFrecuencias,
        forma: FormaDistribucion,
        hipotesis: PruebaHipotesisZ,
    ) -> None:
        self.conjunto       = conjunto
        self.centralizacion = centralizacion
        self.dispersion     = dispersion
        self.frecuencias    = frecuencias
        self.forma          = forma
        self.hipotesis      = hipotesis

        # --- pre-calculo compartido --------------------------------------- #
        self.x_continuo = np.linspace(
            conjunto.minimo - 5, conjunto.maximo + 5, 500
        )
        # y_kde se calcula una sola vez; densidad_kde ya cachea el estimador,
        # pero ademas evitamos llamar al metodo mas de una vez desde aqui.
        self._y_kde: np.ndarray = self.forma.densidad_kde(self.x_continuo)

        # --- cache de figuras --------------------------------------------- #
        self._cache: dict[str, Figure] = {}

    # ------------------------------------------------------------------ #
    #  Helper interno                                                      #
    # ------------------------------------------------------------------ #
    def _cached(self, clave: str, constructor) -> Figure:
        """Devuelve una figura del cache si existe, o la construye y guarda por primera vez.
        Evita recalcular graficas costosas cuando se vuelve a visitar una pestana."""
        if clave not in self._cache:
            self._cache[clave] = constructor()
        return self._cache[clave]

    # ------------------------------------------------------------------ #
    #  HISTOGRAMA                                                          #
    # ------------------------------------------------------------------ #
    def histograma(self, usar_relativas: bool = False) -> Figure:
        """Genera el histograma con barras que muestran frecuencias, la clase modal en verde.
        Permite ver distribucion visual de los datos en intervalos."""
        clave = f"histograma_{usar_relativas}"
        return self._cached(clave, lambda: self._construir_histograma(usar_relativas))

    def _construir_histograma(self, usar_relativas: bool) -> Figure:
        """Construye la figura del histograma con las etiquetas de valores sobre las barras."""
        df = self.frecuencias.tabla
        fig, ax = plt.subplots(figsize=(9, 4.5))

        alturas    = (df["fri"] * 100).tolist() if usar_relativas else df["fi"].tolist()
        etiqueta_y = "Frecuencia relativa (%)" if usar_relativas else "Frecuencia absoluta (fi)"

        colores = [
            Paleta.ACENTO if i == self.frecuencias.indice_modal else Paleta.BARRA
            for i in range(len(df))
        ]
        barras = ax.bar(df["Intervalo"], alturas, color=colores,
                        edgecolor="white", linewidth=1.5)

        for barra, val in zip(barras, alturas):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.12,
                f"{val:.1f}%" if usar_relativas else str(int(val)),
                ha="center", va="bottom", fontsize=9, color="#222222",
            )

        ax.set_title(f"Histograma de frecuencias (n = {self.conjunto.cantidad})")
        ax.set_xlabel("Intervalos")
        ax.set_ylabel(etiqueta_y)
        plt.xticks(rotation=15, ha="right")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  POLIGONO DE FRECUENCIAS                                             #
    # ------------------------------------------------------------------ #
    def poligono_frecuencias(self) -> Figure:
        """Genera el poligono de frecuencias que muestra una vista continua de la distribucion."""
        return self._cached("poligono", self._construir_poligono)

    def _construir_poligono(self) -> Figure:
        """Dibuja el poligono con marcas en cada punto y relleno, mas las lineas de media y mediana."""
        df  = self.frecuencias.tabla
        amp = self.frecuencias.amplitud

        mi_ext = (
            [df["mi"].iloc[0] - amp]
            + df["mi"].tolist()
            + [df["mi"].iloc[-1] + amp]
        )
        fi_ext = [0] + df["fi"].tolist() + [0]

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(mi_ext, fi_ext, color=Paleta.LINEA, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
        ax.fill_between(mi_ext, fi_ext, alpha=self.ALPHA, color=Paleta.LINEA)

        ax.axvline(self.centralizacion.media, color=Paleta.MEDIA,
                   linestyle="--", linewidth=2,
                   label=f"Media = {self.centralizacion.media:.2f}")
        ax.axvline(self.centralizacion.mediana, color=Paleta.MEDIANA,
                   linestyle=":", linewidth=2,
                   label=f"Mediana = {self.centralizacion.mediana:.2f}")

        ax.set_title("Poligono de frecuencias")
        ax.set_xlabel("Marca de clase (mi)")
        ax.set_ylabel("Frecuencia absoluta (fi)")
        ax.legend()
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  OJIVA ABSOLUTA                                                      #
    # ------------------------------------------------------------------ #
    def ojiva_absoluta(self) -> Figure:
        """Genera la ojiva (curva de frecuencia acumulada absoluta) para leer percentiles."""
        return self._cached("ojiva_abs", self._construir_ojiva_absoluta)

    def _construir_ojiva_absoluta(self) -> Figure:
        df  = self.frecuencias.tabla
        x_oj = [self.conjunto.minimo] + df["ub"].tolist()
        y_oj = [0] + df["Fi"].tolist()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x_oj, y_oj, color=Paleta.OJIVA, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
        ax.fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.OJIVA)

        mitad = self.conjunto.cantidad / 2
        ax.axhline(mitad, color=Paleta.MEDIANA, linestyle=":", linewidth=1.5)
        ax.text(self.conjunto.minimo + 1, mitad + 0.6,
                f"n/2 = {int(mitad)}  (mediana \u2248 {self.centralizacion.mediana:.1f})",
                color=Paleta.MEDIANA, fontsize=9)

        ax.set_title("Ojiva: frecuencia acumulada")
        ax.set_xlabel("Limite superior del intervalo")
        ax.set_ylabel("Frecuencia acumulada (Fi)")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  OJIVA RELATIVA                                                      #
    # ------------------------------------------------------------------ #
    def ojiva_relativa(self) -> Figure:
        """Genera la ojiva de frecuencias relativas acumuladas mostrando percentiles."""
        return self._cached("ojiva_rel", self._construir_ojiva_relativa)

    def _construir_ojiva_relativa(self) -> Figure:
        """Dibuja la ojiva relativa con lineas de percentiles para lectura rapida."""
        df  = self.frecuencias.tabla
        x_oj = [self.conjunto.minimo] + df["ub"].tolist()
        y_oj = [0.0] + (df["Fri"] * 100).tolist()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x_oj, y_oj, color=Paleta.ACENTO, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
        ax.fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.ACENTO)

        for pct in [25, 50, 75]:
            ax.axhline(pct, color="gray", linestyle="--", linewidth=1, alpha=0.7)
            ax.text(self.conjunto.maximo + 0.5, pct, f"P{pct}",
                    fontsize=8.5, va="center")

        ax.set_ylim(0, 110)
        ax.set_title("Ojiva: frecuencia relativa acumulada (%)")
        ax.set_xlabel("Limite superior del intervalo")
        ax.set_ylabel("Frecuencia relativa acumulada (%)")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  HISTOGRAMA + POLIGONO SUPERPUESTOS                                 #
    # ------------------------------------------------------------------ #
    def histograma_con_poligono(self) -> Figure:
        """Superpone el histograma con el poligono para ver ambas representaciones a la vez."""
        return self._cached("histo_poli", self._construir_histograma_con_poligono)

    def _construir_histograma_con_poligono(self) -> Figure:
        df  = self.frecuencias.tabla
        fi_ext = [0] + df["fi"].tolist() + [0]

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(df["Intervalo"], df["fi"].tolist(),
               color=Paleta.BARRA, alpha=0.5, edgecolor="white", linewidth=1.2,
               label="Histograma")

        posiciones = list(range(1, len(df) + 1))
        pos_ext    = [0] + posiciones + [len(df) + 1]
        ax.plot(pos_ext, fi_ext, color=Paleta.LINEA, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white",
                markeredgewidth=2, label="Poligono")

        ax.set_xticks(posiciones)
        ax.set_xticklabels(df["Intervalo"].tolist(), rotation=15, ha="right")
        ax.set_title("Histograma y poligono superpuestos")
        ax.set_ylabel("Frecuencia absoluta (fi)")
        ax.legend()
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  DESVIACIONES RESPECTO A LA MEDIA                                   #
    # ------------------------------------------------------------------ #
    def desviaciones(self) -> Figure:
        """Muestra cada dato como una barra que representa su desviacion respecto a la media."""
        return self._cached("desviaciones", self._construir_desviaciones)

    def _construir_desviaciones(self) -> Figure:
        """Dibuja barras coloreadas por fila mostrando desviaciones, con lineas separadoras entre filas."""
        datos = self.conjunto.valores
        diffs = datos - self.centralizacion.media

        colores = []
        for color in Paleta.COLORES_FILAS:
            colores.extend([color] * 10)

        fig, ax = plt.subplots(figsize=(11, 4))
        ax.bar(range(1, len(datos) + 1), diffs, color=colores, alpha=0.8)
        ax.axhline(0, color="black", linewidth=1)

        for sep in [10.5, 20.5, 30.5, 40.5, 50.5]:
            ax.axvline(sep, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)

        parches = [
            mpatches.Patch(color=c, label=n)
            for c, n in zip(Paleta.COLORES_FILAS, self.conjunto.nombres_filas)
        ]
        ax.legend(handles=parches, fontsize=8, ncol=6)
        ax.set_title(f"Desviacion de cada dato respecto a la media ({self.centralizacion.media:.2f})")
        ax.set_xlabel("Dato (ordenado por fila de recoleccion)")
        ax.set_ylabel("xi \u2212 x\u0305")
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  KDE CON MEDIDAS CENTRALES  (usa self._y_kde pre-calculado)        #
    # ------------------------------------------------------------------ #
    def densidad_con_centrales(self) -> Figure:
        """Muestra la curva de densidad KDE con lineas verticales de media, mediana y moda."""
        return self._cached("densidad_centrales", self._construir_densidad_con_centrales)

    def _construir_densidad_con_centrales(self) -> Figure:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(self.x_continuo, self._y_kde, color=Paleta.BARRA, linewidth=2.2)
        ax.fill_between(self.x_continuo, self._y_kde, alpha=self.ALPHA, color=Paleta.BARRA)

        ax.axvline(self.centralizacion.media, color=Paleta.MEDIA, linestyle="--",
                   linewidth=2, label=f"Media = {self.centralizacion.media:.2f}")
        ax.axvline(self.centralizacion.mediana, color=Paleta.MEDIANA, linestyle=":",
                   linewidth=2, label=f"Mediana = {self.centralizacion.mediana:.2f}")

        modas = (self.centralizacion.moda
                 if isinstance(self.centralizacion.moda, list)
                 else [self.centralizacion.moda])
        for i, m in enumerate(modas):
            ax.axvline(m, color=Paleta.MODA, linestyle="-.",
                       linewidth=1.5, alpha=0.9,
                       label=f"Moda = {int(m)}" if i == 0 else f"Moda = {int(m)}")

        ax.set_title("Densidad estimada con medidas de centralizacion")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Densidad")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  KDE VS NORMAL  (usa self._y_kde pre-calculado)                    #
    # ------------------------------------------------------------------ #
    def kde_vs_normal(self) -> Figure:
        """Compara la densidad empirica de los datos con la curva normal de referencia."""
        return self._cached("kde_vs_normal", self._construir_kde_vs_normal)

    def _construir_kde_vs_normal(self) -> Figure:
        y_normal = self.forma.curva_normal(self.x_continuo)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(self.x_continuo, self._y_kde, color=Paleta.BARRA, linewidth=2.2,
                label="Densidad empirica (KDE)")
        ax.fill_between(self.x_continuo, self._y_kde, alpha=self.ALPHA, color=Paleta.BARRA)
        ax.plot(self.x_continuo, y_normal, color=Paleta.LINEA, linewidth=2,
                linestyle="--", label="Normal de referencia")
        ax.axvline(self.centralizacion.media, color=Paleta.MEDIA,
                   linestyle=":", linewidth=1.8,
                   label=f"Media = {self.centralizacion.media:.2f}")

        ax.set_title("Densidad empirica vs curva normal de referencia")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Densidad")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  GRAFICO QQ                                                         #
    # ------------------------------------------------------------------ #
    def grafico_qq(self) -> Figure:
        """Genera un grafico QQ para evaluar visualmente si los datos siguen una distribucion normal."""
        return self._cached("qq", self._construir_qq)

    def _construir_qq(self) -> Figure:
        teoricos, observados, pendiente, intercepto, r = self.forma.puntos_qq()
        x_ref = np.array([teoricos[0], teoricos[-1]])

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(teoricos, observados, color=Paleta.BARRA, alpha=0.75, s=45)
        ax.plot(x_ref, pendiente * x_ref + intercepto, color=Paleta.LINEA,
                linewidth=2, linestyle="--", label=f"Referencia (R = {r:.4f})")

        ax.set_title("Grafico QQ: evaluacion de normalidad")
        ax.set_xlabel("Cuantiles teoricos")
        ax.set_ylabel("Cuantiles observados")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  PRUEBA Z                                                           #
    # ------------------------------------------------------------------ #
    def grafico_prueba_z(self) -> Figure:
        """Dibuja la distribucion normal con regiones de rechazo y el Z calculado marcado."""
        return self._cached("prueba_z", self._construir_prueba_z)

    def _construir_prueba_z(self) -> Figure:
        h = self.hipotesis
        x = np.linspace(-4, 4, 500)
        y = scipy_stats.norm.pdf(x)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x, y, color="#334155", linewidth=2)

        x_izq = x[x <= -h.z_critico]
        x_der = x[x >=  h.z_critico]
        ax.fill_between(x_izq, scipy_stats.norm.pdf(x_izq),
                        alpha=0.35, color=Paleta.NEGATIVO, label="Region de rechazo")
        ax.fill_between(x_der, scipy_stats.norm.pdf(x_der),
                        alpha=0.35, color=Paleta.NEGATIVO)

        for zc in [-h.z_critico, h.z_critico]:
            ax.axvline(zc, color=Paleta.NEGATIVO, linestyle="--", linewidth=1.5,
                       label=f"Z critico = \u00b1{h.z_critico:.2f}" if zc > 0 else None)

        ax.axvline(h.z_calculado, color=Paleta.BARRA, linewidth=2.5,
                   label=f"Z calculado = {h.z_calculado:.3f}")
        ax.axvline(-abs(h.z_calculado), color=Paleta.BARRA, linewidth=2.5,
                   linestyle=":", alpha=0.5)

        ax.text(0, scipy_stats.norm.pdf(0) * 0.45, "No rechazar H\u2080",
                ha="center", fontsize=10, color="#334155",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

        ax.set_title(f"Prueba Z bilateral \u2014 H\u2080: \u03bc = {h.mu0}  |  \u03b1 = {h.alpha}")
        ax.set_xlabel("Z")
        ax.set_ylabel("Densidad")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  DASHBOARD 2x2  (usa self._y_kde pre-calculado)                    #
    # ------------------------------------------------------------------ #
    def dashboard(self) -> Figure:
        """Crea un panel de 2x2 con los graficos mas importantes para una vision general."""
        return self._cached("dashboard", self._construir_dashboard)

    def _construir_dashboard(self) -> Figure:
        """Construye un panel 2x2 con histograma, poligono, ojiva y densidad para un resumen visual completo."""
        df   = self.frecuencias.tabla
        amp  = self.frecuencias.amplitud
        mi_ext = ([df["mi"].iloc[0] - amp]
                  + df["mi"].tolist()
                  + [df["mi"].iloc[-1] + amp])
        fi_ext = [0] + df["fi"].tolist() + [0]
        x_oj   = [self.conjunto.minimo] + df["ub"].tolist()
        y_oj   = [0] + df["Fi"].tolist()

        fig, ejes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Panel general: analisis estadistico de los 60 datos",
                     fontsize=13, fontweight="bold")

        colores = [
            Paleta.ACENTO if i == self.frecuencias.indice_modal else Paleta.BARRA
            for i in range(len(df))
        ]
        ejes[0, 0].bar(df["Intervalo"], df["fi"].tolist(),
                       color=colores, edgecolor="white", linewidth=1)
        ejes[0, 0].set_title("Histograma")
        ejes[0, 0].tick_params(axis="x", rotation=20, labelsize=7)

        ejes[0, 1].plot(mi_ext, fi_ext, color=Paleta.LINEA, linewidth=2,
                        marker="o", markersize=5)
        ejes[0, 1].fill_between(mi_ext, fi_ext, alpha=self.ALPHA, color=Paleta.LINEA)
        ejes[0, 1].set_title("Poligono de frecuencias")

        ejes[1, 0].plot(x_oj, y_oj, color=Paleta.OJIVA, linewidth=2,
                        marker="o", markersize=5)
        ejes[1, 0].fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.OJIVA)
        ejes[1, 0].set_title("Ojiva acumulada")

        # reutiliza _y_kde ya calculado
        ejes[1, 1].plot(self.x_continuo, self._y_kde, color=Paleta.ACENTO, linewidth=2)
        ejes[1, 1].fill_between(self.x_continuo, self._y_kde,
                                alpha=self.ALPHA, color=Paleta.ACENTO)
        ejes[1, 1].axvline(self.centralizacion.media, color=Paleta.MEDIA,
                           linestyle="--", linewidth=1.5,
                           label=f"Media={self.centralizacion.media:.2f}")
        ejes[1, 1].legend(fontsize=8)
        ejes[1, 1].set_title("Densidad empirica (KDE)")

        fig.tight_layout()
        return fig
