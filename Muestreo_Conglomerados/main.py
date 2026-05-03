import os
import sys

# Agregamos el directorio raiz al path para que los imports funcionen
# sin importar desde donde se ejecute el programa
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logica.datos import DATOS_POR_CONGLOMERADO
from logica import datos
from logica.frecuencias import DistribucionFrecuencias
from logica.estadistica import MedidasCentralizacion, MedidasDispersion, FormaDistribucion
from logica.muestreo import MuestreoConglomerados
from visualizacion.graficas import GraficasEstadisticas
from visualizacion.estilos import aplicar_estilo_matplotlib
from interfaz.ventana_principal import VentanaPrincipal


def construir_analisis() -> dict:
    """
    Crea todos los objetos del analisis y los empaca en un diccionario.
    Se hace antes de abrir la ventana para separar los calculos de la UI.
    Si algo falla en los numeros lo veremos antes de que aparezca nada en pantalla.
    """
    conjunto = datos.ConjuntoDatos(DATOS_POR_CONGLOMERADO)

    centralizacion = MedidasCentralizacion(conjunto).calcular()
    dispersion     = MedidasDispersion(conjunto, centralizacion.media).calcular()
    frecuencias    = DistribucionFrecuencias(conjunto).calcular()
    forma          = FormaDistribucion(
                         conjunto,
                         centralizacion.media,
                         centralizacion.mediana,
                         dispersion.desviacion,
                     ).calcular()
    muestreo       = MuestreoConglomerados()

    graficas = GraficasEstadisticas(
        conjunto, centralizacion, dispersion, frecuencias, forma
    )

    return {
        "conjunto":       conjunto,
        "centralizacion": centralizacion,
        "dispersion":     dispersion,
        "frecuencias":    frecuencias,
        "forma":          forma,
        "muestreo":       muestreo,
        "graficas":       graficas,
    }


def main() -> None:
    """Aplica el estilo de matplotlib, calcula el analisis y abre la ventana."""
    aplicar_estilo_matplotlib()
    analisis = construir_analisis()
    ventana  = VentanaPrincipal(analisis)
    ventana.iniciar()


if __name__ == "__main__":
    main()