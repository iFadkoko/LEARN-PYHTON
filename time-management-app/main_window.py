import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
    QSystemTrayIcon, QMenu, QMessageBox, QStatusBar, QApplication
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

from focus_mode import FocusModeWidget
from calendar_widget import CalendarWidget
from styles import get_stylesheet, get_dark_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._is_dark_mode = False   # state awal dark mode
        self._force_exit = False     # flag untuk keluar beneran
        self.init_ui()
        self.create_tray_icon()
        
    def init_ui(self):
        """Inisialisasi antarmuka pengguna"""
        self.setWindowTitle("Time Management App")
        self.setMinimumSize(1000, 700)
        
        # Set stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Add tabs
        self.focus_mode_tab = FocusModeWidget()
        self.calendar_tab = CalendarWidget()
        
        self.tab_widget.addTab(self.focus_mode_tab, "Focus Mode")
        self.tab_widget.addTab(self.calendar_tab, "Calendar")
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Setup menu
        self.create_menus()
        
    def create_menus(self):
        """Membuat menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        export_action = QAction("Export Schedule", self)
        export_action.triggered.connect(self.export_schedule)
        file_menu.addAction(export_action)
        
        backup_action = QAction("Backup Data", self)
        backup_action.triggered.connect(self.backup_data)
        file_menu.addAction(backup_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        dark_mode_action = QAction("Toggle Dark Mode", self)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(dark_mode_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_tray_icon(self):
        """Membuat system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # pastikan ada file icon
        
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.showNormal)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Double click tray icon untuk show
        self.tray_icon.activated.connect(self.on_tray_activated)
        
    def on_tray_activated(self, reason):
        """Double click tray icon untuk restore window"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
        
    def export_schedule(self):
        """Handler untuk export schedule"""
        self.status_bar.showMessage("Exporting schedule...")
        
    def backup_data(self):
        """Handler untuk backup data"""
        self.status_bar.showMessage("Backing up data...")
        
    def toggle_dark_mode(self):
        """Handler untuk toggle dark mode"""
        self._is_dark_mode = not self._is_dark_mode
        
        if self._is_dark_mode:
            self.setStyleSheet(get_dark_stylesheet())
            self.status_bar.showMessage("Dark mode enabled")
        else:
            self.setStyleSheet(get_stylesheet())
            self.status_bar.showMessage("Light mode enabled")
        
    def show_about(self):
        """Menampilkan dialog about"""
        QMessageBox.about(self, "About Time Management App", 
                         "Aplikasi Manajemen Waktu\n"
                         "Versi 1.0.0\n\n"
                         "Aplikasi untuk membantu mengatur waktu dengan fitur "
                         "Focus Mode dan Kalender Bulanan.")
    
    def closeEvent(self, event):
        """Override close event untuk minimize ke tray"""
        if QSystemTrayIcon.isSystemTrayAvailable() and not self._force_exit:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Time Management App",
                "Aplikasi berjalan di background. Klik kanan tray icon untuk menampilkan/keluar.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            event.accept()

    def exit_app(self):
        """Keluar beneran"""
        self._force_exit = True
        self.tray_icon.hide()
        QApplication.quit()
