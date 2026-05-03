from .datos import (
    TODOS_LOS_CONGLOMERADOS,
    CONGLOMERADOS_SELECCIONADOS,
    ESTUDIANTES_POR_SEMESTRE,
    TOTAL_SEMESTRES,
    N_POBLACION,
)


class MuestreoConglomerados:
    """
    Encapsula la informacion conceptual del diseno de muestreo por conglomerados.
    Esta clase no hace calculos estadisticos, solo organiza los datos del diseno
    para que las pestanas de la interfaz los puedan mostrar facilmente.

    Separar esto en su propia clase sigue el principio de responsabilidad unica:
    la logica del muestreo vive aqui, los calculos estadisticos en estadistica.py.
    """

    # Metodos de muestreo para la tabla comparativa del informe
    COMPARACION_METODOS = [
        {
            "Metodo": "Muestreo Aleatorio Simple",
            "Como funcionaria": "Seleccionar 36 estudiantes al azar de los 72",
            "Por que no es mejor": "Requiere lista completa y contacto individual con cada estudiante",
        },
        {
            "Metodo": "Muestreo Estratificado",
            "Como funcionaria": "Seleccionar un numero proporcional de estudiantes de cada semestre",
            "Por que no es mejor": "Mas preciso pero mas complejo, hay que seleccionar dentro de cada grupo",
        },
        {
            "Metodo": "Muestreo por Conglomerados",
            "Como funcionaria": "Seleccionar semestres completos al azar",
            "Por que no es mejor": "Es el mas practico: facil acceso, bajo costo y probabilistico",
        },
        {
            "Metodo": "Muestreo por Conveniencia",
            "Como funcionaria": "Encuestar a los estudiantes que esten disponibles",
            "Por que no es mejor": "No es probabilistico, puede sesgar los resultados",
        },
    ]

    VENTAJAS = [
        "Facil aplicacion: los grupos ya existen, no hay que construirlos.",
        "Bajo costo: se accede a grupos completos en vez de buscar personas individualmente.",
        "Ahorro de tiempo: se recolectan muchos datos en pocas visitas.",
        "Es probabilistico: cada grupo tiene la misma oportunidad de ser seleccionado.",
    ]

    DESVENTAJAS = [
        "Menor precision: si los conglomerados son muy diferentes entre si la muestra puede no ser representativa.",
        "Riesgo de homogeneidad interna: estudiantes del mismo semestre se parecen entre si.",
        "Depende del numero de conglomerados: si hay pocos grupos la seleccion puede ser poco representativa.",
        "Se pierde precision frente al muestreo estratificado.",
    ]

    def __init__(self) -> None:
        self.poblacion_total = N_POBLACION
        self.total_semestres = TOTAL_SEMESTRES
        self.estudiantes_por_semestre = ESTUDIANTES_POR_SEMESTRE
        self.todos_los_conglomerados = TODOS_LOS_CONGLOMERADOS
        self.seleccionados = CONGLOMERADOS_SELECCIONADOS
        self.conglomerados_muestra = len(self.seleccionados)
        self.n_muestra = self.conglomerados_muestra * self.estudiantes_por_semestre

    @property
    def probabilidad_seleccion(self) -> float:
        """Probabilidad de que un conglomerado sea seleccionado."""
        return self.conglomerados_muestra / self.total_semestres

    @property
    def fraccion_muestreo(self) -> float:
        """Que fraccion de la poblacion quedo en la muestra."""
        return self.n_muestra / self.poblacion_total

    def es_seleccionado(self, nombre: str) -> bool:
        """Indica si un conglomerado fue seleccionado para la muestra."""
        return nombre in self.seleccionados

    @property
    def pasos_seleccion(self) -> list:
        """Lista de pasos del procedimiento de seleccion para mostrar en pantalla."""
        return [
            "Numerar los conglomerados del 1 al 6 (un numero por semestre).",
            "Usar una funcion aleatoria (randint de Python) para sortear 3 de los 6.",
            "Resultado del sorteo: conglomerados 2, 4 y 6 (Semestres II, IV y VI).",
            "Incluir los 12 estudiantes de cada semestre seleccionado en la muestra.",
            f"Muestra final: 3 semestres x 12 estudiantes = {self.n_muestra} estudiantes.",
        ]