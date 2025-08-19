# database.py
import sqlite3
import os

DB_NAME = "schedule.db"

def connect_db():
    """Membuat koneksi ke database dan membuat tabel jika belum ada."""
    # Cek apakah file database sudah ada
    db_exists = os.path.exists(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Hanya buat tabel jika database baru dibuat
    if not db_exists:
        print("Membuat tabel 'schedules' baru...")
        cursor.execute("""
        CREATE TABLE schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
        """)
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' siap digunakan.")

def add_schedule(event, date, time):
    """Menambahkan jadwal baru ke database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedules (event, date, time) VALUES (?, ?, ?)",
                   (event, date, time))
    conn.commit()
    conn.close()

def get_all_schedules():
    """Mengambil semua jadwal dari database, diurutkan berdasarkan tanggal dan waktu."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, event, date, time FROM schedules ORDER BY date, time")
    schedules = cursor.fetchall()
    conn.close()
    return schedules

def delete_schedule(schedule_id):
    """Menghapus jadwal berdasarkan ID-nya."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()

# Inisialisasi database saat modul ini pertama kali diimpor
if __name__ == '__main__':
    connect_db()
