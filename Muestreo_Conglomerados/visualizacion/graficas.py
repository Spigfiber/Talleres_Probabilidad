import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure

from logica.estadistica import MedidasCentralizacion, MedidasDispersion, FormaDistribucion
from logica.frecuencias import DistribucionFrecuencias
from logica.datos import ConjuntoDatos
from .estilos import Paleta


class GraficasEstadisticas:
    """
    Crea todas las figuras matplotlib del analisis de conglomerados.
    Recibe los objetos estadisticos ya calculados y se encarga solo de
    convertir esos datos en figuras listas para incrustar en la ventana.
    """

    ALPHA = 0.18

    def __init__(
        self,
        conjunto: ConjuntoDatos,
        centralizacion: MedidasCentralizacion,
        dispersion: MedidasDispersion,
        frecuencias: DistribucionFrecuencias,
        forma: FormaDistribucion,
    ) -> None:
        self.conjunto       = conjunto
        self.centralizacion = centralizacion
        self.dispersion     = dispersion
        self.frecuencias    = frecuencias
        self.forma          = forma

        self.x_continuo = np.linspace(
            conjunto.minimo - 0.3,
            conjunto.maximo + 0.3,
            400,
        )

    def boxplot_por_conglomerado(self) -> Figure:
        """
        Boxplot lado a lado para cada semestre seleccionado.
        Permite comparar visualmente como cambia el rendimiento entre semestres.
        """
        fig, ax = plt.subplots(figsize=(9, 4))

        colores = [Paleta.COLOR_C2, Paleta.COLOR_C4, Paleta.COLOR_C6]
        nombres = self.conjunto.nombres_conglomerados
        datos_lista = [
            self.conjunto.por_conglomerado[nombre]
            for nombre in nombres
        ]

        partes = ax.boxplot(
            datos_lista,
            labels=[n.split("(")[0].strip() for n in nombres],
            patch_artist=True,
            widths=0.5,
        )
        for parche, color in zip(partes["boxes"], colores):
            parche.set(facecolor=color, alpha=0.4)
        for mediana in partes["medians"]:
            mediana.set(color="#222222", linewidth=2)

        # Puntos individuales encima de cada boxplot para ver todos los datos
        for i, (datos, color) in enumerate(zip(datos_lista, colores), start=1):
            ruido = np.random.default_rng(i).uniform(-0.12, 0.12, len(datos))
            ax.scatter(np.full(len(datos), i) + ruido, datos,
                       color=color, alpha=0.7, s=40, zorder=3)

        ax.set_title("Distribucion de promedios por semestre (conglomerado)")
        ax.set_ylabel("Promedio academico (0 a 5)")
        ax.axhline(3.0, color="gray", linestyle=":", linewidth=1.2, alpha=0.7,
                   label="Nota minima aprobatoria (3.0)")
        ax.legend(fontsize=8)
        fig.tight_layout()
        return fig

    def histograma(self, usar_relativas: bool = False) -> Figure:
        """
        Histograma de frecuencias de los promedios academicos.
        La barra de la clase modal se resalta con un borde mas grueso.
        """
        df = self.frecuencias.tabla
        fig, ax = plt.subplots(figsize=(9, 4.5))

        if usar_relativas:
            alturas = (df["fri"] * 100).tolist()
            etiqueta_y = "Frecuencia relativa (%)"
        else:
            alturas = df["fi"].tolist()
            etiqueta_y = "Frecuencia absoluta (fi)"

        colores = [
            Paleta.ACENTO if i == self.frecuencias.indice_modal else Paleta.BARRA
            for i in range(len(df))
        ]

        barras = ax.bar(
            df["Intervalo"], alturas,
            color=colores, edgecolor="white", linewidth=1.2,
        )
        for barra, valor in zip(barras, alturas):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.08,
                f"{valor:.1f}%" if usar_relativas else str(int(valor)),
                ha="center", va="bottom", fontsize=9, color="#222222"
            )

        ax.set_title("Histograma: promedios academicos de la muestra (n=36)")
        ax.set_xlabel("Promedio academico")
        ax.set_ylabel(etiqueta_y)
        plt.xticks(rotation=20, ha="right")
        fig.tight_layout()
        return fig

    def poligono_frecuencias(self) -> Figure:
        """
        Poligono de frecuencias con marcas de clase en el eje X.
        Incluye lineas de media y mediana para comparar su posicion.
        """
        df = self.frecuencias.tabla
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
                   linestyle="--", linewidth=2, label=f"Media = {self.centralizacion.media:.2f}")
        ax.axvline(self.centralizacion.mediana, color=Paleta.MEDIANA,
                   linestyle=":", linewidth=2, label=f"Mediana = {self.centralizacion.mediana:.2f}")

        ax.set_title("Poligono de frecuencias: promedios academicos")
        ax.set_xlabel("Marca de clase")
        ax.set_ylabel("Frecuencia absoluta (fi)")
        ax.legend()
        fig.tight_layout()
        return fig

    def ojiva_absoluta(self) -> Figure:
        """Ojiva de frecuencia acumulada con referencia en n/2 para la mediana."""
        df = self.frecuencias.tabla
        x_oj = [self.conjunto.minimo - 0.05] + df["ub"].tolist()
        y_oj = [0] + df["Fi"].tolist()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x_oj, y_oj, color=Paleta.OJIVA, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
        ax.fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.OJIVA)

        mitad = self.conjunto.cantidad / 2
        ax.axhline(mitad, color=Paleta.MEDIANA, linestyle=":", linewidth=1.5)
        ax.text(self.conjunto.minimo, mitad + 0.3,
                f"n/2 = {int(mitad)}  (mediana aprox.)",
                color=Paleta.MEDIANA, fontsize=9)

        ax.set_title("Ojiva: frecuencia acumulada de promedios")
        ax.set_xlabel("Promedio academico")
        ax.set_ylabel("Frecuencia acumulada (Fi)")
        fig.tight_layout()
        return fig

    def ojiva_relativa(self) -> Figure:
        """Ojiva relativa acumulada en porcentaje con lineas de percentiles."""
        df = self.frecuencias.tabla
        x_oj = [self.conjunto.minimo - 0.05] + df["ub"].tolist()
        y_oj = [0.0] + (df["Fri"] * 100).tolist()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x_oj, y_oj, color=Paleta.ACENTO, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white", markeredgewidth=2)
        ax.fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.ACENTO)

        for pct in [25, 50, 75]:
            ax.axhline(pct, color="gray", linestyle="--", linewidth=1, alpha=0.7)
            ax.text(self.conjunto.maximo + 0.02, pct, f"P{pct}", fontsize=8.5, va="center")

        ax.set_ylim(0, 110)
        ax.set_title("Ojiva: frecuencia relativa acumulada")
        ax.set_xlabel("Promedio academico")
        ax.set_ylabel("Frecuencia relativa acumulada (%)")
        fig.tight_layout()
        return fig

    def histograma_con_poligono(self) -> Figure:
        """Histograma y poligono superpuestos en la misma figura."""
        df = self.frecuencias.tabla
        amp = self.frecuencias.amplitud
        mi_ext = (
            [df["mi"].iloc[0] - amp] + df["mi"].tolist() + [df["mi"].iloc[-1] + amp]
        )
        fi_ext = [0] + df["fi"].tolist() + [0]

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(df["Intervalo"], df["fi"].tolist(),
               color=Paleta.BARRA, alpha=0.5, edgecolor="white", linewidth=1.2,
               label="Histograma")

        posiciones = list(range(1, len(df) + 1))
        pos_ext = [0] + posiciones + [len(df) + 1]
        ax.plot(pos_ext, fi_ext, color=Paleta.LINEA, linewidth=2.2,
                marker="o", markersize=7, markerfacecolor="white",
                markeredgewidth=2, label="Poligono")

        ax.set_xticks(posiciones)
        ax.set_xticklabels(df["Intervalo"].tolist(), rotation=20, ha="right")
        ax.set_title("Histograma y poligono superpuestos")
        ax.set_ylabel("Frecuencia absoluta (fi)")
        ax.legend()
        fig.tight_layout()
        return fig

    def desviaciones(self) -> Figure:
        """
        Desviacion de cada promedio respecto a la media, con colores por conglomerado.
        Permite ver que semestre tiene mas variabilidad interna.
        """
        datos = self.conjunto.valores
        nombres = self.conjunto.nombres_conglomerados
        colores_cong = [Paleta.COLOR_C2, Paleta.COLOR_C4, Paleta.COLOR_C6]
        diffs = datos - self.centralizacion.media

        # Repetimos el color de cada conglomerado para los 12 estudiantes de cada uno
        colores = []
        for color in colores_cong:
            colores.extend([color] * 12)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(range(1, len(datos) + 1), diffs, color=colores, alpha=0.8)
        ax.axhline(0, color="black", linewidth=1)

        # Separadores visuales entre conglomerados
        for sep in [12.5, 24.5]:
            ax.axvline(sep, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)

        # Leyenda de colores por conglomerado
        parches = [
            mpatches.Patch(color=c, label=n.split("(")[0].strip())
            for c, n in zip(colores_cong, nombres)
        ]
        ax.legend(handles=parches, fontsize=8.5)
        ax.set_title(f"Desviacion de cada promedio respecto a la media ({self.centralizacion.media:.2f})")
        ax.set_xlabel("Estudiante (ordenado por semestre)")
        ax.set_ylabel("Promedio menos media")
        fig.tight_layout()
        return fig

    def densidad_con_centrales(self) -> Figure:
        """KDE de los promedios con lineas para media, mediana y moda."""
        y_kde = self.forma.densidad_kde(self.x_continuo)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(self.x_continuo, y_kde, color=Paleta.BARRA, linewidth=2.2)
        ax.fill_between(self.x_continuo, y_kde, alpha=self.ALPHA, color=Paleta.BARRA)

        ax.axvline(self.centralizacion.media, color=Paleta.MEDIA, linestyle="--",
                   linewidth=2, label=f"Media = {self.centralizacion.media:.2f}")
        ax.axvline(self.centralizacion.mediana, color=Paleta.MEDIANA, linestyle=":",
                   linewidth=2, label=f"Mediana = {self.centralizacion.mediana:.2f}")

        # Si la moda es bimodal mostramos las dos lineas
        modas = self.centralizacion.moda if isinstance(self.centralizacion.moda, list) \
                else [self.centralizacion.moda]
        for i, m in enumerate(modas):
            etiqueta = f"Moda = {m}" if i == 0 else f"Moda = {m} (bimodal)"
            ax.axvline(m, color=Paleta.MODA, linestyle="-.",
                       linewidth=1.5, alpha=0.8, label=etiqueta)

        ax.set_title("Densidad estimada de promedios con medidas de centralizacion")
        ax.set_xlabel("Promedio academico")
        ax.set_ylabel("Densidad")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    def kde_vs_normal(self) -> Figure:
        """Compara la densidad real de los datos con una curva normal de referencia."""
        y_kde    = self.forma.densidad_kde(self.x_continuo)
        y_normal = self.forma.curva_normal(self.x_continuo)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(self.x_continuo, y_kde, color=Paleta.BARRA, linewidth=2.2,
                label="Densidad empirica (KDE)")
        ax.fill_between(self.x_continuo, y_kde, alpha=self.ALPHA, color=Paleta.BARRA)
        ax.plot(self.x_continuo, y_normal, color=Paleta.LINEA, linewidth=2,
                linestyle="--", label="Normal de referencia")

        ax.axvline(self.centralizacion.media, color=Paleta.MEDIA,
                   linestyle=":", linewidth=1.8, label=f"Media = {self.centralizacion.media:.2f}")
        ax.axvline(self.centralizacion.mediana, color=Paleta.MEDIANA,
                   linestyle=":", linewidth=1.8, label=f"Mediana = {self.centralizacion.mediana:.2f}")

        ax.set_title("Densidad empirica vs curva normal de referencia")
        ax.set_xlabel("Promedio academico")
        ax.set_ylabel("Densidad")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    def grafico_qq(self) -> Figure:
        """Grafico QQ para evaluar si los promedios siguen una distribucion normal."""
        teoricos, observados, pendiente, intercepto, r = self.forma.puntos_qq()
        x_ref = np.array([teoricos[0], teoricos[-1]])

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(teoricos, observados, color=Paleta.BARRA, alpha=0.75, s=45)
        ax.plot(x_ref, pendiente * x_ref + intercepto, color=Paleta.LINEA,
                linewidth=2, linestyle="--", label=f"Referencia (R={r:.4f})")
        ax.set_title("Grafico QQ: evaluacion de normalidad de los promedios")
        ax.set_xlabel("Cuantiles teoricos")
        ax.set_ylabel("Cuantiles observados")
        ax.legend(fontsize=9)
        fig.tight_layout()
        return fig

    def dashboard(self) -> Figure:
        """Panel de cuatro graficos resumidos en una sola figura para la pestana final."""
        df = self.frecuencias.tabla
        amp = self.frecuencias.amplitud
        mi_ext = [df["mi"].iloc[0] - amp] + df["mi"].tolist() + [df["mi"].iloc[-1] + amp]
        fi_ext  = [0] + df["fi"].tolist() + [0]
        x_oj = [self.conjunto.minimo] + df["ub"].tolist()
        y_oj = [0] + df["Fi"].tolist()
        y_kde = self.forma.densidad_kde(self.x_continuo)

        fig, ejes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Panel general: promedios academicos por conglomerados", fontsize=13, fontweight="bold")

        ejes[0, 0].bar(df["Intervalo"], df["fi"].tolist(),
                       color=Paleta.BARRA, edgecolor="white", linewidth=1)
        ejes[0, 0].set_title("Histograma")
        ejes[0, 0].tick_params(axis="x", rotation=25, labelsize=7)

        ejes[0, 1].plot(mi_ext, fi_ext, color=Paleta.LINEA, linewidth=2, marker="o", markersize=5)
        ejes[0, 1].fill_between(mi_ext, fi_ext, alpha=self.ALPHA, color=Paleta.LINEA)
        ejes[0, 1].set_title("Poligono de frecuencias")

        ejes[1, 0].plot(x_oj, y_oj, color=Paleta.OJIVA, linewidth=2, marker="o", markersize=5)
        ejes[1, 0].fill_between(x_oj, y_oj, alpha=self.ALPHA, color=Paleta.OJIVA)
        ejes[1, 0].set_title("Ojiva acumulada")

        ejes[1, 1].plot(self.x_continuo, y_kde, color=Paleta.ACENTO, linewidth=2)
        ejes[1, 1].fill_between(self.x_continuo, y_kde, alpha=self.ALPHA, color=Paleta.ACENTO)
        ejes[1, 1].set_title("Densidad empirica (KDE)")

        fig.tight_layout()
        return fig