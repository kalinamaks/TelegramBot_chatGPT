# This is a sample tg_bot python script uses openai api.
import telebot
import openai
import os
import traceback
import traceback2 as traceback

API_KEY = "yourapi"
BOT_TOKEN = "yourapi"

# Initialize OpenAI API client
openai.api_key = API_KEY

# Initialize Telegram Bot API client
bot = telebot.TeleBot(BOT_TOKEN)

# Store chat history
chat_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Вижу тебя впервые. Давай поговорим?")

# Handle incoming messages
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Save chat history for each user
    if user_id not in chat_history:
        chat_history[user_id] = []
        bot.send_message(chat_id, "Привет! Спроси меня о чём хочешь")

    # Add message to user's chat history
    chat_history[user_id].append(message.text)
    chat_history[user_id] = chat_history[user_id][-10:]  # keep only the last 10 messages

    # Get response from OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text

    # Send response to user
    bot.send_message(chat_id, response)


# Handle exceptions
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            traceback.print_exc()
            return "An error has occurred."

    return wrapper


bot.polling(none_stop=True, interval=0)

# Keep the bot running and restart it if it stops
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        with open("bot_error_log.txt", "a") as f:
            f.write(str(e))
        continue