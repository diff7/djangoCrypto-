import telegram

# use token generated in first step
def send_to_telegram(message):
    bot=telegram.Bot(token='526566168:AAG9Rfu88tUdwtS2t-DZfMzPQ-4zJYnPy6I')
    status = bot.send_message(chat_id="@coinracer", text=message, parse_mode=telegram.ParseMode.HTML)
