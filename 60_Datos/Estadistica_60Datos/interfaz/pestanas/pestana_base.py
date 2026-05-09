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
    Clase base de la que heredan todas las pestanas.
    Centraliza la creacion de widgets comunes para no repetir codigo.
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
        self.hipotesis      = analisis["hipotesis"]

        self.desplazable = MarcoDesplazable(self)
        self.desplazable.pack(fill="both", expand=True)
        self.cuerpo = self.desplazable.interior
        self.construir()

    @abstractmethod
    def construir(self) -> None:
        """Metodo que debe implementar cada pestana concreta para crear sus propios widgets."""

    def agregar_titulo(self, texto: str) -> None:
        """Agrega un titulo grande y oscuro al cuerpo de la pestana."""
        TituloSeccion(self.cuerpo, texto).pack(anchor="w", padx=16, pady=(12, 4))

    def agregar_subtitulo(self, texto: str) -> None:
        """Agrega un subtitulo mediano para dividir secciones dentro de la pestana."""
        tk.Label(
            self.cuerpo, text=texto,
            font=("Segoe UI", 13, "bold"),
            bg=Paleta.FONDO_VENTANA, fg="#1E293B",
        ).pack(anchor="w", padx=16, pady=(10, 2))

    def agregar_texto(self, texto: str, color: str = "#EFF6FF") -> None:
        """Agrega un bloque de texto explicativo con fondo coloreado para destacar."""
        TextoInfo(self.cuerpo, texto, color_fondo=color).pack(fill="x", padx=16, pady=4)

    def agregar_tarjetas(self, metricas: list[tuple[str, str]]) -> None:
        """Agrega una fila de tarjetas que muestran pares de (etiqueta, valor)."""
        FilaTarjetas(self.cuerpo, metricas).pack(fill="x", padx=16, pady=6)

    def agregar_grafico(self, figura) -> None:
        """Incrusta una figura matplotlib en la pestana para mostrar graficas estadisticas."""
        PanelGrafico(self.cuerpo, figura).pack(fill="both", padx=16, pady=6)

    def agregar_tabla(
        self,
        columnas: list[str],
        filas: list[list],
        fila_resaltada: int = -1,
        alto: int = 8,
    ) -> VistaTabla:
        """Agrega una tabla interactiva con datos. fila_resaltada muestra una fila en verde."""
        tabla = VistaTabla(
            self.cuerpo, columnas, filas,
            fila_resaltada=fila_resaltada, alto=alto,
        )
        tabla.pack(fill="x", padx=16, pady=6)
        return tabla

    def agregar_separador(self) -> None:
        """Agrega una linea horizontal para separar visualmente secciones."""
        Separador(self.cuerpo).pack(fill="x", padx=16, pady=10)
