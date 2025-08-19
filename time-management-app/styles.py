def get_stylesheet():
    """Mengembalikan stylesheet untuk aplikasi (light mode)"""
    return """
        QMainWindow, QWidget {
            background-color: #ecf0f1;
            color: #2c3e50;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
            background: white;
            border-radius: 6px;
            margin: 5px;
        }
        
        QTabBar::tab {
            background: #ecf0f1;
            color: #7f8c8d;
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
            font-weight: 500;
        }
        
        QTabBar::tab:selected {
            background: white;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            font-weight: 600;
        }
        
        QTabBar::tab:hover {
            background: #dfe6e9;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #2c3e50;
        }
        
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
        
        QGroupBox {
            font-weight: bold;
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background: white;
        }
        
        QSpinBox, QComboBox, QLineEdit, QTextEdit {
            padding: 8px;
            background-color: white;
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            selection-background-color: #3498db;
        }
        
        QSpinBox:focus, QComboBox:focus, QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #3498db;
        }
        
        QProgressBar {
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            text-align: center;
            background: white;
            color: #2c3e50;
            font-weight: 500;
        }
        
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 4px;
        }
        
        QLabel {
            color: #2c3e50;
        }
        
        QStatusBar {
            background-color: #34495e;
            color: white;
        }
        
        QMenuBar {
            background-color: #2c3e50;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #3498db;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #bdc3c7;
        }
        
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QDialog {
            background-color: white;
        }
        
        QCalendarWidget {
            background: white;
            border: 1px solid #bdc3c7;
            border-radius: 6px;
        }
    """


def get_dark_stylesheet():
    """Mengembalikan dark mode stylesheet"""
    return """
        QMainWindow, QWidget {
            background-color: #1a2530;
            color: #ecf0f1;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QTabWidget::pane {
            border: 1px solid #34495e;
            background: #2c3e50;
            border-radius: 6px;
            margin: 5px;
        }
        
        QTabBar::tab {
            background: #34495e;
            color: #bdc3c7;
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
            font-weight: 500;
        }
        
        QTabBar::tab:selected {
            background: #2c3e50;
            color: #ecf0f1;
            border-bottom: 3px solid #3498db;
            font-weight: 600;
        }
        
        QTabBar::tab:hover {
            background: #3d566e;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1c6ea4;
        }
        
        QPushButton:disabled {
            background-color: #415b76;
            color: #7f8c8d;
        }
        
        QGroupBox {
            font-weight: bold;
            color: #ecf0f1;
            border: 2px solid #34495e;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 15px;
            background: #2c3e50;
        }
        
        QSpinBox, QComboBox, QLineEdit, QTextEdit {
            padding: 8px;
            background-color: #34495e;
            color: #ecf0f1;
            border: 2px solid #34495e;
            border-radius: 6px;
            selection-background-color: #3498db;
        }
        
        QProgressBar {
            border: 2px solid #34495e;
            border-radius: 6px;
            text-align: center;
            background: #34495e;
            color: #ecf0f1;
            font-weight: 500;
        }
        
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 4px;
        }
        
        QLabel {
            color: #ecf0f1;
        }
        
        QStatusBar {
            background-color: #2c3e50;
            color: white;
        }
        
        QMenuBar {
            background-color: #1a2530;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #3498db;
        }
        
        QMenu {
            background-color: #2c3e50;
            border: 1px solid #34495e;
            color: #ecf0f1;
        }
        
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        QDialog {
            background-color: #2c3e50;
            color: #ecf0f1;
        }
        
        QCalendarWidget {
            background: #34495e;
            border: 1px solid #34495e;
            color: #ecf0f1;
            border-radius: 6px;
        }
    """
