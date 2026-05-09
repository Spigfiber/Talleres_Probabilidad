import matplotlib.pyplot as plt


class Paleta:
    """Colores de la aplicacion de estadistica descriptiva."""

    BARRA    = "#2563EB"
    LINEA    = "#DC2626"
    ACENTO   = "#16A34A"
    MEDIA    = "#D97706"
    MEDIANA  = "#DC2626"
    MODA     = "#7C3AED"
    OJIVA    = "#0891B2"

    POSITIVO = "#16A34A"
    NEGATIVO = "#DC2626"

    # Colores para las seis filas de datos
    COLORES_FILAS = [
        "#3B82F6", "#10B981", "#F59E0B",
        "#EF4444", "#8B5CF6", "#EC4899",
    ]

    FONDO_VENTANA   = "#F8FAFC"
    FONDO_SIDEBAR   = "#1E293B"
    TEXTO_SIDEBAR   = "#F1F5F9"
    FONDO_TARJETA   = "#FFFFFF"
    BORDE_TARJETA   = "#E2E8F0"
    TEXTO_TITULO    = "#1E293B"
    TEXTO_VALOR     = "#2563EB"
    FONDO_TABLA_PAR = "#F8FAFC"
    FONDO_MODAL     = "#DCFCE7"
    FONDO_CABECERA  = "#EFF6FF"

    FUENTE_TITULO  = ("Segoe UI", 15, "bold")
    FUENTE_NORMAL  = ("Segoe UI", 12)
    FUENTE_PEQUENA = ("Segoe UI", 11)
    FUENTE_VALOR   = ("Segoe UI", 20, "bold")
    FUENTE_LABEL   = ("Segoe UI", 11)
    FUENTE_MONO    = ("Consolas", 12)


def aplicar_estilo_matplotlib() -> None:
    """Configura el estilo global de matplotlib para que todos los graficos se vean consistentes.
    Define colores, cuadriculas, fuentes y bordes de acuerdo a la paleta de la aplicacion."""
    plt.rcParams.update({
        "figure.facecolor":   "#FAFBFC",
        "axes.facecolor":     "#FAFBFC",
        "axes.grid":          True,
        "grid.alpha":         0.22,
        "grid.linestyle":     "--",
        "grid.color":         "#CCCCCC",
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.titlesize":     14,
        "axes.titleweight":   "bold",
        "axes.titlecolor":    "#1E293B",
        "axes.labelsize":     12,
        "axes.labelcolor":    "#555555",
        "xtick.labelsize":    11,
        "ytick.labelsize":    11,
        "legend.fontsize":    11,
        "legend.framealpha":  0.8,
        "figure.autolayout":  True,
        "font.family":        "sans-serif",
    })
