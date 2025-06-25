"""
Pestaña de Ayuda - Manual de usuario
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QSpinBox, QPushButton, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QFont, QPixmap
import os

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_view = None
        self.pdf_document = None
        self.page_navigator = None
        self.current_page = 0
        self.total_pages = 0
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Intentar cargar el PDF
        self.load_pdf_content(layout)
    
    def load_pdf_content(self, layout):
        """Intenta cargar el contenido del PDF"""
        try:
            # Verificar si el archivo existe
            pdf_path = "resources/Manual_de_Usuario.pdf"
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")
            
            # Intentar importar las librerías necesarias
            from PyQt6.QtPdfWidgets import QPdfView
            from PyQt6.QtPdf import QPdfDocument
            
            # Crear los componentes PDF
            self.pdf_document = QPdfDocument(self)
            self.pdf_view = QPdfView(self)
            
            # Cargar el documento
            self.pdf_document.load(pdf_path)
            
            # Configurar la vista PDF
            self.pdf_view.setDocument(self.pdf_document)
            self.page_navigator = self.pdf_view.pageNavigator()
            self.total_pages = self.pdf_document.pageCount()
            
            # Crear la interfaz con PDF
            self.create_pdf_interface(layout)
            
        except ImportError as e:
            # Error de importación de PyQt6 PDF
            self.create_error_interface(layout, 
                "Módulos PDF no disponibles",
                "Los módulos de PyQt6 para visualización de PDF no están instalados.\n"
                "Para instalar el soporte PDF, ejecute:\n"
                "pip install PyQt6-PDF\n\n"
                f"Error técnico: {str(e)}")
            
        except FileNotFoundError as e:
            # Archivo no encontrado
            self.create_error_interface(layout,
                "Manual no encontrado", 
                f"No se pudo encontrar el manual de usuario.\n"
                f"Asegúrese de que el archivo 'Manual_de_Usuario.pdf' "
                f"esté en la carpeta 'resources'.\n\n"
                f"Error: {str(e)}")
            
        except Exception as e:
            # Otros errores
            self.create_error_interface(layout,
                "Error al cargar el manual",
                f"Ocurrió un error inesperado al cargar el manual de usuario.\n\n"
                f"Error técnico: {str(e)}")
    
    def create_pdf_interface(self, layout):
        """Crea la interfaz cuando el PDF se carga correctamente"""
        # Barra de navegación
        nav_frame = QFrame()
        nav_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(10, 5, 10, 5)
        
        # Botón página anterior
        self.prev_button = QPushButton("◀ Anterior")
        self.prev_button.clicked.connect(self.previous_page)
        nav_layout.addWidget(self.prev_button)
        
        # Selector de página
        nav_layout.addWidget(QLabel("Página:"))
        self.page_selector = QSpinBox()
        self.page_selector.setMinimum(1)
        self.page_selector.setMaximum(self.total_pages)
        self.page_selector.setValue(1)
        self.page_selector.valueChanged.connect(self.page_selected)
        nav_layout.addWidget(self.page_selector)
        
        # Label total de páginas
        self.total_pages_label = QLabel(f"de {self.total_pages}")
        nav_layout.addWidget(self.total_pages_label)
        
        nav_layout.addStretch()
        
        # Botón página siguiente
        self.next_button = QPushButton("Siguiente ▶")
        self.next_button.clicked.connect(self.next_page)
        nav_layout.addWidget(self.next_button)
        
        layout.addWidget(nav_frame)

        # Botón zoom
        self.zoom_fit_button = QPushButton("Ajustar a ventana")
        self.zoom_fit_button.clicked.connect(self.zoom_to_fit)
        nav_layout.addWidget(self.zoom_fit_button)
        
        # Vista del PDF
        self.pdf_view.setMinimumHeight(400)
        layout.addWidget(self.pdf_view, 1)  # Dar peso 1 para que se expanda
        
        # Conectar señales
        if self.page_navigator:
            self.page_navigator.currentPageChanged.connect(self.on_page_changed)
        
        # Configurar página inicial
        self.current_page = 0
        self.update_navigation_buttons()
        
        # Aplicar estilos
        self.apply_pdf_styles()
    
    def create_error_interface(self, layout, title, message):
        """Crea la interfaz cuando hay un error"""
        # Frame principal de error
        error_frame = QFrame()
        error_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        error_layout = QVBoxLayout(error_frame)
        error_layout.setSpacing(20)
        error_layout.setContentsMargins(40, 40, 40, 40)
        
        # Icono de error
        icon_label = QLabel("⚠️")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        error_layout.addWidget(icon_label)
        
        # Título del error
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #d32f2f;")
        error_layout.addWidget(title_label)
        
        # Mensaje de error
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("color: #666666; line-height: 1.5;")
        error_layout.addWidget(message_label)
        
        # Información alternativa
        alt_info = QLabel(
            "Mientras tanto, puede consultar la documentación en línea o "
            "contactar al desarrollador para obtener ayuda."
        )
        alt_info.setWordWrap(True)
        alt_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alt_info.setStyleSheet("color: #888888; font-style: italic;")
        error_layout.addWidget(alt_info)
        
        error_layout.addStretch()
        
        # Aplicar estilo al frame de error
        error_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 2px dashed #cccccc;
                border-radius: 8px;
            }
        """)
        
        layout.addWidget(error_frame)
    
    def page_selected(self, page_number):
        """Maneja la selección de página desde el SpinBox"""
        if self.page_navigator and self.pdf_document:
            # SpinBox usa base 1, navigator usa base 0
            target_page = page_number - 1
            if 0 <= target_page < self.total_pages:
                self.navigate_to_page(target_page)
    
    def navigate_to_page(self, page_number):
        """Navega a una página específica usando la signatura correcta"""
        if self.page_navigator:
            try:
                # Usar la signatura correcta: jump(page: int, location: QPointF, zoom: float = 0)
                location = QPointF(0, 0)  # Esquina superior izquierda
                self.page_navigator.jump(page_number, location, 0.0)
            except Exception as e:
                print(f"Error navegando a página {page_number}: {e}")
                # Método alternativo: establecer la página directamente
                try:
                    # Intentar usar currentPage como propiedad
                    if hasattr(self.page_navigator, 'currentPage'):
                        # Esto podría no funcionar si es solo lectura, pero vale la pena intentar
                        pass
                except:
                    pass
    
    def on_page_changed(self, page_number):
        """Maneja el cambio de página desde el navegador"""
        self.current_page = page_number
        
        # Actualizar SpinBox sin disparar señales
        if self.page_selector:
            self.page_selector.blockSignals(True)
            self.page_selector.setValue(page_number + 1)  # SpinBox usa base 1
            self.page_selector.blockSignals(False)
        
        self.update_navigation_buttons()
    
    def previous_page(self):
        """Va a la página anterior"""
        if self.page_navigator and self.current_page > 0:
            target_page = self.current_page - 1
            self.navigate_to_page(target_page)
    
    def next_page(self):
        """Va a la página siguiente"""
        if self.page_navigator and self.current_page < self.total_pages - 1:
            target_page = self.current_page + 1
            self.navigate_to_page(target_page)
    
    def zoom_to_fit(self):
        """Ajusta el zoom para que la página se ajuste a la ventana"""
        if self.pdf_view:
            try:
                # Intentar diferentes modos de zoom según la versión de PyQt6
                if hasattr(self.pdf_view, 'setZoomMode'):
                    # Verificar si ZoomMode existe y tiene FitToWidth
                    zoom_mode = getattr(self.pdf_view, 'ZoomMode', None)
                    if zoom_mode and hasattr(zoom_mode, 'FitToWidth'):
                        self.pdf_view.setZoomMode(zoom_mode.FitToWidth)
                    elif zoom_mode and hasattr(zoom_mode, 'FitInView'):
                        self.pdf_view.setZoomMode(zoom_mode.FitInView)
                elif hasattr(self.pdf_view, 'fitToWidth'):
                    self.pdf_view.fitToWidth()
                elif hasattr(self.pdf_view, 'fitInView'):
                    self.pdf_view.fitInView()
                else:
                    # Fallback: ajustar zoom manualmente
                    if hasattr(self.pdf_view, 'setZoomFactor'):
                        self.pdf_view.setZoomFactor(1.0)
                    print("Métodos de zoom no disponibles")
            except Exception as e:
                print(f"Error ajustando zoom: {e}")
    
    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación"""
        if hasattr(self, 'prev_button') and hasattr(self, 'next_button'):
            # Usar lógica simple basada en el número de página actual
            self.prev_button.setEnabled(self.current_page > 0)
            self.next_button.setEnabled(self.current_page < self.total_pages - 1)
    
    def apply_pdf_styles(self):
        """Aplica estilos CSS para la interfaz PDF"""
        style = """
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
            font-size:13pt
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
        
        QSpinBox {
            padding: 4px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            background-color: white;
            min-width: 60px;
        }
        
        QSpinBox:focus {
            border-color: #007bff;
        }
        
        QLabel {
            color: #333333;
            font-size: 13pt;
        }
        """
        self.setStyleSheet(style)
    
    def resizeEvent(self, event):
        """Maneja el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        # Ajustar zoom cuando cambia el tamaño si el PDF está cargado
        if self.pdf_view and hasattr(self, 'zoom_fit_button'):
            # Pequeño delay para que el resize se complete
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(100, self.zoom_to_fit)
