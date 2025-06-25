"""
Controlador para la pestaña de Resumen
"""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from views.summary_tab import SummaryTab
from models.dataset_model import DatasetModel

class SummaryController(QObject):
    # Señales
    dataset_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str, str)
    
    def __init__(self, summary_view: SummaryTab, dataset_model: DatasetModel):
        super().__init__()
        self.view = summary_view
        self.model = dataset_model
        
        # Conectar señales de la vista
        self.view.load_dataset_requested.connect(self.load_dataset)
    
    @pyqtSlot(str)
    def load_dataset(self, file_path: str):
        """Carga un dataset desde el archivo especificado"""
        try:
            # Verificar si ya hay un dataset cargado
            if self.model.original_dataset is not None:
                # Mostrar advertencia de confirmación
                from PyQt6.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self.view,
                    "Confirmar Carga",
                    "Ya existe una base de conocimientos cargada. "
                    "Se perderán todos los datos actuales incluyendo "
                    "las bases balanceadas y resultados de clasificación.\n\n"
                    "¿Desea continuar?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply != QMessageBox.StandardButton.Yes:
                    return
            
            # Intentar cargar el dataset
            success, message = self.model.load_dataset(file_path)
            
            if success:
                # Obtener resumen del dataset
                summary = self.model.get_dataset_summary()
                
                # Actualizar la vista con el resumen
                self.view.show_dataset_summary(summary)
                
                # Emitir señal de éxito
                self.dataset_loaded.emit(summary)
                
            else:
                # Mostrar error
                self.error_occurred.emit("Error al Cargar Dataset", message)
                
        except Exception as e:
            self.error_occurred.emit(
                "Error Inesperado", 
                f"Ocurrió un error inesperado al cargar el dataset:\n{str(e)}"
            )
    
    def get_dataset_summary(self):
        """Retorna el resumen del dataset actual"""
        return self.model.get_dataset_summary()
    
    def is_dataset_loaded(self):
        """Verifica si hay un dataset cargado"""
        return self.model.original_dataset is not None
