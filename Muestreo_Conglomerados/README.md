# Muestreo por Conglomerados: Rendimiento Academico Ing. Sistemas

Aplicacion de escritorio que visualiza el analisis estadistico del informe de
muestreo por conglomerados aplicado al rendimiento academico de estudiantes de
Ingenieria de Sistemas en la Universidad Distrital Francisco Jose de Caldas.

**Autores:** Ian Sandoval (20241020078) y Brayan Santos (20251020157)  
**Profesor:** Alberto Acosta  
**Materia:** Probabilidad y Estadistica

---

## Ejecucion

1. Instalar dependencias:

```
pip install -r requirements.txt
```

2. Ejecutar desde Visual Studio Code abriendo `main.py` y presionando **F5**,
   o desde la terminal integrada:

```
python main.py
```

---

## Estructura del proyecto

```
stats_cong/
    main.py                              Punto de entrada
    requirements.txt                     Dependencias
    README.md
    logica/
        __init__.py
        datos.py                         ConjuntoDatos: promedios por conglomerado
        estadistica.py                   MedidasCentralizacion, MedidasDispersion,
                                         FormaDistribucion
        frecuencias.py                   DistribucionFrecuencias (Sturges, amplitud 0.4)
        muestreo.py                      MuestreoConglomerados: info del diseno muestral
    visualizacion/
        __init__.py
        estilos.py                       Paleta de colores y estilo matplotlib
        graficas.py                      GraficasEstadisticas: figuras matplotlib
    interfaz/
        __init__.py
        componentes.py                   Widgets reutilizables
        ventana_principal.py             Ventana con sidebar y notebook de 9 pestanas
        pestanas/
            __init__.py
            pestana_base.py              Clase base abstracta
            pestana_poblacion.py         Planteamiento, poblacion y diagrama de conglomerados
            pestana_muestra.py           Procedimiento de seleccion y datos recolectados
            pestana_estadistica.py       Centralizacion, Dispersion y Frecuencias
            pestana_analisis.py          Graficas, Forma, Justificacion y Resumen
```

---

## Pestanas de la aplicacion

| Pestana | Contenido |
|---|---|
| Poblacion | Planteamiento, definicion de la poblacion y diagrama visual de los 6 conglomerados con los seleccionados resaltados en verde. |
| Muestra | Procedimiento de seleccion paso a paso, tabla de datos por semestre y datos ordenados de menor a mayor para calcular la mediana. |
| Centralizacion | Media, mediana y moda con su procedimiento. Hace enfasis en que la distribucion es bimodal (3.8 y 4.0) y en el sesgo negativo leve. |
| Dispersion | Rango, varianza, desviacion estandar y CV. Con datos en escala 0 a 5 los valores son pequenos pero la interpretacion es la misma. |
| Frecuencias | Regla de Sturges, tabla fi Fi fri Fri y explorador interactivo de intervalos. |
| Graficas | Boxplot por semestre, histograma con toggle, poligono con media y mediana, ojivas y superposicion histograma mas poligono. |
| Forma | Asimetria negativa leve, curtosis leptocurtica, KDE vs normal y grafico QQ. |
| Justificacion | Por que se eligio conglomerados, comparacion con otros metodos y tabla de ventajas y desventajas. |
| Resumen | Tabla maestra de resultados, dashboard 2x2 y cinco conclusiones. |

---

## Dependencias

| Libreria | Version minima | Uso |
|---|---|---|
| matplotlib | 3.8 | Graficos y canvas incrustado en tkinter |
| pandas | 2.0 | Tabla de frecuencias |
| numpy | 1.26 | Calculos numericos |
| scipy | 1.12 | KDE, asimetria, curtosis, grafico QQ |
| tkinter | incluido en Python | Interfaz grafica |

---

## Resultados esperados del analisis

| Medida | Valor |
|---|---|
| n muestra | 36 |
| Media | 3.67 |
| Mediana | 3.80 |
| Moda | 3.8 y 4.0 (bimodal) |
| Rango | 2.0 |
| Varianza | 0.2405 |
| Desviacion estandar | 0.49 |
| Coef. variacion | 13.3% aprox. |
| Num. intervalos | 6 |
| Amplitud | 0.4 |
| Clase modal | [3.6, 4.0) con 11 estudiantes |
| Asimetria | Negativa (cola a la izquierda) |
| Curtosis | Leptocurtica (pico pronunciado) |