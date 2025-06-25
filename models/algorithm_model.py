"""
Modelo para algoritmos de balanceo y clasificación
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AlgorithmInfo:
    name: str
    description: str
    category: str  # 'balancing' , 'classification' or metric
    enabled: bool = True

class AlgorithmModel:
    def __init__(self):
        self.balancing_algorithms = {
            'SMOTE-COV-LW (En rango)': AlgorithmInfo(
                name='SMOTE-COV-LW (En rango)',
                description='Genera datos sintéticos para clases minoritarias usando una distribución normal multivariada con una covarianza regularizada por el método de Ledoit-Wolf.',
                category='balancing'
            ),
            'SMOTE-COV-LW (Fuera de rango)': AlgorithmInfo(
                name='SMOTE-COV-LW (Fuera de rango)',
                description='Genera datos sintéticos para clases minoritarias usando una distribución normal multivariada con una covarianza regularizada por el método de Ledoit-Wolf.',
                category='balancing'
            ),
            'SMOTE-RL': AlgorithmInfo(
                name='SMOTE-RL',
                description='Genera muestras sintéticas de la clase minoritaria modelando su comportamiento con regresión Lasso, seleccionando los atributos importantes y evitando el sobreajuste.',
                category='balancing'
            ),
            'SMOTE-EN': AlgorithmInfo(
                name='SMOTE-EN',
                description='Genera instancias sintéticas de la clase minoritaria usando regresión Elastic Net, combinando regularización L1 y L2. Es especialmente eficaz en conjuntos de datos con variables altamente correlacionadas.',
                category='balancing'
            )
        }
        
        self.classification_algorithms = {
            'C4.5': AlgorithmInfo(
                name='C4.5',
                description='Es un algoritmo de clasificación que construye árboles de decisión usando la ganancia de información normalizada (gain ratio) para seleccionar atributos. Es robusto ante valores continuos, discretos y faltantes, y aplica poda automática para evitar sobreajuste.',
                category='classification'
            ),
            'MLP': AlgorithmInfo(
                name='MLP',
                description='Es una red neuronal con capas de neuronas interconectadas que utiliza funciones de activación no lineales para clasificar datos complejos.',
                category='classification'
            ),
            'KNN': AlgorithmInfo(
                name='KNN',
                description='Es un algoritmo de clasificación que asigna a un nuevo dato la clase más común entre sus k vecinos más cercanos, usando una métrica de distancia.',
                category='classification'
            ),
            'Random Forest': AlgorithmInfo(
                name='Random Forest',
                description='Es un algoritmo de clasificación basado en el ensamblaje de múltiples árboles de decisión entrenados sobre subconjuntos aleatorios del conjunto de datos y de atributos. Sus predicciones se combinan mediante votación mayoritaria.',
                category='classification'
            ),
            'SVM': AlgorithmInfo(
                name='SVM',
                description='Es un algoritmo de clasificación que busca encontrar un hiperplano que separe las clases con el mayor margen posible. Utiliza vectores de soporte para definir esa frontera.',
                category='classification'
            )
        }
        
        self.metrics = {
            'AUC': AlgorithmInfo(
                name='AUC',
                description='Resume la capacidad del clasificador para distinguir entre clases al calcular la probabilidad de que una instancia positiva reciba una puntuación mayor que una negativa',
                category='metric'
            ),
            'F1-Score': AlgorithmInfo(
                name='F1-Score',
                description='Mide el balance entre precisión y recall en clasificación',
                category='metric'
            ),
            'Precision': AlgorithmInfo(
                name='Precision',
                description='Mide la exactitud de las predicciones positivas. Indica qué porcentaje de casos clasificados como positivos son realmente positivos.',
                category='metric'
            )
        }
        
        self.selected_balancing = []
        self.selected_classification = []
        self.selected_metrics = []
    
    def get_balancing_algorithms(self) -> Dict[str, AlgorithmInfo]:
        return self.balancing_algorithms
    
    def get_classification_algorithms(self) -> Dict[str, AlgorithmInfo]:
        return self.classification_algorithms
    
    def get_metrics(self) -> Dict[str, AlgorithmInfo]:
        return self.metrics
    
    def set_selected_balancing(self, algorithms: List[str]):
        self.selected_balancing = algorithms
    
    def set_selected_classification(self, algorithms: List[str]):
        self.selected_classification = algorithms
    
    def set_selected_metrics(self, metrics: List[str]):
        self.selected_metrics = metrics
    
    def get_selected_balancing(self) -> List[str]:
        return self.selected_balancing
    
    def get_selected_classification(self) -> List[str]:
        return self.selected_classification
    
    def get_selected_metrics(self) -> List[str]:
        return self.selected_metrics
