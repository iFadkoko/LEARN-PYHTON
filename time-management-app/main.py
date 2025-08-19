import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from main_window import MainWindow
from styles import get_stylesheet


def main():
    """
    Fungsi utama untuk menjalankan aplikasi
    """
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Time Management App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("MyCompany")
    
    # Terapkan stylesheet global
    app.setStyleSheet(get_stylesheet())
    
    # 🎨 Definisi warna (biar mudah dipakai ulang)
    bg_light = QColor(236, 240, 241)
    text_primary = QColor(44, 62, 80)
    accent = QColor(52, 152, 219)
    white = QColor(255, 255, 255)
    
    # Buat palette konsisten
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, bg_light)  
    palette.setColor(QPalette.ColorRole.WindowText, text_primary)  
    palette.setColor(QPalette.ColorRole.Base, white)
    palette.setColor(QPalette.ColorRole.AlternateBase, bg_light)  
    palette.setColor(QPalette.ColorRole.ToolTipBase, text_primary)  
    palette.setColor(QPalette.ColorRole.ToolTipText, bg_light)  
    palette.setColor(QPalette.ColorRole.Text, text_primary)  
    palette.setColor(QPalette.ColorRole.Button, accent)  
    palette.setColor(QPalette.ColorRole.ButtonText, white)
    palette.setColor(QPalette.ColorRole.BrightText, white)
    palette.setColor(QPalette.ColorRole.Highlight, accent)  
    palette.setColor(QPalette.ColorRole.HighlightedText, white)
    
    app.setPalette(palette)
    
    # Tampilkan main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
