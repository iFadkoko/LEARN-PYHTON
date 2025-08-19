from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QGridLayout, QComboBox, QLineEdit, 
    QDialog, QDialogButtonBox, QFormLayout, QTextEdit,
    QApplication, QSizePolicy
)
from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QColor

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = QDate.currentDate()
        self.init_ui()
        
    def init_ui(self):
        """Inisialisasi UI untuk kalender"""
        layout = QVBoxLayout(self)
        
        # Navigation
        nav_layout = QHBoxLayout()
        
        self.prev_month_btn = QPushButton("←")
        self.prev_month_btn.clicked.connect(self.previous_month)
        nav_layout.addWidget(self.prev_month_btn)
        
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        nav_layout.addWidget(self.month_label)
        
        self.next_month_btn = QPushButton("→")
        self.next_month_btn.clicked.connect(self.next_month)
        nav_layout.addWidget(self.next_month_btn)
        
        layout.addLayout(nav_layout)
        
        # Calendar grid
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(5)
        
        # Add day names
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-weight: bold; background-color: #f0f0f0;")
            self.calendar_grid.addWidget(label, 0, i)
        
        layout.addLayout(self.calendar_grid)
        
        # Schedule details
        self.schedule_detail = QTextEdit()
        self.schedule_detail.setReadOnly(True)
        layout.addWidget(self.schedule_detail)
        
        # Add event button
        self.add_event_btn = QPushButton("Add Event")
        self.add_event_btn.clicked.connect(self.show_add_event_dialog)
        layout.addWidget(self.add_event_btn)
        
        self.update_calendar()
        
    def update_calendar(self):
        """Memperbarui tampilan kalender"""
        # Clear previous days (skip day names)
        for i in range(self.calendar_grid.count() - 7, 0, -1):
            item = self.calendar_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                
        # Update month label
        self.month_label.setText(self.current_date.toString("MMMM yyyy"))
        
        # Get first day of month and number of days
        first_day = QDate(self.current_date.year(), self.current_date.month(), 1)
        days_in_month = first_day.daysInMonth()
        
        # Calculate starting position (Monday is day 1)
        start_day = first_day.dayOfWeek()
        if start_day == 7:  # Qt.Sunday is 7, but we want it to be 0 in our grid
            start_day = 0
        
        # Add days to grid
        row, col = 1, start_day
        for day in range(1, days_in_month + 1):
            day_widget = DayWidget(day)
            day_widget.clicked.connect(self.day_clicked)
            self.calendar_grid.addWidget(day_widget, row, col)
            
            col += 1
            if col > 6:  # Sunday
                col = 0
                row += 1
                
    def day_clicked(self, day):
        """Handler ketika hari diklik"""
        date = QDate(self.current_date.year(), self.current_date.month(), day)
        self.schedule_detail.setText(f"Schedule for {date.toString('dddd, MMMM d, yyyy')}\n\nNo events scheduled.")
        
    def previous_month(self):
        """Pergi ke bulan sebelumnya"""
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()
        
    def next_month(self):
        """Pergi ke bulan berikutnya"""
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()
        
    def show_add_event_dialog(self):
        """Menampilkan dialog untuk menambah event"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Event")
        
        layout = QFormLayout(dialog)
        
        date_edit = QLineEdit(self.current_date.toString("yyyy-MM-dd"))
        title_edit = QLineEdit()
        description_edit = QTextEdit()
        category_combo = QComboBox()
        category_combo.addItems(["Work", "Meeting", "Project", "Personal"])
        
        layout.addRow("Date:", date_edit)
        layout.addRow("Title:", title_edit)
        layout.addRow("Category:", category_combo)
        layout.addRow("Description:", description_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Save event to database (placeholder)
            self.schedule_detail.setText(
                f"Event added:\n"
                f"Date: {date_edit.text()}\n"
                f"Title: {title_edit.text()}\n"
                f"Category: {category_combo.currentText()}\n"
                f"Description: {description_edit.toPlainText()}"
            )


# Perbarui class DayWidget dengan styling yang lebih baik
class DayWidget(QPushButton):
    clicked = pyqtSignal(int)  # Mengirimkan hari ketika diklik
    
    def __init__(self, day):
        super().__init__(str(day))
        self.day = day
        self.setFixedSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.clicked.connect(self.emit_click)
        
        # Style untuk hari ini
        if day == QDate.currentDate().day():
            self.setStyleSheet("""
                DayWidget {
                    background-color: #3498db;
                    color: white;
                    border: 2px solid #2980b9;
                    border-radius: 6px;
                    font-weight: bold;
                }
            """)
        
    def emit_click(self):
        """Emit sinyal dengan hari"""
        self.clicked.emit(self.day)
        
    def paintEvent(self, event):
        """Custom paint event untuk menambahkan indikator event"""
        super().paintEvent(event)
        
        # Contoh: tambahkan dot indicator jika ada event
        # Ini adalah placeholder - implementasi sebenarnya akan memeriksa database
        if self.day % 7 == 0:  # Contoh: hari yang habis dibagi 7 punya event
            painter = QPainter(self)
            painter.setBrush(QColor(46, 204, 113))  # Warna success
            painter.drawEllipse(45, 5, 10, 10)
            painter.end()
        elif self.day % 5 == 0:  # Event lain
            painter = QPainter(self)
            painter.setBrush(QColor(243, 156, 18))  # Warna warning
            painter.drawEllipse(45, 5, 10, 10)
            painter.end()