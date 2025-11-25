#!/usr/bin/env python3
"""
Telegram Agent - Автоматическая публикация постов в Telegram канал
Посты о трансформации подсознания с использованием AIDA и SMART frameworks
"""

import os
import asyncio
import logging
from datetime import datetime, time, timedelta
import pytz
from telegram import Bot
from telegram.error import TelegramError
import json

# Импорт генератора контента
from content_generator import generate_content

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8143120662:AAFuniDLhtehe4ZWUtjMLVjSwqZmKJQ1www')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')  # Нужно будет указать ID канала
TIMEZONE = pytz.timezone('Europe/Moscow')  # Московское время
POST_TIME = time(10, 0)  # 10:00 МСК
POST_INTERVAL_DAYS = 3  # Каждые 3 дня


class TelegramAgent:
    """Агент для автоматической публикации постов в Telegram канал"""
    
    def __init__(self, bot_token: str, channel_id: str):
        """
        Инициализация агента
        
        Args:
            bot_token: Токен Telegram бота
            channel_id: ID Telegram канала (например, @channel_name или -100123456789)
        """
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
        self.last_post_time = None
        logger.info(f"Telegram Agent инициализирован для канала: {channel_id}")
    
    async def send_post(self, content: str) -> bool:
        """
        Отправить пост в Telegram канал
        
        Args:
            content: Текст поста для публикации
            
        Returns:
            bool: True если пост успешно отправлен, False в случае ошибки
        """
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=content,
                parse_mode='HTML'  # Поддержка HTML форматирования
            )
            self.last_post_time = datetime.now(TIMEZONE)
            logger.info(f"Пост успешно опубликован в {self.last_post_time}")
            return True
        except TelegramError as e:
            logger.error(f"Ошибка при отправке поста: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Проверить подключение к Telegram API
        
        Returns:
            bool: True если подключение успешно
        """
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Подключение успешно! Бот: @{bot_info.username}")
            return True
        except TelegramError as e:
            logger.error(f"Ошибка подключения к Telegram: {e}")
            return False
    
    def get_next_post_time(self) -> datetime:
        """
        Вычислить время следующей публикации
        
        Returns:
            datetime: Время следующей публикации
        """
        now = datetime.now(TIMEZONE)
        
        # Если это первый пост или прошло больше интервала
        if self.last_post_time is None:
            next_post = now.replace(hour=POST_TIME.hour, minute=POST_TIME.minute, second=0, microsecond=0)
            # Если время уже прошло сегодня, планируем на завтра
            if next_post <= now:
                next_post += timedelta(days=1)
        else:
            # Следующий пост через POST_INTERVAL_DAYS дней
            next_post = self.last_post_time + timedelta(days=POST_INTERVAL_DAYS)
            next_post = next_post.replace(hour=POST_TIME.hour, minute=POST_TIME.minute, second=0, microsecond=0)
        
        return next_post
    
    def should_post_now(self) -> bool:
        """
        Проверить, нужно ли публиковать пост сейчас
        
        Returns:
            bool: True если пришло время публикации
        """
        now = datetime.now(TIMEZONE)
        next_post_time = self.get_next_post_time()
        
        # Разрешаем публикацию в течение 5 минут от запланированного времени
        time_diff = abs((now - next_post_time).total_seconds())
        return time_diff < 300  # 5 минут = 300 секунд
    
    async def run_scheduler(self, content_generator):
        """
        Запустить планировщик постов
        
        Args:
            content_generator: Функция для генерации контента постов
        """
        logger.info("Запуск планировщика постов...")
        logger.info(f"Расписание: каждые {POST_INTERVAL_DAYS} дня в {POST_TIME.hour}:{POST_TIME.minute:02d} МСК")
        
        while True:
            try:
                if self.should_post_now():
                    logger.info("Время публикации! Генерируем контент...")
                    
                    # Генерируем контент
                    post_content = await content_generator()
                    
                    # Публикуем пост
                    success = await self.send_post(post_content)
                    
                    if success:
                        next_post = self.get_next_post_time()
                        logger.info(f"Следующая публикация: {next_post}")
                    else:
                        logger.error("Не удалось опубликовать пост")
                else:
                    next_post = self.get_next_post_time()
                    now = datetime.now(TIMEZONE)
                    time_until_next = (next_post - now).total_seconds()
                    
                    if time_until_next > 3600:  # Больше часа
                        logger.info(f"Следующая публикация: {next_post} (через {time_until_next/3600:.1f} часов)")
                    else:
                        logger.info(f"Следующая публикация: {next_post} (через {time_until_next/60:.0f} минут)")
                
                # Проверяем каждые 60 секунд
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                await asyncio.sleep(60)


async def main():
    """Главная функция запуска агента"""
    
    # Проверяем наличие ID канала
    if not CHANNEL_ID:
        logger.error("ОШИБКА: Не указан TELEGRAM_CHANNEL_ID!")
        logger.info("Укажите ID вашего канала в переменной окружения TELEGRAM_CHANNEL_ID")
        logger.info("Например: @your_channel или -100123456789")
        return
    
    # Создаем агента
    agent = TelegramAgent(BOT_TOKEN, CHANNEL_ID)
    
    # Тестируем подключение
    logger.info("Проверка подключения к Telegram...")
    if not await agent.test_connection():
        logger.error("Не удалось подключиться к Telegram. Проверьте токен бота.")
        return
    
    logger.info("✅ Подключение к Telegram успешно!")
    logger.info("=" * 60)
    logger.info("Telegram Agent запущен!")
    logger.info(f"Канал: {CHANNEL_ID}")
    logger.info(f"Расписание: каждые {POST_INTERVAL_DAYS} дня в {POST_TIME.hour}:{POST_TIME.minute:02d} МСК")
    logger.info("=" * 60)
    
    # Запускаем планировщик
    try:
        await agent.run_scheduler(generate_content)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    # Запускаем агента
    asyncio.run(main())