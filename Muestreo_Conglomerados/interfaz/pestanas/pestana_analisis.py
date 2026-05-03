import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from interfaz.componentes import PanelGrafico
from .pestana_base import PestanaBase


class PestanaGraficas(PestanaBase):
    """
    Muestra todos los graficos estadisticos del analisis:
    boxplot por semestre, histograma (con toggle), poligono,
    ojivas y la superposicion histograma mas poligono.
    """

    def construir(self) -> None:
        self.agregar_titulo("Graficas Estadisticas")
        self.agregar_separador()

        self.agregar_subtitulo("Distribucion de promedios por semestre")
        self.agregar_texto(
            "Cada caja representa un semestre. Los puntos individuales muestran "
            "los 12 promedios de cada grupo. La linea punteada gris es la nota minima aprobatoria (3.0)."
        )
        self.agregar_grafico(self.graficas.boxplot_por_conglomerado())
        self.agregar_separador()

        self.construir_histograma_interactivo()
        self.agregar_separador()

        self.agregar_subtitulo("Poligono de frecuencias")
        self.agregar_texto(
            "Las lineas verticales marcan la media (naranja) y la mediana (roja). "
            "La diferencia de posicion confirma el sesgo negativo leve."
        )
        self.agregar_grafico(self.graficas.poligono_frecuencias())
        self.agregar_separador()

        self.agregar_subtitulo("Ojiva de frecuencia acumulada")
        self.agregar_grafico(self.graficas.ojiva_absoluta())
        self.agregar_separador()

        self.agregar_subtitulo("Ojiva de frecuencia relativa acumulada")
        self.agregar_grafico(self.graficas.ojiva_relativa())
        self.agregar_separador()

        self.agregar_subtitulo("Histograma y poligono superpuestos")
        self.agregar_grafico(self.graficas.histograma_con_poligono())

    def construir_histograma_interactivo(self) -> None:
        """Histograma con checkbox para alternar frecuencias absolutas y relativas."""
        self.agregar_subtitulo("Histograma de frecuencias")
        self.agregar_texto(
            "La barra verde es la clase modal: promedios entre 3.6 y 4.0, "
            "con 11 estudiantes (30.56% de la muestra)."
        )

        controles = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        controles.pack(fill="x", padx=16, pady=(0, 4))

        usar_relativas = tk.BooleanVar(value=False)

        marco_hist = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco_hist.pack(fill="both", padx=16)
        PanelGrafico(marco_hist, self.graficas.histograma(False)).pack(fill="both", expand=True)

        def cambiar_tipo():
            PanelGrafico.reemplazar(marco_hist, self.graficas.histograma(usar_relativas.get()))

        ttk.Checkbutton(
            controles,
            text="Mostrar frecuencias relativas (%)",
            variable=usar_relativas,
            command=cambiar_tipo,
        ).pack(side="left")


