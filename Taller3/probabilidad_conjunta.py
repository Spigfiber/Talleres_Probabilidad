
# T3 - Probabilidad Conjunta - Caso Discreto y Caso Continuo

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import integrate

# Configuración visual general

plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "axes.titlesize":  13,
    "axes.labelsize":  11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
})

AZUL   = "#1a5a9e"
ROJO   = "#c0392b"
VERDE  = "#27ae60"
GRIS   = "#7f8c8d"
FONDO  = "#f4f6f9"

#  CASO 1 — DISCRETO

def caso_discreto():
    print("=" * 60)
    print("  CASO DISCRETO")
    print("=" * 60)

    # Distribución conjunta 
    # Filas = X ∈ {0,1,2},  Columnas = Y ∈ {0,1}
    P = np.array([
        [0.10, 0.20],   # X=0
        [0.20, 0.30],   # X=1
        [0.10, 0.10],   # X=2
    ])
    X_vals = np.array([0, 1, 2])
    Y_vals = np.array([0, 1])

    # Verificación 
    total = P.sum()
    print(f"\n[1] Verificación: suma de todas las probabilidades = {total:.2f}")
    assert np.isclose(total, 1.0), "¡La distribución no es válida!"
    print("    ✓ La distribución es válida.")

    # Marginales 
    P_X = P.sum(axis=1)          # suma sobre columnas (Y)
    P_Y = P.sum(axis=0)          # suma sobre filas   (X)

    print("\n[2] Distribución marginal de X:")
    for x, px in zip(X_vals, P_X):
        print(f"    P(X={x}) = {px:.2f}")

    print("\n[3] Distribución marginal de Y:")
    for y, py in zip(Y_vals, P_Y):
        print(f"    P(Y={y}) = {py:.2f}")

    # Probabilidad condicional P(X=1 | Y=1)
    x_cond, y_cond = 1, 1
    p_cond = P[x_cond, y_cond] / P_Y[y_cond]
    print(f"\n[4] Probabilidad condicional:")
    print(f"    P(X={x_cond} | Y={y_cond}) = P(X={x_cond}, Y={y_cond}) / P(Y={y_cond})")
    print(f"                              = {P[x_cond, y_cond]:.2f} / {P_Y[y_cond]:.2f}")
    print(f"                              = {p_cond:.4f}")

    # Distribución condicional completa P(X | Y=1)
    print(f"\n[5] Distribución condicional completa P(X | Y=1):")
    for x in X_vals:
        print(f"    P(X={x} | Y=1) = {P[x, 1]/P_Y[1]:.4f}")

    # Estadísticas adicionales 
    E_X = np.sum(X_vals * P_X)
    E_Y = np.sum(Y_vals * P_Y)
    Var_X = np.sum((X_vals - E_X)**2 * P_X)
    Var_Y = np.sum((Y_vals - E_Y)**2 * P_Y)

    # Covarianza: E[XY] - E[X]*E[Y]
    E_XY = sum(X_vals[i] * Y_vals[j] * P[i, j]
               for i in range(len(X_vals))
               for j in range(len(Y_vals)))
    cov   = E_XY - E_X * E_Y
    corr  = cov / np.sqrt(Var_X * Var_Y) if (Var_X * Var_Y) > 0 else 0

    print(f"\n[6] Estadísticas:")
    print(f"    E[X] = {E_X:.4f}   Var(X) = {Var_X:.4f}")
    print(f"    E[Y] = {E_Y:.4f}   Var(Y) = {Var_Y:.4f}")
    print(f"    Cov(X,Y)  = {cov:.4f}")
    print(f"    Corr(X,Y) = {corr:.4f}")

    # Gráficas 
    fig = plt.figure(figsize=(14, 9), facecolor=FONDO)
    fig.suptitle("Caso Discreto — Distribución de probabilidad conjunta",
                 fontsize=15, fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.45, wspace=0.38,
                           left=0.07, right=0.97,
                           top=0.91, bottom=0.08)

    # 1) Mapa de calor (tabla conjunta)
    ax1 = fig.add_subplot(gs[0, :2])
    im = ax1.imshow(P, cmap="Blues", aspect="auto", vmin=0, vmax=0.35)
    ax1.set_xticks(range(len(Y_vals)))
    ax1.set_xticklabels([f"Y={y}" for y in Y_vals])
    ax1.set_yticks(range(len(X_vals)))
    ax1.set_yticklabels([f"X={x}" for x in X_vals])
    ax1.set_title("Tabla conjunta P(X, Y)", fontweight="bold")
    for i in range(len(X_vals)):
        for j in range(len(Y_vals)):
            color = "white" if P[i, j] > 0.22 else "black"
            ax1.text(j, i, f"{P[i, j]:.2f}",
                     ha="center", va="center",
                     fontsize=14, fontweight="bold", color=color)
    fig.colorbar(im, ax=ax1, label="Probabilidad", shrink=0.85)

    # 2) Marginal de X
    ax2 = fig.add_subplot(gs[0, 2])
    bars = ax2.bar(X_vals, P_X, color=AZUL, width=0.5,
                   edgecolor="white", linewidth=1.5)
    ax2.set_xlabel("X"); ax2.set_ylabel("P(X)")
    ax2.set_title("Marginal de X", fontweight="bold")
    ax2.set_xticks(X_vals)
    for bar, val in zip(bars, P_X):
        ax2.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f"{val:.2f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")
    ax2.set_ylim(0, 0.65)

    # 3) Marginal de Y
    ax3 = fig.add_subplot(gs[1, 0])
    bars2 = ax3.bar(Y_vals, P_Y, color=ROJO, width=0.4,
                    edgecolor="white", linewidth=1.5)
    ax3.set_xlabel("Y"); ax3.set_ylabel("P(Y)")
    ax3.set_title("Marginal de Y", fontweight="bold")
    ax3.set_xticks(Y_vals)
    for bar, val in zip(bars2, P_Y):
        ax3.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f"{val:.2f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")
    ax3.set_ylim(0, 0.75)

    # 4) Distribución condicional P(X | Y=1)
    ax4 = fig.add_subplot(gs[1, 1])
    p_cond_all = P[:, 1] / P_Y[1]
    bars3 = ax4.bar(X_vals, p_cond_all, color=VERDE, width=0.5,
                    edgecolor="white", linewidth=1.5)
    ax4.set_xlabel("X"); ax4.set_ylabel("P(X | Y=1)")
    ax4.set_title("Condicional P(X | Y=1)", fontweight="bold")
    ax4.set_xticks(X_vals)
    ax4.axhline(1/3, color=GRIS, linestyle="--",
                linewidth=1, label="Uniforme (ref.)")
    for bar, val in zip(bars3, p_cond_all):
        ax4.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f"{val:.2f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")
    ax4.set_ylim(0, 0.65)
    ax4.legend(fontsize=9)

    # 5) Diagrama de dispersión proporcional
    ax5 = fig.add_subplot(gs[1, 2])
    xg, yg = np.meshgrid(Y_vals, X_vals)
    sizes = P.flatten() * 4000
    scatter = ax5.scatter(xg.flatten(), yg.flatten(),
                          s=sizes, c=P.flatten(),
                          cmap="Blues", edgecolors=AZUL,
                          linewidths=1.5, alpha=0.85)
    ax5.set_xlabel("Y"); ax5.set_ylabel("X")
    ax5.set_title("Burbujas proporcionales a P(X,Y)",
                  fontweight="bold")
    ax5.set_xticks(Y_vals); ax5.set_yticks(X_vals)
    for i in range(len(X_vals)):
        for j in range(len(Y_vals)):
            ax5.annotate(f"{P[i,j]:.2f}",
                         (Y_vals[j], X_vals[i]),
                         textcoords="offset points",
                         xytext=(0, 14),
                         ha="center", fontsize=9, color=AZUL,
                         fontweight="bold")
    ax5.set_xlim(-0.5, 1.5); ax5.set_ylim(-0.5, 2.5)

    plt.show()

    return P, P_X, P_Y


