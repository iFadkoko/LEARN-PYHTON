from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QSpinBox, QGroupBox, QProgressBar,
    QGridLayout, QComboBox
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class FocusModeWidget(QWidget):
    session_completed = pyqtSignal(int)  # Signal ketika sesi selesai
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_timer()
        
    def init_ui(self):
        """Inisialisasi UI untuk focus mode"""
        layout = QVBoxLayout(self)
        
        # Timer display
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        layout.addWidget(self.timer_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        layout.addWidget(self.progress_bar)
        
        # Controls group
        controls_group = QGroupBox("Session Controls")
        controls_layout = QGridLayout(controls_group)
        
        # Work time setting
        controls_layout.addWidget(QLabel("Work Time (min):"), 0, 0)
        self.work_time_spin = QSpinBox()
        self.work_time_spin.setRange(1, 60)
        self.work_time_spin.setValue(25)
        controls_layout.addWidget(self.work_time_spin, 0, 1)
        
        # Break time setting
        controls_layout.addWidget(QLabel("Break Time (min):"), 1, 0)
        self.break_time_spin = QSpinBox()
        self.break_time_spin.setRange(1, 30)
        self.break_time_spin.setValue(5)
        controls_layout.addWidget(self.break_time_spin, 1, 1)
        
        # Session type
        controls_layout.addWidget(QLabel("Session Type:"), 2, 0)
        self.session_type_combo = QComboBox()
        self.session_type_combo.addItems(["Work", "Break"])
        controls_layout.addWidget(self.session_type_combo, 2, 1)
        
        layout.addWidget(controls_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        buttons_layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)
        buttons_layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        buttons_layout.addWidget(self.reset_button)
        
        layout.addLayout(buttons_layout)
        
        # Statistics
        stats_group = QGroupBox("Today's Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.sessions_label = QLabel("Sessions Completed: 0")
        stats_layout.addWidget(self.sessions_label)
        
        self.total_time_label = QLabel("Total Focus Time: 0 min")
        stats_layout.addWidget(self.total_time_label)
        
        layout.addWidget(stats_group)
        
        layout.addStretch()
        
    def init_timer(self):
        """Inisialisasi timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.is_running = False
        self.is_work_session = True
        self.remaining_seconds = 25 * 60  # Default 25 minutes
        self.total_sessions = 0
        self.total_focus_time = 0  # in minutes
        
    def start_timer(self):
        """Memulai timer"""
        if not self.is_running:
            # Set session time based on type
            if self.session_type_combo.currentText() == "Work":
                self.is_work_session = True
                self.remaining_seconds = self.work_time_spin.value() * 60
            else:
                self.is_work_session = False
                self.remaining_seconds = self.break_time_spin.value() * 60
                
            self.update_display()
            
            self.timer.start(1000)  # Update every second
            self.is_running = True
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            
    def pause_timer(self):
        """Menjeda timer"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            
    def reset_timer(self):
        """Mengatur ulang timer"""
        self.timer.stop()
        self.is_running = False
        
        if self.is_work_session:
            self.remaining_seconds = self.work_time_spin.value() * 60
        else:
            self.remaining_seconds = self.break_time_spin.value() * 60
            
        self.update_display()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        
    def update_timer(self):
        """Update timer setiap detik"""
        self.remaining_seconds -= 1
        
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.is_running = False
            self.session_completed.emit(
                self.work_time_spin.value() if self.is_work_session else 0
            )
            
            # Update statistics if it was a work session
            if self.is_work_session:
                self.total_sessions += 1
                self.total_focus_time += self.work_time_spin.value()
                self.sessions_label.setText(f"Sessions Completed: {self.total_sessions}")
                self.total_time_label.setText(f"Total Focus Time: {self.total_focus_time} min")
            
            # Toggle session type for next run
            self.is_work_session = not self.is_work_session
            self.session_type_combo.setCurrentText("Break" if self.is_work_session else "Work")
            
            # Show notification (would need platform-specific code for proper notifications)
            self.show_notification()
            
            # Reset timer for next session
            self.reset_timer()
            
        self.update_display()
        
    def update_display(self):
        """Update tampilan timer"""
        # PERBAIKAN: Baris ini sebelumnya berada di luar method
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
        
        # Update progress bar dengan warna berbeda berdasarkan session type
        total_seconds = (
            self.work_time_spin.value() * 60 if self.is_work_session 
            else self.break_time_spin.value() * 60
        )
        progress = int((total_seconds - self.remaining_seconds) / total_seconds * 100)
        self.progress_bar.setValue(progress)
        
        # Ubah warna progress bar berdasarkan jenis sesi
        if self.is_work_session:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #bdc3c7;
                    border-radius: 6px;
                    text-align: center;
                    background: white;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    border-radius: 4px;
                }
            """)
        else:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #bdc3c7;
                    border-radius: 6px;
                    text-align: center;
                    background: white;
                }
                QProgressBar::chunk {
                    background-color: #2ecc71;
                    border-radius: 4px;
                }
            """)
        
    def show_notification(self):
        """Menampilkan notifikasi (placeholder)"""
        # Implementasi notifikasi yang sesungguhnya akan membutuhkan
        # platform-specific code atau library pihak ketiga
        message = "Work session completed! Time for a break." if self.is_work_session else "Break is over! Time to focus."
        self.timer_label.setText(message)