import telebot
import requests

# Вставьте свой API ключ из RapidAPI и токен Telegram бота
API_KEY = '19da571f01msh286ccd6bf50a5d2p1314f4jsnc6c40dd61c10'
BOT_TOKEN = '7441793544:AAFKMo4vHdm-4cgj1w4KrHpvAj2bHmqs7WI'

bot = telebot.TeleBot(BOT_TOKEN)

def search_hotels(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "en_US"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Введите название города для поиска отелей.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text
    bot.reply_to(message, f"Ищу отели в {city}...")
    
    # Поиск отелей через API
    data = search_hotels(city)
    
    try:
        locations = data['suggestions'][0]['entities']
        if locations:
            response_text = "Найденные отели:\n\n"
            for location in locations:
                response_text += f"🏨 {location['name']} - {location['caption']}\n"
            bot.reply_to(message, response_text)
        else:
            bot.reply_to(message, "Отелей не найдено.")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при поиске отелей.")

# Запуск бота
bot.polling()
