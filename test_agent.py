#!/usr/bin/env python3
"""
Тестовый скрипт для проверки всех компонентов Telegram Agent
"""

import asyncio
import sys
from telegram_agent import TelegramAgent, BOT_TOKEN, CHANNEL_ID
from content_generator import generate_content
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def test_connection():
    """Тест 1: Проверка подключения к Telegram API"""
    print("\n" + "=" * 60)
    print("ТЕСТ 1: Проверка подключения к Telegram API")
    print("=" * 60)
    
    if not CHANNEL_ID:
        print("❌ ОШИБКА: TELEGRAM_CHANNEL_ID не установлен!")
        print("Установите ID канала в переменной окружения TELEGRAM_CHANNEL_ID")
        return False
    
    agent = TelegramAgent(BOT_TOKEN, CHANNEL_ID)
    
    print(f"Токен бота: {'*' * 20}{BOT_TOKEN[-10:]}")
    print(f"ID канала: {CHANNEL_ID}")
    print("\nПопытка подключения...")
    
    success = await agent.test_connection()
    
    if success:
        print("✅ Подключение успешно!")
        return True
    else:
        print("❌ Не удалось подключиться к Telegram")
        print("Проверьте:")
        print("1. Правильность токена бота")
        print("2. Доступ к интернету")
        print("3. Не заблокирован ли Telegram API")
        return False


async def test_content_generation():
    """Тест 2: Проверка генерации контента"""
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Проверка генерации контента")
    print("=" * 60)
    
    print("Генерация тестового поста...")
    
    try:
        # Генерируем 3 поста для проверки разнообразия
        for i in range(3):
            print(f"\n--- Пост {i+1} ---")
            content = await generate_content()
            print(content)
            print("\n" + "-" * 60)
        
        print("\n✅ Генерация контента работает!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при генерации контента: {e}")
        return False


async def test_send_post():
    """Тест 3: Отправка тестового поста"""
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Отправка тестового поста в канал")
    print("=" * 60)
    
    if not CHANNEL_ID:
        print("❌ ОШИБКА: TELEGRAM_CHANNEL_ID не установлен!")
        return False
    
    # Спрашиваем подтверждение
    print(f"Этот тест отправит реальный пост в канал: {CHANNEL_ID}")
    response = input("Продолжить? (yes/no): ")
    
    if response.lower() not in ['yes', 'y', 'да']:
        print("Тест отменен пользователем")
        return False
    
    agent = TelegramAgent(BOT_TOKEN, CHANNEL_ID)
    
    # Генерируем контент
    print("\nГенерация контента...")
    content = await generate_content()
    
    print("\nПост для публикации:")
    print("-" * 60)
    print(content)
    print("-" * 60)
    
    # Отправляем пост
    print("\nОтправка поста...")
    success = await agent.send_post(content)
    
    if success:
        print("✅ Пост успешно отправлен!")
        print(f"Проверьте ваш канал: {CHANNEL_ID}")
        return True
    else:
        print("❌ Не удалось отправить пост")
        print("Проверьте:")
        print("1. Бот добавлен в канал как администратор")
        print("2. У бота есть права на публикацию сообщений")
        print("3. ID канала указан правильно")
        return False


async def test_scheduling():
    """Тест 4: Проверка системы планирования"""
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Проверка системы планирования")
    print("=" * 60)
    
    if not CHANNEL_ID:
        print("❌ ОШИБКА: TELEGRAM_CHANNEL_ID не установлен!")
        return False
    
    agent = TelegramAgent(BOT_TOKEN, CHANNEL_ID)
    
    # Проверяем вычисление времени следующей публикации
    next_post = agent.get_next_post_time()
    print(f"Время следующей публикации: {next_post}")
    
    # Проверяем, нужно ли публиковать сейчас
    should_post = agent.should_post_now()
    print(f"Нужно ли публиковать сейчас: {should_post}")
    
    print("\n✅ Система планирования работает!")
    return True


async def run_all_tests():
    """Запустить все тесты"""
    print("\n")
    print("🧪 ЗАПУСК ТЕСТОВ TELEGRAM AGENT")
    print("=" * 60)
    
    results = {}
    
    # Тест 1: Подключение
    results['connection'] = await test_connection()
    
    # Тест 2: Генерация контента
    results['content_generation'] = await test_content_generation()
    
    # Тест 3: Планирование
    results['scheduling'] = await test_scheduling()
    
    # Тест 4: Отправка поста (опционально)
    print("\n" + "=" * 60)
    print("ТЕСТ 4: Отправка тестового поста (опционально)")
    print("=" * 60)
    response = input("Хотите протестировать отправку реального поста? (yes/no): ")
    if response.lower() in ['yes', 'y', 'да']:
        results['send_post'] = await test_send_post()
    else:
        print("Тест отправки пропущен")
        results['send_post'] = None
    
    # Итоги
    print("\n" + "=" * 60)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    for test_name, result in results.items():
        if result is None:
            status = "⏭️  ПРОПУЩЕН"
        elif result:
            status = "✅ ПРОЙДЕН"
        else:
            status = "❌ ПРОВАЛЕН"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    # Общий результат
    passed = sum(1 for r in results.values() if r is True)
    total = sum(1 for r in results.values() if r is not None)
    
    print("\n" + "=" * 60)
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"⚠️  Пройдено тестов: {passed}/{total}")
    print("=" * 60)


async def main():
    """Главная функция"""
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        
        if test_name == "connection":
            await test_connection()
        elif test_name == "content":
            await test_content_generation()
        elif test_name == "send":
            await test_send_post()
        elif test_name == "schedule":
            await test_scheduling()
        elif test_name == "all":
            await run_all_tests()
        else:
            print("Неизвестный тест. Доступные тесты:")
            print("  connection - тест подключения")
            print("  content    - тест генерации контента")
            print("  send       - тест отправки поста")
            print("  schedule   - тест системы планирования")
            print("  all        - все тесты")
    else:
        # Запускаем все тесты по умолчанию
        await run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())