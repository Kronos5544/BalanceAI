"""
Ventana principal de la aplicación BalanceAI
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                            QWidget, QMenuBar, QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from views.summary_tab import SummaryTab
from views.balancing_tab import BalancingTab
from views.classification_tab import ClassificationTab
from views.about_tab import AboutTab
from views.help_tab import HelpTab

class MainWindow(QMainWindow):
    # Señales
    dataset_load_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("BalanceAI - Balanceo y Evaluación de Datasets")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Configurar ventana para pantalla completa
        self.setMinimumSize(800, 600)  # Tamaño mínimo más pequeño
        self.showMaximized()  # Iniciar maximizada
        
        # Configurar icono
        try:
            icon = QIcon("resources/logo.png")
            self.setWindowIcon(icon)
        except:
            pass
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)  # Márgenes más pequeños
        layout.setSpacing(0)
        
        # Crear pestañas
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Crear las pestañas
        self.summary_tab = SummaryTab()
        self.balancing_tab = BalancingTab()
        self.classification_tab = ClassificationTab()
        self.about_tab = AboutTab()
        self.help_tab = HelpTab()
        
        # Agregar pestañas
        self.tab_widget.addTab(self.summary_tab, "Resumen")
        self.tab_widget.addTab(self.balancing_tab, "Balanceo")
        self.tab_widget.addTab(self.classification_tab, "Clasificación")
        self.tab_widget.addTab(self.about_tab, "Acerca de")
        self.tab_widget.addTab(self.help_tab, "Ayuda")
        
        # Inicialmente deshabilitar pestañas excepto Resumen y Acerca de
        self.set_tabs_enabled(False)
        
        layout.addWidget(self.tab_widget)
        
        # Crear barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo - Cargue una base de conocimientos para comenzar")
        
        # Aplicar estilos
        self.apply_styles()
    
    def apply_styles(self):
        """Aplica estilos CSS a la ventana"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
            margin: 0px;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #e1e1e1;
            border: 1px solid #c0c0c0;
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 80px;
            font-size: 13pt;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        
        QTabBar::tab:disabled {
            background-color: #d0d0d0;
            color: #808080;
        }
        
        QStatusBar {
            background-color: #e1e1e1;
            border-top: 1px solid #c0c0c0;
            padding: 5px;
        }
        """
        self.setStyleSheet(style)
    
    def set_tabs_enabled(self, enabled: bool, exclude_about: bool = True):
        """Habilita o deshabilita las pestañas"""
        self.tab_widget.setTabEnabled(1, enabled)  # Balanceo
        self.tab_widget.setTabEnabled(2, enabled)  # Clasificación
        # La pestaña "Acerca de" siempre está habilitada
    
    def show_message(self, title: str, message: str, msg_type: str = "information"):
        """Muestra un mensaje al usuario"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "question":
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            return msg_box.exec() == QMessageBox.StandardButton.Yes
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        msg_box.exec()
        return True
    
    def update_status(self, message: str):
        """Actualiza la barra de estado"""
        self.status_bar.showMessage(message)
    
    def get_summary_tab(self):
        return self.summary_tab
    
    def get_balancing_tab(self):
        return self.balancing_tab
    
    def get_classification_tab(self):
        return self.classification_tab