#  CASO 2 — CONTINUO

def caso_continuo():
    print("\n" + "=" * 60)
    print("  CASO CONTINUO")
    print("=" * 60)

    # Función de densidad conjunta 
    # f(x,y) = 2  para  0 ≤ y ≤ x ≤ 1
    def f_joint(x, y):
        return np.where((y >= 0) & (y <= x) & (x <= 1), 2.0, 0.0)

    def f_X(x):
        """Marginal de X: f_X(x) = 2x"""
        return 2 * x

    def f_Y(y):
        """Marginal de Y: f_Y(y) = 2(1-y)"""
        return 2 * (1 - y)

    def f_cond_X_given_Y(x, y):
        """Condicional f(x|y) = 1/(1-y),  y ≤ x ≤ 1"""
        return np.where((x >= y) & (x <= 1), 1.0 / (1 - y), 0.0)

    # Verificación numérica (integración doble) 
    total, err = integrate.dblquad(
        lambda y, x: f_joint(x, y),
        0, 1,            # límites de x
        0, lambda x: x   # límites de y: 0 a x
    )
    print(f"\n[1] Verificación (integración numérica):")
    print(f"    ∫∫ f(x,y) dy dx = {total:.8f}  (error estimado: {err:.2e})")
    print(f"    ✓ La f.d.p. es válida.")

    # Verificación marginales
    int_fX, _ = integrate.quad(f_X, 0, 1)
    int_fY, _ = integrate.quad(f_Y, 0, 1)
    print(f"\n[2] Verificación marginales:")
    print(f"    ∫ f_X(x) dx = {int_fX:.6f}  ✓")
    print(f"    ∫ f_Y(y) dy = {int_fY:.6f}  ✓")

    # Estadísticas de X 
    E_X,   _ = integrate.quad(lambda x: x * f_X(x), 0, 1)
    E_X2,  _ = integrate.quad(lambda x: x**2 * f_X(x), 0, 1)
    Var_X     = E_X2 - E_X**2

    E_Y,   _ = integrate.quad(lambda y: y * f_Y(y), 0, 1)
    E_Y2,  _ = integrate.quad(lambda y: y**2 * f_Y(y), 0, 1)
    Var_Y     = E_Y2 - E_Y**2

    E_XY, _  = integrate.dblquad(
        lambda y, x: x * y * f_joint(x, y),
        0, 1, 0, lambda x: x)
    cov       = E_XY - E_X * E_Y
    corr      = cov / np.sqrt(Var_X * Var_Y)

    print(f"\n[3] Estadísticas:")
    print(f"    E[X] = {E_X:.4f}   Var(X) = {Var_X:.4f}")
    print(f"    E[Y] = {E_Y:.4f}   Var(Y) = {Var_Y:.4f}")
    print(f"    Cov(X,Y)  = {cov:.4f}")
    print(f"    Corr(X,Y) = {corr:.4f}")

    # Condicional para un valor específico
    y0 = 0.3
    print(f"\n[4] Densidad condicional f(x | Y={y0}):")
    print(f"    f(x | Y={y0}) = 1 / (1 - {y0}) = {1/(1-y0):.4f}")
    print(f"    → X | Y={y0}  ~  Uniforme({y0}, 1)")

    # Probabilidad P(X > 0.5) 
    p_X_gt05, _ = integrate.quad(f_X, 0.5, 1)
    print(f"\n[5] P(X > 0.5) = ∫_{{0.5}}^1 2x dx = {p_X_gt05:.4f}")

    # Gráficas
    fig = plt.figure(figsize=(14, 9), facecolor=FONDO)
    fig.suptitle("Caso Continuo — Función de densidad conjunta f(x,y) = 2",
                 fontsize=15, fontweight="bold", y=0.97)
    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.45, wspace=0.38,
                           left=0.07, right=0.97,
                           top=0.91, bottom=0.08)

    n = 300
    x_arr = np.linspace(0, 1, n)
    y_arr = np.linspace(0, 1, n)
    X_grid, Y_grid = np.meshgrid(x_arr, y_arr)
    Z = f_joint(X_grid, Y_grid)

    # 1) Mapa de calor 2D de f(x,y)
    ax1 = fig.add_subplot(gs[0, :2])
    cf = ax1.contourf(X_grid, Y_grid, Z, levels=20, cmap="Blues", alpha=0.9)
    ax1.plot([0, 1], [0, 1], color=AZUL, lw=2, label="$y = x$")
    ax1.fill_between([0, 1], [0, 1], 0, alpha=0.12, color=AZUL,
                     label="Región soporte")
    ax1.set_xlabel("$x$"); ax1.set_ylabel("$y$")
    ax1.set_title("Densidad conjunta $f(x,y) = 2$", fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.set_aspect("equal")
    fig.colorbar(cf, ax=ax1, label="$f(x,y)$", shrink=0.85)

    # 2) Densidad marginal de X
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(x_arr, f_X(x_arr), color=AZUL, lw=2.5)
    ax2.fill_between(x_arr, f_X(x_arr), alpha=0.2, color=AZUL)
    ax2.set_xlabel("$x$"); ax2.set_ylabel("$f_X(x)$")
    ax2.set_title("Marginal de $X$: $f_X(x) = 2x$", fontweight="bold")
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 2.2)

    # 3) Densidad marginal de Y
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(y_arr, f_Y(y_arr), color=ROJO, lw=2.5)
    ax3.fill_between(y_arr, f_Y(y_arr), alpha=0.2, color=ROJO)
    ax3.set_xlabel("$y$"); ax3.set_ylabel("$f_Y(y)$")
    ax3.set_title("Marginal de $Y$: $f_Y(y) = 2(1-y)$", fontweight="bold")
    ax3.set_xlim(0, 1); ax3.set_ylim(0, 2.2)

    # 4) Densidad condicional f(x | Y=y) para varios valores de y
    ax4 = fig.add_subplot(gs[1, 1])
    colores_cond = [AZUL, VERDE, ROJO, "#8e44ad"]
    for y_val, col in zip([0.0, 0.2, 0.5, 0.7], colores_cond):
        x_range = np.linspace(y_val, 1, 200)
        fxy_vals = f_cond_X_given_Y(x_range, y_val)
        ax4.plot(x_range, fxy_vals, color=col, lw=2,
                 label=f"$y={y_val}$")
    ax4.set_xlabel("$x$"); ax4.set_ylabel("$f(x\\,|\\,Y=y)$")
    ax4.set_title("Condicional $f(x \\mid Y=y)$", fontweight="bold")
    ax4.legend(fontsize=9, title="$y$ fijo")
    ax4.set_xlim(0, 1.05); ax4.set_ylim(0, 3.5)

    # 5) Superficie 3D
    ax5 = fig.add_subplot(gs[1, 2], projection="3d")
    n3 = 60
    x3 = np.linspace(0.001, 1, n3)
    y3 = np.linspace(0.001, 1, n3)
    X3, Y3 = np.meshgrid(x3, y3)
    Z3 = f_joint(X3, Y3)
    ax5.plot_surface(X3, Y3, Z3, cmap="Blues",
                     edgecolor="none", alpha=0.85)
    ax5.set_xlabel("$x$", labelpad=4)
    ax5.set_ylabel("$y$", labelpad=4)
    ax5.set_zlabel("$f(x,y)$", labelpad=4)
    ax5.set_title("Superficie 3D de $f(x,y)$",
                  fontweight="bold", pad=8)
    ax5.view_init(elev=28, azim=-55)

    plt.show()


