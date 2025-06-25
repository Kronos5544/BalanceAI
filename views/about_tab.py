"""
Pestaña Acerca de - Información sobre la aplicación
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Widget de contenido
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        
        # Header con logo y título
        self.create_header(content_layout)
        
        # Información de la aplicación
        self.create_app_info(content_layout)
        
        # Información del autor
        self.create_author_info(content_layout)
        
        # Tecnologías utilizadas
        self.create_tech_info(content_layout)
        
        # Licencia
        self.create_license_info(content_layout)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_header(self, layout):
        """Crea el encabezado con logo y título"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_label = QLabel()
        try:
            pixmap = QPixmap("resources/logo.png")
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
        except:
            logo_label.setText("🔬")  # Emoji como fallback
            logo_label.setStyleSheet("font-size: 64px;")
        
        logo_layout.addWidget(logo_label)
        header_layout.addLayout(logo_layout)
        
        # Título
        title_label = QLabel("BalanceAI")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Balanceo y Evaluación de Datasets para Clasificación Binaria")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_font.setItalic(True)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666666;")
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
    
    def create_app_info(self, layout):
        """Crea la sección de información de la aplicación"""
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        
        # Título de sección
        section_title = QLabel("Información de la Aplicación")
        section_font = QFont()
        section_font.setPointSize(16)
        section_font.setBold(True)
        section_title.setFont(section_font)
        section_title.setStyleSheet("font-size: 17pt")
        info_layout.addWidget(section_title)
        
        # Información
        info_text = """
        <p><strong>Versión:</strong> 1.0</p>
        <p><strong>Objetivo:</strong> Automatizar el análisis, balanceo y evaluación de bases de conocimiento 
        para clasificación binaria, mejorando la eficiencia en la investigación de IA.</p>
        
        <p><strong>Funcionalidades principales:</strong></p>
        <ul>
            <li>Carga y análisis de bases de datos en formato CSV</li>
            <li>Detección automática de desbalance en los datos</li>
            <li>Aplicación de técnicas de balanceo avanzadas (SMOTE-EN, SMOTE-RL, SMOTE-COV-LW)</li>
            <li>Evaluación de algoritmos de clasificación binaria (C4.5, KNN, MLP, Random Forest, SVM)</li>
            <li>Cálculo de métricas de rendimiento (F1-Score, Precisión, AUC)</li>
            <li>Generación de informes detallados</li>
            <li>Exportación de bases balanceadas y resultados</li>
        </ul>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 15pt")
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_frame)
    
    def create_author_info(self, layout):
        """Crea la sección de información del autor"""
        author_frame = QFrame()
        author_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        author_layout = QVBoxLayout(author_frame)
        
        # Título de sección
        section_title = QLabel("Autor")
        section_font = QFont()
        section_font.setPointSize(16)
        section_font.setBold(True)
        section_title.setFont(section_font)
        section_title.setStyleSheet("font-size: 17pt")
        author_layout.addWidget(section_title)
        
        # Información del autor
        author_text = """
        <p><strong>Desarrollador:</strong> Marcos A. Rodríguez Guerra</p>
        <p><strong>Institución:</strong> Universidad de Camagüey "Ignacio Agramonte Loynaz"</p>
        <p><strong>Facultad:</strong> Ciencias Aplicadas</p>
        <p><strong>Carrera:</strong> Ingeniería en Ciencias Informáticas</p>
        <p><strong>Año:</strong> 2025</p>
        """
        
        author_label = QLabel(author_text)
        author_label.setWordWrap(True)
        author_label.setTextFormat(Qt.TextFormat.RichText)
        author_label.setStyleSheet("font-size: 15pt")
        author_layout.addWidget(author_label)
        
        layout.addWidget(author_frame)
    
    def create_tech_info(self, layout):
        """Crea la sección de tecnologías utilizadas"""
        tech_frame = QFrame()
        tech_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        tech_layout = QVBoxLayout(tech_frame)
        
        # Título de sección
        section_title = QLabel("Tecnologías Utilizadas")
        section_font = QFont()
        section_font.setPointSize(16)
        section_font.setBold(True)
        section_title.setFont(section_font)
        section_title.setStyleSheet("font-size: 17pt")
        tech_layout.addWidget(section_title)
        
        # Tecnologías
        tech_text = """
        <p><strong>Lenguaje de Programación:</strong> Python 3.11+</p>
        <p><strong>Interfaz Gráfica:</strong> PyQt6</p>
        <p><strong>Análisis de Datos:</strong> pandas, NumPy</p>
        <p><strong>Aprendizaje Automático:</strong> scikit-learn</p>
        <p><strong>Visualización:</strong> matplotlib</p>
        <p><strong>Procesamiento Paralelo:</strong> joblib</p>
        <p><strong>Algoritmos de Balanceo:</strong> Implementaciones personalizadas desarrolladas en la Universidad de Camagüey</p>
        
        <p><strong>Algoritmos de Balanceo Incluidos:</strong></p>
        <ul>
            <li><strong>SMOTE-COV-LW:</strong> SMOTE con covarianza regularizada por Ledoit-Wolf</li>
            <li><strong>SMOTE-RL:</strong> SMOTE con regresión Lasso</li>
            <li><strong>SMOTE-EN:</strong> SMOTE con regresión Elastic Net</li>
        </ul>
        """
        
        tech_label = QLabel(tech_text)
        tech_label.setWordWrap(True)
        tech_label.setTextFormat(Qt.TextFormat.RichText)
        tech_label.setStyleSheet("font-size: 15pt")
        tech_layout.addWidget(tech_label)
        
        layout.addWidget(tech_frame)
    
    def create_license_info(self, layout):
        """Crea la sección de licencia"""
        license_frame = QFrame()
        license_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        license_layout = QVBoxLayout(license_frame)
        
        # Título de sección
        section_title = QLabel("Licencia y Derechos de Uso")
        section_font = QFont()
        section_font.setPointSize(16)
        section_font.setBold(True)
        section_title.setFont(section_font)
        section_title.setStyleSheet("font-size: 17pt")
        license_layout.addWidget(section_title)
        
        # Información de licencia
        license_text = """
        <p>Este software ha sido desarrollado como parte de un proyecto de investigación en la 
        Universidad de Camagüey "Ignacio Agramonte Loynaz".</p>
        
        <p><strong>Uso Académico:</strong> Permitido para fines educativos y de investigación.</p>
        <p><strong>Distribución:</strong> Se permite la distribución con fines académicos citando apropiadamente la fuente.</p>
        <p><strong>Modificación:</strong> Las modificaciones están permitidas para uso académico.</p>
        
        <p><strong>Cita Sugerida:</strong><br>
        Rodríguez Guerra, M. A. (2025). BalanceAI: Herramienta para Balanceo y Evaluación de Datasets. 
        Universidad de Camagüey "Ignacio Agramonte Loynaz".</p>
        
        <p><em>Para uso comercial o distribución fuera del ámbito académico, contacte con el autor.</em></p>
        """
        
        license_label = QLabel(license_text)
        license_label.setWordWrap(True)
        license_label.setTextFormat(Qt.TextFormat.RichText)
        license_label.setStyleSheet("font-size: 15pt")
        license_layout.addWidget(license_label)
        
        layout.addWidget(license_frame)
    
    def apply_styles(self):
        """Aplica estilos CSS"""
        style = """
        QFrame {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QLabel {
            line-height: 1.5;
        }
        """
        self.setStyleSheet(style)
