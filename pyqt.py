import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QDateEdit, QTimeEdit, QHeaderView, QMessageBox
)
from PyQt6.QtCore import QDate, QTime, Qt

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Manajemen Jadwal")
        self.setGeometry(100, 100, 700, 500)

        # Widget utama dan layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_input_widgets()
        self._create_table()
        self._create_buttons()

    def _create_input_widgets(self):
        """Membuat widget untuk input pengguna."""
        input_layout = QHBoxLayout()

        # Input untuk nama kegiatan
        self.event_label = QLabel("Kegiatan:")
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("Masukkan nama kegiatan...")

        # Input untuk tanggal
        self.date_label = QLabel("Tanggal:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        # Input untuk waktu
        self.time_label = QLabel("Waktu:")
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm")

        input_layout.addWidget(self.event_label)
        input_layout.addWidget(self.event_input)
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.time_label)
        input_layout.addWidget(self.time_input)

        self.layout.addLayout(input_layout)

    def _create_table(self):
        """Membuat tabel untuk menampilkan jadwal."""
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Kegiatan", "Tanggal", "Waktu"])
        
        # Mengatur agar lebar kolom menyesuaikan isi
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # Mengaktifkan pengurutan berdasarkan kolom
        self.table.setSortingEnabled(True)
        # Mengatur agar tidak bisa diedit langsung di tabel
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Mengatur agar pilihan adalah per baris
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


        self.layout.addWidget(self.table)

    def _create_buttons(self):
        """Membuat tombol untuk menambah dan menghapus jadwal."""
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Tambah Jadwal")
        self.add_button.clicked.connect(self.add_schedule)

        self.delete_button = QPushButton("Hapus Jadwal Terpilih")
        self.delete_button.clicked.connect(self.delete_schedule)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        
    def add_schedule(self):
        """Fungsi untuk menambahkan jadwal ke tabel."""
        event = self.event_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")

        if not event:
            QMessageBox.warning(self, "Input Kosong", "Nama kegiatan tidak boleh kosong.")
            return

        # Menambahkan baris baru
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Membuat item untuk setiap sel
        event_item = QTableWidgetItem(event)
        date_item = QTableWidgetItem(date)
        time_item = QTableWidgetItem(time)

        # Memasukkan item ke dalam tabel
        self.table.setItem(row_position, 0, event_item)
        self.table.setItem(row_position, 1, date_item)
        self.table.setItem(row_position, 2, time_item)

        # Mengurutkan tabel berdasarkan kolom tanggal (indeks 1) secara menaik
        self.table.sortByColumn(1, Qt.SortOrder.AscendingOrder)

        # Mengosongkan input setelah ditambahkan
        self.event_input.clear()

    def delete_schedule(self):
        """Fungsi untuk menghapus jadwal yang dipilih dari tabel."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            # Konfirmasi sebelum menghapus
            confirm = QMessageBox.question(self, "Konfirmasi Hapus",
                                           f"Apakah Anda yakin ingin menghapus jadwal '{self.table.item(selected_row, 0).text()}'?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Tidak Ada Pilihan", "Silakan pilih jadwal yang ingin dihapus terlebih dahulu.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())
