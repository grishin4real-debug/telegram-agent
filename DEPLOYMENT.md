# 🚀 Руководство по развертыванию Telegram Agent

Это руководство поможет вам развернуть и запустить Telegram Agent в различных окружениях.

---

## 📋 Быстрый старт

### 1. Подготовка окружения

```bash
# Клонируйте или скачайте проект
cd telegram-agent

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env из примера
cp .env.example .env
```

### 2. Настройка

Откройте файл `.env` и заполните:

```bash
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
TELEGRAM_CHANNEL_ID=@ваш_канал_или_id
```

### 3. Тестирование

```bash
# Проверьте конфигурацию
python config.py

# Запустите тесты
python test_agent.py all
```

### 4. Запуск

```bash
# Запустите агента
python telegram_agent.py
```

---

## 🖥️ Локальный запуск

### Запуск в фоновом режиме (Linux/Mac)

**Вариант 1: Используя nohup**

```bash
nohup python telegram_agent.py > agent.log 2>&1 &
```

Просмотр логов:
```bash
tail -f agent.log
```

Остановка:
```bash
ps aux | grep telegram_agent.py
kill <PID>
```

**Вариант 2: Используя screen**

```bash
# Создать новую screen сессию
screen -S telegram-agent

# Запустить агента
python telegram_agent.py

# Отсоединиться: Ctrl+A, затем D

# Вернуться к сессии
screen -r telegram-agent

# Остановить: вернуться к сессии и нажать Ctrl+C
```

**Вариант 3: Используя tmux**

```bash
# Создать tmux сессию
tmux new -s telegram-agent

# Запустить агента
python telegram_agent.py

# Отсоединиться: Ctrl+B, затем D

# Вернуться к сессии
tmux attach -t telegram-agent
```

### Запуск на Windows

**PowerShell (фоновый режим):**

```powershell
Start-Process python -ArgumentList "telegram_agent.py" -WindowStyle Hidden
```

**Создать .bat файл:**

```batch
@echo off
start /B python telegram_agent.py
```

---

## 🏭 Production развертывание

### Linux с systemd (рекомендуется)

#### Шаг 1: Создайте systemd service файл

```bash
sudo nano /etc/systemd/system/telegram-agent.service
```

Вставьте следующее содержимое:

```ini
[Unit]
Description=Telegram Agent для автоматической публикации постов
After=network.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/путь/к/проекту
Environment="TELEGRAM_BOT_TOKEN=ваш_токен"
Environment="TELEGRAM_CHANNEL_ID=@ваш_канал"
ExecStart=/usr/bin/python3 /путь/к/проекту/telegram_agent.py
Restart=always
RestartSec=10

# Логирование
StandardOutput=append:/var/log/telegram-agent/output.log
StandardError=append:/var/log/telegram-agent/error.log

[Install]
WantedBy=multi-user.target
```

#### Шаг 2: Создайте директорию для логов

```bash
sudo mkdir -p /var/log/telegram-agent
sudo chown ваш_пользователь:ваш_пользователь /var/log/telegram-agent
```

#### Шаг 3: Активируйте и запустите сервис

```bash
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable telegram-agent

# Запустите сервис
sudo systemctl start telegram-agent

# Проверьте статус
sudo systemctl status telegram-agent
```

#### Управление сервисом

```bash
# Остановить
sudo systemctl stop telegram-agent

# Перезапустить
sudo systemctl restart telegram-agent

# Посмотреть логи
sudo journalctl -u telegram-agent -f

# Выключить автозапуск
sudo systemctl disable telegram-agent
```

---

## ☁️ Cloud развертывание

### 1. VPS (DigitalOcean, AWS, etc.)

#### Подготовка VPS

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Python и pip
sudo apt install python3 python3-pip git -y

# Клонируйте проект
git clone https://github.com/ваш-репозиторий/telegram-agent.git
cd telegram-agent

# Установите зависимости
pip3 install -r requirements.txt
```

#### Настройка переменных окружения

```bash
# Создайте .env файл
nano .env

# Добавьте:
# TELEGRAM_BOT_TOKEN=ваш_токен
# TELEGRAM_CHANNEL_ID=@ваш_канал
```

#### Настройте systemd (как описано выше)

### 2. Docker (рекомендуется для облака)

#### Создайте Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируйте зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте код
COPY . .

# Запуск
CMD ["python", "telegram_agent.py"]
```

#### Создайте docker-compose.yml

```yaml
version: '3.8'

services:
  telegram-agent:
    build: .
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHANNEL_ID=${TELEGRAM_CHANNEL_ID}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

#### Запуск

```bash
# Создайте .env файл с переменными
echo "TELEGRAM_BOT_TOKEN=ваш_токен" > .env
echo "TELEGRAM_CHANNEL_ID=@ваш_канал" >> .env

