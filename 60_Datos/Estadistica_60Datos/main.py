import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logica.datos import DATOS_FILAS, ConjuntoDatos
from logica.estadistica import MedidasCentralizacion, MedidasDispersion, FormaDistribucion
from logica.frecuencias import DistribucionFrecuencias
from logica.hipotesis import PruebaHipotesisZ
from visualizacion.graficas import GraficasEstadisticas
from visualizacion.estilos import aplicar_estilo_matplotlib
from interfaz.ventana_principal import VentanaPrincipal


def construir_analisis() -> dict:
    """
    Crea todos los objetos del analisis y los empaca en un diccionario.
    Se ejecuta antes de abrir la ventana para separar calculos de UI.
    """
    conjunto = ConjuntoDatos(DATOS_FILAS)

    centralizacion = MedidasCentralizacion(conjunto).calcular()
    dispersion     = MedidasDispersion(conjunto, centralizacion.media).calcular()
    frecuencias    = DistribucionFrecuencias(conjunto).calcular()
    forma          = FormaDistribucion(
                         conjunto,
                         centralizacion.media,
                         centralizacion.mediana,
                         dispersion.desviacion,
                     ).calcular()
    hipotesis      = PruebaHipotesisZ().calcular()

    graficas = GraficasEstadisticas(
        conjunto, centralizacion, dispersion, frecuencias, forma, hipotesis
    )

    return {
        "conjunto":       conjunto,
        "centralizacion": centralizacion,
        "dispersion":     dispersion,
        "frecuencias":    frecuencias,
        "forma":          forma,
        "hipotesis":      hipotesis,
        "graficas":       graficas,
    }


def main() -> None:
    aplicar_estilo_matplotlib()
    analisis = construir_analisis()
    ventana  = VentanaPrincipal(analisis)
    ventana.iniciar()


if __name__ == "__main__":
    main()
