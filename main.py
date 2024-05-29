import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import openai

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Токен Telegram API
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Ключ OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация OpenAI API
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение, когда команда /start выполнена."""
    await update.message.reply_text('Привет, бро! Я бот, использующий GPT-4. Задавай свои вопросы.')

async def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение, когда команда /help выполнена."""
    await update.message.reply_text('Тебе уже ничего не поможет.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обрабатывает входящие текстовые сообщения."""
    user_message = update.message.text

    # Отправка промежуточного сообщения
    await update.message.reply_text("Дай-ка подумать ... 🤔")

    # Запрос к модели GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    # Получение ответа от модели
    bot_response = response['choices'][0]['message']['content']

    # Отправка ответа пользователю
    await update.message.reply_text(bot_response)

def main() -> None:
    """Запуск бота."""
    # Создаем Application и передаем ему токен вашего бота.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработка всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
