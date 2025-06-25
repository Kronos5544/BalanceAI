"""
Controlador para diálogos de selección de algoritmos
"""

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QDialog
from views.algorithm_selection_dialog import AlgorithmSelectionDialog
from models.algorithm_model import AlgorithmModel
from typing import List, Dict

class DialogController(QObject):
    def __init__(self):
        super().__init__()
    
    def show_balancing_algorithm_selection(self, algorithm_model: AlgorithmModel, 
                                         current_selection: List[str], 
                                         parent=None) -> tuple[bool, List[str]]:
        """
        Muestra el diálogo de selección de algoritmos de balanceo
        Returns: (accepted, selected_algorithms)
        """
        algorithms = algorithm_model.get_balancing_algorithms()
        
        dialog = AlgorithmSelectionDialog(
            algorithms,
            current_selection,
            "Seleccionar Algoritmos de Balanceo",
            parent
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return True, dialog.get_selected_algorithms()
        else:
            return False, current_selection
    
    def show_classification_algorithm_selection(self, algorithm_model: AlgorithmModel,
                                              current_selection: List[str],
                                              parent=None) -> tuple[bool, List[str]]:
        """
        Muestra el diálogo de selección de algoritmos de clasificación
        Returns: (accepted, selected_algorithms)
        """
        algorithms = algorithm_model.get_classification_algorithms()
        
        dialog = AlgorithmSelectionDialog(
            algorithms,
            current_selection,
            "Seleccionar Algoritmos de Clasificación",
            parent
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return True, dialog.get_selected_algorithms()
        else:
            return False, current_selection
    
    def show_metrics_selection(self, algorithm_model: AlgorithmModel,
                             current_selection: List[str],
                             parent=None) -> tuple[bool, List[str]]:
        """
        Muestra el diálogo de selección de métricas
        Returns: (accepted, selected_metrics)
        """
        metrics = algorithm_model.get_metrics()
        
        dialog = AlgorithmSelectionDialog(
            metrics,
            current_selection,
            "Seleccionar Métricas",
            parent
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return True, dialog.get_selected_algorithms()  # Reutiliza el mismo método
        else:
            return False, current_selection
