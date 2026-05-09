import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from logica.datos import N_POBLACION, DATOS_POR_FILA, TOTAL_FILAS
from .pestana_base import PestanaBase


class PestanaDatos(PestanaBase):
    """
    Muestra los datos originales organizados por fila de recoleccion,
    las sumas parciales y los 60 datos ordenados de menor a mayor
    para calcular la mediana.
    """

    def construir(self) -> None:
        """Construye la pestana mostrando los datos originales, sumas y datos ordenados."""
        self.agregar_titulo("Datos Originales y Organizacion")
        self.agregar_separador()

        self.agregar_subtitulo("Descripcion de la poblacion")
        self.agregar_texto(
            f"Poblacion: N = {N_POBLACION} datos aleatorios sin unidad concreta.\n"
            f"Organizacion: {TOTAL_FILAS} filas de {DATOS_POR_FILA} datos cada una.\n"
            "Rango observado: del 2 al 99.\n"
            "Objetivo: aplicar estadistica descriptiva completa (centralizacion, dispersion y forma)."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Datos originales (orden de recoleccion)")
        self.construir_tabla_original()

        self.agregar_separador()
        self.agregar_subtitulo("Sumas parciales por fila")
        sumas = self.conjunto.suma_por_fila
        self.agregar_tarjetas([
            (nombre, f"{suma:.0f}")
            for nombre, suma in sumas.items()
        ])
        self.agregar_texto(
            f"Suma total: {' + '.join(str(int(s)) for s in sumas.values())} = "
            f"{self.conjunto.suma:.0f}\n"
            f"Media = {self.conjunto.suma:.0f} / {self.conjunto.cantidad} = "
            f"{self.conjunto.suma / self.conjunto.cantidad:.2f}"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Datos ordenados de menor a mayor")
        self.agregar_texto(
            f"Los {self.conjunto.cantidad} datos ordenados para calcular la mediana.\n"
            f"Con n par, los datos centrales son x30 y x31 (posiciones 30 y 31).\n"
            f"Minimo = {int(self.conjunto.minimo)}     Maximo = {int(self.conjunto.maximo)}"
        )
        self.construir_tabla_ordenada()

    def construir_tabla_original(self) -> None:
        """Crea la tabla que muestra los datos originales organizados por fila de recoleccion."""
        columnas = ["Fila"] + [f"D{i}" for i in range(1, 11)] + ["Suma"]
        filas = []
        sumas = self.conjunto.suma_por_fila
        for nombre in self.conjunto.nombres_filas:
            datos = self.conjunto.por_fila[nombre]
            fila = [nombre] + [int(v) for v in datos] + [int(sumas[nombre])]
            filas.append(fila)
        tabla = self.agregar_tabla(columnas, filas, alto=TOTAL_FILAS + 1)
        tabla.arbol.column("Fila", width=60)
        tabla.arbol.column("Suma", width=70)

    def construir_tabla_ordenada(self) -> None:
        """Crea la tabla que muestra los datos ordenados con los datos centrales resaltados."""
        ordenados = self.conjunto.ordenados
        filas_datos = ordenados.reshape(6, 10)

        columnas = [f"x{i}" for i in range(1, 11)]
        filas = [
            [int(v) for v in fila]
            for fila in filas_datos
        ]

        prefijos = [
            "x1 a x10", "x11 a x20", "x21 a x30",
            "x31 a x40", "x41 a x50", "x51 a x60",
        ]
        columnas_con_prefijo = ["Posiciones"] + columnas
        filas_con_prefijo = [
            [prefijos[i]] + fila for i, fila in enumerate(filas)
        ]

        tabla = self.agregar_tabla(columnas_con_prefijo, filas_con_prefijo,
                                   fila_resaltada=2, alto=6)
        tabla.arbol.column("Posiciones", width=100)

        x30 = float(ordenados[29])
        x31 = float(ordenados[30])
        self.agregar_texto(
            f"Datos centrales: x30 = {int(x30)}   x31 = {int(x31)}  "
            f"(fila resaltada en verde)\n"
            f"Mediana = ({int(x30)} + {int(x31)}) / 2 = {(x30 + x31) / 2:.1f}",
            color="#FEFCE8"
        )
