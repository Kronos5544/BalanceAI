"""
Pestaña de Clasificación - Evaluación de algoritmos de clasificación
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QComboBox, QFrame, QTableWidget, QTableWidgetItem,
                            QFileDialog, QProgressBar, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QFont
import pandas as pd
from views.algorithm_selection_dialog import AlgorithmSelectionDialog

class ClassificationWorker(QThread):
    """Worker thread para ejecutar evaluación de clasificación"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, classification_service, dataset, selected_algorithms, selected_metrics):
        super().__init__()
        self.classification_service = classification_service
        self.dataset = dataset
        self.selected_algorithms = selected_algorithms
        self.selected_metrics = selected_metrics
    
    def run(self):
        try:
            results = self.classification_service.evaluate_algorithms(
                self.dataset, self.selected_algorithms, self.selected_metrics
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class ClassificationTab(QWidget):
    # Señales
    evaluation_requested = pyqtSignal(str, list, list)
    export_results_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.dataset_model = None
        self.algorithm_model = None
        self.results_model = None
        self.classification_service = None
        self.selected_algorithms = []
        self.selected_metrics = []
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Sección de controles
        self.create_controls_section(layout)
        
        # Mensaje de advertencia
        self.create_warning_section(layout)
        
        # Tabla de resultados
        self.create_results_section(layout)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_controls_section(self, layout):
        """Crea la sección de controles"""
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Primera fila
        first_row = QHBoxLayout()
        
        # Selección de algoritmos de clasificación
        self.select_algorithms_button = QPushButton("Seleccionar Algoritmos de Clasificación")
        self.select_algorithms_button.clicked.connect(self.select_classification_algorithms)
        first_row.addWidget(self.select_algorithms_button)
        
        # Selección de base de conocimientos
        message = QLabel("BC:")
        message.setStyleSheet("font-size: 14pt")
        first_row.addWidget(message)
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(150)
        first_row.addWidget(self.dataset_combo)
        
        first_row.addStretch()
        
        # Botón exportar resultados
        self.export_button = QPushButton("Exportar Resultados")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        first_row.addWidget(self.export_button)
        
        controls_layout.addLayout(first_row)
        
        # Segunda fila
        second_row = QHBoxLayout()
        
        # Selección de métricas
        self.select_metrics_button = QPushButton("Seleccionar Métricas")
        self.select_metrics_button.clicked.connect(self.select_metrics)
        second_row.addWidget(self.select_metrics_button)
        
        second_row.addStretch()
        
        controls_layout.addLayout(second_row)
        
        # Tercera fila
        third_row = QHBoxLayout()
        
        # Botón ejecutar evaluación
        self.execute_button = QPushButton("Ejecutar Evaluación")
        self.execute_button.clicked.connect(self.execute_evaluation)
        third_row.addWidget(self.execute_button)
        
        third_row.addStretch()
        
        controls_layout.addLayout(third_row)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        controls_layout.addWidget(self.progress_bar)
        
        layout.addWidget(controls_frame)
    
    def create_warning_section(self, layout):
        """Crea la sección de mensaje de advertencia"""
        self.warning_frame = QFrame()
        self.warning_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        warning_layout = QVBoxLayout(self.warning_frame)
        
        self.warning_label = QLabel(
            "Debe seleccionar al menos un algoritmo de clasificación y alguna métrica "
            "para poder continuar."
        )
        self.warning_label.setWordWrap(True)
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning_layout.addWidget(self.warning_label)
        
        # Estilo de advertencia
        self.warning_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
            }
            QLabel {
                color: #856404;
                font-weight: bold;
                font-size: 14pt;
            }
        """)
        
        layout.addWidget(self.warning_frame)
    
    def create_results_section(self, layout):
        """Crea la sección de resultados"""
        results_frame = QFrame()
        results_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        results_layout = QVBoxLayout(results_frame)
        
        # Título
        title = QLabel("Resultados de Evaluación")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        results_layout.addWidget(title)
        
        # Tabla
        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.results_table)
        
        layout.addWidget(results_frame)
    
    def set_models(self, dataset_model, algorithm_model, results_model, classification_service):
        """Configura los modelos y servicios"""
        self.dataset_model = dataset_model
        self.algorithm_model = algorithm_model
        self.results_model = results_model
        self.classification_service = classification_service
        self.update_dataset_combo()
        self.update_warning_visibility()
    
    def update_dataset_combo(self):
        """Actualiza el combo de datasets"""
        if not self.dataset_model:
            return
        
        self.dataset_combo.clear()
        datasets = self.dataset_model.get_available_datasets()
        self.dataset_combo.addItems(datasets)
    
    def select_classification_algorithms(self):
        """Abre el diálogo de selección de algoritmos de clasificación"""
        if not self.algorithm_model:
            return
        
        from views.algorithm_selection_dialog import AlgorithmSelectionDialog
        
        dialog = AlgorithmSelectionDialog(
            self.algorithm_model.get_classification_algorithms(),
            self.selected_algorithms,
            "Seleccionar Algoritmos de Clasificación",
            self
        )
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.selected_algorithms = dialog.get_selected_algorithms()
            self.update_warning_visibility()
    
    def select_metrics(self):
        """Abre el diálogo de selección de métricas"""
        if not self.algorithm_model:
            return
        
        from views.algorithm_selection_dialog import AlgorithmSelectionDialog
        
        dialog = AlgorithmSelectionDialog(
            self.algorithm_model.get_metrics(),
            self.selected_metrics,
            "Seleccionar Métricas",
            self
        )
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.selected_metrics = dialog.get_selected_algorithms()  # Reutiliza el método
            self.update_warning_visibility()
    
    def update_warning_visibility(self):
        """Actualiza la visibilidad del mensaje de advertencia"""
        show_warning = not self.selected_algorithms or not self.selected_metrics
        self.warning_frame.setVisible(show_warning)
    
    def execute_evaluation(self):
        """Ejecuta la evaluación de algoritmos"""
        if not self.selected_algorithms or not self.selected_metrics:
            return
        
        dataset_name = self.dataset_combo.currentText()
        if not dataset_name or not self.dataset_model:
            return
        
        dataset = self.dataset_model.get_dataset(dataset_name)
        if dataset is None:
            return
        
        # Mostrar progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.execute_button.setEnabled(False)
        
        # Ejecutar en hilo separado
        self.worker = ClassificationWorker(
            self.classification_service,
            dataset,
            self.selected_algorithms,
            self.selected_metrics
        )
        self.worker.finished.connect(self.on_evaluation_finished)
        self.worker.error.connect(self.on_evaluation_error)
        self.worker.start()
    
    @pyqtSlot(dict)
    def on_evaluation_finished(self, results):
        """Maneja la finalización de la evaluación"""
        # Actualizar tabla de resultados
        self.update_results_table(results)
        
        # Ocultar progreso
        self.progress_bar.setVisible(False)
        self.execute_button.setEnabled(True)
        self.export_button.setEnabled(True)
        
        # Emitir señal
        dataset_name = self.dataset_combo.currentText()
        self.evaluation_requested.emit(dataset_name, self.selected_algorithms, self.selected_metrics)
    
    @pyqtSlot(str)
    def on_evaluation_error(self, error_message):
        """Maneja errores en la evaluación"""
        self.progress_bar.setVisible(False)
        self.execute_button.setEnabled(True)
        print(f"Error en evaluación: {error_message}")
    
    def update_results_table(self, results):
        """Actualiza la tabla de resultados"""
        if not results:
            return
        
        # Preparar datos para la tabla
        algorithms = list(results.keys())
        metrics = list(next(iter(results.values())).keys()) if results else []
        
        # Configurar tabla
        self.results_table.setRowCount(len(algorithms))
        self.results_table.setColumnCount(len(metrics) + 1)
        
        # Headers
        headers = ["Algoritmo"] + metrics
        self.results_table.setHorizontalHeaderLabels(headers)
        
        # Configurar header vertical (números de fila)
        vertical_headers = [str(i + 1) for i in range(len(algorithms))]
        self.results_table.setVerticalHeaderLabels(vertical_headers)
        
        # Llenar datos
        for row, algorithm in enumerate(algorithms):
            # Columna de algoritmo
            algorithm_item = QTableWidgetItem(algorithm)
            algorithm_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            algorithm_item.setFlags(algorithm_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.results_table.setItem(row, 0, algorithm_item)
            
            # Columnas de métricas
            for col, metric in enumerate(metrics):
                value = results[algorithm].get(metric, 0.0)
                metric_item = QTableWidgetItem(f"{value:.4f}")
                metric_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                metric_item.setFlags(metric_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.results_table.setItem(row, col + 1, metric_item)
        
        # Ajustar columnas
        self.results_table.resizeColumnsToContents()
        
        # Configurar el header horizontal
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(1, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        # Mostrar headers
        print(self.results_table.horizontalHeader().isEnabled())
        #self.results_table.verticalHeader().setVisible(True)"""
    
    def export_results(self):
        """Exporta los resultados a CSV"""
        if not self.results_model or not self.results_model.has_results():
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Resultados",
            "resultados_clasificacion.csv",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        
        if file_path:
            self.export_results_requested.emit(file_path)
    
    def apply_styles(self):
        """Aplica estilos CSS"""
        style = """
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-height: 30px;
            font-size: 14pt
        }
        
        QPushButton:hover {
            background-color: #0056b3;
        }
        
        QPushButton:pressed {
            background-color: #004085;
        }
        
        QPushButton:disabled {
            background-color: #6c757d;
        }
        
        QFrame {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            
        }
        
        QComboBox {
            padding: 5px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14pt;
        }
        
        QComboBox:hover {
            border-color: #007bff;
        }

        QComboBox:focus {
            border-color: #007bff;
        }
        
        QTableWidget {
            gridline-color: #dee2e6;
            background-color: white;
            alternate-background-color: #f8f9fa;
            font-size: 14pt;
        }
        
        QHeaderView::section {
            background-color: #e9ecef;
            padding: 8px;
            border: 1px solid #dee2e6;
            font-weight: bold;
            font-size: 16pt;
        }
        
        QProgressBar {
            border: 1px solid #ced4da;
            border-radius: 4px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #007bff;
            border-radius: 3px;
        }
        """
        self.setStyleSheet(style)
