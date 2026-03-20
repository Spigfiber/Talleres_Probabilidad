"""
T4 - Distribuciones de Probabilidad
Binomial · Poisson · Normal · Exponencial
Valida los ejercicios del informe LaTeX con scipy.stats
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import tkinter as tk
from tkinter import font as tkfont

# Colores 
C_AZUL   = "#1a5a9e"
C_ROJO   = "#c0392b"
C_VERDE  = "#27ae60"
C_MORADO = "#8e44ad"
C_GRIS   = "#7f8c8d"
C_FONDO  = "#f4f6f9"
C_CARD   = "#ffffff"
C_LINE   = "#dde3ec"
C_TEXT   = "#2c3e50"
C_MUTED  = "#95a5a6"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    12,
    "axes.labelsize":    10,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.facecolor":  C_FONDO,
})

SEP = "─" * 56

def titulo(texto):
    print(f"\n{'═'*56}\n  {texto}\n{'═'*56}")

def seccion(texto):
    print(f"\n  [{texto}]\n  {SEP}")


#  1 · BINOMIAL

def dist_binomial():
    titulo("DISTRIBUCIÓN BINOMIAL")

    d5  = stats.binom(n=5, p=0.5)   # moneda
    d4  = stats.binom(n=4, p=0.5)   # familia

    seccion("Ejercicio 1 · Moneda  [n=5, p=0.5]")
    print(f"  P(X = 3)  = {d5.pmf(3):.4f}   [LaTeX: 0.3125]")
    print(f"  P(X ≤ 2)  = {d5.cdf(2):.4f}   [LaTeX: 0.5000]")
    print(f"  E[X]      = {d5.mean():.4f}   [LaTeX: 2.5000]")
    print(f"  Var(X)    = {d5.var():.4f}   [LaTeX: 1.2500]")

    seccion("Ejercicio 2 · Familia  [n=4, p=0.5]")
    print(f"  P(X = 2)  = {d4.pmf(2):.4f}   [LaTeX: 0.3750]")
    print(f"  P(X ≥ 3)  = {1-d4.cdf(2):.4f}   [LaTeX: 0.3125]")
    print(f"  E[X]      = {d4.mean():.4f}   [LaTeX: 2.0000]")
    print(f"  Var(X)    = {d4.var():.4f}   [LaTeX: 1.0000]")

    # Gráficas
    fig = plt.figure(figsize=(13, 7), facecolor=C_FONDO)
    fig.suptitle("Distribución Binomial", fontsize=14,
                 fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.50, wspace=0.32,
                           left=0.08, right=0.97,
                           top=0.90, bottom=0.09)

    k5 = np.arange(0, 6)
    k4 = np.arange(0, 5)

    # 1a) FMP moneda
    ax1 = fig.add_subplot(gs[0, 0])
    col5 = [C_ROJO if k <= 2 else C_AZUL for k in k5]
    bars = ax1.bar(k5, d5.pmf(k5), color=col5,
                   width=0.6, edgecolor="white", linewidth=1.2)
    ax1.set_title("FMP Bin(5, 0.5)\nRojo: P(X≤2) = 0.50",
                  fontweight="bold")
    ax1.set_xlabel("k"); ax1.set_ylabel("P(X = k)")
    ax1.set_xticks(k5)
    for b, v in zip(bars, d5.pmf(k5)):
        ax1.text(b.get_x()+b.get_width()/2,
                 b.get_height()+0.008,
                 f"{v:.4f}", ha="center",
                 fontsize=8, fontweight="bold")
    ax1.set_ylim(0, 0.42)

    # 1b) FDA moneda
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.step(k5, d5.cdf(k5), where="post",
             color=C_AZUL, lw=2.5)
    ax2.axhline(0.5, color=C_ROJO, linestyle="--",
                lw=1.5, label="F(2) = 0.50")
    ax2.set_title("FDA Bin(5, 0.5)", fontweight="bold")
    ax2.set_xlabel("k"); ax2.set_ylabel("F(k)")
    ax2.set_xticks(k5); ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=9)

    # 2a) FMP familia
    ax3 = fig.add_subplot(gs[1, 0])
    col4 = [C_VERDE if k >= 3 else C_MORADO for k in k4]
    bars2 = ax3.bar(k4, d4.pmf(k4), color=col4,
                    width=0.5, edgecolor="white", linewidth=1.2)
    ax3.set_title("FMP Bin(4, 0.5)\nVerde: P(X≥3) = 0.3125",
                  fontweight="bold")
    ax3.set_xlabel("k"); ax3.set_ylabel("P(X = k)")
    ax3.set_xticks(k4)
    for b, v in zip(bars2, d4.pmf(k4)):
        ax3.text(b.get_x()+b.get_width()/2,
                 b.get_height()+0.008,
                 f"{v:.4f}", ha="center",
                 fontsize=9, fontweight="bold")
    ax3.set_ylim(0, 0.48)

    # 2b) Comparación Bin(5,0.5) vs Bin(4,0.5)
    ax4 = fig.add_subplot(gs[1, 1])
    x_max = np.arange(0, 6)
    ax4.plot(k5, d5.pmf(k5), "o-", color=C_AZUL,
             lw=2, markersize=6, label="Bin(5, 0.5)")
    ax4.plot(k4, d4.pmf(k4), "s-", color=C_MORADO,
             lw=2, markersize=6, label="Bin(4, 0.5)")
    ax4.axvline(d5.mean(), color=C_AZUL,   lw=1.5,
                linestyle="--", alpha=0.7)
    ax4.axvline(d4.mean(), color=C_MORADO, lw=1.5,
                linestyle="--", alpha=0.7)
    ax4.set_title("Comparación Bin(5) vs Bin(4)",
                  fontweight="bold")
    ax4.set_xlabel("k")
    ax4.legend(fontsize=9); ax4.set_ylim(0, 0.45)

    plt.show()


#  2 · POISSON

def dist_poisson():
    titulo("DISTRIBUCIÓN DE POISSON")

    d2 = stats.poisson(mu=2)
    d3 = stats.poisson(mu=3)

    seccion("Ejercicio 1 · Clientes por hora  [λ=2]")
    print(f"  P(X = 0)  = {d2.pmf(0):.4f}   [LaTeX: 0.1353]")
    print(f"  P(X = 2)  = {d2.pmf(2):.4f}   [LaTeX: 0.2707]")
    print(f"  P(X > 3)  = {1-d2.cdf(3):.4f}   [LaTeX: 0.1429]")

    seccion("Ejercicio 2 · Mensajes por minuto  [λ=3]")
    print(f"  P(X = 1)  = {d3.pmf(1):.4f}   [LaTeX: 0.1494]")
    print(f"  P(X ≤ 2)  = {d3.cdf(2):.4f}   [LaTeX: 0.4232]")
    print(f"  E[X]      = {d3.mean():.4f}   [LaTeX: 3.0000]")
    print(f"  σ(X)      = {d3.std():.4f}   [LaTeX: 1.7321]")

    # Gráficas 
    fig = plt.figure(figsize=(13, 7), facecolor=C_FONDO)
    fig.suptitle("Distribución de Poisson", fontsize=14,
                 fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.50, wspace=0.32,
                           left=0.08, right=0.97,
                           top=0.90, bottom=0.09)

    k = np.arange(0, 11)

    # 1a) FMP λ=2
    ax1 = fig.add_subplot(gs[0, 0])
    col2 = [C_ROJO   if v == 0 else
            (C_VERDE if v > 3 else C_MORADO)
            for v in k]
    bars = ax1.bar(k, d2.pmf(k), color=col2,
                   width=0.6, edgecolor="white", linewidth=1.2)
    ax1.set_title("FMP Poisson(2)\nRojo: X=0 · Verde: X>3",
                  fontweight="bold")
    ax1.set_xlabel("k"); ax1.set_ylabel("P(X = k)")
    ax1.set_xticks(k)
    for b, v in zip(bars, d2.pmf(k)):
        if v > 0.01:
            ax1.text(b.get_x()+b.get_width()/2,
                     b.get_height()+0.004,
                     f"{v:.3f}", ha="center",
                     fontsize=7.5, fontweight="bold")
    ax1.set_ylim(0, 0.32)

    # 1b) FDA λ=2
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.step(k, d2.cdf(k), where="post",
             color=C_MORADO, lw=2.5)
    ax2.axhline(d2.cdf(3), color=C_VERDE,
                linestyle="--", lw=1.5,
                label=f"F(3)={d2.cdf(3):.3f}")
    ax2.set_title("FDA Poisson(2)", fontweight="bold")
    ax2.set_xlabel("k"); ax2.set_ylabel("F(k)")
    ax2.set_xticks(k); ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=9)

    # 2a) FMP λ=3
    ax3 = fig.add_subplot(gs[1, 0])
    col3 = [C_AZUL if v <= 2 else C_ROJO if v == 1 else C_AZUL
            for v in k]
    col3 = [C_ROJO if v == 1 else
            (C_VERDE if v <= 2 else C_AZUL)
            for v in k]
    bars2 = ax3.bar(k, d3.pmf(k), color=col3,
                    width=0.6, edgecolor="white", linewidth=1.2)
    ax3.set_title("FMP Poisson(3)\nVerde: X≤2 (42.32%) · Rojo: X=1",
                  fontweight="bold")
    ax3.set_xlabel("k"); ax3.set_ylabel("P(X = k)")
    ax3.set_xticks(k)
    for b, v in zip(bars2, d3.pmf(k)):
        if v > 0.01:
            ax3.text(b.get_x()+b.get_width()/2,
                     b.get_height()+0.004,
                     f"{v:.3f}", ha="center",
                     fontsize=7.5, fontweight="bold")
    ax3.set_ylim(0, 0.28)

    # 2b) Comparación λ=2 vs λ=3
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(k, d2.pmf(k), "o-", color=C_MORADO,
             lw=2, markersize=6, label="λ = 2")
    ax4.plot(k, d3.pmf(k), "s-", color=C_AZUL,
             lw=2, markersize=6, label="λ = 3")
    ax4.axvline(2, color=C_MORADO, lw=1.2, linestyle="--", alpha=0.6)
    ax4.axvline(3, color=C_AZUL,   lw=1.2, linestyle="--", alpha=0.6)
    ax4.set_title("Comparación λ=2 vs λ=3",
                  fontweight="bold")
    ax4.set_xlabel("k")
    ax4.legend(fontsize=9); ax4.set_ylim(0, 0.32)

    plt.show()


#  3 · NORMAL

def dist_normal():
    titulo("DISTRIBUCIÓN NORMAL")

    d_t = stats.norm(loc=50,  scale=10)   # test
    d_p = stats.norm(loc=200, scale=10)   # peso

    seccion("Ejercicio 1 · Test  [μ=50, σ=10]")
    print(f"  P(X > 60)        = {1-d_t.cdf(60):.4f}   [LaTeX: 0.1587]")
    print(f"  P(40 < X < 60)   = {d_t.cdf(60)-d_t.cdf(40):.4f}   [LaTeX: 0.6827]")
    print(f"  Percentil 95     = {d_t.ppf(0.95):.4f}   [LaTeX: 66.45]")

    seccion("Ejercicio 2 · Peso  [μ=200, σ=10]")
    print(f"  P(180 ≤ X ≤ 220) = {d_p.cdf(220)-d_p.cdf(180):.4f}   [LaTeX: 0.9545]")
    print(f"  P(X < 185)       = {d_p.cdf(185):.4f}   [LaTeX: 0.0668]")
    print(f"  Percentil 90     = {d_p.ppf(0.90):.4f}   [LaTeX: 212.82]")

    # Gráficas
    fig = plt.figure(figsize=(13, 7), facecolor=C_FONDO)
    fig.suptitle("Distribución Normal", fontsize=14,
                 fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.50, wspace=0.32,
                           left=0.08, right=0.97,
                           top=0.90, bottom=0.09)

    x_t = np.linspace(10, 90, 400)
    x_p = np.linspace(160, 240, 400)

    # 1a) Regla empírica test
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x_t, d_t.pdf(x_t), color=C_ROJO, lw=2.5)
    ax1.fill_between(np.linspace(30,70,200),
                     d_t.pdf(np.linspace(30,70,200)),
                     alpha=0.15, color=C_ROJO, label="μ±2σ (95.45%)")
    ax1.fill_between(np.linspace(40,60,200),
                     d_t.pdf(np.linspace(40,60,200)),
                     alpha=0.35, color=C_ROJO, label="μ±σ (68.27%)")
    ax1.axvline(50, color=C_GRIS, lw=1.5, linestyle="--")
    ax1.set_title("N(50,100) — Regla empírica",
                  fontweight="bold")
    ax1.set_xlabel("x"); ax1.set_ylabel("f(x)")
    ax1.legend(fontsize=8)

    # 1b) P(X>60) sombreado
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(x_t, d_t.pdf(x_t), color=C_ROJO, lw=2.5)
    ax2.fill_between(np.linspace(60,90,200),
                     d_t.pdf(np.linspace(60,90,200)),
                     alpha=0.40, color=C_AZUL,
                     label=f"P(X>60)={1-d_t.cdf(60):.4f}")
    ax2.axvline(d_t.ppf(0.95), color=C_VERDE, lw=1.8,
                linestyle="-.", label=f"P95={d_t.ppf(0.95):.2f}")
    ax2.set_title("N(50,100) — P(X>60) y percentil 95",
                  fontweight="bold")
    ax2.set_xlabel("x"); ax2.set_ylabel("f(x)")
    ax2.legend(fontsize=8)

    # 2a) Control de peso
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(x_p, d_p.pdf(x_p), color=C_MORADO, lw=2.5)
    ax3.fill_between(np.linspace(180,220,200),
                     d_p.pdf(np.linspace(180,220,200)),
                     alpha=0.25, color=C_VERDE,
                     label=f"Aceptado: {d_p.cdf(220)-d_p.cdf(180):.4f}")
    ax3.fill_between(np.linspace(160,180,200),
                     d_p.pdf(np.linspace(160,180,200)),
                     alpha=0.35, color=C_ROJO,
                     label="Rechazado < 180")
    ax3.fill_between(np.linspace(220,240,200),
                     d_p.pdf(np.linspace(220,240,200)),
                     alpha=0.35, color=C_ROJO,
                     label="Rechazado > 220")
    ax3.axvline(200, color=C_GRIS, lw=1.5, linestyle="--")
    ax3.set_title("N(200,100) — Control de peso",
                  fontweight="bold")
    ax3.set_xlabel("gramos"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=7.5)

    # 2b) FDA peso
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(x_p, d_p.cdf(x_p), color=C_MORADO, lw=2.5)
    ax4.axhline(0.90, color=C_VERDE, lw=1.5, linestyle="--",
                label=f"P90 = {d_p.ppf(0.90):.2f} g")
    ax4.axvline(d_p.ppf(0.90), color=C_VERDE, lw=1.5,
                linestyle="--")
    ax4.set_title("FDA N(200,100)", fontweight="bold")
    ax4.set_xlabel("gramos"); ax4.set_ylabel("F(x)")
    ax4.set_ylim(0, 1.05)
    ax4.legend(fontsize=9)

    plt.show()


#  4 · EXPONENCIAL

def dist_exponencial():
    titulo("DISTRIBUCIÓN EXPONENCIAL")

    d1   = stats.expon(scale=1)    # λ=1
    d05  = stats.expon(scale=2)    # λ=0.5

    seccion("Ejercicio 1 · Cajero  [λ=1]")
    print(f"  P(X > 1)         = {1-d1.cdf(1):.4f}   [LaTeX: 0.3679]")
    print(f"  P(0.5 < X < 2)   = {d1.cdf(2)-d1.cdf(0.5):.4f}   [LaTeX: 0.4712]")
    print(f"  E[X]             = {d1.mean():.4f}   [LaTeX: 1.0000]")
    print(f"  Mediana          = {d1.median():.4f}   [LaTeX: 0.6931]")

    seccion("Ejercicio 2 · Fallas  [λ=0.5]")
    print(f"  P(X > 2)         = {1-d05.cdf(2):.4f}   [LaTeX: 0.3679]")
    print(f"  P(1 < X < 3)     = {d05.cdf(3)-d05.cdf(1):.4f}   [LaTeX: 0.3834]")
    print(f"  E[X]             = {d05.mean():.4f}   [LaTeX: 2.0000]")
    print(f"  Var(X)           = {d05.var():.4f}   [LaTeX: 4.0000]")

    # Gráficas
    fig = plt.figure(figsize=(13, 7), facecolor=C_FONDO)
    fig.suptitle("Distribución Exponencial", fontsize=14,
                 fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.50, wspace=0.32,
                           left=0.08, right=0.97,
                           top=0.90, bottom=0.09)

    x1  = np.linspace(0, 6, 400)
    x05 = np.linspace(0, 10, 400)

    # 1a) Densidad λ=1
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x1, d1.pdf(x1), color=C_VERDE, lw=2.5)
    ax1.fill_between(np.linspace(0.5, 2, 200),
                     d1.pdf(np.linspace(0.5, 2, 200)),
                     alpha=0.30, color=C_AZUL,
                     label=f"P(0.5<X<2)={d1.cdf(2)-d1.cdf(0.5):.4f}")
    ax1.fill_between(np.linspace(1, 6, 200),
                     d1.pdf(np.linspace(1, 6, 200)),
                     alpha=0.20, color=C_ROJO,
                     label=f"P(X>1)={1-d1.cdf(1):.4f}")
    ax1.axvline(1,         color=C_ROJO,   lw=1.8, linestyle="--",
                label=f"Media={d1.mean():.1f}")
    ax1.axvline(d1.median(), color=C_MORADO, lw=1.8, linestyle="-.",
                label=f"Mediana={d1.median():.3f}")
    ax1.set_title("Exp(λ=1) — Cajero", fontweight="bold")
    ax1.set_xlabel("minutos"); ax1.set_ylabel("f(x)")
    ax1.legend(fontsize=7.5); ax1.set_ylim(0, 1.15)

    # 1b) FDA λ=1
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(x1, d1.cdf(x1), color=C_VERDE, lw=2.5)
    ax2.axhline(0.5, color=C_MORADO, lw=1.5, linestyle="--",
                label=f"F=0.5 → x={d1.median():.3f}")
    ax2.axvline(d1.median(), color=C_MORADO, lw=1.5, linestyle="--")
    ax2.set_title("FDA Exp(λ=1)", fontweight="bold")
    ax2.set_xlabel("minutos"); ax2.set_ylabel("F(x)")
    ax2.set_ylim(0, 1.05); ax2.legend(fontsize=9)

    # 2a) Densidad λ=0.5
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(x05, d05.pdf(x05), color=C_AZUL, lw=2.5)
    ax3.fill_between(np.linspace(1, 3, 200),
                     d05.pdf(np.linspace(1, 3, 200)),
                     alpha=0.30, color=C_VERDE,
                     label=f"P(1<X<3)={d05.cdf(3)-d05.cdf(1):.4f}")
    ax3.fill_between(np.linspace(2, 10, 200),
                     d05.pdf(np.linspace(2, 10, 200)),
                     alpha=0.18, color=C_ROJO,
                     label=f"P(X>2)={1-d05.cdf(2):.4f}")
    ax3.axvline(2,           color=C_ROJO,   lw=1.8, linestyle="--",
                label="Media=2")
    ax3.axvline(d05.median(), color=C_MORADO, lw=1.8, linestyle="-.",
                label=f"Mediana={d05.median():.3f}")
    ax3.set_title("Exp(λ=0.5) — Fallas", fontweight="bold")
    ax3.set_xlabel("horas"); ax3.set_ylabel("f(x)")
    ax3.legend(fontsize=7.5)

    # 2b) Comparación Exp(1) vs Exp(0.5)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(x05, d1.pdf(x05),  color=C_VERDE, lw=2,
             label="λ=1  (media=1)")
    ax4.plot(x05, d05.pdf(x05), color=C_AZUL,  lw=2,
             linestyle="--", label="λ=0.5 (media=2)")
    ax4.axvline(1, color=C_VERDE, lw=1, linestyle=":", alpha=0.7)
    ax4.axvline(2, color=C_AZUL,  lw=1, linestyle=":", alpha=0.7)
    ax4.set_title("Comparación λ=1 vs λ=0.5",
                  fontweight="bold")
    ax4.set_xlabel("x"); ax4.set_ylim(0, 1.1)
    ax4.legend(fontsize=9)

    plt.show()


#  MENÚ PRINCIPAL

ENUNCIADO = (
    "T4 · Distribuciones de Probabilidad\n"
    "─────────────────────────────────────────────────────\n\n"
    "Valida los ejercicios del informe LaTeX con scipy.stats.\n\n"
    "  📊  Binomial  Bin(n, p)\n"
    "       Ej. 1: moneda equilibrada    [n=5,  p=0.5]\n"
    "       Ej. 2: familia con 4 hijos   [n=4,  p=0.5]\n\n"
    "  📬  Poisson  Pois(λ)\n"
    "       Ej. 1: clientes por hora     [λ=2]\n"
    "       Ej. 2: mensajes por minuto   [λ=3]\n\n"
    "  📈  Normal  N(μ, σ²)\n"
    "       Ej. 1: puntajes de un test   [μ=50,  σ=10]\n"
    "       Ej. 2: control de peso       [μ=200, σ=10]\n\n"
    "  ⏱   Exponencial  Exp(λ)\n"
    "       Ej. 1: tiempo de atención    [λ=1]\n"
    "       Ej. 2: tiempo entre fallas   [λ=0.5]\n\n"
    "Seleccioná la distribución a explorar:"
)

DISTRIBUCIONES = [
    ("📊  Binomial",    "binomial",    C_AZUL),
    ("📬  Poisson",     "poisson",     C_MORADO),
    ("📈  Normal",      "normal",      C_ROJO),
    ("⏱   Exponencial", "exponencial", C_VERDE),
]

ACCIONES = {
    "binomial":    dist_binomial,
    "poisson":     dist_poisson,
    "normal":      dist_normal,
    "exponencial": dist_exponencial,
}


def _darken(hex_color, factor=0.80):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(
        int(r*factor), int(g*factor), int(b*factor))


def mostrar_menu():
    root = tk.Tk()
    root.title("T4 · Distribuciones de Probabilidad")
    root.configure(bg=C_FONDO)
    root.resizable(False, False)

    ancho, alto = 620, 700
    root.update_idletasks()
    sx = (root.winfo_screenwidth()  - ancho) // 2
    sy = (root.winfo_screenheight() - alto)  // 2
    root.geometry(f"{ancho}x{alto}+{sx}+{sy}")

    f_titulo = tkfont.Font(family="Helvetica", size=13, weight="bold")
    f_subtit = tkfont.Font(family="Helvetica", size=9,  slant="italic")
    f_cuerpo = tkfont.Font(family="Courier",   size=11)
    f_btn    = tkfont.Font(family="Helvetica", size=10, weight="bold")

    # Encabezado
    frm_h = tk.Frame(root, bg=C_AZUL, pady=14)
    frm_h.pack(fill="x")
    tk.Label(frm_h, text="Distribuciones de Probabilidad",
             font=f_titulo, bg=C_AZUL, fg="white").pack()
    tk.Label(frm_h,
             text="Discreto: Binomial · Poisson   |   "
                  "Continuo: Normal · Exponencial",
             font=f_subtit, bg=C_AZUL, fg="#adc8f0").pack()

    # Cuerpo
    frm_b = tk.Frame(root, bg=C_FONDO, padx=22, pady=12)
    frm_b.pack(fill="both", expand=True)

    card = tk.Frame(frm_b, bg=C_CARD,
                    highlightbackground=C_LINE,
                    highlightthickness=1,
                    padx=14, pady=12)
    card.pack(fill="x")
    tk.Label(card, text=ENUNCIADO,
             font=f_cuerpo, bg=C_CARD, fg=C_TEXT,
             justify="left", anchor="w").pack(anchor="w")

    tk.Frame(frm_b, bg=C_LINE, height=1).pack(fill="x", pady=(12, 8))

    opcion = {"valor": None}

    def elegir(caso):
        opcion["valor"] = caso
        root.destroy()

    # Botones 2×2
    frm_grid = tk.Frame(frm_b, bg=C_FONDO)
    frm_grid.pack(fill="x")

    for idx, (label, clave, color) in enumerate(DISTRIBUCIONES):
        row, col = divmod(idx, 2)

        def make_cmd(c=clave):
            return lambda: elegir(c)

        btn = tk.Button(
            frm_grid, text=label, font=f_btn,
            bg=color, fg="white",
            activebackground=color, activeforeground="white",
            relief="flat", padx=12, pady=9,
            command=make_cmd(),
        )
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
        frm_grid.columnconfigure(col, weight=1)
        dark = _darken(color)
        btn.bind("<Enter>", lambda e, b=btn, d=dark: b.configure(bg=d))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

    # Salir
    tk.Frame(frm_b, bg=C_FONDO, height=4).pack()
    f_s = tkfont.Font(family="Helvetica", size=9)
    btn_s = tk.Button(
        frm_b, text="Salir", font=f_s,
        bg=C_FONDO, fg=C_MUTED,
        activebackground=C_FONDO, activeforeground=C_TEXT,
        relief="flat", pady=4,
        command=lambda: elegir("salir"),
    )
    btn_s.pack()
    btn_s.bind("<Enter>", lambda e: btn_s.configure(
        fg=C_TEXT, cursor="hand2"))
    btn_s.bind("<Leave>", lambda e: btn_s.configure(fg=C_MUTED))

    root.mainloop()
    return opcion["valor"]

#  MAIN

if __name__ == "__main__":
    while True:
        eleccion = mostrar_menu()
        if eleccion in ACCIONES:
            ACCIONES[eleccion]()
        else:
            print("\nAplicación cerrada.")
            break