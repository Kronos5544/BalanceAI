"""
Servicio para ejecutar algoritmos de clasificación y calcular métricas
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score, precision_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder

class ClassificationService:
    def __init__(self):
        self.algorithms = {
            'C4.5': DecisionTreeClassifier(criterion='entropy', random_state=42),
            'MLP': MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42)
        }
        
        self.metrics = {
            'AUC': self._calculate_auc,
            'F1-Score': self._calculate_f1,
            'Precision': self._calculate_precision
        }
    
    def evaluate_algorithms(self, dataset: pd.DataFrame, selected_algorithms: List[str], 
                          selected_metrics: List[str], cv_folds: int = 5) -> Dict[str, Dict[str, float]]:
        """
        Evalúa los algoritmos seleccionados con las métricas especificadas
        Returns: Dict con estructura {algoritmo: {metrica: valor}}
        """
        results = {}
        
        # Preparar datos
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        
        # Codificar etiquetas si son categóricas
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        # Configurar validación cruzada estratificada
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        
        
        for algorithm_name in selected_algorithms:
            if algorithm_name not in self.algorithms:
                continue
                
            
            classifier = self.algorithms[algorithm_name]
            
            try:
                algorithm_results = {}
                for metric_name in selected_metrics:
                    if metric_name not in self.metrics:
                        continue
                    
                    # Calcular métrica usando validación cruzada
                    scores = self.metrics[metric_name](classifier, X, y_encoded, cv)
                    algorithm_results[metric_name] = np.mean(scores)
                
                results[algorithm_name] = algorithm_results
                
            except Exception as e:
                print(f"Error evaluando {algorithm_name}: {str(e)}")
                continue
        
        return results
    
    def _calculate_auc(self, classifier, X: np.ndarray, y: np.ndarray, cv) -> np.ndarray:
        """Calcula AUC usando validación cruzada"""
        return cross_val_score(classifier, X, y, cv=cv, scoring='roc_auc')
    
    def _calculate_f1(self, classifier, X: np.ndarray, y: np.ndarray, cv) -> np.ndarray:
        """Calcula F1-Score usando validación cruzada"""
        return cross_val_score(classifier, X, y, cv=cv, scoring='f1')
    
    def _calculate_precision(self, classifier, X: np.ndarray, y: np.ndarray, cv) -> np.ndarray:
        """Calcula Precision usando validación cruzada"""
        return cross_val_score(classifier, X, y, cv=cv, scoring='precision')
