# T3 · Probabilidad Conjunta

Aplicación Python que resuelve los dos casos del informe LaTeX sobre probabilidad conjunta: discreto y continuo.

## Requisitos

Python 3.8+ y las siguientes librerías:

```
pip install numpy matplotlib scipy
```

> `tkinter` viene incluido con Python, no necesita instalación aparte.

## Cómo ejecutar

```
python probabilidad_conjunta.py
```

Al iniciar se abre una ventana con el enunciado del trabajo y dos botones para elegir qué caso explorar. Después de ver uno, el menú vuelve a aparecer para ver el otro o salir.

## Qué hace cada caso

**Caso Discreto** — distribución conjunta de solicitudes en dos servidores (X ∈ {0,1,2}, Y ∈ {0,1}):
- Verifica que la suma de probabilidades sea 1
- Calcula marginales P(X) y P(Y)
- Calcula la condicional P(X | Y=1)
- Muestra E[X], Var(X), Cov(X,Y) y Corr(X,Y)
- Gráficas: mapa de calor, barras marginales, condicional y burbujas proporcionales

**Caso Continuo** — función de densidad f(x,y) = 2 sobre la región 0 ≤ y ≤ x ≤ 1:
- Verifica la integral doble numéricamente con `scipy`
- Calcula marginales f_X(x) = 2x y f_Y(y) = 2(1−y)
- Calcula la condicional f(x|y) ~ Uniforme(y, 1)
- Muestra E[X], Var(X), Cov(X,Y) y Corr(X,Y)
- Gráficas: mapa de calor 2D, marginales, condicionales para distintos y, superficie 3D

## Archivos

```
probabilidad_conjunta.py   # código principal
README.md                  # este archivo
```