#  MENÚ PRINCIPAL

import tkinter as tk
from tkinter import font as tkfont

# Paleta compartida con matplotlib
C_BG      = "#f4f6f9"
C_CARD    = "#ffffff"
C_AZUL    = "#1a5a9e"
C_AZUL_LT = "#e8f0fb"
C_ROJO    = "#c0392b"
C_ROJO_LT = "#fdf0ef"
C_TEXT    = "#2c3e50"
C_MUTED   = "#7f8c8d"
C_LINE    = "#dde3ec"

ENUNCIADO = (
    "T3 · Probabilidad Conjunta\n"
    "Caso Discreto y Caso Continuo\n\n"
    "Esta aplicación resuelve de forma computacional los dos casos\n"
    "desarrollados en el informe LaTeX:\n\n"
    "  • Caso Discreto — se analiza la distribución conjunta de\n"
    "    solicitudes en dos servidores (X ∈ {0,1,2}, Y ∈ {0,1}).\n"
    "    Se verifican las probabilidades, se calculan las marginales\n"
    "    P(X) y P(Y), la condicional P(X | Y=1), y estadísticos\n"
    "    como E[X], Var(X) y Cov(X,Y).\n\n"
    "  • Caso Continuo — se trabaja con la función de densidad\n"
    "    conjunta f(x,y) = 2 sobre la región 0 ≤ y ≤ x ≤ 1.\n"
    "    Se verifica la integral doble, se obtienen las marginales\n"
    "    f_X(x) = 2x y f_Y(y) = 2(1−y), la densidad condicional\n"
    "    f(x|y) ~ Uniforme(y,1), y las estadísticas poblacionales.\n\n"
    "Seleccioná el caso a explorar:"
)


