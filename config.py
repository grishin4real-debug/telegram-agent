"""
Конфигурация Telegram Agent
Настройки для бота и публикации постов
"""

import os
from datetime import time
import pytz

# =============================================================================
# ОСНОВНЫЕ НАСТРОЙКИ БОТА
# =============================================================================

# Токен Telegram бота (получить у @BotFather)
TELEGRAM_BOT_TOKEN = os.getenv(
    'TELEGRAM_BOT_TOKEN',
    '8143120662:AAFuniDLhtehe4ZWUtjMLVjSwqZmKJQ1www'
)

# ID Telegram канала для публикаций
# Формат: @channel_name или -100123456789
# Чтобы получить ID канала:
# 1. Добавьте бота в канал как администратора
# 2. Отправьте сообщение в канал
# 3. Перейдите на https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
# 4. Найдите chat id в ответе
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')

# =============================================================================
# НАСТРОЙКИ ПУБЛИКАЦИЙ
# =============================================================================

# Часовой пояс для публикаций
TIMEZONE = pytz.timezone('Europe/Moscow')  # Московское время (МСК)

# Время публикации (часы, минуты)
POST_HOUR = int(os.getenv('POST_HOUR', '10'))  # 10:00 утра
POST_MINUTE = int(os.getenv('POST_MINUTE', '0'))

# Интервал между публикациями (в днях)
POST_INTERVAL_DAYS = int(os.getenv('POST_INTERVAL_DAYS', '3'))  # Каждые 3 дня

# =============================================================================
# НАСТРОЙКИ КОНТЕНТА
# =============================================================================

# Включить эмодзи в постах
USE_EMOJI = os.getenv('USE_EMOJI', 'true').lower() == 'true'

# Добавлять хэштеги к постам
USE_HASHTAGS = os.getenv('USE_HASHTAGS', 'true').lower() == 'true'

# Хэштеги для постов
DEFAULT_HASHTAGS = [
    '#подсознание',
    '#трансформация', 
    '#саморазвитие',
    '#успех'
]

# =============================================================================
# НАСТРОЙКИ ЛОГИРОВАНИЯ
# =============================================================================

# Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Путь к файлу лога (если пустой, логи только в консоль)
LOG_FILE = os.getenv('LOG_FILE', 'telegram_agent.log')

# =============================================================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# =============================================================================

# Тестовый режим (не публикует посты, только логирует)
TEST_MODE = os.getenv('TEST_MODE', 'false').lower() == 'true'

# Максимальное количество повторных попыток при ошибке
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# Задержка между повторными попытками (в секундах)
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '60'))


def validate_config() -> bool:
    """
    Проверить корректность конфигурации
    
    Returns:
        bool: True если конфигурация корректна
    """
    errors = []
    
    # Проверка токена бота
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == '':
        errors.append("TELEGRAM_BOT_TOKEN не установлен")
    
    # Проверка ID канала
    if not TELEGRAM_CHANNEL_ID or TELEGRAM_CHANNEL_ID == '':
        errors.append("TELEGRAM_CHANNEL_ID не установлен")
    
    # Проверка времени публикации
    if not (0 <= POST_HOUR <= 23):
        errors.append(f"POST_HOUR должен быть от 0 до 23, получено: {POST_HOUR}")
    
    if not (0 <= POST_MINUTE <= 59):
        errors.append(f"POST_MINUTE должен быть от 0 до 59, получено: {POST_MINUTE}")
    
    # Проверка интервала публикаций
    if POST_INTERVAL_DAYS < 1:
        errors.append(f"POST_INTERVAL_DAYS должен быть >= 1, получено: {POST_INTERVAL_DAYS}")
    
    if errors:
        print("ОШИБКИ КОНФИГУРАЦИИ:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    
    return True


def print_config():
    """Вывести текущую конфигурацию"""
    print("=" * 60)
    print("КОНФИГУРАЦИЯ TELEGRAM AGENT")
    print("=" * 60)
    print(f"Бот токен:           {'*' * 20}{TELEGRAM_BOT_TOKEN[-10:]}")
    print(f"ID канала:           {TELEGRAM_CHANNEL_ID or 'НЕ УСТАНОВЛЕН'}")
    print(f"Часовой пояс:        {TIMEZONE}")
    print(f"Время публикации:    {POST_HOUR:02d}:{POST_MINUTE:02d}")
    print(f"Интервал:            каждые {POST_INTERVAL_DAYS} дня")
    print(f"Эмодзи:              {'✅ Да' if USE_EMOJI else '❌ Нет'}")
    print(f"Хэштеги:             {'✅ Да' if USE_HASHTAGS else '❌ Нет'}")
    print(f"Тестовый режим:      {'✅ Да' if TEST_MODE else '❌ Нет'}")
    print(f"Уровень логов:       {LOG_LEVEL}")
    print("=" * 60)


if __name__ == "__main__":
    # Проверка конфигурации при запуске файла напрямую
    print_config()
    print()
    if validate_config():
        print("✅ Конфигурация корректна!")
    else:
        print("❌ Исправьте ошибки конфигурации перед запуском.")