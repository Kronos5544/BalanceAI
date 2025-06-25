"""
Controlador para la pestaña de Balanceo
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from views.balancing_tab import BalancingTab
from models.dataset_model import DatasetModel
from models.algorithm_model import AlgorithmModel
from services.balancing_service import BalancingService

class BalancingController(QObject):
    # Señales
    balancing_completed = pyqtSignal(list)
    error_occurred = pyqtSignal(str, str)
    
    def __init__(self, balancing_view: BalancingTab, dataset_model: DatasetModel, 
                 algorithm_model: AlgorithmModel, balancing_service: BalancingService):
        super().__init__()
        self.view = balancing_view
        self.dataset_model = dataset_model
        self.algorithm_model = algorithm_model
        self.balancing_service = balancing_service
        
        # Configurar la vista con los modelos
        self.view.set_models(dataset_model, algorithm_model, balancing_service)
        
        # Conectar señales de la vista
        self.view.algorithms_selected.connect(self.on_algorithms_selected)
        self.view.export_dataset_requested.connect(self.export_dataset)
    
    def update_dataset(self):
        """Actualiza la vista cuando cambia el dataset"""
        self.view.update_dataset_combo()
    
    @pyqtSlot(list)
    def on_algorithms_selected(self, algorithm_names):
        """Maneja la selección y ejecución de algoritmos de balanceo"""
        try:
            # Verificar que hay algoritmos seleccionados
            if not algorithm_names:
                self.error_occurred.emit(
                    "Sin Algoritmos",
                    "No se seleccionaron algoritmos de balanceo."
                )
                return
            
            # Verificar que hay un dataset original
            if self.dataset_model.original_dataset is None:
                self.error_occurred.emit(
                    "Sin Dataset",
                    "No hay un dataset cargado para balancear."
                )
                return
            
            # Los algoritmos ya fueron ejecutados en la vista (BalancingWorker)
            # Solo necesitamos emitir la señal de finalización
            self.balancing_completed.emit(algorithm_names)
            
        except Exception as e:
            self.error_occurred.emit(
                "Error en Balanceo",
                f"Ocurrió un error durante el proceso de balanceo:\n{str(e)}"
            )
    
    @pyqtSlot(str, str)
    def export_dataset(self, dataset_name, file_path):
        """Exporta un dataset específico"""
        try:
            success, message = self.dataset_model.export_dataset(dataset_name, file_path)
            
            if success:
                # Mostrar mensaje de éxito (opcional, se puede manejar en la vista)
                pass
            else:
                self.error_occurred.emit("Error de Exportación", message)
                
        except Exception as e:
            self.error_occurred.emit(
                "Error de Exportación",
                f"Ocurrió un error al exportar el dataset:\n{str(e)}"
            )
    
    def get_available_datasets(self):
        """Retorna la lista de datasets disponibles"""
        return self.dataset_model.get_available_datasets()
    
    def get_dataset_distribution(self, dataset_name):
        """Retorna la distribución de clases para un dataset"""
        return self.dataset_model.get_class_distribution(dataset_name)
