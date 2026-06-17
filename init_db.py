# init_db.py
import sqlite3
import os
import sys

def init_database():
    """Создает файл базы данных в директории с правами на запись"""
    try:
        # Вариант 1: Используем текущую директорию пользователя
        home_dir = os.path.expanduser("~")
        db_dir = os.path.join(home_dir, 'translit_app_data')
        
        # Создаем директорию если ее нет
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"📁 Created directory: {db_dir}")
        
        db_path = os.path.join(db_dir, 'translations.db')
        
        # Проверяем права на запись
        try:
            test_file = os.path.join(db_dir, 'test_write.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("✅ Directory has write permissions")
        except Exception as e:
            print(f"❌ No write permissions: {e}")
            # Пробуем использовать temp
            import tempfile
            temp_dir = tempfile.gettempdir()
            db_dir = os.path.join(temp_dir, 'translit_app_data')
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            db_path = os.path.join(db_dir, 'translations.db')
            print(f"📁 Using temp directory: {db_dir}")
        
        print(f"📁 Database path: {db_path}")
        
        # Создаем подключение (создаст файл если его нет)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем таблицу
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original TEXT NOT NULL,
                translated TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON translations (created_at DESC)
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database created successfully at: {db_path}")
        print(f"📁 File exists: {os.path.exists(db_path)}")
        print(f"📊 File size: {os.path.getsize(db_path)} bytes")
        
        # Сохраняем путь в файл для использования в app.py
        with open('db_path.txt', 'w') as f:
            f.write(db_path)
        print("💾 Database path saved to db_path.txt")
        
        return db_path
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    init_database()