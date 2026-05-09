import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from interfaz.pestanas.pestana_datos import PestanaDatos
from interfaz.pestanas.pestana_centralizacion import PestanaCentralizacion
from interfaz.pestanas.pestana_dispersion import PestanaDispersion
from interfaz.pestanas.pestana_frecuencias import PestanaFrecuencias
from interfaz.pestanas.pestana_graficas import PestanaGraficas
from interfaz.pestanas.pestana_forma import PestanaForma
from interfaz.pestanas.pestana_hipotesis import PestanaHipotesis
from interfaz.pestanas.pestana_resumen import PestanaResumen


class VentanaPrincipal(tk.Tk):
    """
    Ventana principal de la aplicacion de estadistica descriptiva.
    Contiene la barra superior, el sidebar con metricas clave
    y el notebook con ocho pestanas que cubren todas las secciones del informe.
    """

    ANCHO_SIDEBAR = 220

    def __init__(self, analisis: dict) -> None:
        super().__init__()
        self.analisis = analisis
        self.title("Estadistica Descriptiva — 60 Datos Aleatorios")
        self.geometry("1320x840")
        self.minsize(960, 650)
        self.configure(bg=Paleta.FONDO_VENTANA)
        self.configurar_estilos()
        self.construir_layout()

    def configurar_estilos(self) -> None:
        """Define los estilos visuales para las pestanas del notebook.
        Configura colores, fuentes y efectos visuales cuando se selecciona una pestana."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TNotebook",
                         background=Paleta.FONDO_VENTANA, tabmargins=[2, 4, 0, 0])
        estilo.configure("TNotebook.Tab",
                         font=("Segoe UI", 11), padding=[12, 6],
                         background="#CBD5E1", foreground="#1E293B")
        estilo.map("TNotebook.Tab",
                   background=[("selected", Paleta.BARRA)],
                   foreground=[("selected", "white")],
                   font=[("selected", ("Segoe UI", 11, "bold"))])
        estilo.configure("Pestana.TFrame", background=Paleta.FONDO_VENTANA)

    def construir_layout(self) -> None:
        """Organiza la estructura principal: header, sidebar con metricas y notebook con pestanas."""
        self.construir_header()
        area = tk.Frame(self, bg=Paleta.FONDO_VENTANA)
        area.pack(fill="both", expand=True)
        self.construir_sidebar(area)
        self.construir_notebook(area)

    def construir_header(self) -> None:
        """Crea la barra superior azul con el titulo de la app y los autores."""
        header = tk.Frame(self, bg=Paleta.BARRA, height=56)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Estadistica Descriptiva  |  Analisis de 60 Datos Aleatorios",
            font=("Segoe UI", 15, "bold"),
            bg=Paleta.BARRA, fg="white",
        ).pack(side="left", padx=20, pady=14)

        tk.Label(
            header,
            text="Ian Sandoval  |  Brayan Santos  |  Prof. Alberto Acosta",
            font=("Segoe UI", 11),
            bg=Paleta.BARRA, fg="#BFDBFE",
        ).pack(side="right", padx=20, pady=14)

    def construir_sidebar(self, padre) -> None:
        """Construye el panel lateral oscuro que muestra todas las metricas clave del analisis.
        Agrupa las medidas por categoria: poblacion, centralizacion, dispersion, etc."""
        ct = self.analisis["centralizacion"]
        dp = self.analisis["dispersion"]
        fm = self.analisis["forma"]
        fr = self.analisis["frecuencias"]
        h  = self.analisis["hipotesis"]

        sidebar = tk.Frame(padre, bg=Paleta.FONDO_SIDEBAR, width=self.ANCHO_SIDEBAR)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        def grupo(titulo: str) -> None:
            tk.Label(sidebar, text=titulo, font=("Segoe UI", 11, "bold"),
                     bg=Paleta.FONDO_SIDEBAR, fg="#94A3B8").pack(
                anchor="w", padx=16, pady=(14, 2))

        def metrica(etiqueta: str, valor: str) -> None:
            fila = tk.Frame(sidebar, bg=Paleta.FONDO_SIDEBAR)
            fila.pack(fill="x", padx=16, pady=2)
            tk.Label(fila, text=etiqueta, font=("Segoe UI", 11),
                     bg=Paleta.FONDO_SIDEBAR, fg="#CBD5E1").pack(side="left")
            tk.Label(fila, text=valor, font=("Segoe UI", 11, "bold"),
                     bg=Paleta.FONDO_SIDEBAR, fg="white").pack(side="right")

        def linea() -> None:
            ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=12, pady=6)

        tk.Label(sidebar, text="Resumen",
                 font=("Segoe UI", 14, "bold"),
                 bg=Paleta.FONDO_SIDEBAR, fg="white").pack(anchor="w", padx=16, pady=(18, 4))

        linea()
        grupo("Poblacion")
        metrica("n",      "60")
        metrica("Minimo", "2")
        metrica("Maximo", "99")
        metrica("Rango",  f"{int(dp.rango)}")

        linea()
        grupo("Centralizacion")
        metrica("Media",   f"{ct.media:.2f}")
        metrica("Mediana", f"{ct.mediana:.2f}")
        metrica("Moda",    ct.moda_texto)

        linea()
        grupo("Dispersion")
        metrica("Varianza",   f"{dp.varianza:.2f}")
        metrica("Desv. Est.", f"{dp.desviacion:.2f}")
        metrica("CV",         f"{dp.coeficiente_variacion:.1f}%")

        linea()
        grupo("Frecuencias")
        metrica("k",          str(fr.k))
        metrica("Amplitud",   str(int(fr.amplitud)))
        metrica("Cl. modal",  fr.clase_modal.strip())

        linea()
        grupo("Forma")
        metrica("Asimetria", f"{fm.asimetria:.4f}")
        metrica("Curtosis",  f"{fm.curtosis:.4f}")

        linea()
        grupo("Hipotesis (Z)")
        metrica("Z calc.", f"{h.z_calculado:.3f}")
        metrica("Z crit.", f"\u00b1{h.z_critico:.2f}")
        metrica("Valor-p", f"{h.valor_p:.4f}")

    def construir_notebook(self, padre) -> None:
        """Crea el contenedor de pestanas con todos los analisis y graficas.
        Cada pestana contiene un tipo diferente de analisis estadistico."""
        notebook = ttk.Notebook(padre)
        notebook.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        pestanas = [
            ("Datos",           PestanaDatos),
            ("Centralizacion",  PestanaCentralizacion),
            ("Dispersion",      PestanaDispersion),
            ("Frecuencias",     PestanaFrecuencias),
            ("Graficas",        PestanaGraficas),
            ("Forma",           PestanaForma),
            ("Hipotesis",       PestanaHipotesis),
            ("Resumen",         PestanaResumen),
        ]

        for nombre, Clase in pestanas:
            pestana = Clase(notebook, self.analisis)
            notebook.add(pestana, text=f"  {nombre}  ")

        self.bind_all("<MouseWheel>", self._enrutar_scroll)

    def _enrutar_scroll(self, evento) -> None:
        """Maneja el scroll del mouse dirigiendo el evento al marco desplazable correcto."""
        from interfaz.componentes import MarcoDesplazable
        widget = evento.widget
        while widget is not None:
            if widget in MarcoDesplazable._instancias:
                widget.desplazar(evento.delta)
                return
            try:
                widget = widget.master
            except AttributeError:
                break

    def iniciar(self) -> None:
        """Inicia el loop principal de la ventana para mostrar la interfaz al usuario."""
        self.mainloop()
