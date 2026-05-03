import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from logica.datos import (
    TODOS_LOS_CONGLOMERADOS,
    CONGLOMERADOS_SELECCIONADOS,
    ESTUDIANTES_POR_SEMESTRE,
    N_POBLACION,
)
from .pestana_base import PestanaBase


class PestanaPoblacion(PestanaBase):
    """
    Muestra el planteamiento del problema, la definicion de la poblacion
    y el diagrama visual de los seis conglomerados con los seleccionados resaltados.
    Esta pestana es la introduccion del informe en formato interactivo.
    """

    def construir(self) -> None:
        self.agregar_titulo("Planteamiento del Problema y Poblacion")
        self.agregar_separador()

        self.agregar_subtitulo("Pregunta de investigacion")
        self.agregar_texto(
            "Como es el rendimiento academico (promedio de notas) de los estudiantes\n"
            "de Ingenieria de Sistemas de la Universidad Distrital, y que podemos\n"
            "concluir sobre su distribucion?",
            color="#EBF5FB"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Objetivo")
        self.agregar_texto(
            "Aplicar el muestreo por conglomerados al estudio del rendimiento academico,\n"
            "calcular las medidas estadisticas descriptivas sobre la muestra obtenida\n"
            "y analizar que tan bien representa el muestreo a la poblacion."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Definicion de la poblacion")

        self.agregar_tarjetas([
            ("Poblacion total (N)",        f"{N_POBLACION} estudiantes"),
            ("Semestres disponibles",      f"{len(TODOS_LOS_CONGLOMERADOS)} conglomerados"),
            ("Estudiantes por semestre",   f"{ESTUDIANTES_POR_SEMESTRE}"),
            ("Variable de estudio",        "Promedio academico (0.0 a 5.0)"),
        ])

        self.agregar_texto(
            "Unidad de analisis: estudiante activo del programa de Ingenieria de Sistemas\n"
            "que cursa del semestre I al VI en el periodo actual.\n"
            "Tipo de variable: cuantitativa continua en escala de 0.0 a 5.0.\n"
            "Nota minima aprobatoria: 3.0"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Diagrama de conglomerados")
        self.agregar_texto(
            "Los recuadros en verde son los tres semestres seleccionados al azar para la muestra.\n"
            "Los recuadros en gris son los semestres que NO entraron al muestreo."
        )
        self.construir_diagrama()

        self.agregar_separador()
        self.agregar_subtitulo("Que es el muestreo por conglomerados")
        self.agregar_texto(
            "Es una tecnica probabilistica donde la poblacion se divide en grupos naturales.\n"
            "Reglas clave:\n"
            "  1. Los grupos deben existir de forma natural, no se crean artificialmente.\n"
            "  2. Se seleccionan algunos grupos completos al azar.\n"
            "  3. Se estudian TODOS los elementos del grupo seleccionado.\n\n"
            "En este caso los grupos son los semestres del programa, que ya estan "
            "formados y organizados por la universidad."
        )

    def construir_diagrama(self) -> None:
        """
        Dibuja el diagrama de conglomerados usando un canvas de tkinter.
        Los semestres seleccionados se muestran en verde, los demas en gris.
        Se agrega una leyenda al pie del diagrama.
        """
        marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco.pack(fill="x", padx=16, pady=6)

        canvas = tk.Canvas(marco, height=260, bg=Paleta.FONDO_VENTANA,
                           highlightthickness=0)
        canvas.pack(fill="x")

        ancho = 800
        margen_x = 40
        espacio = (ancho - margen_x * 2) / len(TODOS_LOS_CONGLOMERADOS)
        y_centro = 120
        alto_caja = 80
        ancho_caja = int(espacio * 0.78)

        # Caja de poblacion total en la parte superior
        canvas.create_rectangle(280, 8, 520, 44, fill="#D6EAF8", outline="#2980B9", width=2)
        canvas.create_text(400, 26, text=f"Poblacion total: {N_POBLACION} estudiantes",
                           font=("Segoe UI", 12, "bold"), fill="#1B2A4A")

        # Linea que conecta la poblacion con los conglomerados
        canvas.create_line(400, 44, 400, 65, fill="#888888", width=1)

        for i, nombre in enumerate(TODOS_LOS_CONGLOMERADOS):
            cx = int(margen_x + i * espacio + espacio / 2)
            x1 = cx - ancho_caja // 2
            x2 = cx + ancho_caja // 2
            y1 = y_centro - alto_caja // 2
            y2 = y_centro + alto_caja // 2

            seleccionado = nombre in CONGLOMERADOS_SELECCIONADOS
            color_fondo  = "#D5F5E3" if seleccionado else "#F2F3F4"
            color_borde  = "#27AE60" if seleccionado else "#AAB7B8"
            grosor_borde = 2 if seleccionado else 1

            # Linea desde la caja de poblacion hasta cada conglomerado
            canvas.create_line(400, 65, cx, y1, fill="#BBBBBB", width=1)

            canvas.create_rectangle(x1, y1, x2, y2,
                                    fill=color_fondo, outline=color_borde,
                                    width=grosor_borde)

            etiqueta = nombre.replace("  ", " ").replace("(", "\n(")
            canvas.create_text(cx, y_centro - 12, text=etiqueta,
                               font=("Segoe UI", 11, "bold" if seleccionado else "normal"),
                               fill="#1B2A4A", justify="center")
            canvas.create_text(cx, y_centro + 18,
                               text=f"{ESTUDIANTES_POR_SEMESTRE} est.",
                               font=("Segoe UI", 10), fill="#555555")

            if seleccionado:
                canvas.create_text(cx, y_centro + 32, text="SELECCIONADO",
                                   font=("Segoe UI", 9, "bold"), fill="#27AE60")

        # Leyenda en la parte inferior del canvas
        canvas.create_rectangle(200, 210, 370, 240, fill="#D5F5E3", outline="#27AE60", width=2)
        canvas.create_text(285, 225, text="Conglomerado seleccionado",
                           font=("Segoe UI", 11), fill="#1B2A4A")

        canvas.create_rectangle(430, 210, 600, 240, fill="#F2F3F4", outline="#AAB7B8", width=1)
        canvas.create_text(515, 225, text="No seleccionado",
                           font=("Segoe UI", 11), fill="#555555")