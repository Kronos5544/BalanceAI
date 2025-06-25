"""
BalanceAI - Aplicación para balanceo y evaluación de datasets
Autor: Marcos A. Rodríguez Guerra
Versión: 1.0
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from controllers.main_controller import MainController

def main():
    # Crear la aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("BalanceAI")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Universidad de Camagüey")
    
    # Configurar el icono de la aplicación
    if os.path.exists("resources/logo.png"):
        app.setWindowIcon(QIcon("resources/logo.png"))
    
    # Configurar el estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar el controlador principal
    controller = MainController()
    controller.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
