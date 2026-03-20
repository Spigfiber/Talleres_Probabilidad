# T4 · Distribuciones de Probabilidad

Aplicación interactiva para explorar y validar ejercicios de distribuciones de probabilidad usando `scipy.stats` y `matplotlib`.

## Distribuciones incluidas

| Tipo | Distribución | Parámetros |
|------|-------------|------------|
| Discreta | Binomial | n=5/4, p=0.5 |
| Discreta | Poisson | λ=2, λ=3 |
| Continua | Normal | μ=50/200, σ=10 |
| Continua | Exponencial | λ=1, λ=0.5 |

Cada distribución incluye dos ejercicios con cálculos de probabilidad (FMP, FDA, percentiles, media, varianza) y sus gráficas correspondientes.

## Requisitos

```
Python 3.8+
numpy
matplotlib
scipy
tkinter  # incluido en la mayoría de instalaciones de Python
```

Instalación de dependencias:

```bash
pip install numpy matplotlib scipy
```

## Uso

```bash
python t4_distribuciones.py
```

Se abre un menú gráfico con cuatro botones. Al seleccionar una distribución, se imprimen los resultados numéricos en consola y se muestran las gráficas en una ventana de matplotlib.

## Estructura del código

```
t4_distribuciones.py
├── dist_binomial()     # Ejercicios y gráficas Binomial
├── dist_poisson()      # Ejercicios y gráficas Poisson
├── dist_normal()       # Ejercicios y gráficas Normal
├── dist_exponencial()  # Ejercicios y gráficas Exponencial
└── mostrar_menu()      # Menú principal con tkinter
```