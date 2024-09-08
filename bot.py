import telebot
from secrets import secrets
from handlers import register_handlers

# Initialize bot
token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

# Register all the handlers
register_handlers(bot)

# Start polling
bot.polling(none_stop=True, interval=0)
