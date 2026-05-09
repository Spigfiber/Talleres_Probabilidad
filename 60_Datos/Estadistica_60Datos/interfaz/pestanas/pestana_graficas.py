import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from interfaz.componentes import PanelGrafico
from .pestana_base import PestanaBase


class PestanaGraficas(PestanaBase):
    """
    Muestra todas las graficas estadisticas:
    histograma (con toggle), poligono, ojivas y superposicion.
    """

    def construir(self) -> None:
        """Construye la pestana mostrando todos los graficos estadisticos disponibles."""
        self.agregar_titulo("Graficas Estadisticas")
        self.agregar_separador()

        # ---------- HISTOGRAMA ----------
        self.construir_histograma_interactivo()
        self.agregar_separador()

        # ---------- POLIGONO ----------
        self.agregar_subtitulo("Poligono de Frecuencias")
        self.agregar_texto(
            "Conecta los puntos (marca de clase, frecuencia) con una linea poligonal. "
            "Permite ver la forma de la distribucion de manera mas continua que el histograma.\n"
            "Las lineas verticales muestran la media (naranja) y la mediana (roja): "
            "estan muy cerca, confirmando la casi simetria."
        )
        self.agregar_grafico(self.graficas.poligono_frecuencias())
        self.agregar_separador()

        # ---------- OJIVA ABSOLUTA ----------
        self.agregar_subtitulo("Ojiva de Frecuencia Acumulada")
        self.agregar_texto(
            "Representa Fi en funcion del limite superior de cada intervalo. "
            "Util para leer percentiles directamente.\n"
            "La linea punteada en Fi = 30 (n/2) cruza la ojiva aproximadamente "
            "en x \u2248 50.5, que coincide con la mediana calculada."
        )
        self.agregar_grafico(self.graficas.ojiva_absoluta())
        self.agregar_separador()

        # ---------- OJIVA RELATIVA ----------
        self.agregar_subtitulo("Ojiva de Frecuencia Relativa Acumulada")
        self.agregar_grafico(self.graficas.ojiva_relativa())
        self.agregar_separador()

        # ---------- HISTOGRAMA + POLIGONO ----------
        self.agregar_subtitulo("Histograma y Poligono Superpuestos")
        self.agregar_grafico(self.graficas.histograma_con_poligono())

    def construir_histograma_interactivo(self) -> None:
        """Crea un histograma con checkbox para alternar entre frecuencias absolutas y relativas."""
        self.agregar_subtitulo("Histograma de Frecuencias")
        self.agregar_texto(
            "Cada barra representa un intervalo de amplitud A = 14. "
            "La barra verde es la clase modal: [44, 58) con 11 datos (18.33% de la muestra).\n"
            "La forma ligeramente acampanada con un maximo en el centro confirma "
            "la casi simetria de la distribucion."
        )

        controles = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        controles.pack(fill="x", padx=16, pady=(0, 4))

        usar_relativas = tk.BooleanVar(value=False)

        marco_hist = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco_hist.pack(fill="both", padx=16)
        PanelGrafico(marco_hist, self.graficas.histograma(False)).pack(fill="both", expand=True)

        def cambiar_tipo():
            PanelGrafico.reemplazar(marco_hist, self.graficas.histograma(usar_relativas.get()))

        ttk.Checkbutton(
            controles,
            text="Mostrar frecuencias relativas (%)",
            variable=usar_relativas,
            command=cambiar_tipo,
        ).pack(side="left")
