import tkinter as tk

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaResumen(PestanaBase):
    """
    Vista final con tabla maestra de resultados, dashboard y conclusiones.
    """

    def construir(self) -> None:
        """Construye la pestana final con tabla resumen de todos los resultados y conclusiones."""
        ct = self.centralizacion
        dp = self.dispersion
        fr = self.frecuencias
        fm = self.forma
        h  = self.hipotesis
        n  = self.conjunto.cantidad

        self.agregar_titulo("Resumen de Resultados y Conclusiones")
        self.agregar_separador()

        # ---------- TABLA MAESTRA ----------
        self.agregar_subtitulo("Tabla resumen de todas las medidas")
        columnas = ["Categoria", "Medida", "Valor"]
        filas = [
            ["Centralizacion", "Media (x\u0305)",       f"{ct.media:.2f}"],
            ["Centralizacion", "Mediana (Me)",   f"{ct.mediana:.2f}"],
            ["Centralizacion", "Moda (Mo)",      f"{ct.moda_texto}  (unimodal)"],
            ["Dispersion",     "Rango (R)",      f"{dp.rango:.0f}"],
            ["Dispersion",     "Varianza",       f"{dp.varianza:.2f}"],
            ["Dispersion",     "Desv. Estandar", f"{dp.desviacion:.2f}"],
            ["Dispersion",     "Coef. Variacion",f"{dp.coeficiente_variacion:.1f}%"],
            ["Distribucion",   "N clases (k)",   str(fr.k)],
            ["Distribucion",   "Amplitud (A)",   str(int(fr.amplitud))],
            ["Distribucion",   "Clase modal",    fr.clase_modal],
            ["Forma",          "Asimetria",      fm.etiqueta_asimetria],
            ["Forma",          "Curtosis",       fm.etiqueta_curtosis],
            ["Poblacion",      "n",              str(n)],
            ["Hipotesis",      "H\u2080: \u03bc = 50", h.decision],
            ["Hipotesis",      "Z calculado",    f"{h.z_calculado:.3f}"],
            ["Hipotesis",      "Valor-p",        f"{h.valor_p:.4f}"],
        ]
        self.agregar_tabla(columnas, filas, alto=len(filas) + 1)

        # ---------- DASHBOARD ----------
        self.agregar_separador()
        self.agregar_subtitulo("Vista general de graficas")
        self.agregar_grafico(self.graficas.dashboard())

        # ---------- CONCLUSIONES ----------
        self.agregar_separador()
        self.construir_conclusiones()

    def construir_conclusiones(self) -> None:
        """Construye la seccion final con conclusiones detalladas sobre todo el analisis realizado."""
        ct = self.centralizacion
        dp = self.dispersion
        fr = self.frecuencias
        fm = self.forma
        h  = self.hipotesis
        n  = self.conjunto.cantidad

        self.agregar_subtitulo("Conclusiones")

        conclusiones = [
            (
                "1. Comportamiento general",
                f"Los datos se distribuyen de manera bastante uniforme a lo largo del rango "
                f"[{int(self.conjunto.minimo)}, {int(self.conjunto.maximo)}], con una tendencia central "
                f"alrededor de {ct.mediana}\u2013{ct.media:.2f}, confirmada por la media ({ct.media:.2f}) "
                f"y la mediana ({ct.mediana:.2f}) muy cercanas entre si."
            ),
            (
                "2. Nivel de dispersion",
                f"Con una desviacion estandar de {dp.desviacion:.2f} y un rango de {int(dp.rango)} unidades, "
                f"los datos tienen alta dispersion. El coeficiente de variacion del {dp.coeficiente_variacion:.1f}% "
                "confirma que no hay concentracion notable alrededor de la media."
            ),
            (
                "3. Tipo de distribucion",
                f"La distribucion es ligeramente asimetrica hacia la derecha "
                f"(sesgo positivo muy pequeno: {fm.diferencia_media_mediana:+.2f}) y de tipo "
                f"platicurtica (aplastada). Esto es esperado dada la naturaleza aleatoria de los datos."
            ),
            (
                "4. Moda",
                f"El unico valor que se repite es el {ct.moda_texto} ({ct.veces_moda} veces), "
                "lo que indica que practicamente todos los datos son unicos y que la distribucion "
                "no tiene un valor dominante. Esto refuerza el caracter uniforme de los datos."
            ),
            (
                "5. Tabla de frecuencias",
                f"La clase modal es {fr.clase_modal} con {fr.frecuencia_modal} datos "
                f"({fr.frecuencia_modal / n * 100:.2f}% de la poblacion). Las frecuencias de los "
                "demas intervalos son bastante similares entre si (entre 6 y 11 datos), lo que "
                "refuerza el caracter platicurtico de la distribucion."
            ),
            (
                "6. Prueba de hipotesis",
                f"La prueba Z bilateral con H\u2080: \u03bc = {h.mu0:.0f} y n = {h.n} datos "
                f"arrojo Z = {h.z_calculado:.3f} (valor-p = {h.valor_p:.4f}). "
                f"Como |Z| = {abs(h.z_calculado):.3f} < {h.z_critico:.2f}, {h.decision}. "
                f"Esto es consistente con que la media real de la poblacion es {ct.media:.2f}, "
                f"muy cercana a {h.mu0:.0f} dado el nivel de dispersion (\u03c3 = {dp.desviacion:.2f})."
            ),
        ]

        for titulo, texto in conclusiones:
            marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_TARJETA, relief="flat", bd=1,
                             highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
            marco.pack(fill="x", padx=16, pady=4)
            tk.Label(marco, text=titulo, font=("Segoe UI", 12, "bold"),
                     bg=Paleta.FONDO_TARJETA, fg=Paleta.TEXTO_TITULO,
                     padx=12).pack(anchor="w", pady=(8, 2))
            tk.Label(marco, text=texto, font=Paleta.FUENTE_NORMAL,
                     bg=Paleta.FONDO_TARJETA, fg="#444444",
                     wraplength=820, justify="left",
                     padx=12).pack(anchor="w", pady=(2, 10))