def mostrar_menu():
    """Ventana principal de bienvenida y selección de caso."""

    root = tk.Tk()
    root.title("T3 · Probabilidad Conjunta")
    root.configure(bg=C_BG)
    root.resizable(False, False)

    # ── centrar en pantalla ────────────────────────────────────────────────
    ancho, alto = 620, 560
    root.update_idletasks()
    sx = (root.winfo_screenwidth()  - ancho) // 2
    sy = (root.winfo_screenheight() - alto)  // 2
    root.geometry(f"{ancho}x{alto}+{sx}+{sy}")

    # ── fuentes ───────────────────────────────────────────────────────────
    f_titulo  = tkfont.Font(family="Helvetica", size=15, weight="bold")
    f_subtit  = tkfont.Font(family="Helvetica", size=10, slant="italic")
    f_cuerpo  = tkfont.Font(family="Helvetica", size=10)
    f_btn     = tkfont.Font(family="Helvetica", size=11, weight="bold")

    # ── encabezado ────────────────────────────────────────────────────────
    frm_header = tk.Frame(root, bg=C_AZUL, pady=18)
    frm_header.pack(fill="x")
    tk.Label(frm_header, text="Probabilidad Conjunta",
             font=f_titulo, bg=C_AZUL, fg="white").pack()
    tk.Label(frm_header, text="Aplicación Python · T3",
             font=f_subtit, bg=C_AZUL, fg="#adc8f0").pack()

    # ── cuerpo ────────────────────────────────────────────────────────────
    frm_body = tk.Frame(root, bg=C_BG, padx=28, pady=16)
    frm_body.pack(fill="both", expand=True)

    # card con el enunciado
    card = tk.Frame(frm_body, bg=C_CARD,
                    highlightbackground=C_LINE,
                    highlightthickness=1,
                    padx=18, pady=14)
    card.pack(fill="both", expand=True)

    tk.Label(card, text=ENUNCIADO,
             font=f_cuerpo, bg=C_CARD, fg=C_TEXT,
             justify="left", anchor="w",
             wraplength=540).pack(anchor="w")

    # ── separador ─────────────────────────────────────────────────────────
    tk.Frame(frm_body, bg=C_LINE, height=1).pack(fill="x", pady=(14, 10))

    # ── botones de caso ───────────────────────────────────────────────────
    frm_btns = tk.Frame(frm_body, bg=C_BG)
    frm_btns.pack(fill="x")

    opcion = {"valor": None}   # contenedor mutable para capturar la elección

    def elegir(caso):
        opcion["valor"] = caso
        root.destroy()

    def _hover_enter(btn, color_bg, color_fg="white"):
        btn.configure(bg=color_bg, fg=color_fg, cursor="hand2")

    def _hover_leave(btn, color_bg, color_fg="white"):
        btn.configure(bg=color_bg, fg=color_fg)

    # botón Caso Discreto
    btn_d = tk.Button(
        frm_btns,
        text="📊  Ver Caso Discreto",
        font=f_btn, bg=C_AZUL, fg="white",
        activebackground="#14478a", activeforeground="white",
        relief="flat", padx=20, pady=10,
        command=lambda: elegir("discreto")
    )
    btn_d.pack(side="left", expand=True, fill="x", padx=(0, 6))
    btn_d.bind("<Enter>", lambda e: _hover_enter(btn_d, "#14478a"))
    btn_d.bind("<Leave>", lambda e: _hover_leave(btn_d, C_AZUL))

    # botón Caso Continuo
    btn_c = tk.Button(
        frm_btns,
        text="📈  Ver Caso Continuo",
        font=f_btn, bg=C_ROJO, fg="white",
        activebackground="#a93226", activeforeground="white",
        relief="flat", padx=20, pady=10,
        command=lambda: elegir("continuo")
    )
    btn_c.pack(side="left", expand=True, fill="x", padx=(6, 0))
    btn_c.bind("<Enter>", lambda e: _hover_enter(btn_c, "#a93226"))
    btn_c.bind("<Leave>", lambda e: _hover_leave(btn_c, C_ROJO))

    # botón Salir
    tk.Frame(frm_body, bg=C_BG, height=8).pack()
    btn_salir = tk.Button(
        frm_body,
        text="Salir",
        font=tkfont.Font(family="Helvetica", size=9),
        bg=C_BG, fg=C_MUTED,
        activebackground=C_BG, activeforeground=C_TEXT,
        relief="flat", pady=4,
        command=lambda: elegir("salir")
    )
    btn_salir.pack()
    btn_salir.bind("<Enter>", lambda e: btn_salir.configure(fg=C_TEXT))
    btn_salir.bind("<Leave>", lambda e: btn_salir.configure(fg=C_MUTED))

    root.mainloop()
    return opcion["valor"]


#  MAIN

if __name__ == "__main__":
    while True:
        eleccion = mostrar_menu()

        if eleccion == "discreto":
            caso_discreto()
        elif eleccion == "continuo":
            caso_continuo()
        else:
            print("\nAplicación cerrada.")
            break