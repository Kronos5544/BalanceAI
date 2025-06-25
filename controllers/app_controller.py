"""
Controlador de aplicación para manejar configuración global y estado
"""

from PyQt6.QtCore import QObject, QSettings
from PyQt6.QtWidgets import QApplication
import os
import sys

class AppController(QObject):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Universidad de Camagüey", "BalanceAI")
        self.setup_application()
    
    def setup_application(self):
        """Configura la aplicación"""
        app = QApplication.instance()
        if app:
            # Configurar propiedades de la aplicación
            app.setApplicationName("BalanceAI")
            app.setApplicationVersion("1.0")
            app.setOrganizationName("Universidad de Camagüey")
            app.setOrganizationDomain("reduc.edu.cu")
            
            # Configurar estilo
            self.setup_application_style()
    
    def setup_application_style(self):
        """Configura el estilo global de la aplicación"""
        app = QApplication.instance()
        if app:
            # Aplicar estilo Fusion para mejor apariencia
            app.setStyle('Fusion')
            
            # Configurar paleta de colores profesional
            from PyQt6.QtGui import QPalette, QColor
            from PyQt6.QtCore import Qt
            
            palette = QPalette()
            
            # Colores base
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorRole.Link, QColor(0, 123, 255))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 123, 255))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            
            app.setPalette(palette)
    
    def save_window_geometry(self, window):
        """Guarda la geometría de la ventana"""
        self.settings.setValue("geometry", window.saveGeometry())
        self.settings.setValue("windowState", window.saveState())
    
    def restore_window_geometry(self, window):
        """Restaura la geometría de la ventana"""
        geometry = self.settings.value("geometry")
        if geometry:
            window.restoreGeometry(geometry)
        
        window_state = self.settings.value("windowState")
        if window_state:
            window.restoreState(window_state)
    
    def get_recent_files(self):
        """Obtiene la lista de archivos recientes"""
        return self.settings.value("recentFiles", [])
    
    def add_recent_file(self, file_path):
        """Agrega un archivo a la lista de recientes"""
        recent_files = self.get_recent_files()
        
        # Remover si ya existe
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Agregar al inicio
        recent_files.insert(0, file_path)
        
        # Mantener solo los últimos 10
        recent_files = recent_files[:10]
        
        self.settings.setValue("recentFiles", recent_files)
    
    def get_last_directory(self):
        """Obtiene el último directorio usado"""
        return self.settings.value("lastDirectory", os.path.expanduser("~"))
    
    def set_last_directory(self, directory):
        """Establece el último directorio usado"""
        self.settings.setValue("lastDirectory", directory)
    
    def cleanup(self):
        """Limpieza al cerrar la aplicación"""
        # Guardar configuraciones finales si es necesario
        pass
