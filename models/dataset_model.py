"""
Modelo para manejo de datasets y datos de la aplicación
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class DatasetModel:
    def __init__(self):
        self.original_dataset: Optional[pd.DataFrame] = None
        self.balanced_datasets: Dict[str, pd.DataFrame] = {}
        self.dataset_name: str = ""
        self.dataset_path: str = ""
        self.class_column: str = ""
        self.classes: List[str] = []
        self.imbalance_ratio: float = 0.0
        self.is_balanced: bool = False
        
    def load_dataset(self, file_path: str) -> Tuple[bool, str]:
        """
        Carga un dataset desde un archivo CSV
        Returns: (success, message)
        """
        try:
            # Validar extensión
            if not file_path.lower().endswith('.csv'):
                return False, "El archivo debe tener extensión .csv"
            
            # Cargar el dataset
            df = pd.read_csv(file_path)
            
            if df.empty:
                return False, "El archivo CSV está vacío"
            
            if len(df.columns) < 2:
                return False, "El dataset debe tener al menos 2 columnas"
            
            # Validar que todos los atributos excepto el último sean numéricos
            feature_columns = df.columns[:-1]
            for col in feature_columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    return False, f"El atributo '{col}' debe ser numérico"
            
            # Preprocesamiento básico de columnas
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

            # Preprocesamiento de la columna clase
            class_column = df.columns[-1]
            df[class_column] = df[class_column].apply(str.strip)
            df[class_column] = df[class_column].apply(str.lower)
            
            # Validar que la última columna sea la clase
            class_col = df.columns[-1]
            unique_classes = df[class_col].dropna().unique()
            
            if len(unique_classes) != 2:
                return False, "La versión actual solo soporta clasificación binaria (exactamente 2 clases)"
            
            # Verificar que no hay valores nulos en la columna de clase
            if df[class_col].isnull().any():
                return False, "La columna de clase no puede contener valores nulos"
            
            # Guardar información del dataset
            self.original_dataset = df
            self.dataset_name = Path(file_path).stem
            self.dataset_path = file_path
            self.class_column = class_col
            self.classes = list(unique_classes)
            
            # Calcular ratio de desbalance
            class_counts = df[class_col].value_counts()
            majority_count = class_counts.max()
            minority_count = class_counts.min()
            self.imbalance_ratio = majority_count / minority_count if minority_count > 0 else float('inf')
            self.is_balanced = self.imbalance_ratio < 1.5
            
            # Limpiar datasets balanceados anteriores
            self.balanced_datasets.clear()
            
            return True, "Dataset cargado exitosamente"
            
        except FileNotFoundError:
            return False, "No se pudo encontrar el archivo especificado"
        except pd.errors.EmptyDataError:
            return False, "El archivo CSV está vacío o corrupto"
        except pd.errors.ParserError:
            return False, "Error al parsear el archivo CSV. Verifique el formato."
        except Exception as e:
            return False, f"Error al cargar el dataset: {str(e)}"
    
    def get_dataset_summary(self) -> Dict:
        """Retorna un resumen del dataset actual"""
        if self.original_dataset is None:
            return {}
        
        df = self.original_dataset
        class_counts = df[self.class_column].value_counts()
        
        return {
            'name': self.dataset_name,
            'num_attributes': len(df.columns) - 1,
            'classes': self.classes,
            'class_counts': dict(class_counts),
            'total_instances': len(df),
            'missing_values': df.isnull().sum().sum(),
            'imbalance_ratio': round(self.imbalance_ratio, 2),
            'is_balanced': self.is_balanced
        }
    
    def add_balanced_dataset(self, algorithm_name: str, balanced_df: pd.DataFrame):
        """Agrega un dataset balanceado"""
        self.balanced_datasets[algorithm_name] = balanced_df
    
    def get_available_datasets(self) -> List[str]:
        """Retorna lista de datasets disponibles"""
        if self.original_dataset is None:
            return []
        
        datasets = ['Original']
        datasets.extend(list(self.balanced_datasets.keys()))
        return datasets
    
    def get_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """Retorna un dataset específico"""
        if name == 'Original':
            return self.original_dataset
        return self.balanced_datasets.get(name)
    
    def get_class_distribution(self, dataset_name: str) -> Dict[str, int]:
        """Retorna la distribución de clases para un dataset"""
        df = self.get_dataset(dataset_name)
        if df is None or self.class_column not in df.columns:
            return {}
        
        return dict(df[self.class_column].value_counts())
    
    def export_dataset(self, dataset_name: str, file_path: str) -> Tuple[bool, str]:
        """Exporta un dataset a CSV"""
        try:
            df = self.get_dataset(dataset_name)
            if df is None:
                return False, "Dataset no encontrado"
            
            df.to_csv(file_path, index=False)
            return True, "Dataset exportado exitosamente"
            
        except Exception as e:
            return False, f"Error al exportar: {str(e)}"
