import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaCentralizacion(PestanaBase):
    """
    Muestra el procedimiento de media, mediana y moda para los promedios academicos.
    Hace enfasis en que la moda es bimodal (3.8 y 4.0) y en que la media es
    menor que la mediana, lo que indica sesgo negativo leve.
    """

    def construir(self) -> None:
        ct = self.centralizacion

        self.agregar_titulo("Medidas de Centralizacion")
        self.agregar_tarjetas([
            ("Media (x\u0305)",    f"{ct.media:.2f}"),
            ("Mediana (Me)", f"{ct.mediana:.2f}"),
            ("Moda (Mo)",    ct.moda_texto),
        ])

        self.agregar_separador()
        self.agregar_subtitulo("Media Aritmetica")
        self.agregar_texto(
            "El promedio academico tipico de un estudiante de la muestra.\n"
            "Se suman los promedios de los tres conglomerados y se divide entre n."
        )
        sumas = self.conjunto.suma_por_conglomerado
        detalle = "  +  ".join(f"{v:.1f}" for v in sumas.values())
        self.agregar_texto(
            f"Formula: x barra = suma de xi / n\n"
            f"Sumas por semestre: {detalle} = {self.conjunto.suma:.1f}\n"
            f"Media = {self.conjunto.suma:.1f} / {self.conjunto.cantidad} = {ct.media:.4f}",
            color="#FEF9E7"
        )
        self.agregar_texto(
            f"Interpretacion: el promedio academico tipico es {ct.media:.2f} sobre 5.0, "
            "un nivel aprobado y moderadamente satisfactorio."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Mediana")
        x18 = ct.posicion_baja
        x19 = ct.posicion_alta
        self.agregar_texto(
            f"Con n = {self.conjunto.cantidad} (par), la mediana es el promedio de x18 y x19.\n"
            f"Formula: Me = (x18 + x19) / 2\n"
            f"De la tabla ordenada: x18 = {x18:.1f}  y  x19 = {x19:.1f}\n"
            f"Me = ({x18:.1f} + {x19:.1f}) / 2 = {ct.mediana:.2f}",
            color="#FEF9E7"
        )
        self.agregar_texto(
            f"Que media ({ct.media:.2f}) sea menor que mediana ({ct.mediana:.2f}) indica "
            "un sesgo negativo leve: unos pocos promedios bajos del Semestre II jalan "
            "la media hacia abajo sin afectar la mediana.",
            color="#FDEDEC"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Moda")
        self.agregar_texto(
            "El valor (o valores) que mas veces aparecen en los 36 promedios.\n"
            "Este conjunto es BIMODAL: dos valores empatan en frecuencia maxima."
        )
        repetidos = [
            (v, c) for v, c in ct.tabla_frecuencias.items() if c >= 3
        ]
        repetidos.sort(key=lambda x: -x[1])

        columnas = ["Promedio", "Frecuencia"]
        filas = [[f"{v:.1f}", c] for v, c in repetidos]
        self.agregar_tabla(columnas, filas, alto=len(filas) + 1)

        self.agregar_texto(
            f"Moda = {ct.moda_texto}  (distribucion bimodal)\n"
            "Esto puede reflejar dos perfiles tipicos: estudiantes con promedio "
            "aceptable-bueno (3.8) y estudiantes de alto rendimiento (4.0).",
            color="#EAFAF1"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Comparacion visual de las tres medidas")
        self.agregar_grafico(self.graficas.densidad_con_centrales())


class PestanaDispersion(PestanaBase):
    """
    Muestra el rango, varianza y desviacion estandar de los promedios.
    Con datos en escala 0 a 5 los valores son mucho mas pequenos que en
    el primer informe, lo que se explica en los textos de interpretacion.
    """

    def construir(self) -> None:
        dp = self.dispersion
        ct = self.centralizacion

        self.agregar_titulo("Medidas de Dispersion")
        self.agregar_tarjetas([
            ("Rango (R)",               f"{dp.rango:.2f}"),
            ("Varianza (\u03c3\u00b2)", f"{dp.varianza:.4f}"),
            ("Desv. Estandar (\u03c3)", f"{dp.desviacion:.2f}"),
            ("Coef. Variacion",         f"{dp.coeficiente_variacion:.2f}%"),
        ])

        self.agregar_separador()
        self.agregar_subtitulo("Rango")
        self.agregar_texto(
            f"Formula: R = promedio maximo menos promedio minimo\n"
            f"R = {self.conjunto.maximo:.1f} menos {self.conjunto.minimo:.1f} = {dp.rango:.1f}\n\n"
            "Un rango de 2.0 sobre una escala de 5.0 indica variabilidad moderada. "
            "Los datos no estan ni muy concentrados ni extremadamente dispersos."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Varianza Poblacional")
        self.agregar_texto(
            "Mide que tan lejos estan los promedios de la media en promedio.\n"
            "Formula computacional: varianza = (suma de xi cuadrado / n) menos media al cuadrado"
        )
        self.agregar_texto(
            f"Paso 1: suma de xi cuadrado = {dp.suma_cuadrados:.2f}\n"
            f"Paso 2: {dp.suma_cuadrados:.2f} / {self.conjunto.cantidad} = "
            f"{dp.suma_cuadrados / self.conjunto.cantidad:.4f}\n"
            f"Paso 3: {dp.suma_cuadrados / self.conjunto.cantidad:.4f} menos "
            f"{ct.media:.4f} al cuadrado = {dp.varianza:.4f}",
            color="#FEF9E7"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Desviacion Estandar")
        bajo = ct.media - dp.desviacion
        alto = ct.media + dp.desviacion
        self.agregar_texto(
            f"Formula: sigma = raiz cuadrada de la varianza\n"
            f"sigma = raiz de {dp.varianza:.4f} = {dp.desviacion:.4f}\n\n"
            f"Un estudiante tipico de esta muestra tiene un promedio entre "
            f"{bajo:.2f} y {alto:.2f}."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Coeficiente de Variacion")
        cv = dp.coeficiente_variacion
        self.agregar_texto(
            f"Formula: CV = (sigma / media) por 100\n"
            f"CV = ({dp.desviacion:.2f} / {ct.media:.2f}) por 100 = {cv:.2f}%\n\n"
            f"Con CV menor al 30%, la variabilidad relativa es BAJA. "
            "Los promedios de la muestra son bastante homogeneos."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Intervalos sigma")
        columnas = ["Intervalo", "Limite inferior", "Limite superior", "Datos dentro", "Porcentaje"]
        filas = []
        for k in [1, 2, 3]:
            lo, hi = dp.intervalo_sigma(k)
            conteo = dp.conteo_en_intervalo(k)
            filas.append([
                f"media +/- {k} sigma",
                f"{lo:.2f}",
                f"{hi:.2f}",
                conteo,
                f"{conteo / self.conjunto.cantidad * 100:.1f}%",
            ])
        self.agregar_tabla(columnas, filas, alto=3)

        self.agregar_separador()
        self.agregar_subtitulo("Desviacion de cada promedio respecto a la media")
        self.agregar_grafico(self.graficas.desviaciones())


class PestanaFrecuencias(PestanaBase):
    """
    Muestra el procedimiento de Sturges, la tabla completa de frecuencias
    y el explorador interactivo de intervalos.
    """

    def construir(self) -> None:
        import numpy as np
        fr = self.frecuencias

        self.agregar_titulo("Distribucion de Frecuencias")
        self.agregar_separador()

        self.agregar_subtitulo("Regla de Sturges")
        self.agregar_texto(
            f"Formula: k = 1 + 3.322 * log10(n)\n"
            f"k = 1 + 3.322 * log10({self.conjunto.cantidad}) = "
            f"1 + 3.322 * {np.log10(self.conjunto.cantidad):.4f} = "
            f"{fr.k_exacto:.4f} redondeado a {fr.k}",
            color="#FEF9E7"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Amplitud")
        self.agregar_texto(
            f"Formula: A = redondear arriba (R / k)\n"
            f"A = redondear arriba ({fr.rango:.2f} / {fr.k}) = "
            f"redondear arriba ({fr.rango / fr.k:.3f}) = {fr.amplitud:.1f}\n"
            "Se redondea a 0.4 para obtener limites mas limpios en la escala de notas.",
            color="#FEF9E7"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Tabla de distribucion de frecuencias")
        self.agregar_texto(
            f"n = {self.conjunto.cantidad}  |  k = {fr.k} intervalos  |  A = {fr.amplitud:.1f}\n"
            f"Clase modal (verde): {fr.clase_modal} con fi = {fr.frecuencia_modal} estudiantes "
            f"({fr.frecuencia_modal / self.conjunto.cantidad * 100:.2f}%)"
        )

        df = fr.tabla
        columnas = ["Intervalo", "Marca mi", "fi", "Fi", "fri", "Fri", "fri %"]
        filas = []
        for _, fila in df.iterrows():
            filas.append([
                fila["Intervalo"],
                f"{fila['mi']:.1f}",
                int(fila["fi"]),
                int(fila["Fi"]),
                f"{fila['fri']:.4f}",
                f"{fila['Fri']:.4f}",
                f"{fila['fri'] * 100:.2f}%",
            ])
        self.agregar_tabla(columnas, filas, fila_resaltada=fr.indice_modal, alto=fr.k + 1)

        self.agregar_separador()
        self.construir_explorador()

    def construir_explorador(self) -> None:
        """Selector que muestra exactamente que promedios caen en cada intervalo."""
        self.agregar_subtitulo("Explorador de intervalos")
        self.agregar_texto("Selecciona un intervalo para ver que promedios lo componen.")

        marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco.pack(fill="x", padx=16, pady=4)

        intervalos = self.frecuencias.tabla["Intervalo"].tolist()
        var = tk.StringVar(value=intervalos[0])

        combo = ttk.Combobox(marco, textvariable=var, values=intervalos,
                             state="readonly", width=16, font=Paleta.FUENTE_NORMAL)
        combo.pack(side="left", padx=(0, 10))

        resultado = tk.Frame(marco, bg=Paleta.FONDO_TARJETA, relief="flat", bd=1,
                             highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
        resultado.pack(side="left", fill="x", expand=True, padx=4)

        etiqueta = tk.Label(resultado, text="Selecciona un intervalo",
                            font=Paleta.FUENTE_NORMAL, bg=Paleta.FONDO_TARJETA,
                            fg="#555555", wraplength=700, justify="left", padx=10, pady=8)
        etiqueta.pack(anchor="w")

        def al_seleccionar(evento=None):
            idx = intervalos.index(var.get())
            fila = self.frecuencias.tabla.iloc[idx]
            datos = self.frecuencias.datos_del_intervalo(idx)
            etiqueta.configure(
                text=(
                    f"Intervalo: {var.get()}  |  Marca: {fila['mi']:.1f}  |  "
                    f"fi = {int(fila['fi'])}  |  fri = {fila['fri']:.4f}  |  "
                    f"Fi = {int(fila['Fi'])}\n"
                    f"Promedios en este intervalo: {datos}"
                )
            )

        combo.bind("<<ComboboxSelected>>", al_seleccionar)
        al_seleccionar()