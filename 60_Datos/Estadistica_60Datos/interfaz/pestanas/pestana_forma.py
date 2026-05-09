from .pestana_base import PestanaBase


class PestanaForma(PestanaBase):
    """
    Muestra la asimetria (sesgo) y curtosis de los 60 datos.
    Sesgo: positivo muy leve (media apenas 0.15 mayor que mediana).
    Curtosis: negativa (platicurtica) por la distribucion uniforme-ish de los datos.
    """

    def construir(self) -> None:
        """Construye la pestana que analiza la asimetria y curtosis de la distribucion."""
        fm = self.forma
        ct = self.centralizacion

        self.agregar_titulo("Forma de la Distribucion")
        self.agregar_tarjetas([
            ("Asimetria (Fisher)",          f"{fm.asimetria:.4f}"),
            ("Curtosis de exceso (Fisher)", f"{fm.curtosis:.4f}"),
            ("Media \u2212 Mediana",        f"{fm.diferencia_media_mediana:.4f}"),
        ])

        # ---------- ASIMETRIA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Asimetria (Sesgo)")
        self.agregar_texto(
            "La forma mas directa de determinar el sesgo sin el coeficiente formal de Pearson "
            "es comparar la media con la mediana."
        )

        diff = fm.diferencia_media_mediana
        color = "#FFF7ED" if diff > 0 else "#FEF2F2"
        self.agregar_texto(
            f"Media = {ct.media:.2f}     Mediana = {ct.mediana:.2f}\n"
            f"Diferencia x\u0305 \u2212 Me = {diff:+.4f}\n\n"
            f"x\u0305 > Me  \u21d2  {fm.etiqueta_asimetria}",
            color=color
        )
        self.agregar_texto(
            f"Interpretacion: la diferencia entre media ({ct.media:.2f}) y mediana "
            f"({ct.mediana:.2f}) es apenas {abs(diff):.2f}, lo que indica que el sesgo "
            "es muy leve. En la practica, la distribucion es casi simetrica. "
            "Esto tiene sentido: al ser datos aleatorios sobre un rango amplio, "
            "no hay concentracion fuerte en ningun extremo."
        )

        self.agregar_subtitulo("Tipos de asimetria")
        tipos = [
            ("\u25b6  Sesgo positivo (x\u0305 > Me)",
             "Cola hacia la derecha. Los valores extremos altos jalan la media hacia arriba."),
            ("\u25c4  Sesgo negativo (x\u0305 < Me)",
             "Cola hacia la izquierda. Los valores extremos bajos jalan la media hacia abajo."),
            ("\u2194  Sin sesgo (x\u0305 \u2248 Me)",
             "Distribucion simetrica. La media y la mediana coinciden (o se acercan mucho)."),
        ]
        for titulo, desc in tipos:
            self._tarjeta_concepto(titulo, desc, "#F8FAFC")

        # ---------- CURTOSIS ----------
        self.agregar_separador()
        self.agregar_subtitulo("Curtosis")
        self.agregar_texto(
            "Describe el 'pico' de la distribucion comparado con una normal estandar.\n"
            "Se usa la curtosis de exceso: si > 0 es mas puntiaguda que la normal, "
            "si < 0 es mas aplastada."
        )

        color_k = "#FEF2F2" if fm.curtosis < 0 else "#F0FDF4"
        self.agregar_texto(
            f"Curtosis de exceso = {fm.curtosis:.4f}\n"
            f"Resultado: {fm.etiqueta_curtosis}",
            color=color_k
        )
        self.agregar_texto(
            "Interpretacion: la distribucion es platicurtica porque los datos estan "
            "dispersos a lo largo de un rango amplio (97 unidades) y las frecuencias "
            "por intervalo son relativamente uniformes (entre 6 y 11). "
            "No hay concentracion fuerte alrededor de la media."
        )

        self.agregar_subtitulo("Tipos de curtosis")
        tipos_k = [
            ("Leptocurtica (curtosis > 0)",
             "Pico pronunciado. Datos muy concentrados en el centro, colas pesadas."),
            ("Mesocurtica (curtosis \u2248 0)",
             "Similar a la normal. Pico y colas de referencia."),
            ("Platicurtica (curtosis < 0)",
             "Distribucion aplastada. Datos dispersos sin pico marcado. Es nuestro caso."),
        ]
        for titulo, desc in tipos_k:
            self._tarjeta_concepto(titulo, desc, "#F8FAFC")

        # ---------- GRAFICOS ----------
        self.agregar_separador()
        self.agregar_subtitulo("Densidad empirica vs curva normal de referencia")
        self.agregar_texto(
            "La curva azul es la densidad empirica suavizada (KDE) de los 60 datos. "
            "La curva roja punteada es la distribucion normal con la misma media y sigma. "
            "Si la distribucion fuera perfectamente normal, ambas curvas coincidirian."
        )
        self.agregar_grafico(self.graficas.kde_vs_normal())

        self.agregar_separador()
        self.agregar_subtitulo("Grafico QQ: evaluacion de normalidad")
        self.agregar_texto(
            "Cuanto mas cerca esten los puntos de la linea roja, "
            "mas cerca esta la distribucion de ser normal. "
            "Desviaciones sistematicas indican asimetria o colas no normales."
        )
        self.agregar_grafico(self.graficas.grafico_qq())

    def _tarjeta_concepto(self, titulo: str, desc: str, color: str) -> None:
        """Crea una tarjeta de titulo + descripcion para tipos de asimetria/curtosis."""
        import tkinter as tk
        from visualizacion.estilos import Paleta
        marco = tk.Frame(self.cuerpo, bg=color, relief="flat", bd=1,
                         highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
        marco.pack(fill="x", padx=16, pady=2)
        tk.Label(marco, text=titulo, font=("Segoe UI", 12, "bold"),
                 bg=color, fg=Paleta.TEXTO_TITULO, padx=12).pack(anchor="w", pady=(5, 0))
        tk.Label(marco, text=desc, font=Paleta.FUENTE_NORMAL,
                 bg=color, fg="#444444", wraplength=820, justify="left",
                 padx=12).pack(anchor="w", pady=(0, 6))
