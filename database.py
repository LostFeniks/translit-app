# database.py
import sqlite3
import os
from typing import List, Optional
import threading
from datetime import datetime

class TranslationStorage:
    def __init__(self, db_path: str = None):
        self.lock = threading.Lock()
        
        if db_path is None:
            # Если путь не указан, используем путь по умолчанию
            home_dir = os.path.expanduser("~")
            db_dir = os.path.join(home_dir, 'translit_app_data')
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            self.db_path = os.path.join(db_dir, 'translations.db')
        else:
            self.db_path = db_path
        
        # Создаем директорию если ее нет
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.connection.cursor()
            
            # Создаем таблицу если ее нет
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original TEXT NOT NULL,
                    translated TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Создаем индекс для быстрого поиска
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON translations (created_at DESC)
            ''')
            
            self.connection.commit()
            print(f"✅ Database initialized at: {self.db_path}")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            raise
    
    def close(self):
        """Закрытие соединения с базой данных"""
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
    
    def save(self, original: str, translated: str) -> bool:
        """
        Сохраняет пару оригинал-перевод в базу данных
        """
        with self.lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    'INSERT INTO translations (original, translated) VALUES (?, ?)',
                    (original, translated)
                )
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error saving to database: {e}")
                return False
    
    def get_last_n(self, n: int = 5) -> List[str]:
        """
        Возвращает последние N транслитераций
        """
        with self.lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    'SELECT translated FROM translations ORDER BY id DESC LIMIT ?',
                    (n,)
                )
                results = cursor.fetchall()
                return [row[0] for row in results]
            except Exception as e:
                print(f"Error getting history: {e}")
                return []
    
    def get_all_records(self) -> List[dict]:
        """
        Возвращает все записи (для отладки)
        """
        records = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT original, translated, created_at FROM translations ORDER BY id DESC'
            )
            results = cursor.fetchall()
            for row in results:
                records.append({
                    'original': row[0],
                    'translated': row[1],
                    'created_at': row[2]
                })
        except Exception as e:
            print(f"Error getting all records: {e}")
        return records
    
    def get_count(self) -> int:
        """
        Возвращает количество записей в базе
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM translations')
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error getting count: {e}")
            return 0
    
    def clear_all(self) -> bool:
        """
        Очищает все записи (для тестирования)
        """
        with self.lock:
            try:
                cursor = self.connection.cursor()
                cursor.execute('DELETE FROM translations')
                cursor.execute('DELETE FROM sqlite_sequence WHERE name="translations"')
                self.connection.commit()
                return True
            except Exception as e:
                print(f"Error clearing database: {e}")
                return False