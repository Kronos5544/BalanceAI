"""
Diálogo para selección de algoritmos de balanceo, clasificación y métricas
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLineEdit, QListWidget, QListWidgetItem, QLabel,
                            QCheckBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from typing import Dict, List
from models.algorithm_model import AlgorithmInfo

class AlgorithmListItem(QFrame):
    """Widget personalizado para mostrar información de algoritmo"""
    
    def __init__(self, algorithm_info: AlgorithmInfo, is_selected: bool = False):
        super().__init__()
        self.algorithm_info = algorithm_info
        self._updating_checkbox = False  # Flag para evitar recursión
        self.init_ui(is_selected)
    
    def init_ui(self, is_selected: bool):
        """Inicializa la interfaz del item"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(is_selected)
        layout.addWidget(self.checkbox)
        
        # Información del algoritmo
        info_layout = QVBoxLayout()
        
        # Nombre
        name_label = QLabel(self.algorithm_info.name)
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(10)
        name_label.setFont(name_font)
        name_label.setStyleSheet("font-size: 16pt")
        
        # Descripción
        desc_label = QLabel(self.algorithm_info.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666666; font-size: 14pt;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout, 1)
        
        # Estilo del frame
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                margin: 2px;
            }
            QFrame:hover {
                background-color: #f8f9fa;
                border-color: #007bff;
            }
        """)
    
    def is_checked(self) -> bool:
        """Retorna si el item está seleccionado"""
        return self.checkbox.isChecked()
    
    def set_checked(self, checked: bool):
        """Establece el estado de selección sin disparar señales"""
        self._updating_checkbox = True
        self.checkbox.setChecked(checked)
        self._updating_checkbox = False

class AlgorithmSelectionDialog(QDialog):
    """Diálogo para seleccionar algoritmos"""
    
    def __init__(self, algorithms: Dict[str, AlgorithmInfo], 
                 selected_algorithms: List[str], title: str, parent=None):
        super().__init__(parent)
        self.algorithms = algorithms
        self.selected_algorithms = selected_algorithms.copy()
        self.algorithm_items = {}
        self._updating_select_all = False  # Flag para evitar recursión
        self.init_ui(title)
    
    def init_ui(self, title: str):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(700, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("font-size: 14pt;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Escriba para filtrar algoritmos por nombre...")
        self.search_input.textChanged.connect(self.filter_algorithms)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Checkbox "Seleccionar Todo"
        self.select_all_checkbox = QCheckBox("Seleccionar Todo")
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_changed)
        layout.addWidget(self.select_all_checkbox)
        
        # Lista de algoritmos
        self.create_algorithm_list(layout)
        
        # Botones
        self.create_buttons(layout)
        
        # Aplicar estilos
        self.apply_styles()
        
        # Actualizar estado inicial
        self.update_select_all_state()
    
    def create_algorithm_list(self, layout):
        """Crea la lista de algoritmos"""
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Widget contenedor
        self.list_widget = QFrame()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setSpacing(5)
        
        # Crear items para cada algoritmo
        for name, algorithm_info in self.algorithms.items():
            is_selected = name in self.selected_algorithms
            item = AlgorithmListItem(algorithm_info, is_selected)
            item.checkbox.stateChanged.connect(self.on_item_selection_changed)
            
            self.algorithm_items[name] = item
            self.list_layout.addWidget(item)
        
        self.list_layout.addStretch()
        scroll_area.setWidget(self.list_widget)
        layout.addWidget(scroll_area)
    
    def create_buttons(self, layout):
        """Crea los botones del diálogo"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Botón Cancelar
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        # Botón Aceptar
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.clicked.connect(self.accept)
        self.accept_button.setDefault(True)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.accept_button)
        
        layout.addLayout(button_layout)
    
    def filter_algorithms(self, text: str):
        """Filtra los algoritmos según el texto de búsqueda (solo por nombre)"""
        text = text.lower().strip()
        
        for name, item in self.algorithm_items.items():
            # Buscar solo en el nombre del algoritmo, no en la descripción
            matches = text in name.lower() if text else True
            item.setVisible(matches)
        
        # Actualizar estado del "Seleccionar Todo" después del filtrado
        self.update_select_all_state()
    
    def on_select_all_changed(self, state):
        """Maneja el cambio en "Seleccionar Todo" """
        if self._updating_select_all:
            return
        
        checked = state == Qt.CheckState.Checked.value
        
        # Actualizar solo los items visibles
        for item in self.algorithm_items.values():
            item.set_checked(checked)
    
    def on_item_selection_changed(self):
        """Maneja el cambio de selección de un item"""
        # Solo actualizar si no estamos en medio de una actualización masiva
        sender = self.sender()
        if hasattr(sender, 'parent') and hasattr(sender.parent(), '_updating_checkbox'):
            if sender.parent()._updating_checkbox:
                return
        
        self.update_select_all_state()
    
    def update_select_all_state(self):
        """Actualiza el estado del checkbox "Seleccionar Todo" """
        checked_count = sum(1 for item in self.algorithm_items.values() if item.is_checked())
        if checked_count == len(self.algorithm_items):
            self.select_all_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.select_all_checkbox.setCheckState(Qt.CheckState.Unchecked)

    
    def get_selected_algorithms(self) -> List[str]:
        """Retorna la lista de algoritmos seleccionados"""
        selected = []
        for name, item in self.algorithm_items.items():
            if item.is_checked():
                selected.append(name)
        return selected
    
    def apply_styles(self):
        """Aplica estilos CSS"""
        style = """
        QDialog {
            background-color: #f8f9fa;
        }
        
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
            font-size: 14pt;
        }
        
        QPushButton:hover {
            background-color: #0056b3;
        }
        
        QPushButton:pressed {
            background-color: #004085;
        }
        
        QPushButton#cancel_button {
            background-color: #6c757d;
        }
        
        QPushButton#cancel_button:hover {
            background-color: #545b62;
        }
        
        QLineEdit {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ced4da;
            background-color: white;
            font-size: 14pt;
        }
        
        QLineEdit:focus {
            border-color: #007bff;
        }
        
        QScrollArea {
            border: 1px solid #dee2e6;
            border-radius: 4px;
            background-color: white;
        }
        
        QCheckBox {
            font-weight: bold;
            spacing: 5px;
            font-size: 14pt;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 2px solid #ced4da;
            background-color: white;
            border-radius: 3px;
        }
        
        QCheckBox::indicator:checked {
            border: 2px solid #007bff;
            background-color: #007bff;
            border-radius: 3px;
        }
        
        QCheckBox::indicator:indeterminate {
            border: 2px solid #007bff;
            background-color: #007bff;
            border-radius: 3px;
        }
        """
        self.setStyleSheet(style)
        self.cancel_button.setObjectName("cancel_button")
