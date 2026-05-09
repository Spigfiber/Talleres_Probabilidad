import tkinter as tk

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaHipotesis(PestanaBase):
    """
    Explica los conceptos de hipotesis estadistica y muestra el ejemplo
    practico del informe: prueba Z bilateral para la media de los 60 datos.
    H0: mu = 50  vs  H1: mu != 50  con n=36, x_barra=55, alpha=0.05
    Resultado: no se rechaza H0 (Z = 1.161 < 1.96)
    """

    def construir(self) -> None:
        """Construye la pestana que explica hipotesis estadisticas y muestra el test Z del informe."""
        h = self.hipotesis

        self.agregar_titulo("Complemento: Hipotesis Estadistica")
        self.agregar_separador()

        # ---------- DEFINICION ----------
        self.agregar_subtitulo("Definicion")
        self.agregar_texto(
            "Una hipotesis estadistica es una afirmacion o suposicion sobre uno o mas "
            "parametros de una poblacion (\u03bc, \u03c3 o p) que se somete a verificacion "
            "mediante datos muestrales.\n\n"
            "Tres caracteristicas fundamentales:\n"
            "  1. Basada en datos: se verifica con evidencia estadistica de una muestra representativa.\n"
            "  2. Sobre parametros: se refiere a caracteristicas desconocidas de la poblacion.\n"
            "  3. Verificable: puede ser rechazada o no rechazada con pruebas estadisticas; "
            "nunca se 'acepta' de forma definitiva."
        )

        # ---------- TIPOS H0 / H1 ----------
        self.agregar_separador()
        self.agregar_subtitulo("Tipos de hipotesis")
        columnas = ["Hipotesis", "Descripcion", "Ejemplo"]
        filas = [
            ["Nula (H\u2080)",
             "Hipotesis de 'no efecto'. Siempre incluye igualdad (=, \u2264 o \u2265). Es la que se pone a prueba.",
             "H\u2080: \u03bc = 30"],
            ["Alternativa (H\u2081)",
             "Lo que el investigador quiere demostrar. Determina si la prueba es bilateral o unilateral.",
             "H\u2081: \u03bc \u2260 30"],
        ]
        tabla = self.agregar_tabla(columnas, filas, alto=2)
        tabla.arbol.column("Hipotesis",   width=100)
        tabla.arbol.column("Descripcion", width=420)
        tabla.arbol.column("Ejemplo",     width=100)

        # ---------- TIPOS DE PRUEBA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Tipos de prueba segun la direccion")
        columnas2 = ["Tipo", "H\u2081", "Cuando usarla"]
        filas2 = [[t, h1, c] for t, h1, c in self.hipotesis.TIPOS_PRUEBA]
        tabla2 = self.agregar_tabla(columnas2, filas2, alto=3)
        tabla2.arbol.column("Tipo",        width=160)
        tabla2.arbol.column("H\u2081",     width=100)
        tabla2.arbol.column("Cuando usarla", width=380)

        # ---------- ERRORES ----------
        self.agregar_separador()
        self.agregar_subtitulo("Errores en la prueba de hipotesis")
        self.agregar_texto(
            "Al tomar una decision basada en una muestra siempre existe la posibilidad de equivocarse.\n\n"
            "Error Tipo I (\u03b1): rechazar H\u2080 cuando en realidad es verdadera.\n"
            "  Se controla fijando el nivel de significancia (\u03b1 = 0.05 o \u03b1 = 0.01 son los mas comunes).\n\n"
            "Error Tipo II (\u03b2): no rechazar H\u2080 cuando en realidad es falsa.\n"
            "  Se relaciona con la potencia de la prueba (1-\u03b2): capacidad de detectar un efecto real.\n\n"
            "Valor-p: probabilidad de obtener un resultado tan extremo si H\u2080 fuera cierta.\n"
            "  Un valor-p peque\u00f1o es evidencia fuerte contra H\u2080.\n"
            "  valor-p < \u03b1  \u21d2  Se rechaza H\u2080"
        )

        # ---------- EJEMPLO PRACTICO ----------
        self.agregar_separador()
        self.agregar_subtitulo("Ejemplo practico con los 60 datos del informe")
        self.agregar_texto(
            f"Parametros poblacionales calculados en este informe:\n"
            f"  N = {self.conjunto.cantidad}   \u03bc = {self.centralizacion.media:.2f}   "
            f"\u03c3 = {self.dispersion.desviacion:.2f}\n\n"
            f"Escenario: se extrae una muestra de n = {h.n} datos de la poblacion.\n"
            f"La muestra arroja una media muestral de x\u0305 = {h.x_barra:.2f}.\n"
            f"Pregunta: \u00bfrespaldan los datos muestrales que \u03bc = {h.mu0:.0f}? "
            f"(\u03b1 = {h.alpha})"
        )

        # Pasos del procedimiento
        pasos = [
            ("Paso 1 \u2014 Hipotesis",
             f"H\u2080: \u03bc = {h.mu0:.0f}     H\u2081: \u03bc \u2260 {h.mu0:.0f}\n"
             f"Prueba bilateral (dos colas) porque no se especifica una direccion concreta.",
             "#EFF6FF"),
            ("Paso 2 \u2014 Nivel de significancia y valores criticos",
             f"\u03b1 = {h.alpha}  \u2192  Z_\u03b1/2 = Z_0.025 = \u00b1{h.z_critico:.2f}",
             "#EFF6FF"),
            ("Paso 3 \u2014 Estadistico de prueba",
             "Se usa la prueba Z porque n \u2265 30 y \u03c3 es conocida (calculada sobre la poblacion).\n"
             "Formula: Z = (x\u0305 \u2212 \u03bc\u2080) / (\u03c3 / \u221an)",
             "#EFF6FF"),
            ("Paso 4 \u2014 Calculo del estadistico",
             f"Z = ({h.x_barra:.2f} \u2212 {h.mu0:.2f}) / ({h.sigma:.2f} / \u221a{h.n})\n"
             f"  = {h.x_barra - h.mu0:.2f} / ({h.sigma:.2f} / {h.n**0.5:.0f})\n"
             f"  = {h.x_barra - h.mu0:.2f} / {h.error_estandar:.3f}\n"
             f"  = {h.z_calculado:.3f}",
             "#FEFCE8"),
            ("Paso 5 \u2014 Region critica",
             f"Rechazar H\u2080 si  |Z| > {h.z_critico:.2f}\n"
             f"Es decir: si Z < -{h.z_critico:.2f}  o  Z > {h.z_critico:.2f}",
             "#EFF6FF"),
            ("Paso 6 \u2014 Decision",
             f"\u2212{h.z_critico:.2f} < Z = {h.z_calculado:.3f} < {h.z_critico:.2f}\n"
             f"  \u21d2  {h.decision}\n\n"
             f"Valor-p = {h.valor_p:.4f}  ({'< 0.05' if h.valor_p < 0.05 else '> 0.05'})\n\n"
             f"Conclusion: con \u03b1 = {h.alpha}, no hay evidencia estadistica suficiente "
             f"para rechazar que \u03bc = {h.mu0:.0f}. El estadistico Z = {h.z_calculado:.3f} "
             f"cae dentro de la zona de no rechazo [\u2212{h.z_critico:.2f}; {h.z_critico:.2f}], "
             f"lo cual es consistente con la media real de {self.centralizacion.media:.2f}.",
             "#F0FDF4" if not h.en_region_critica else "#FEF2F2"),
        ]

        for titulo, texto, color in pasos:
            marco = tk.Frame(self.cuerpo, bg=color, relief="flat", bd=1,
                             highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
            marco.pack(fill="x", padx=16, pady=3)
            tk.Label(marco, text=titulo, font=("Segoe UI", 12, "bold"),
                     bg=color, fg=Paleta.TEXTO_TITULO, padx=12).pack(anchor="w", pady=(6, 1))
            tk.Label(marco, text=texto, font=Paleta.FUENTE_NORMAL,
                     bg=color, fg="#333333", wraplength=820, justify="left",
                     padx=12).pack(anchor="w", pady=(1, 8))

        # Grafico de la prueba Z
        self.agregar_separador()
        self.agregar_subtitulo("Grafico de la prueba Z")
        self.agregar_texto(
            f"Las zonas rojas son las regiones de rechazo (|Z| > {h.z_critico:.2f}). "
            f"La linea azul es el estadistico calculado Z = {h.z_calculado:.3f}.\n"
            "Como la linea azul cae dentro de la zona blanca, no se rechaza H\u2080."
        )
        self.agregar_grafico(self.graficas.grafico_prueba_z())

        # Tabla de conceptos clave
        self.agregar_separador()
        self.agregar_subtitulo("Resumen de conceptos clave")
        columnas3 = ["Concepto", "Descripcion"]
        filas3 = list(self.hipotesis.CONCEPTOS)
        tabla3 = self.agregar_tabla(columnas3, filas3, alto=len(filas3) + 1)
        tabla3.arbol.column("Concepto",    width=160)
        tabla3.arbol.column("Descripcion", width=600)
