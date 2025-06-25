"""
Controlador para la pestaña de Clasificación
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from views.classification_tab import ClassificationTab
from models.dataset_model import DatasetModel
from models.algorithm_model import AlgorithmModel
from models.results_model import ResultsModel
from services.classification_service import ClassificationService

class ClassificationController(QObject):
    # Señales
    classification_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str, str)
    
    def __init__(self, classification_view: ClassificationTab, dataset_model: DatasetModel,
                 algorithm_model: AlgorithmModel, results_model: ResultsModel,
                 classification_service: ClassificationService):
        super().__init__()
        self.view = classification_view
        self.dataset_model = dataset_model
        self.algorithm_model = algorithm_model
        self.results_model = results_model
        self.classification_service = classification_service
        
        # Configurar la vista con los modelos
        self.view.set_models(dataset_model, algorithm_model, results_model, classification_service)
        
        # Conectar señales de la vista
        self.view.evaluation_requested.connect(self.run_evaluation)
        self.view.export_results_requested.connect(self.export_results)
    
    def update_dataset(self):
        """Actualiza la vista cuando cambia el dataset"""
        self.view.update_dataset_combo()
    
    @pyqtSlot(str, list, list)
    def run_evaluation(self, dataset_name, selected_algorithms, selected_metrics):
        """Ejecuta la evaluación de algoritmos de clasificación"""
        try:
            # Validaciones
            if not selected_algorithms:
                self.error_occurred.emit(
                    "Sin Algoritmos",
                    "Debe seleccionar al menos un algoritmo de clasificación para poder continuar."
                )
                return
            
            if not selected_metrics:
                self.error_occurred.emit(
                    "Sin Métricas",
                    "Debe seleccionar al menos una métrica para poder continuar."
                )
                return
            
            # Obtener el dataset
            dataset = self.dataset_model.get_dataset(dataset_name)
            if dataset is None:
                self.error_occurred.emit(
                    "Dataset No Encontrado",
                    f"No se pudo encontrar el dataset '{dataset_name}'."
                )
                return
            
            # Ejecutar evaluación
            results = self.classification_service.evaluate_algorithms(
                dataset, selected_algorithms, selected_metrics
            )
            
            if not results:
                self.error_occurred.emit(
                    "Sin Resultados",
                    "No se pudieron obtener resultados de la evaluación."
                )
                return
            
            # Almacenar resultados en el modelo
            self.results_model.clear_results()
            for algorithm, metrics in results.items():
                for metric, value in metrics.items():
                    self.results_model.add_result(dataset_name, algorithm, metric, value)
            
            # Emitir señal de finalización
            self.classification_completed.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(
                "Error en Clasificación",
                f"Ocurrió un error durante la evaluación:\n{str(e)}"
            )
    
    @pyqtSlot(str)
    def export_results(self, file_path):
        """Exporta los resultados de clasificación"""
        try:
            if not self.results_model.has_results():
                self.error_occurred.emit(
                    "Sin Resultados",
                    "No hay resultados para exportar. Ejecute primero una evaluación."
                )
                return
            
            success, message = self.results_model.export_results(file_path)
            
            if not success:
                self.error_occurred.emit("Error de Exportación", message)
                
        except Exception as e:
            self.error_occurred.emit(
                "Error de Exportación",
                f"Ocurrió un error al exportar los resultados:\n{str(e)}"
            )
    
    def get_available_datasets(self):
        """Retorna la lista de datasets disponibles"""
        return self.dataset_model.get_available_datasets()
    
    def get_results_dataframe(self):
        """Retorna los resultados como DataFrame"""
        return self.results_model.get_results_dataframe()
