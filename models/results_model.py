"""
Modelo para almacenar y manejar resultados de clasificación
"""

import pandas as pd
from typing import Dict, List, Optional

class ResultsModel:
    def __init__(self):
        self.results: Dict[str, Dict[str, float]] = {}
        # Estructura: {dataset_name: {algorithm_metric: value}}
        
    def add_result(self, dataset_name: str, algorithm: str, metric: str, value: float):
        """Agrega un resultado de evaluación"""
        key = f"{dataset_name}"
        if key not in self.results:
            self.results[key] = {}
        
        metric_key = f"{algorithm}_{metric}"
        self.results[key][metric_key] = value
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Retorna los resultados como DataFrame para visualización"""
        if not self.results:
            return pd.DataFrame()
        
        # Crear lista de filas para el DataFrame
        rows = []
        
        # Obtener todos los algoritmos y métricas únicos
        all_algorithms = set()
        all_metrics = set()
        
        for dataset_results in self.results.values():
            for key in dataset_results.keys():
                if '_' in key:
                    algorithm, metric = key.rsplit('_', 1)
                    all_algorithms.add(algorithm)
                    all_metrics.add(metric)
        
        # Crear filas del DataFrame
        for dataset_name, dataset_results in self.results.items():
            for algorithm in sorted(all_algorithms):
                row = {'Dataset': dataset_name, 'Algoritmo': algorithm}
                for metric in sorted(all_metrics):
                    key = f"{algorithm}_{metric}"
                    row[metric] = dataset_results.get(key, 0.0)
                rows.append(row)
        
        return pd.DataFrame(rows)
    
    def export_results(self, file_path: str) -> tuple[bool, str]:
        """Exporta los resultados a CSV"""
        try:
            df = self.get_results_dataframe()
            if df.empty:
                return False, "No hay resultados para exportar"
            
            df.to_csv(file_path, index=False)
            return True, "Resultados exportados exitosamente"
            
        except Exception as e:
            return False, f"Error al exportar resultados: {str(e)}"
    
    def clear_results(self):
        """Limpia todos los resultados"""
        self.results.clear()
    
    def has_results(self) -> bool:
        """Verifica si hay resultados disponibles"""
        return bool(self.results)
