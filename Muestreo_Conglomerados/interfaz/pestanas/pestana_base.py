import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from visualizacion.estilos import Paleta
from interfaz.componentes import (
    MarcoDesplazable, TituloSeccion, FilaTarjetas,
    PanelGrafico, Separador, TextoInfo, VistaTabla,
)


class PestanaBase(ttk.Frame, ABC):
    """
    Clase base de la que heredan todas las pestanas de la aplicacion.
    Centraliza la logica de creacion de widgets comunes para no repetir
    codigo en cada pestana concreta.

    Hereda de ttk.Frame para poder agregarse directamente a un Notebook,
    y de ABC para obligar a las subclases a implementar el metodo construir.
    """

    def __init__(self, padre, analisis: dict) -> None:
        super().__init__(padre)
        self.configure(style="Pestana.TFrame")
        self.analisis       = analisis
        self.conjunto       = analisis["conjunto"]
        self.centralizacion = analisis["centralizacion"]
        self.dispersion     = analisis["dispersion"]
        self.frecuencias    = analisis["frecuencias"]
        self.forma          = analisis["forma"]
        self.graficas       = analisis["graficas"]
        self.muestreo       = analisis["muestreo"]

        self.desplazable = MarcoDesplazable(self)
        self.desplazable.pack(fill="both", expand=True)
        self.cuerpo = self.desplazable.interior

        self.construir()

    @abstractmethod
    def construir(self) -> None:
        """Cada pestana concreta crea sus propios widgets aqui."""

    def agregar_titulo(self, texto: str) -> None:
        TituloSeccion(self.cuerpo, texto).pack(anchor="w", padx=16, pady=(12, 4))

    def agregar_subtitulo(self, texto: str) -> None:
        tk.Label(
            self.cuerpo, text=texto,
            font=("Segoe UI", 13, "bold"),
            bg=Paleta.FONDO_VENTANA, fg="#1B2A4A",
        ).pack(anchor="w", padx=16, pady=(10, 2))

    def agregar_texto(self, texto: str, color: str = "#EBF5FB") -> None:
        TextoInfo(self.cuerpo, texto, color_fondo=color).pack(fill="x", padx=16, pady=4)

    def agregar_tarjetas(self, metricas: list[tuple[str, str]]) -> None:
        FilaTarjetas(self.cuerpo, metricas).pack(fill="x", padx=16, pady=6)

    def agregar_grafico(self, figura) -> None:
        PanelGrafico(self.cuerpo, figura).pack(fill="both", padx=16, pady=6)

    def agregar_tabla(
        self,
        columnas: list[str],
        filas: list[list],
        fila_resaltada: int = -1,
        alto: int = 8,
    ) -> VistaTabla:
        tabla = VistaTabla(
            self.cuerpo, columnas, filas,
            fila_resaltada=fila_resaltada, alto=alto
        )
        tabla.pack(fill="x", padx=16, pady=6)
        return tabla

    def agregar_separador(self) -> None:
        Separador(self.cuerpo).pack(fill="x", padx=16, pady=10)