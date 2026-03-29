ПОШАГОВЫЙ ДЕПЛОЙ НА RAILWAY
═══════════════════════════════════════════════════

ШАГ 1 — Залить код на GitHub
──────────────────────────────
cd FALT_BOT
git init
git add .
git commit -m "Initial commit"
# Создать репозиторий на github.com, затем:
git remote add origin https://github.com/YOUR/FALT_BOT.git
git push -u origin main


ШАГ 2 — Создать проект на Railway
──────────────────────────────────
1. Зайти на https://railway.app
2. New Project → Deploy from GitHub repo → выбрать FALT_BOT
3. Railway автоматически определит railway.json и запустит:
   python start_all.py


ШАГ 3 — Задать переменные окружения
─────────────────────────────────────
В Railway Dashboard → вкладка Variables → добавить:

  TOKEN              = токен от BotFather
  ADMIN_CHAT_ID      = @ваш_username (или числовой ID)
  JWT_SECRET_KEY     = (сгенерировать ниже)
  MINI_APP_URL       = пока оставить пустым, заполним после ШАГА 4

Генерация JWT_SECRET_KEY:
  python -c "import secrets; print(secrets.token_hex(32))"


ШАГ 4 — Получить домен
────────────────────────
Railway Dashboard → Settings → Networking → Generate Domain
Получите URL вида: https://falt-bot-production.up.railway.app

Теперь обновить переменную:
  MINI_APP_URL = https://falt-bot-production.up.railway.app


ШАГ 5 — Настроить BotFather
─────────────────────────────
В Telegram написать @BotFather:

  /mybots
  → выбрать вашего бота
  → Bot Settings
  → Menu Button
  → Edit menu button URL
  → вставить: https://falt-bot-production.up.railway.app

  Также:
  /setdomain → вставить домен без https://


ШАГ 6 — Пользователь привязывает email
────────────────────────────────────────
Чтобы открыть Mini App, пользователь должен:
  1. Пройти регистрацию через /start
  2. Выполнить /setemail и ввести email
  3. После этого /miniapp будет доступен


═══════════════════════════════════════════════════
ОБНОВЛЕНИЕ КОДА (после изменений)
═══════════════════════════════════════════════════
git add .
git commit -m "update"
git push

Railway пересоберёт и задеплоит автоматически.


═══════════════════════════════════════════════════
ПОЛЕЗНЫЕ КОМАНДЫ Railway CLI
═══════════════════════════════════════════════════
railway logs          — логи в реальном времени
railway status        — статус сервиса
railway variables     — список переменных
railway open          — открыть дашборд


═══════════════════════════════════════════════════
ЛОКАЛЬНЫЙ ЗАПУСК (для разработки)
═══════════════════════════════════════════════════
cp .env.example .env
# Заполнить .env

pip install -r requirements.txt
python start_all.py

Mini App доступен на: http://localhost:8000