class PestanaForma(PestanaBase):
    """
    Muestra la asimetria y curtosis de los promedios academicos.
    El sesgo es negativo porque los promedios bajos del Semestre II
    jalan la media hacia abajo. La curtosis es positiva (leptocurtica)
    porque la mayoria de los estudiantes se concentra en el rango 3.6 a 4.0.
    """

    def construir(self) -> None:
        fm = self.forma
        ct = self.centralizacion

        self.agregar_titulo("Forma de la Distribucion")
        self.agregar_tarjetas([
            ("Asimetria (Fisher)",          f"{fm.asimetria:.4f}"),
            ("Curtosis de exceso (Fisher)", f"{fm.curtosis:.4f}"),
            ("Media menos Mediana",         f"{fm.diferencia_media_mediana:.4f}"),
        ])
        self.agregar_separador()

        self.agregar_subtitulo("Asimetria")
        diff = fm.diferencia_media_mediana
        color = "#FDEDEC" if diff < 0 else "#EAFAF1"
        self.agregar_texto(
            f"Media = {ct.media:.2f}     Mediana = {ct.mediana:.2f}\n"
            f"Diferencia = {diff:.4f}  (negativa: la media esta a la izquierda de la mediana)\n\n"
            f"Resultado: {fm.etiqueta_asimetria}",
            color=color
        )
        self.agregar_texto(
            "Por que hay sesgo negativo: la mayoria de los estudiantes tiene promedios altos "
            "(entre 3.6 y 4.5), pero unos pocos con promedios bajos del Semestre II "
            "jalan la media hacia abajo sin mover la mediana. Eso genera una cola a la izquierda."
        )

        self.agregar_separador()
        self.agregar_subtitulo("Curtosis")
        self.agregar_texto(
            "Compara el pico de la distribucion con una normal estandar.\n"
            "Leptocurtica (mayor a 0): pico pronunciado, datos muy concentrados en el centro.\n"
            "Mesocurtica (igual a 0): similar a la normal.\n"
            "Platicurtica (menor a 0): distribucion aplanada, datos dispersos."
        )
        self.agregar_texto(
            f"Curtosis calculada = {fm.curtosis:.4f}\n"
            f"Resultado: {fm.etiqueta_curtosis}\n\n"
            "Los promedios se concentran bastante en las dos clases centrales "
            "[3.6, 4.0) y [4.0, 4.4) con 11 y 10 datos respectivamente, "
            "mientras los extremos tienen muy pocos casos (solo 2 cada uno).",
            color="#EAFAF1"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Densidad empirica vs curva normal de referencia")
        self.agregar_grafico(self.graficas.kde_vs_normal())

        self.agregar_separador()
        self.agregar_subtitulo("Grafico QQ: evaluacion de normalidad")
        self.agregar_texto(
            "Cuanto mas cerca esten los puntos de la linea roja, "
            "mas cerca esta la distribucion de ser normal."
        )
        self.agregar_grafico(self.graficas.grafico_qq())


class PestanaJustificacion(PestanaBase):
    """
    Explica por que se eligio el muestreo por conglomerados en este contexto,
    lo compara con otros metodos y muestra las ventajas y desventajas.
    Esta pestana no tiene graficos sino texto y tablas comparativas.
    """

    def construir(self) -> None:
        self.agregar_titulo("Justificacion del Muestreo por Conglomerados")
        self.agregar_separador()

        self.agregar_subtitulo("Por que conglomerados y no otro metodo?")
        razones = [
            ("1. Los grupos ya existen",
             "Los semestres son grupos naturales de la universidad. No hay que formarlos, "
             "lo que ahorra tiempo y hace el proceso mas realista."),
            ("2. Reduce costos y esfuerzo",
             "En lugar de buscar a 72 estudiantes individualmente, solo se necesita acceder "
             "a las listas de 3 cursos. En la practica significaria visitar 3 salones."),
            ("3. Es rapido y factible",
             "Un investigador puede recolectar los datos de un semestre completo en una sola sesion. "
             "Con muestreo aleatorio simple habria que contactar a estudiantes dispersos."),
            ("4. Es probabilistico",
             f"A diferencia del muestreo por conveniencia, cada conglomerado tiene la misma "
             f"probabilidad de ser seleccionado ({self.muestreo.probabilidad_seleccion:.0%}), "
             "lo que da representatividad estadistica."),
        ]

        for titulo, descripcion in razones:
            marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_TARJETA, relief="flat", bd=1,
                             highlightbackground=Paleta.BORDE_TARJETA, highlightthickness=1)
            marco.pack(fill="x", padx=16, pady=3)
            tk.Label(marco, text=titulo, font=("Segoe UI", 12, "bold"),
                     bg=Paleta.FONDO_TARJETA, fg=Paleta.TEXTO_TITULO,
                     padx=12).pack(anchor="w", pady=(7, 1))
            tk.Label(marco, text=descripcion, font=Paleta.FUENTE_NORMAL,
                     bg=Paleta.FONDO_TARJETA, fg="#444444",
                     wraplength=820, justify="left", padx=12).pack(anchor="w", pady=(1, 8))

        self.agregar_separador()
        self.agregar_subtitulo("Comparacion con otros metodos de muestreo")
        columnas = ["Metodo", "Como funcionaria aqui", "Por que no es mejor"]
        filas = [
            [
                m["Metodo"],
                m["Como funcionaria"],
                m["Por que no es mejor"],
            ]
            for m in self.muestreo.COMPARACION_METODOS
        ]
        tabla = self.agregar_tabla(columnas, filas, fila_resaltada=2, alto=4)
        tabla.arbol.column("Metodo", width=160)
        tabla.arbol.column("Como funcionaria aqui", width=280)
        tabla.arbol.column("Por que no es mejor", width=340)

        self.agregar_separador()
        self.construir_ventajas_desventajas()

    def construir_ventajas_desventajas(self) -> None:
        """Tabla de dos columnas con ventajas a la izquierda y desventajas a la derecha."""
        self.agregar_subtitulo("Ventajas y desventajas del muestreo por conglomerados")

        marco = tk.Frame(self.cuerpo, bg=Paleta.FONDO_VENTANA)
        marco.pack(fill="x", padx=16, pady=6)

        for titulo, items, color_fondo in [
            ("Ventajas", self.muestreo.VENTAJAS, "#EAFAF1"),
            ("Desventajas", self.muestreo.DESVENTAJAS, "#FDEDEC"),
        ]:
            columna = tk.LabelFrame(
                marco, text=titulo,
                font=("Segoe UI", 12, "bold"),
                bg=Paleta.FONDO_VENTANA, fg=Paleta.TEXTO_TITULO,
                padx=10, pady=8,
            )
            columna.pack(side="left", fill="both", expand=True, padx=6)

            for item in items:
                marco_item = tk.Frame(columna, bg=color_fondo, relief="flat",
                                      highlightbackground="#CCCCCC", highlightthickness=1)
                marco_item.pack(fill="x", pady=3)
                tk.Label(marco_item, text=f"  {item}", font=Paleta.FUENTE_NORMAL,
                         bg=color_fondo, fg="#333333",
                         wraplength=360, justify="left", padx=8, pady=6).pack(anchor="w")


