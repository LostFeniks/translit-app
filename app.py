# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os

from translit import transliterate
from database import TranslationStorage

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание приложения
app = Flask(__name__, static_folder='static')
CORS(app)

# Читаем путь к базе данных из файла
db_path = None
try:
    if os.path.exists('db_path.txt'):
        with open('db_path.txt', 'r') as f:
            db_path = f.read().strip()
        logger.info(f"Database path loaded from db_path.txt: {db_path}")
except Exception as e:
    logger.warning(f"Could not read db_path.txt: {e}")

# Инициализация базы данных
try:
    if db_path:
        storage = TranslationStorage(db_path=db_path)
    else:
        # Если файл не найден, используем путь по умолчанию
        default_path = os.path.join(os.path.expanduser('~'), 'translit_app_data', 'translations.db')
        storage = TranslationStorage(db_path=default_path)
    
    logger.info(f"Database connection established")
    count = storage.get_count()
    logger.info(f"Current records in database: {count}")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    storage = None

@app.route('/')
def index():
    """Главная страница"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Статические файлы"""
    return send_from_directory('static', path)

@app.route('/api', methods=['POST'])
def api_transliterate():
    """API эндпоинт для транслитерации"""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing "data" field'
            }), 400
        
        original_text = data['data'].strip()
        if not original_text:
            return jsonify({
                'status': 'error',
                'message': 'Empty text'
            }), 400
        
        # Транслитерируем
        translated_text = transliterate(original_text)
        
        # Сохраняем в базу данных
        if storage:
            success = storage.save(original_text, translated_text)
            if not success:
                logger.warning(f"Failed to save translation: {original_text}")
        
        return jsonify({
            'status': 'success',
            'data': translated_text
        })
    
    except Exception as e:
        logger.error(f"Error in /api: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Возвращает историю последних N переводов"""
    try:
        n = request.args.get('n', default=5, type=int)
        n = max(1, min(100, n))  # Ограничиваем от 1 до 100
        
        if storage:
            history = storage.get_last_n(n)
        else:
            history = []
        
        return jsonify({
            'data': history,
            'total': storage.get_count() if storage else 0
        })
    
    except Exception as e:
        logger.error(f"Error in /history: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния приложения"""
    return jsonify({
        'status': 'ok',
        'database': storage is not None,
        'records': storage.get_count() if storage else 0
    })

@app.route('/clear', methods=['POST'])
def clear_history():
    """Очистка истории (для административных целей)"""
    if storage:
        success = storage.clear_all()
        return jsonify({
            'status': 'success' if success else 'error',
            'message': 'History cleared' if success else 'Failed to clear history'
        })
    return jsonify({
        'status': 'error',
        'message': 'Database not available'
    }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting transliteration app...")
        logger.info("Open http://localhost:8080 in your browser")
        app.run(host='0.0.0.0', port=8080, debug=True)
    finally:
        if storage:
            storage.close()
            logger.info("Database connection closed")