import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from visualizacion.estilos import Paleta


class MarcoDesplazable(tk.Frame):
    """Frame con barra de desplazamiento vertical."""

    _instancias: set = set()

    def __init__(self, padre, **opciones) -> None:
        super().__init__(padre, bg=Paleta.FONDO_VENTANA, **opciones)
        MarcoDesplazable._instancias.add(self)
        self.bind("<Destroy>", lambda e: MarcoDesplazable._instancias.discard(self))

        self.canvas = tk.Canvas(self, bg=Paleta.FONDO_VENTANA, highlightthickness=0)
        barra = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.interior = tk.Frame(self.canvas, bg=Paleta.FONDO_VENTANA)
        self.ventana_canvas = self.canvas.create_window(
            (0, 0), window=self.interior, anchor="nw"
        )

        self.interior.bind("<Configure>", self.al_cambiar_tamano)
        self.canvas.bind("<Configure>", self.al_cambiar_canvas)

    def al_cambiar_tamano(self, evento) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def al_cambiar_canvas(self, evento) -> None:
        self.canvas.itemconfig(self.ventana_canvas, width=evento.width)

    def desplazar(self, delta: int) -> None:
        self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")


class TarjetaMetrica(tk.Frame):
    """Tarjeta visual con etiqueta y valor grande."""

    def __init__(self, padre, etiqueta: str, valor: str, **opciones) -> None:
        super().__init__(
            padre,
            bg=Paleta.FONDO_TARJETA,
            relief="flat", bd=1,
            highlightbackground=Paleta.BORDE_TARJETA,
            highlightthickness=1,
            **opciones,
        )
        self.configure(padx=14, pady=10)
        tk.Label(self, text=etiqueta, font=Paleta.FUENTE_LABEL,
                 bg=Paleta.FONDO_TARJETA, fg="#888888").pack(anchor="w")
        tk.Label(self, text=valor, font=Paleta.FUENTE_VALOR,
                 bg=Paleta.FONDO_TARJETA, fg=Paleta.TEXTO_VALOR).pack(anchor="w")


class FilaTarjetas(tk.Frame):
    """Fila horizontal de tarjetas de metricas."""

    def __init__(self, padre, metricas: list[tuple[str, str]], **opciones) -> None:
        super().__init__(padre, bg=Paleta.FONDO_VENTANA, **opciones)
        for i, (etiqueta, valor) in enumerate(metricas):
            tarjeta = TarjetaMetrica(self, etiqueta, valor)
            tarjeta.grid(row=0, column=i, padx=6, pady=6, sticky="ew")
            self.columnconfigure(i, weight=1)


class TituloSeccion(tk.Label):
    """Titulo principal de cada seccion de la interfaz.
    Usa la fuente grande y el color oscuro para que destaque."""

    def __init__(self, padre, texto: str, **opciones) -> None:
        super().__init__(
            padre, text=texto,
            font=Paleta.FUENTE_TITULO,
            bg=Paleta.FONDO_VENTANA,
            fg=Paleta.TEXTO_TITULO,
            **opciones,
        )


class TextoInfo(tk.Label):
    """Etiqueta para mostrar texto informativo con fondo coloreado.
    Perfecta para explicaciones, notas y detalles adicionales de forma clara."""

    def __init__(self, padre, texto: str, color_fondo: str = "#EFF6FF", **opciones) -> None:
        super().__init__(
            padre, text=texto,
            font=Paleta.FUENTE_NORMAL,
            bg=color_fondo, fg="#1E3A5F",
            wraplength=820, justify="left",
            padx=10, pady=8,
            **opciones,
        )


class VistaTabla(tk.Frame):
    """Tabla interactiva basada en ttk.Treeview."""

    def __init__(
        self,
        padre,
        columnas: list[str],
        filas: list[list],
        fila_resaltada: int = -1,
        alto: int = 10,
        **opciones,
    ) -> None:
        super().__init__(padre, bg=Paleta.FONDO_VENTANA, **opciones)

        estilo = ttk.Style()
        estilo.configure("Tabla.Treeview", font=Paleta.FUENTE_NORMAL,
                         rowheight=30, background=Paleta.FONDO_TARJETA)
        estilo.configure("Tabla.Treeview.Heading",
                         font=("Segoe UI", 12, "bold"),
                         background=Paleta.FONDO_CABECERA)

        self.arbol = ttk.Treeview(
            self, columns=columnas, show="headings",
            height=alto, style="Tabla.Treeview",
        )
        for col in columnas:
            self.arbol.heading(col, text=col)
            self.arbol.column(col, anchor="center", width=110)

        for i, fila in enumerate(filas):
            tag = "modal" if i == fila_resaltada else ("par" if i % 2 == 0 else "impar")
            self.arbol.insert("", "end", values=[str(v) for v in fila], tags=(tag,))

        self.arbol.tag_configure("par",   background=Paleta.FONDO_TABLA_PAR)
        self.arbol.tag_configure("impar", background=Paleta.FONDO_TARJETA)
        self.arbol.tag_configure("modal", background=Paleta.FONDO_MODAL)

        barra_scroll = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra_scroll.set)
        self.arbol.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")


class PanelGrafico(tk.Frame):
    """Incrusta una figura matplotlib en un Frame de tkinter."""

    def __init__(self, padre, figura: Figure, **opciones) -> None:
        super().__init__(padre, bg=Paleta.FONDO_VENTANA, **opciones)

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        barra = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        barra.update()

        barra.pack(side="bottom", fill="x")
        canvas.get_tk_widget().pack(fill="both", expand=True)

    @staticmethod
    def reemplazar(padre, figura: Figure) -> "PanelGrafico":
        """Destruye el contenido anterior y reemplaza con un nuevo panel grafico.\n        Util para cambiar graficas dinamicamente (por ejemplo, toggle histograma)."""
        for hijo in padre.winfo_children():
            hijo.destroy()
        panel = PanelGrafico(padre, figura)
        panel.pack(fill="both", expand=True)
        return panel


class Separador(ttk.Separator):
    """Linea horizontal que divide visualmente las secciones.
    Le da respiro a la interfaz y organiza mejor el contenido."""

    def __init__(self, padre, **opciones) -> None:
        super().__init__(padre, orient="horizontal", **opciones)
