# Time Management App

Aplikasi desktop untuk manajemen waktu dengan fitur focus mode dan jadwal kerja bulanan.

## Fitur

- Focus Mode dengan timer Pomodoro yang dapat disesuaikan
- Kalender bulanan untuk penjadwalan
- Statistik produktivitas
- System tray integration
- Ekspor jadwal (dalam pengembangan)

## Instalasi

1. Pastikan Python 3.8+ terinstall
2. Clone atau download proyek ini
3. Install dependencies:

## Penggunaan

### Focus Mode
- Atur waktu kerja dan istirahat sesuai preferensi
- Klik "Start" untuk memulai sesi
- Gunakan "Pause" untuk menjeda dan "Reset" untuk mengulang
- Lihat statistik harian di bagian bawah

### Kalender
- Gunakan tombol panah untuk navigasi bulan
- Klik pada hari untuk melihat/menambah jadwal
- Gunakan tombol "Add Event" untuk menambah kegiatan

## Struktur Kode

- `main.py` - Entry point aplikasi
- `main_window.py` - Window utama dengan tab dan menu
- `focus_mode.py` - Implementasi focus mode/Pomodoro timer
- `calendar_widget.py` - Kalender dan penjadwalan
- `database.py` - Manajemen database SQLite
- `models.py` - Model data untuk tabel
- `styles.py` - Stylesheet untuk tampilan aplikasi

## Pengembangan

Aplikasi ini dibuat dengan PyQt6 dan menggunakan arsitektur modular untuk memudahkan pengembangan lebih lanjut.

## Lisensi

MIT License