class PestanaResumen(PestanaBase):
    """
    Vista final con la tabla maestra de resultados, el dashboard de
    cuatro graficos y las cinco conclusiones del informe.
    """

    def construir(self) -> None:
        ct = self.centralizacion
        dp = self.dispersion
        fr = self.frecuencias
        fm = self.forma
        n  = self.conjunto.cantidad

        self.agregar_titulo("Resumen de Resultados y Conclusiones")
        self.agregar_separador()

        self.agregar_subtitulo("Tabla resumen de todas las medidas")
        columnas = ["Categoria", "Medida", "Valor"]
        filas = [
            ["Centralizacion", "Media",              f"{ct.media:.2f}"],
            ["Centralizacion", "Mediana",            f"{ct.mediana:.2f}"],
            ["Centralizacion", "Moda",               ct.moda_texto + " (bimodal)"],
            ["Dispersion",     "Rango",              f"{dp.rango:.2f}"],
            ["Dispersion",     "Varianza",           f"{dp.varianza:.4f}"],
            ["Dispersion",     "Desv. Estandar",     f"{dp.desviacion:.2f}"],
            ["Dispersion",     "Coef. Variacion",    f"{dp.coeficiente_variacion:.2f}%"],
            ["Distribucion",   "Num. intervalos",    str(fr.k)],
            ["Distribucion",   "Amplitud",           f"{fr.amplitud:.1f}"],
            ["Distribucion",   "Clase modal",        fr.clase_modal],
            ["Forma",          "Asimetria",          fm.etiqueta_asimetria],
            ["Forma",          "Curtosis",           fm.etiqueta_curtosis],
            ["Muestreo",       "N poblacion",        "72"],
            ["Muestreo",       "n muestra",          str(n)],
            ["Muestreo",       "Fraccion muestreo",  f"{self.muestreo.fraccion_muestreo:.1%}"],
        ]
        self.agregar_tabla(columnas, filas, alto=len(filas) + 1)

        self.agregar_separador()
        self.agregar_subtitulo("Vista general de graficas")
        self.agregar_grafico(self.graficas.dashboard())

        self.agregar_separador()
        self.construir_conclusiones()

    def construir_conclusiones(self) -> None:
        """Cinco conclusiones del informe generadas con los valores calculados."""
        ct = self.centralizacion
        dp = self.dispersion
        fr = self.frecuencias
        n  = self.conjunto.cantidad

        self.agregar_subtitulo("Conclusiones")

        conclusiones = [
            (
                "1. Sobre el muestreo",
                "La tecnica de conglomerados permitio obtener una muestra de "
                f"{n} estudiantes de forma eficiente, sin necesidad de acceder "
                "a la lista completa de los 72. El proceso es replicable en "
                "cualquier contexto universitario real."
            ),
            (
                "2. Sobre el rendimiento academico",
                f"El promedio tipico es {ct.media:.2f} sobre 5.0, con mediana de {ct.mediana:.2f}. "
                "Esto indica un nivel aprobado y moderadamente satisfactorio. "
                f"Los valores bimodales ({ct.moda_texto}) muestran dos perfiles predominantes "
                "entre los estudiantes."
            ),
            (
                "3. Sobre la dispersion",
                f"Con sigma de {dp.desviacion:.2f}, la variabilidad es moderada. "
                "No hay estudiantes con notas extremadamente alejadas del promedio: "
                f"el rango va de {self.conjunto.minimo:.1f} a {self.conjunto.maximo:.1f}, "
                "consistente con el filtro academico que ocurre en semestres tempranos."
            ),
            (
                "4. Sobre la representatividad",
                "La muestra es probablemente representativa en terminos de rangos de notas, "
                "pero tiene un sesgo estructural: al excluir los semestres I, III y V, "
                "no se muestra la dificultad de los primeros semestres. Un muestreo "
                "estratificado habria dado mayor control sobre esto."
            ),
            (
                "5. Leccion principal",
                "El muestreo por conglomerados es ideal cuando los grupos ya existen y "
                "el acceso es mas facil por grupo que de forma individual. En entornos "
                "educativos, de salud o industriales, este tipo de muestreo es muy comun "
                "y practico. Sin embargo, siempre hay que evaluar si los grupos son "
                "suficientemente heterogeneos internamente para que la muestra sea representativa."
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