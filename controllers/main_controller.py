"""
Controlador principal de la aplicación BalanceAI
Coordina la comunicación entre modelos y vistas
"""

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSlot
from views.main_window import MainWindow
from models.dataset_model import DatasetModel
from models.algorithm_model import AlgorithmModel
from models.results_model import ResultsModel
from services.balancing_service import BalancingService
from services.classification_service import ClassificationService
from controllers.summary_controller import SummaryController
from controllers.balancing_controller import BalancingController
from controllers.classification_controller import ClassificationController
from controllers.app_controller import AppController

class MainController(QObject):
    def __init__(self):
        super().__init__()
        
        # Inicializar controlador de aplicación
        self.app_controller = AppController()
        
        # Inicializar modelos
        self.dataset_model = DatasetModel()
        self.algorithm_model = AlgorithmModel()
        self.results_model = ResultsModel()
        
        # Inicializar servicios
        self.balancing_service = BalancingService()
        self.classification_service = ClassificationService()
        
        # Inicializar vista principal
        self.main_window = MainWindow()
        
        # Restaurar geometría de ventana
        self.app_controller.restore_window_geometry(self.main_window)
        
        # Inicializar controladores de pestañas
        self.summary_controller = SummaryController(
            self.main_window.get_summary_tab(),
            self.dataset_model
        )
        
        self.balancing_controller = BalancingController(
            self.main_window.get_balancing_tab(),
            self.dataset_model,
            self.algorithm_model,
            self.balancing_service
        )
        
        self.classification_controller = ClassificationController(
            self.main_window.get_classification_tab(),
            self.dataset_model,
            self.algorithm_model,
            self.results_model,
            self.classification_service
        )
        
        # Conectar señales entre controladores
        self.connect_signals()
        
        # Configurar estado inicial
        self.setup_initial_state()
    
    def connect_signals(self):
        """Conecta las señales entre controladores"""
        
        # Cuando se carga un dataset en Summary, actualizar otras pestañas
        self.summary_controller.dataset_loaded.connect(self.on_dataset_loaded)
        
        # Cuando se completa el balanceo, habilitar clasificación
        self.balancing_controller.balancing_completed.connect(self.on_balancing_completed)
        
        # Cuando se completa la clasificación, actualizar resultados
        self.classification_controller.classification_completed.connect(self.on_classification_completed)
        
        # Manejo de errores globales
        self.summary_controller.error_occurred.connect(self.show_error_message)
        self.balancing_controller.error_occurred.connect(self.show_error_message)
        self.classification_controller.error_occurred.connect(self.show_error_message)
        
        # Conectar cierre de ventana para guardar configuración
        self.main_window.closeEvent = self.on_close_event
    
    def setup_initial_state(self):
        """Configura el estado inicial de la aplicación"""
        # Deshabilitar pestañas hasta que se cargue un dataset
        self.main_window.set_tabs_enabled(False)
        self.main_window.update_status("Listo - Cargue una base de conocimientos para comenzar")
    
    @pyqtSlot(dict)
    def on_dataset_loaded(self, dataset_info):
        """Maneja la carga exitosa de un dataset"""
        # Habilitar pestañas apropiadas
        is_balanced = dataset_info.get('is_balanced', False)
        
        if is_balanced:
            # Si está balanceado, deshabilitar balanceo pero habilitar clasificación
            self.main_window.set_tabs_enabled(True)
            self.main_window.tab_widget.setTabEnabled(1, False)  # Deshabilitar Balanceo
            self.main_window.show_message(
                "Dataset Balanceado",
                "La base de conocimientos presenta un nivel de desbalance inferior a 1.5, "
                "por lo que se considera balanceada. El módulo de balanceo estará deshabilitado.",
                "warning"
            )
        else:
            # Habilitar todas las pestañas
            self.main_window.set_tabs_enabled(True)
        
        # Actualizar controladores con el nuevo dataset
        self.balancing_controller.update_dataset()
        self.classification_controller.update_dataset()
        
        # Actualizar barra de estado
        dataset_name = dataset_info.get('name', 'Dataset')
        total_instances = dataset_info.get('total_instances', 0)
        self.main_window.update_status(
            f"Dataset cargado: {dataset_name} ({total_instances} instancias)"
        )
    
    @pyqtSlot(list)
    def on_balancing_completed(self, algorithm_names):
        """Maneja la finalización del proceso de balanceo"""
        self.main_window.update_status(
            f"Balanceo completado - {len(algorithm_names)} algoritmos ejecutados"
        )
        
        # Actualizar controlador de clasificación con nuevos datasets
        self.classification_controller.update_dataset()
        
        # Mostrar mensaje de éxito
        self.main_window.show_message(
            "Balanceo Completado",
            f"Se han ejecutado exitosamente {len(algorithm_names)} algoritmos de balanceo.\n"
            f"Algoritmos: {', '.join(algorithm_names)}",
            "information"
        )
    
    @pyqtSlot(dict)
    def on_classification_completed(self, results):
        """Maneja la finalización del proceso de clasificación"""
        num_algorithms = len(results)
        self.main_window.update_status(
            f"Clasificación completada - {num_algorithms} algoritmos evaluados"
        )
        
        # Mostrar mensaje de éxito
        self.main_window.show_message(
            "Clasificación Completada",
            f"Se han evaluado exitosamente {num_algorithms} algoritmos de clasificación.",
            "information"
        )
    
    @pyqtSlot(str, str)
    def show_error_message(self, title, message):
        """Muestra un mensaje de error"""
        self.main_window.show_message(title, message, "error")
        self.main_window.update_status(f"Error: {title}")
    
    def on_close_event(self, event):
        """Maneja el evento de cierre de la aplicación"""
        # Guardar geometría de ventana
        self.app_controller.save_window_geometry(self.main_window)
        
        # Limpiar recursos
        self.app_controller.cleanup()
        
        # Aceptar el evento de cierre
        event.accept()
    
    def show(self):
        """Muestra la ventana principal"""
        self.main_window.show()
    
    def close(self):
        """Cierra la aplicación"""
        self.main_window.close()