# Запустите
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### 3. Heroku

#### Подготовка

Создайте `Procfile`:

```
worker: python telegram_agent.py
```

Создайте `runtime.txt`:

```
python-3.11.0
```

#### Развертывание

```bash
# Установите Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Войдите
heroku login

# Создайте приложение
heroku create your-telegram-agent

# Установите переменные окружения
heroku config:set TELEGRAM_BOT_TOKEN=ваш_токен
heroku config:set TELEGRAM_CHANNEL_ID=@ваш_канал

# Деплой
git push heroku main

# Запустите worker
heroku ps:scale worker=1

# Просмотр логов
heroku logs --tail
```

### 4. Railway.app

1. Создайте аккаунт на [Railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
4. Railway автоматически деплоит ваш проект

---

## 📊 Мониторинг и обслуживание

### Просмотр логов

**Локально:**
```bash
tail -f telegram_agent.log
```

**systemd:**
```bash
sudo journalctl -u telegram-agent -f
```

**Docker:**
```bash
docker-compose logs -f
```

### Мониторинг работы

Создайте простой health check скрипт:

```python
# health_check.py
import sys
from datetime import datetime, timedelta
import pytz

# Проверяем, что лог файл обновлялся недавно
try:
    import os
    log_file = 'telegram_agent.log'
    
    if os.path.exists(log_file):
        mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        now = datetime.now()
        
        # Если лог не обновлялся более 2 часов
        if (now - mod_time) > timedelta(hours=2):
            print("ALERT: Agent may not be running!")
            sys.exit(1)
        else:
            print("OK: Agent is running")
            sys.exit(0)
    else:
        print("ERROR: Log file not found")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
```

Настройте cron для проверки:

```bash
# Открыть crontab
crontab -e

# Добавить проверку каждые 30 минут
*/30 * * * * python3 /путь/к/проекту/health_check.py
```

---

## 🔧 Обновление

### Обновление кода

```bash
# Остановите агента
sudo systemctl stop telegram-agent

# Получите последние изменения
git pull

# Установите новые зависимости (если есть)
pip install -r requirements.txt

# Перезапустите агента
sudo systemctl start telegram-agent
```

### Обновление конфигурации

```bash
# Отредактируйте .env или config.py
nano .env

# Перезапустите агента
sudo systemctl restart telegram-agent
```

---

## 🐛 Решение проблем

### Агент не запускается

1. Проверьте логи:
   ```bash
   tail -f telegram_agent.log
   ```

2. Проверьте конфигурацию:
   ```bash
   python config.py
   ```

3. Проверьте зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### Агент не публикует посты

1. Проверьте, что бот добавлен в канал
2. Проверьте права бота (публикация сообщений)
3. Проверьте ID канала в конфигурации
4. Запустите тест:
   ```bash
   python test_agent.py send
   ```

### Ошибки подключения к Telegram

1. Проверьте интернет соединение
2. Проверьте токен бота
3. Проверьте, не заблокирован ли Telegram API
4. Попробуйте использовать VPN/прокси

---

## 🔒 Безопасность

### Рекомендации

1. **Никогда не коммитьте .env файл в Git**
   ```bash
   # Добавьте в .gitignore
   echo ".env" >> .gitignore
   ```

2. **Используйте переменные окружения**
   ```bash
   export TELEGRAM_BOT_TOKEN="ваш_токен"
   export TELEGRAM_CHANNEL_ID="@ваш_канал"
   ```

3. **Ограничьте доступ к файлам**
   ```bash
   chmod 600 .env
   chmod 700 telegram_agent.py
   ```

4. **Регулярно обновляйте зависимости**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

---

## 📈 Масштабирование

### Несколько каналов

Для управления несколькими каналами создайте отдельные экземпляры:

```bash
# Создайте папки для каждого канала
mkdir channel1 channel2

# Скопируйте файлы
cp telegram_agent.py channel1/
cp content_generator.py channel1/
# ... и т.д.

# Настройте разные .env файлы
nano channel1/.env
nano channel2/.env
```

Создайте отдельные systemd сервисы для каждого канала.

---

## 🎯 Оптимизация

### Уменьшение использования ресурсов

1. Увеличьте интервал проверки в `telegram_agent.py`:
   ```python
   await asyncio.sleep(300)  # Проверять каждые 5 минут вместо 1
   ```

2. Используйте легковесную систему:
   - Alpine Linux для Docker
   - Minimal VPS конфигурация

---

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте логи
2. Запустите диагностику: `python test_agent.py all`
3. Проверьте конфигурацию: `python config.py`
4. Посмотрите документацию в README.md

---

**Успешного развертывания! 🚀**