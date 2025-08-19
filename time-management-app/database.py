import sqlite3
from datetime import datetime, date
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = Path.home() / ".time_management" / "app.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """Inisialisasi database dan tabel"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabel untuk sesi focus
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS focus_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME,
                    duration INTEGER,  -- dalam menit
                    session_type TEXT CHECK(session_type IN ('work', 'break'))
                )
            """)
            
            # Tabel untuk jadwal/event
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schedule_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    start_time TIME,
                    end_time TIME
                )
            """)
            
            # Tabel untuk pengaturan
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            
            conn.commit()
            
    def add_focus_session(self, start_time, end_time, duration, session_type):
        """Menambahkan sesi focus ke database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO focus_sessions (start_time, end_time, duration, session_type) VALUES (?, ?, ?, ?)",
                (start_time, end_time, duration, session_type)
            )
            conn.commit()
            
    def get_daily_stats(self, date):
        """Mendapatkan statistik harian"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*), SUM(duration) FROM focus_sessions WHERE date(start_time) = ? AND session_type = 'work'",
                (date,)
            )
            result = cursor.fetchone()
            return {
                'sessions': result[0] or 0,
                'total_minutes': result[1] or 0
            }
            
    def add_schedule_event(self, event_data):
        """Menambahkan event jadwal"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO schedule_events 
                (date, title, description, category, start_time, end_time) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    event_data['date'],
                    event_data['title'],
                    event_data.get('description', ''),
                    event_data.get('category', ''),
                    event_data.get('start_time'),
                    event_data.get('end_time')
                )
            )
            conn.commit()
            
    def get_events_for_date(self, date):
        """Mendapatkan event untuk tanggal tertentu"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM schedule_events WHERE date = ? ORDER BY start_time",
                (date,)
            )
            return cursor.fetchall()