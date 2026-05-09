import tkinter as tk
from tkinter import ttk

from visualizacion.estilos import Paleta
from .pestana_base import PestanaBase


class PestanaCentralizacion(PestanaBase):
    """
    Muestra el procedimiento de calculo de media, mediana y moda.
    Con datos entre 2 y 99, la media (50.65) y la mediana (50.5)
    son casi identicas → distribucion practicamente simetrica.
    La moda es unimodal: solo el 55 se repite dos veces.
    """

    def construir(self) -> None:
        """Construye la pestana mostrando el calculo detallado de media, mediana y moda."""
        ct = self.centralizacion

        self.agregar_titulo("Medidas de Centralizacion")
        self.agregar_tarjetas([
            ("Media (x\u0305)",    f"{ct.media:.2f}"),
            ("Mediana (Me)", f"{ct.mediana:.2f}"),
            ("Moda (Mo)",    ct.moda_texto),
        ])

        # ---------- MEDIA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Media Aritmetica (x\u0305)")
        self.agregar_texto(
            "Es el promedio de todos los datos. Se suman los 60 valores y se divide entre n = 60.\n"
            "Formula: x\u0305 = (\u03a3 xi) / n"
        )
        sumas = self.conjunto.suma_por_fila
        linea_sumas = "  +  ".join(str(int(v)) for v in sumas.values())
        self.agregar_texto(
            f"Sumas por fila: {linea_sumas}\n"
            f"Total: {self.conjunto.suma:.0f}\n"
            f"Media = {self.conjunto.suma:.0f} / {self.conjunto.cantidad} = "
            f"{ct.media:.4f} \u2248 {ct.media:.2f}",
            color="#FEFCE8"
        )
        self.agregar_texto(
            f"Interpretacion: el valor promedio de este conjunto de datos es {ct.media:.2f}. "
            "Este valor esta justo en la parte media del rango [2, 99], lo que indica "
            "que los datos no estan sesgados hacia ningun extremo."
        )

        # ---------- MEDIANA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Mediana (Me)")
        self.agregar_texto(
            f"Con n = {self.conjunto.cantidad} (par), la mediana es el promedio de x30 y x31.\n"
            "Formula: Me = (x30 + x31) / 2"
        )
        x30 = ct.posicion_baja
        x31 = ct.posicion_alta
        self.agregar_texto(
            f"De la tabla ordenada:\n"
            f"  x30 = {int(x30)}   x31 = {int(x31)}\n"
            f"  Me = ({int(x30)} + {int(x31)}) / 2 = {(x30 + x31) / 2:.1f}",
            color="#FEFCE8"
        )
        self.agregar_texto(
            f"Interpretacion: la mitad de los datos es menor que {ct.mediana:.1f} "
            f"y la otra mitad es mayor. La diferencia con la media ({ct.media:.2f}) "
            f"es apenas {abs(ct.media - ct.mediana):.2f}, lo que confirma que la "
            "distribucion es casi simetrica.",
            color="#F0FDF4"
        )

        # ---------- MODA ----------
        self.agregar_separador()
        self.agregar_subtitulo("Moda (Mo)")
        self.agregar_texto(
            "Es el valor que mas veces aparece. Se recorre el conjunto buscando repeticiones.\n"
            f"El unico dato que se repite es el 55 (aparece {ct.veces_moda} veces: "
            "fila 2 posicion 4 y fila 5 posicion 5).\n"
            "El resto de los 60 valores son unicos."
        )
        self.agregar_texto(
            f"Mo = {ct.moda_texto}  (distribucion unimodal)\n"
            "Interpretacion: la escasa repeticion es consistente con el origen "
            "aleatorio de los datos; practicamente no hay un valor dominante.",
            color="#F0FDF4"
        )

        self.agregar_separador()
        self.agregar_subtitulo("Comparacion visual de las tres medidas")
        self.agregar_grafico(self.graficas.densidad_con_centrales())
