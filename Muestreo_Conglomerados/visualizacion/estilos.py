import matplotlib.pyplot as plt


class Paleta:
    """
    Colores de la aplicacion, todos en un solo lugar.
    Los colores base son un poco mas calidos que en el proyecto anterior
    para dar un tono mas academico y menos tecnico al dashboard.
    """

    BARRA    = "#2E86AB"
    LINEA    = "#E84855"
    ACENTO   = "#3BB273"
    MEDIANA  = "#E84855"
    MEDIA    = "#F18F01"
    MODA     = "#7B2D8B"
    OJIVA    = "#4ECDC4"

    RELLENO_BARRA  = "#2E86AB"
    RELLENO_LINEA  = "#E84855"
    RELLENO_ACENTO = "#3BB273"

    POSITIVO = "#3BB273"
    NEGATIVO = "#E84855"

    # Colores para diferenciar cada conglomerado en los graficos
    COLOR_C2 = "#FF9F1C"
    COLOR_C4 = "#2EC4B6"
    COLOR_C6 = "#9B5DE5"

    FONDO_VENTANA   = "#F7F9FC"
    FONDO_SIDEBAR   = "#1B2A4A"
    TEXTO_SIDEBAR   = "#ECF0F1"
    FONDO_TARJETA   = "#FFFFFF"
    BORDE_TARJETA   = "#DEE2E6"
    TEXTO_TITULO    = "#1B2A4A"
    TEXTO_VALOR     = "#2E86AB"
    FONDO_TABLA_PAR = "#F8F9FA"
    FONDO_MODAL     = "#D4EDDA"
    FONDO_CABECERA  = "#E8F4FD"

    FUENTE_TITULO  = ("Segoe UI", 15, "bold")
    FUENTE_NORMAL  = ("Segoe UI", 12)
    FUENTE_PEQUENA = ("Segoe UI", 11)
    FUENTE_VALOR   = ("Segoe UI", 20, "bold")
    FUENTE_LABEL   = ("Segoe UI", 11)
    FUENTE_MONO    = ("Consolas", 12)


def aplicar_estilo_matplotlib() -> None:
    """
    Estilo global de matplotlib. Se llama una vez al inicio del programa
    antes de crear cualquier figura para que todas tengan el mismo aspecto.
    """
    plt.rcParams.update({
        "figure.facecolor":      "#FAFBFC",
        "axes.facecolor":        "#FAFBFC",
        "axes.grid":             True,
        "grid.alpha":            0.22,
        "grid.linestyle":        "--",
        "grid.color":            "#CCCCCC",
        "axes.spines.top":       False,
        "axes.spines.right":     False,
        "axes.titlesize":        14,
        "axes.titleweight":      "bold",
        "axes.titlecolor":       "#1B2A4A",
        "axes.labelsize":        12,
        "axes.labelcolor":       "#555555",
        "xtick.labelsize":       11,
        "ytick.labelsize":       11,
        "legend.fontsize":       11,
        "legend.framealpha":     0.8,
        "figure.autolayout":     True,
        "font.family":           "sans-serif",
    })