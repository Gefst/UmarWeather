import requests
import datetime
from config import tg_bot_token, open_weather_token
from telebot import TeleBot
from telebot import types

bot = TeleBot(tg_bot_token)

@bot.message_handler(commands=["start"])
def start(message: types.Message):
    mess = f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>"
    bot.reply_to(message, mess, parse_mode="html")

@bot.message_handler()
def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        r.raise_for_status()  # Check if the request was successful

        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!")

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        bot.reply_to(message, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***"
              )

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"\U00002620 Ошибка при запросе к OpenWeatherMap API: {e} \U00002620")
    except Exception as e:
        bot.reply_to(message, f"\U00002620 Произошла ошибка: {e} \U00002620")

if __name__ == "__main__":
    bot.polling(none_stop=True)



