import tkinter as tk
from tkinter import ttk
import numpy as np

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaFrecuencias(PestanaBase):
    """
    Muestra el procedimiento de Sturges, la amplitud, los limites de
    cada intervalo y la tabla completa de frecuencias con explorador.
    """

    def construir(self) -> None:
        """Construye la pestana mostrando la tabla de frecuencias calculada con la regla de Sturges."""
        fr = self.frecuencias

        self.agregar_titulo("Distribucion de Frecuencias")
        self.agregar_separador()

        # ---------- STURGES ----------
        self.agregar_subtitulo("Regla de Sturges: numero de intervalos (k)")
        self.agregar_texto(
            "La regla de Sturges da un numero razonable de intervalos segun el tamano de la muestra.\n"
            "Ni pocos (perderíamos detalle) ni muchos (quedaria demasiado fragmentado).\n"
            "Formula: k = 1 + 3.322 \u00d7 log10(n)"
        )
        self.agregar_texto(
            f"k = 1 + 3.322 \u00d7 log10({self.conjunto.cantidad})\n"
            f"k = 1 + 3.322 \u00d7 {np.log10(self.conjunto.cantidad):.4f}\n"
            f"k = {fr.k_exacto:.4f}  \u2248  {fr.k} intervalos",
            color="#FEFCE8"
        )

        # ---------- AMPLITUD ----------
        self.agregar_separador()
        self.agregar_subtitulo("Amplitud de cada intervalo (A)")
        self.agregar_texto(
            "Formula: A = \u2308 R / k \u2309  (redondeo hacia arriba)\n"
            f"A = \u2308 {fr.rango:.0f} / {fr.k} \u2309 = \u2308 {fr.rango / fr.k:.2f} \u2309 = {int(fr.amplitud)}\n\n"
            "Se redondea hacia arriba para que todos los datos queden cubiertos."
        )

        # ---------- LIMITES ----------
        self.agregar_separador()
        self.agregar_subtitulo("Limites de los intervalos")
        self.agregar_texto(
            f"Se empieza desde el minimo (x_min = {int(self.conjunto.minimo)}) "
            f"y se suman {int(fr.amplitud)} unidades consecutivamente:\n"
            "  " + "  \u2192  ".join(
                str(int(fr.inicio + i * fr.amplitud))
                for i in range(fr.k + 1)
            ) + "\n\n"
            f"Esto da {fr.k} intervalos semiabiertos de la forma [a, b)."
        )

        # ---------- TABLA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Tabla de distribucion de frecuencias")
        self.agregar_texto(
            f"n = {self.conjunto.cantidad}  |  k = {fr.k} intervalos  |  A = {int(fr.amplitud)}\n"
            f"Clase modal (verde): {fr.clase_modal} con fi = {fr.frecuencia_modal} datos "
            f"({fr.frecuencia_modal / self.conjunto.cantidad * 100:.2f}%)"
        )

        df = fr.tabla
        columnas = ["Intervalo", "Marca mi", "fi", "Fi", "fri", "Fri", "fri %"]
        filas = []
        for _, fila in df.iterrows():
            filas.append([
                fila["Intervalo"],
                f"{fila['mi']:.0f}",
                int(fila["fi"]),
                int(fila["Fi"]),
                f"{fila['fri']:.4f}",
                f"{fila['Fri']:.4f}",
                f"{fila['fri'] * 100:.2f}%",
            ])
        tabla = self.agregar_tabla(columnas, filas,
                                   fila_resaltada=fr.indice_modal,
                                   alto=fr.k + 1)
        tabla.arbol.column("Intervalo", width=90)
        tabla.arbol.column("Marca mi", width=70)

        # ---------- COMO SE CUENTA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Como se cuenta la frecuencia de cada intervalo")
        self.agregar_texto(
            "Se toman los datos ordenados y se ve cuales caen dentro de cada rango.\n"
            "Ejemplo: en [2, 16) entran los datos: 2, 9, 10, 11, 12, 13, 14  →  fi = 7\n"
            "En [16, 30) entran: 19, 20, 21, 22, 23, 24, 26, 29  →  fi = 8\n"
            "Y asi sucesivamente para todos los intervalos."
        )

        # ---------- EXPLORADOR ----------
        self.agregar_separador()
        self.construir_explorador()

    def construir_explorador(self) -> None:
        """Crea un selector dropdown donde puedes escoger cada intervalo y ver sus datos.\n        Util para investigar exactamente que valores cayeron en cada rango."""
        self.agregar_subtitulo("Explorador de intervalos")
        self.agregar_texto("Selecciona un intervalo para ver exactamente que datos lo componen.")

        marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco.pack(fill="x", padx=16, pady=4)

        intervalos = self.frecuencias.tabla["Intervalo"].tolist()
        var = tk.StringVar(value=intervalos[0])

        combo = ttk.Combobox(marco, textvariable=var, values=intervalos,
                             state="readonly", width=14, font=Paleta.FUENTE_NORMAL)
        combo.pack(side="left", padx=(0, 10))

        resultado = tk.Frame(marco, bg=Paleta.FONDO_TARJETA, relief="flat", bd=1,
                             highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
        resultado.pack(side="left", fill="x", expand=True, padx=4)

        etiqueta = tk.Label(resultado, text="",
                            font=Paleta.FUENTE_NORMAL, bg=Paleta.FONDO_TARJETA,
                            fg="#555555", wraplength=700, justify="left",
                            padx=10, pady=8)
        etiqueta.pack(anchor="w")

        def al_seleccionar(evento=None):
            idx = intervalos.index(var.get())
            fila = self.frecuencias.tabla.iloc[idx]
            datos = self.frecuencias.datos_del_intervalo(idx)
            etiqueta.configure(text=(
                f"Intervalo: {var.get()}  |  Marca: {fila['mi']:.0f}  |  "
                f"fi = {int(fila['fi'])}  |  fri = {fila['fri']:.4f}  |  "
                f"Fi = {int(fila['Fi'])}\n"
                f"Datos en este intervalo: {datos}"
            ))

        combo.bind("<<ComboboxSelected>>", al_seleccionar)
        al_seleccionar()
