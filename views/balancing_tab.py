"""
Pestaña de Balanceo - Selección y ejecución de algoritmos de balanceo
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QFrame, QFileDialog, QProgressBar,
                            QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BalancingWorker(QThread):
    """Worker thread para ejecutar algoritmos de balanceo"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, balancing_service, dataset, selected_algorithms):
        super().__init__()
        self.balancing_service = balancing_service
        self.dataset = dataset
        self.selected_algorithms = selected_algorithms
    
    def run(self):
        try:
            results = self.balancing_service.run_balancing_algorithms(
                self.dataset, self.selected_algorithms
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class BalancingTab(QWidget):
    # Señales
    algorithms_selected = pyqtSignal(list)
    export_dataset_requested = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.dataset_model = None
        self.algorithm_model = None
        self.balancing_service = None
        self.selected_algorithms = []
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Sección de controles
        self.create_controls_section(layout)
        
        # Sección de visualización
        self.create_visualization_section(layout)
        
        # Sección de información
        self.create_info_section(layout)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_controls_section(self, layout):
        """Crea la sección de controles"""
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Primera fila de controles
        first_row = QHBoxLayout()
        
        # Selección de base de conocimientos
        message = QLabel("Base de conocimientos")
        message.setStyleSheet("font-size: 14pt")
        first_row.addWidget(message)
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(200)
        self.dataset_combo.currentTextChanged.connect(self.on_dataset_changed)
        first_row.addWidget(self.dataset_combo)
        
        first_row.addStretch()
        
        # Botón de exportar
        self.export_button = QPushButton("Exportar Base de Conocimientos")
        self.export_button.clicked.connect(self.export_dataset)
        self.export_button.setEnabled(False)
        first_row.addWidget(self.export_button)
        
        controls_layout.addLayout(first_row)
        
        # Segunda fila de controles
        second_row = QHBoxLayout()
        
        # Botón de seleccionar algoritmos
        self.select_algorithms_button = QPushButton("Seleccionar Algoritmos de Balanceo")
        self.select_algorithms_button.clicked.connect(self.select_algorithms)
        second_row.addWidget(self.select_algorithms_button)
        
        second_row.addStretch()
        
        controls_layout.addLayout(second_row)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        controls_layout.addWidget(self.progress_bar)
        
        layout.addWidget(controls_frame)
    
    def create_visualization_section(self, layout):
        """Crea la sección de visualización"""
        viz_frame = QFrame()
        viz_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        viz_layout = QVBoxLayout(viz_frame)
        viz_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title = QLabel("Distribución de Clases")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        viz_layout.addWidget(title)
        
        # Gráfico con tamaño fijo mínimo
        self.figure = Figure(figsize=(12, 6), dpi=80)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(300)
        
        # Configurar política de tamaño correctamente para PyQt6
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.setSizePolicy(size_policy)
        
        viz_layout.addWidget(self.canvas)
        
        layout.addWidget(viz_frame, 1)  # Dar peso 1 para que se expanda
    
    def create_info_section(self, layout):
        """Crea la sección de información"""
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        
        self.info_label = QLabel("Seleccione una base de conocimientos para ver detalles")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        layout.addWidget(info_frame)
    
    def set_models(self, dataset_model, algorithm_model, balancing_service):
        """Configura los modelos y servicios"""
        self.dataset_model = dataset_model
        self.algorithm_model = algorithm_model
        self.balancing_service = balancing_service
        self.update_dataset_combo()
    
    def update_dataset_combo(self):
        """Actualiza el combo de datasets"""
        if not self.dataset_model:
            return
        
        self.dataset_combo.clear()
        datasets = self.dataset_model.get_available_datasets()
        self.dataset_combo.addItems(datasets)
        
        if datasets:
            self.export_button.setEnabled(True)
            self.update_visualization()
    
    def on_dataset_changed(self):
        """Maneja el cambio de dataset seleccionado"""
        self.update_visualization()
        self.update_info()
    
    def update_visualization(self):
        """Actualiza la visualización del gráfico"""
        if not self.dataset_model:
            return
        
        current_dataset = self.dataset_combo.currentText()
        if not current_dataset:
            return
        
        # Obtener distribución de clases
        distribution = self.dataset_model.get_class_distribution(current_dataset)
        
        if not distribution:
            return
        
        # Limpiar figura completamente
        self.figure.clear()
        
        # Crear subplot con márgenes apropiados
        ax = self.figure.add_subplot(111)
        
        # Crear gráfico de barras
        classes = list(distribution.keys())
        counts = list(distribution.values())
        colors = ['#3498db', '#e74c3c']
        
        bars = ax.bar(classes, counts, color=colors[:len(classes)], width=0.6)
        
        # Configurar ejes y título
        ax.set_xlabel('Clases de Clasificación', fontsize=10)
        ax.set_ylabel('Número de Instancias', fontsize=10)
        ax.set_title(f'Distribución de Clases - {current_dataset}', fontsize=12, pad=20)
        
        # Agregar valores en las barras
        max_count = max(counts) if counts else 1
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max_count*0.02,
               f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Ajustar límites del eje Y para dar espacio a las etiquetas
        ax.set_ylim(0, max_count * 1.15)
        
        # Mejorar el layout
        self.figure.tight_layout(pad=2.0)
        
        # Redibujar
        self.canvas.draw()
    
    def update_info(self):
        """Actualiza la información mostrada"""
        if not self.dataset_model:
            return
        
        current_dataset = self.dataset_combo.currentText()
        if not current_dataset:
            return
        
        distribution = self.dataset_model.get_class_distribution(current_dataset)
        
        if not distribution:
            return
        
        # Calcular instancias generadas para la clase minoritaria
        if current_dataset != 'Original':
            original_dist = self.dataset_model.get_class_distribution('Original')
            if original_dist:
                minority_class = min(original_dist.keys(), key=original_dist.get)
                original_count = original_dist[minority_class]
                current_count = distribution.get(minority_class, 0)
                generated = current_count - original_count
                
                self.info_label.setText(
                    f"Instancias de clase '{minority_class}' generadas: {generated}"
                )
            else:
                self.info_label.setText("Información no disponible")
        else:
            self.info_label.setText("Dataset original - No se han generado instancias sintéticas")
        self.info_label.setStyleSheet("font-size: 15pt")
    
    def select_algorithms(self):
        """Abre el diálogo de selección de algoritmos"""
        if not self.algorithm_model:
            return
        
        from views.algorithm_selection_dialog import AlgorithmSelectionDialog
        
        dialog = AlgorithmSelectionDialog(
            self.algorithm_model.get_balancing_algorithms(),
            self.selected_algorithms,
            "Seleccionar Algoritmos de Balanceo",
            self
        )
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.selected_algorithms = dialog.get_selected_algorithms()
            if self.selected_algorithms:
                self.run_balancing()
    
    def run_balancing(self):
        """Ejecuta los algoritmos de balanceo seleccionados"""
        if not self.dataset_model or not self.selected_algorithms:
            return
        
        original_dataset = self.dataset_model.get_dataset('Original')
        if original_dataset is None:
            return
        
        # Mostrar progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.select_algorithms_button.setEnabled(False)
        
        # Ejecutar en hilo separado
        self.worker = BalancingWorker(
            self.balancing_service, 
            original_dataset, 
            self.selected_algorithms
        )
        self.worker.finished.connect(self.on_balancing_finished)
        self.worker.error.connect(self.on_balancing_error)
        self.worker.start()
    
    @pyqtSlot(dict)
    def on_balancing_finished(self, results):
        """Maneja la finalización del balanceo"""
        # Agregar datasets balanceados al modelo
        for algorithm_name, balanced_dataset in results.items():
            self.dataset_model.add_balanced_dataset(algorithm_name, balanced_dataset)
        
        # Actualizar interfaz
        self.update_dataset_combo()
        self.progress_bar.setVisible(False)
        self.select_algorithms_button.setEnabled(True)
        
        # Emitir señal
        self.algorithms_selected.emit(list(results.keys()))
    
    @pyqtSlot(str)
    def on_balancing_error(self, error_message):
        """Maneja errores en el balanceo"""
        self.progress_bar.setVisible(False)
        self.select_algorithms_button.setEnabled(True)
        # Aquí se podría mostrar un mensaje de error
        print(f"Error en balanceo: {error_message}")
    
    def export_dataset(self):
        """Exporta el dataset seleccionado"""
        current_dataset = self.dataset_combo.currentText()
        if not current_dataset or not self.dataset_model:
            return
        
        # Generar nombre por defecto
        base_name = self.dataset_model.dataset_name
        if current_dataset != 'Original':
            default_name = f"{base_name}_{current_dataset}.csv"
        else:
            default_name = f"{base_name}_original.csv"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Base de Conocimientos",
            default_name,
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        
        if file_path:
            success, message = self.dataset_model.export_dataset(current_dataset, file_path)
            # Aquí se podría mostrar un mensaje de éxito/error
            print(f"Exportación: {message}")
    
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
            font-size: 14pt;
        }
        
        Qlabel {
            font-size: 15pt;        
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
            padding: 10px;
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
