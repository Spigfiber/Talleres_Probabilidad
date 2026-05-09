from .pestana_base import PestanaBase


class PestanaDispersion(PestanaBase):
    """
    Muestra rango, varianza, desviacion estandar y coeficiente de variacion.
    Con un CV de ~51%, los datos tienen alta variabilidad relativa, lo que
    es esperable dado que cubren casi todo el rango [2, 99].
    """

    def construir(self) -> None:
        """Construye la pestana mostrando calculos de rango, varianza, desviacion y coeficiente de variacion."""
        dp = self.dispersion
        ct = self.centralizacion

        self.agregar_titulo("Medidas de Dispersion")
        self.agregar_tarjetas([
            ("Rango (R)",               f"{dp.rango:.0f}"),
            ("Varianza (\u03c3\u00b2)", f"{dp.varianza:.2f}"),
            ("Desv. Estandar (\u03c3)", f"{dp.desviacion:.2f}"),
            ("Coef. Variacion (CV)",    f"{dp.coeficiente_variacion:.1f}%"),
        ])

        # ---------- RANGO ----------
        self.agregar_separador()
        self.agregar_subtitulo("Rango (R)")
        self.agregar_texto(
            f"Formula: R = x_max \u2212 x_min\n"
            f"R = {int(self.conjunto.maximo)} \u2212 {int(self.conjunto.minimo)} = "
            f"{int(dp.rango)}\n\n"
            "Interpretacion: los datos se extienden a lo largo de 97 unidades. "
            "Dado que los valores van de 2 a 99, cubren practicamente todo el rango "
            "posible, lo que confirma una variabilidad alta."
        )

        # ---------- VARIANZA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Varianza Poblacional (\u03c3\u00b2)")
        self.agregar_texto(
            "Mide que tan lejos estan los datos, en promedio, respecto a la media.\n"
            "Se usa la formula computacional (equivalente a la definicion):\n"
            "  \u03c3\u00b2 = (\u03a3 xi\u00b2 / n) \u2212 x\u0305\u00b2"
        )
        self.agregar_texto(
            f"Paso 1: \u03a3 xi\u00b2 = {dp.suma_cuadrados:,.0f}\n"
            f"Paso 2: {dp.suma_cuadrados:,.0f} / {self.conjunto.cantidad} = "
            f"{dp.suma_cuadrados / self.conjunto.cantidad:.4f}\n"
            f"Paso 3: {dp.suma_cuadrados / self.conjunto.cantidad:.4f} \u2212 "
            f"({ct.media:.4f})\u00b2 = "
            f"{dp.suma_cuadrados / self.conjunto.cantidad:.4f} \u2212 "
            f"{ct.media**2:.4f} = {dp.varianza:.2f}",
            color="#FEFCE8"
        )
        self.agregar_texto(
            f"Interpretacion: la varianza de {dp.varianza:.2f} confirma "
            "que los datos tienen una dispersion considerable alrededor de la media."
        )

        # ---------- DESV ESTANDAR ----------
        self.agregar_separador()
        self.agregar_subtitulo("Desviacion Estandar (\u03c3)")
        bajo, alto = ct.media - dp.desviacion, ct.media + dp.desviacion
        self.agregar_texto(
            f"Formula: \u03c3 = \u221a\u03c3\u00b2 = \u221a{dp.varianza:.2f} = {dp.desviacion:.2f}\n\n"
            f"Interpretacion: en promedio, los datos se alejan {dp.desviacion:.2f} unidades "
            f"de la media ({ct.media:.2f}).\n"
            f"Un dato 'tipico' de esta distribucion esta entre "
            f"{bajo:.2f} y {alto:.2f}."
        )

        # ---------- COEFICIENTE DE VARIACION ----------
        self.agregar_separador()
        self.agregar_subtitulo("Coeficiente de Variacion (CV)")
        cv = dp.coeficiente_variacion
        self.agregar_texto(
            f"Formula: CV = (\u03c3 / x\u0305) \u00d7 100\n"
            f"CV = ({dp.desviacion:.2f} / {ct.media:.2f}) \u00d7 100 = {cv:.1f}%\n\n"
            "Un CV > 30% indica alta variabilidad relativa. "
            f"Con CV = {cv:.1f}%, los datos son muy dispersos respecto a su media, "
            "lo cual es esperable dado su origen aleatorio sobre un rango amplio.",
            color="#FFF7ED"
        )

        # ---------- INTERVALOS SIGMA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Intervalos sigma")
        columnas = ["Intervalo", "Lim. inferior", "Lim. superior", "Datos dentro", "Porcentaje"]
        filas = []
        for k in [1, 2, 3]:
            lo, hi = dp.intervalo_sigma(k)
            conteo = dp.conteo_en_intervalo(k)
            filas.append([
                f"x\u0305 \u00b1 {k}\u03c3",
                f"{lo:.2f}",
                f"{hi:.2f}",
                conteo,
                f"{conteo / self.conjunto.cantidad * 100:.1f}%",
            ])
        self.agregar_texto(
            f"Referencia teorica (normalidad): 68.3%, 95.4%, 99.7%\n"
            "Si los porcentajes observados se acercan a estos valores, la distribucion "
            "se comporta de manera similar a una normal."
        )
        self.agregar_tabla(columnas, filas, alto=3)

        # ---------- GRAFICO DE DESVIACIONES ----------
        self.agregar_separador()
        self.agregar_subtitulo("Desviacion de cada dato respecto a la media")
        self.agregar_grafico(self.graficas.desviaciones())
