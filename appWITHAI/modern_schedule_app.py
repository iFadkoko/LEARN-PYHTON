# modern_schedule_app.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableView, QHeaderView,
    QMessageBox, QDateEdit, QTimeEdit
)
from PyQt6.QtCore import (
    QAbstractTableModel, Qt, QDate, QTime, QSortFilterProxyModel
)
import database as db

class ScheduleModel(QAbstractTableModel):
    """
    Model data untuk jadwal, bertugas sebagai perantara antara
    database dan QTableView.
    """
    def __init__(self):
        super().__init__()
        self._headers = ["ID", "Kegiatan", "Tanggal", "Waktu"]
        self._data = []
        self.load_data()

    def load_data(self):
        """Memuat ulang data dari database."""
        self.beginResetModel()
        self._data = db.get_all_schedules()
        self.endResetModel()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[row][col]
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            # Pusatkan teks untuk kolom Tanggal dan Waktu
            if col in [2, 3]:
                return Qt.AlignmentFlag.AlignCenter

        return None

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def get_id_for_row(self, row):
        """Mendapatkan ID unik dari database untuk baris tertentu."""
        return self._data[row][0]


class ModernScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Manajemen Jadwal Modern")
        self.setGeometry(100, 100, 800, 600)
        
        # Inisialisasi database
        db.connect_db()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_input_widgets()
        self._create_table_view()
        self._create_buttons()

    def _create_input_widgets(self):
        input_layout = QHBoxLayout()
        self.event_label = QLabel("Kegiatan:")
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("Masukkan nama kegiatan...")
        self.date_label = QLabel("Tanggal:")
        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.time_label = QLabel("Waktu:")
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm")

        input_layout.addWidget(self.event_label)
        input_layout.addWidget(self.event_input, 2) # Beri porsi lebih besar
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.time_label)
        input_layout.addWidget(self.time_input)
        self.layout.addLayout(input_layout)

    def _create_table_view(self):
        """Membuat QTableView dan menghubungkannya dengan model."""
        self.table_view = QTableView()
        self.model = ScheduleModel()
        
        # Proxy model untuk sorting
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        
        # Sembunyikan kolom ID (indeks 0)
        self.table_view.hideColumn(0)

        # Atur lebar kolom
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.table_view)

    def _create_buttons(self):
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Tambah Jadwal")
        self.add_button.clicked.connect(self.add_schedule)
        self.delete_button = QPushButton("Hapus Jadwal Terpilih")
        self.delete_button.clicked.connect(self.delete_schedule)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

    def add_schedule(self):
        event = self.event_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")

        if not event:
            QMessageBox.warning(self, "Input Kosong", "Nama kegiatan tidak boleh kosong.")
            return

        db.add_schedule(event, date, time)
        self.model.load_data() # Muat ulang data untuk memperbarui tampilan
        self.event_input.clear()
        
    def delete_schedule(self):
        # Dapatkan indeks terpilih dari view (proxy model)
        selected_indexes = self.table_view.selectionModel().selectedRows()
        
        if not selected_indexes:
            QMessageBox.warning(self, "Tidak Ada Pilihan", "Silakan pilih jadwal untuk dihapus.")
            return

        # Ambil indeks pertama yang dipilih
        proxy_index = selected_indexes[0]
        # Konversi ke indeks model sumber (source model) untuk mendapatkan data asli
        source_index = self.proxy_model.mapToSource(proxy_index)
        
        # Dapatkan ID database dan nama kegiatan dari model sumber
        schedule_id = self.model.get_id_for_row(source_index.row())
        event_name = self.model.index(source_index.row(), 1).data()

        confirm = QMessageBox.question(self, "Konfirmasi Hapus",
                                       f"Apakah Anda yakin ingin menghapus jadwal '{event_name}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            db.delete_schedule(schedule_id)
            self.model.load_data() # Muat ulang data untuk memperbarui tampilan



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load file style.qss
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = ModernScheduleApp()
    window.show()
    sys.exit(app.exec())

