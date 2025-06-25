"""
Pestaña de Resumen - Carga y análisis inicial de datasets
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QFrame, QScrollArea, QGridLayout, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

class SummaryTab(QWidget):
    # Señales
    load_dataset_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.dataset_loaded = False
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título con logo
        self.create_header(layout)
        
        # Botón de carga
        self.create_load_section(layout)
        
        # Área de contenido (inicialmente muestra instrucciones)
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Widget de contenido inicial
        self.show_initial_content()
        
        layout.addWidget(self.content_area)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_header(self, layout):
        """Crea el encabezado con logo y título"""
        header_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap("resources/logo.png")
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
        except:
            pass
        
        # Título
        title_label = QLabel("BalanceAI")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
    
    def create_load_section(self, layout):
        """Crea la sección de carga de dataset"""
        load_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Cargar Nueva Base de Conocimientos")
        self.load_button.setMinimumHeight(40)
        self.load_button.clicked.connect(self.load_dataset)
        
        load_layout.addWidget(self.load_button)
        load_layout.addStretch()
        
        layout.addLayout(load_layout)
    
    def show_initial_content(self):
        """Muestra el contenido inicial con instrucciones"""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Mensaje principal
        main_message = QLabel("No se ha cargado ninguna base de conocimientos.")
        main_font = QFont()
        main_font.setPointSize(14)
        main_font.setBold(True)
        main_message.setStyleSheet("font-size: 18pt")
        main_message.setFont(main_font)
        
        instruction_message = QLabel(
            "Por favor, cargue un archivo antes de continuar y asegúrese de que "
            "cumple con los siguientes requisitos:"
        )
        instruction_message.setWordWrap(True)
        instruction_message.setStyleSheet("font-size: 15pt")
        
        # Lista de requisitos
        requirements = [
            "• El archivo debe estar en formato CSV.",
            "• Todos los atributos deben ser numéricos y continuos.",
            "• La clase a clasificar debe ubicarse como el último atributo.",
            "• La clase de salida debe ser binaria, es decir, debe contener exactamente dos posibles valores."
        ]
        
        layout.addWidget(main_message)
        layout.addWidget(instruction_message)
        
        for req in requirements:
            req_label = QLabel(req)
            req_label.setWordWrap(True)
            req_label.setStyleSheet("font-size: 15pt")
            layout.addWidget(req_label)
        
        # Ejemplo
        example_label = QLabel("\nEjemplo de formato válido:")
        example_font = QFont()
        example_font.setBold(True)
        example_label.setStyleSheet("font-size: 15pt")
        example_label.setFont(example_font)
        
        example_text = QLabel(
            "attr1, attr2, attr3, class\n"
            "5, 4, 1, positive\n"
            "2, 1, 3, negative"
        )
        example_text.setStyleSheet("background-color: #f0f0f0; padding: 10px; font-family: monospace; font-size: 15pt")
        
        layout.addWidget(example_label)
        layout.addWidget(example_text)
        layout.addStretch()
        
        self.content_area.setWidget(content_widget)
    
    def show_dataset_summary(self, summary_data):
        """Muestra el resumen del dataset cargado"""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("Resumen de la Base de Conocimientos")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("font-size: 18pt")
        layout.addWidget(title)
        
        # Grid con información
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QGridLayout(info_frame)
        info_layout.setSpacing(10)
        
        # Información del dataset
        info_items = [
            ("Nombre de la base de conocimientos:", summary_data.get('name', 'N/A')),
            ("Número de atributos:", str(summary_data.get('num_attributes', 0))),
            ("Clases de clasificación:", ", ".join(summary_data.get('classes', []))),
            ("Instancias totales:", str(summary_data.get('total_instances', 0))),
            ("Valores faltantes:", str(summary_data.get('missing_values', 0))),
            ("Nivel de desbalance:", str(summary_data.get('imbalance_ratio', 0.0)))
        ]
        
        # Agregar conteos de clases
        class_counts = summary_data.get('class_counts', {})
        for class_name, count in class_counts.items():
            info_items.append((f"Instancias de clase '{class_name}':", str(count)))
        
        row = 0
        for label_text, value_text in info_items:
            label = QLabel(label_text)
            label_font = QFont()
            label_font.setBold(True)
            label.setFont(label_font)
            
            value = QLabel(value_text)

            label.setStyleSheet("font-size: 15pt")
            value.setStyleSheet("font-size: 15pt")
            
            info_layout.addWidget(label, row, 0)
            info_layout.addWidget(value, row, 1)
            row += 1
        
        layout.addWidget(info_frame)
        
        # Mensaje de desbalance si aplica
        if summary_data.get('is_balanced', False):
            warning_label = QLabel(
                "⚠️ La base de conocimientos presenta un nivel de desbalance inferior a 1.5, "
                "por lo que se considera balanceada. El módulo de balanceo estará deshabilitado."
            )
            warning_label.setWordWrap(True)
            warning_label.setStyleSheet("color: orange; background-color: #fff3cd; padding: 10px; border-radius: 4px; font-size: 15pt;")
            layout.addWidget(warning_label)
        
        layout.addStretch()
        self.content_area.setWidget(content_widget)
        self.dataset_loaded = True
    
    def load_dataset(self):
        """Abre el diálogo para cargar dataset"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Base de Conocimientos",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        
        if file_path:
            self.load_dataset_requested.emit(file_path)
    
    def apply_styles(self):
        """Aplica estilos CSS"""
        style = """
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 14pt;
        }
        
        QPushButton:hover {
            background-color: #0056b3;
        }
        
        QPushButton:pressed {
            background-color: #004085;
        }
        
        QFrame {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
        }
        
        QScrollArea {
            border: 1px solid #dee2e6;
            border-radius: 4px;
            background-color: white;
        }
        """
        self.setStyleSheet(style)
