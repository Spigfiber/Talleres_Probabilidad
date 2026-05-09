# Estadistica Descriptiva — Análisis de 60 Datos Aleatorios

Aplicacion de escritorio que visualiza el analisis estadistico completo
del informe sobre una poblacion de 60 datos aleatorios.

**Autores:** Ian Sandoval (20241020078) y Brayan Santos (20251020157)  
**Profesor:** Alberto Acosta  
**Materia:** Probabilidad y Estadistica  
**Universidad:** Distrital Francisco Jose de Caldas

---

## Ejecucion

1. Instalar dependencias:
```
pip install -r requirements.txt
```

2. Ejecutar desde la terminal:
```
python main.py
```

---

## Estructura del proyecto

```
Estadistica_60Datos/
    main.py                          Punto de entrada
    requirements.txt
    logica/
        datos.py                     ConjuntoDatos: los 60 valores organizados por fila
        estadistica.py               MedidasCentralizacion, MedidasDispersion, FormaDistribucion
        frecuencias.py               DistribucionFrecuencias (Sturges, k=7, A=14)
        hipotesis.py                 PruebaHipotesisZ: prueba bilateral H0: mu=50
    visualizacion/
        estilos.py                   Paleta de colores y estilo matplotlib
        graficas.py                  GraficasEstadisticas: todas las figuras matplotlib
    interfaz/
        componentes.py               Widgets reutilizables (MarcoDesplazable, etc.)
        ventana_principal.py         Ventana con sidebar y notebook de 8 pestanas
        pestanas/
            pestana_base.py          Clase base abstracta
            pestana_datos.py         Datos originales y ordenados
            pestana_centralizacion.py  Media, mediana y moda con procedimiento
            pestana_dispersion.py    Rango, varianza, desviacion estandar y CV
            pestana_frecuencias.py   Sturges, tabla fi-Fi-fri-Fri y explorador
            pestana_graficas.py      Histograma (toggle), poligono, ojivas
            pestana_forma.py         Asimetria, curtosis, KDE vs normal, QQ
            pestana_hipotesis.py     Conceptos y ejemplo practico prueba Z
            pestana_resumen.py       Tabla maestra, dashboard y conclusiones
```

---

## Pestanas de la aplicacion

| Pestana | Contenido |
|---|---|
| Datos | Datos originales por fila, sumas parciales y los 60 datos ordenados de menor a mayor. |
| Centralizacion | Media (50.65), mediana (50.5) y moda (55) con procedimiento paso a paso. |
| Dispersion | Rango (97), varianza (667.63), desviacion estandar (25.84) y CV (51%). |
| Frecuencias | Regla de Sturges (k=7, A=14), tabla fi Fi fri Fri y explorador interactivo de intervalos. |
| Graficas | Histograma con toggle abs/rel, poligono con media y mediana, ojivas absoluta y relativa, superposicion. |
| Forma | Asimetria positiva leve, curtosis platicurtica, densidad KDE vs normal, grafico QQ. |
| Hipotesis | Conceptos teoricos + ejemplo practico: prueba Z bilateral H0: mu=50 con n=36, x_barra=55. |
| Resumen | Tabla maestra de 16 medidas, dashboard 2x2 y seis conclusiones del informe. |

---

## Resultados esperados

| Medida | Valor |
|---|---|
| n | 60 |
| Media | 50.65 |
| Mediana | 50.50 |
| Moda | 55 (unimodal) |
| Rango | 97 |
| Varianza | 667.63 |
| Desviacion estandar | 25.84 |
| Coef. variacion | ~51% |
| k (Sturges) | 7 |
| Amplitud | 14 |
| Clase modal | [44, 58) con 11 datos |
| Asimetria | Positiva leve |
| Curtosis | Platicurtica |
| Z calculado (H0: mu=50) | 1.161 |
| Decision | No se rechaza H0 |
