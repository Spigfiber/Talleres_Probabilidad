import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from interfaz.pestanas.pestana_poblacion import PestanaPoblacion
from interfaz.pestanas.pestana_muestra import PestanaMuestra
from interfaz.pestanas.pestana_estadistica import PestanaCentralizacion, PestanaDispersion, PestanaFrecuencias
from interfaz.pestanas.pestana_analisis import PestanaGraficas, PestanaForma, PestanaJustificacion, PestanaResumen


class VentanaPrincipal(tk.Tk):
    """
    Ventana principal de la aplicacion de muestreo por conglomerados.
    Contiene la barra superior, el sidebar con metricas clave
    y el notebook con nueve pestanas que cubren todas las secciones del informe.
    """

    ANCHO_SIDEBAR = 220

    def __init__(self, analisis: dict) -> None:
        super().__init__()
        self.analisis = analisis
        self.title("Muestreo por Conglomerados: Rendimiento Academico Ing. Sistemas")
        self.geometry("1320x840")
        self.minsize(960, 650)
        self.configure(bg=Paleta.FONDO_VENTANA)
        self.configurar_estilos()
        self.construir_layout()

    def configurar_estilos(self) -> None:
        """Aplica estilos ttk para un aspecto limpio y consistente."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TNotebook",
                         background=Paleta.FONDO_VENTANA, tabmargins=[2, 4, 0, 0])
        estilo.configure("TNotebook.Tab",
                         font=("Segoe UI", 11), padding=[12, 6],
                         background="#D5D8DC", foreground="#2C3E50")
        estilo.map("TNotebook.Tab",
                   background=[("selected", Paleta.BARRA)],
                   foreground=[("selected", "white")],
                   font=[("selected", ("Segoe UI", 11, "bold"))])
        estilo.configure("Pestana.TFrame", background=Paleta.FONDO_VENTANA)

    def construir_layout(self) -> None:
        self.construir_header()
        area = tk.Frame(self, bg=Paleta.FONDO_VENTANA)
        area.pack(fill="both", expand=True)
        self.construir_sidebar(area)
        self.construir_notebook(area)

    def construir_header(self) -> None:
        """Barra superior con titulo y autores."""
        header = tk.Frame(self, bg=Paleta.BARRA, height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Muestreo por Conglomerados  |  Rendimiento Academico Ing. Sistemas",
            font=("Segoe UI", 15, "bold"),
            bg=Paleta.BARRA, fg="white",
        ).pack(side="left", padx=20, pady=14)

        tk.Label(
            header,
            text="Ian Sandoval  |  Brayan Santos  |  Prof. Alberto Acosta",
            font=("Segoe UI", 11),
            bg=Paleta.BARRA, fg="#BDC3C7",
        ).pack(side="right", padx=20, pady=14)

    def construir_sidebar(self, padre) -> None:
        """
        Panel lateral con las metricas clave del analisis.
        Tambien muestra informacion del diseno muestral para que
        el usuario tenga siempre el contexto del muestreo visible.
        """
        ct = self.analisis["centralizacion"]
        dp = self.analisis["dispersion"]
        fm = self.analisis["forma"]
        ms = self.analisis["muestreo"]

        sidebar = tk.Frame(padre, bg=Paleta.FONDO_SIDEBAR, width=self.ANCHO_SIDEBAR)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        def grupo(titulo: str) -> None:
            tk.Label(sidebar, text=titulo, font=("Segoe UI", 11, "bold"),
                     bg=Paleta.FONDO_SIDEBAR, fg="#95A5A6").pack(
                anchor="w", padx=16, pady=(14, 2))

        def metrica(etiqueta: str, valor: str) -> None:
            fila = tk.Frame(sidebar, bg=Paleta.FONDO_SIDEBAR)
            fila.pack(fill="x", padx=16, pady=2)
            tk.Label(fila, text=etiqueta, font=("Segoe UI", 11),
                     bg=Paleta.FONDO_SIDEBAR, fg="#BDC3C7").pack(side="left")
            tk.Label(fila, text=valor, font=("Segoe UI", 11, "bold"),
                     bg=Paleta.FONDO_SIDEBAR, fg="white").pack(side="right")

        def linea() -> None:
            ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=12, pady=6)

        tk.Label(sidebar, text="Resumen",
                 font=("Segoe UI", 14, "bold"),
                 bg=Paleta.FONDO_SIDEBAR, fg="white").pack(anchor="w", padx=16, pady=(18, 4))

        linea()
        grupo("Muestreo")
        metrica("N poblacion", "72")
        metrica("n muestra",   str(ms.n_muestra))
        metrica("Semestres",   "II, IV y VI")
        metrica("Fraccion",    f"{ms.fraccion_muestreo:.1%}")

        linea()
        grupo("Centralizacion")
        metrica("Media",   f"{ct.media:.2f}")
        metrica("Mediana", f"{ct.mediana:.2f}")
        metrica("Moda",    ct.moda_texto)

        linea()
        grupo("Dispersion")
        metrica("Rango",      f"{dp.rango:.2f}")
        metrica("Desv. Est.", f"{dp.desviacion:.2f}")
        metrica("Varianza",   f"{dp.varianza:.4f}")
        metrica("CV",         f"{dp.coeficiente_variacion:.2f}%")

        linea()
        grupo("Forma")
        metrica("Asimetria", f"{fm.asimetria:.4f}")
        metrica("Curtosis",  f"{fm.curtosis:.4f}")

    def construir_notebook(self, padre) -> None:
        """Notebook con nueve pestanas, una por seccion del informe."""
        notebook = ttk.Notebook(padre)
        notebook.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        pestanas = [
            ("Poblacion",       PestanaPoblacion),
            ("Muestra",         PestanaMuestra),
            ("Centralizacion",  PestanaCentralizacion),
            ("Dispersion",      PestanaDispersion),
            ("Frecuencias",     PestanaFrecuencias),
            ("Graficas",        PestanaGraficas),
            ("Forma",           PestanaForma),
            ("Justificacion",   PestanaJustificacion),
            ("Resumen",         PestanaResumen),
        ]

        for nombre, Clase in pestanas:
            pestana = Clase(notebook, self.analisis)
            notebook.add(pestana, text=f"  {nombre}  ")

        # Un unico binding global que enruta el scroll al MarcoDesplazable visible.
        # bind_all captura el evento sin importar en que widget este el cursor,
        # por lo que no hace falta vincular nada en widgets hijos.
        self.bind_all("<MouseWheel>", self._enrutar_scroll)

    def _enrutar_scroll(self, evento) -> None:
        """
        Busca el MarcoDesplazable que esta dentro de la pestana activa y
        le delega el desplazamiento. Al ser un bind_all sobre la ventana
        raiz, este metodo es el unico punto de entrada para el scroll.
        """
        from interfaz.componentes import MarcoDesplazable
        widget = evento.widget
        # Subimos por la jerarquia de widgets hasta encontrar un MarcoDesplazable
        while widget is not None:
            if widget in MarcoDesplazable._instancias:
                widget.desplazar(evento.delta)
                return
            try:
                widget = widget.master
            except AttributeError:
                break

    def iniciar(self) -> None:
        """Lanza el loop principal de tkinter."""
        self.mainloop()