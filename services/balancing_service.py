"""
Servicio para ejecutar algoritmos de balanceo
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from algorithms.SMOTE_COV_LW import SMOTECOVLW
from algorithms.SMOTE_RL import SMOTERL
from algorithms.SMOTE_EN import SMOTEEN

class BalancingService:
    def __init__(self):
        self.algorithms = {
            'SMOTE-COV-LW (En rango)': self._run_smote_cov_lw_in_range,
            'SMOTE-COV-LW (Fuera de rango)': self._run_smote_cov_lw_out_range,
            'SMOTE-RL': self._run_smote_rl,
            'SMOTE-EN': self._run_smote_en
        }
    
    def run_balancing_algorithms(self, dataset: pd.DataFrame, selected_algorithms: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Ejecuta los algoritmos de balanceo seleccionados
        Returns: Dict con nombre_algoritmo -> dataset_balanceado
        """
        results = {}
        
        # Preparar datos para los algoritmos
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        
        for algorithm_name in selected_algorithms:
            try:
                if algorithm_name in self.algorithms:
                    balanced_data = self.algorithms[algorithm_name](X, y)
                    
                    # Convertir resultado a DataFrame
                    if isinstance(balanced_data, dict):
                        # Para SMOTE-COV-LW que retorna múltiples versiones
                        if algorithm_name == 'SMOTE-COV-LW (En rango)':
                            X_balanced, y_balanced = balanced_data['in_range']
                        else:  # SMOTE-COV-LW (Fuera de rango)
                            X_balanced, y_balanced = balanced_data['free_range']
                    else:
                        # Para otros algoritmos que retornan tupla
                        X_balanced, y_balanced = balanced_data
                    
                    # Crear DataFrame balanceado
                    balanced_df = pd.DataFrame(X_balanced, columns=dataset.columns[:-1])
                    balanced_df[dataset.columns[-1]] = y_balanced
                    
                    results[algorithm_name] = balanced_df
                    
            except Exception as e:
                print(f"Error ejecutando {algorithm_name}: {str(e)}")
                continue
        
        return results
    
    def _run_smote_cov_lw_in_range(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Ejecuta SMOTE-COV-LW en rango"""
        smote_cov_lw = SMOTECOVLW()
        return smote_cov_lw.fit_resample(X, y)
    
    def _run_smote_cov_lw_out_range(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Ejecuta SMOTE-COV-LW fuera de rango"""
        smote_cov_lw = SMOTECOVLW()
        return smote_cov_lw.fit_resample(X, y)
    
    def _run_smote_rl(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Ejecuta SMOTE-RL"""
        smote_rl = SMOTERL()
        return smote_rl.fit_resample(X, y)
    
    def _run_smote_en(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Ejecuta SMOTE-EN"""
        smote_en = SMOTEEN()
        return smote_en.fit_resample(X, y)
