import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaMuestra(PestanaBase):
    """
    Muestra el procedimiento de seleccion paso a paso, los datos de los
    36 estudiantes organizados por semestre, y los mismos datos ordenados
    de menor a mayor para facilitar el calculo de la mediana.
    """

    def construir(self) -> None:
        ms = self.muestreo

        self.agregar_titulo("Procedimiento de Muestreo y Datos Recolectados")
        self.agregar_separador()

        self.agregar_subtitulo("Tipo de muestreo")
        self.agregar_texto(
            "Muestreo por conglomerados de UNA SOLA ETAPA:\n"
            "se seleccionan los semestres al azar y se incluyen TODOS sus estudiantes.\n"
            "No se hace una segunda seleccion dentro del semestre."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Procedimiento de seleccion")
        for i, paso in enumerate(ms.pasos_seleccion, start=1):
            self.agregar_texto(f"Paso {i}: {paso}", color="#FDFEFE")

        self.agregar_tarjetas([
            ("Conglomerados seleccionados", f"{ms.conglomerados_muestra} de {ms.total_semestres}"),
            ("Probabilidad de seleccion",   f"{ms.probabilidad_seleccion:.0%}"),
            ("n de la muestra",             str(ms.n_muestra)),
            ("Fraccion de muestreo",        f"{ms.fraccion_muestreo:.1%}"),
        ])

        self.agregar_separador()
        self.agregar_subtitulo("Datos recolectados por semestre")
        self.agregar_texto(
            "Promedios academicos (escala 0.0 a 5.0) de los 12 estudiantes de cada\n"
            "semestre seleccionado. Se observa que los semestres mas avanzados tienen\n"
            "promedios mas altos: los estudiantes de bajo rendimiento de semestres\n"
            "tempranos ya no continuaron en el programa."
        )
        self.construir_tabla_por_conglomerado()

        self.agregar_separador()
        self.agregar_subtitulo("Datos ordenados de menor a mayor")
        self.agregar_texto(
            f"Los {self.conjunto.cantidad} promedios ordenados para calcular la mediana.\n"
            f"Con n par, los datos centrales son x18 y x19 (posiciones 18 y 19)."
        )
        self.construir_tabla_ordenada()

    def construir_tabla_por_conglomerado(self) -> None:
        """Tabla con tres filas, una por semestre, mostrando los 12 promedios."""
        nombres = self.conjunto.nombres_conglomerados
        sumas = self.conjunto.suma_por_conglomerado

        columnas = ["Semestre"] + [f"E{i}" for i in range(1, 13)] + ["Suma"]
        filas = []

        for nombre in nombres:
            datos = self.conjunto.por_conglomerado[nombre]
            etiqueta = nombre.replace("  ", " ")
            fila = [etiqueta] + [f"{v:.1f}" for v in datos] + [f"{sumas[nombre]:.1f}"]
            filas.append(fila)

        self.agregar_tabla(columnas, filas, alto=3)

        # Nota sobre la tendencia de semestres avanzados
        tk.Label(
            self.cuerpo,
            text="Los promedios tienden a subir en semestres mas avanzados porque "
                 "los estudiantes de bajo rendimiento no llegan a esos semestres.",
            font=Paleta.FUENTE_PEQUENA,
            bg=Paleta.FONDO_VENTANA, fg="#666666",
            wraplength=820, justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 4))

    def construir_tabla_ordenada(self) -> None:
        """Los 36 promedios en cuatro filas de 9 para replicar la tabla del informe."""
        ordenados = self.conjunto.ordenados
        filas_datos = ordenados.reshape(4, 9)

        columnas = [f"+{i}" for i in range(1, 10)]
        filas = [
            [f"{v:.1f}" for v in fila]
            for fila in filas_datos
        ]

        self.agregar_tabla(columnas, filas, alto=4)

        x18 = float(ordenados[17])
        x19 = float(ordenados[18])
        self.agregar_texto(
            f"Datos centrales: x18 = {x18:.1f}  y  x19 = {x19:.1f}  "
            f"(ambos resaltados en amarillo en el informe)\n"
            f"Mediana = ({x18:.1f} + {x19:.1f}) / 2 = {(x18 + x19) / 2:.2f}",
            color="#FEF9E7"
        )