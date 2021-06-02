import requests

import json
from config import *
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import os
import psycopg2

#DATABASE_URL = os.environ[db_url]

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def weather_command(update, context):
    icon_set = ['', '', '🌩', '🌦', '', '🌧', '🌨', '', '⛅', '☀']
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,alerts," \
          "hourly&appid=%s&units=metric" % (
              lat, lon, api_key)

    # print(url)
    response = requests.get(url)
    today_data = json.loads(response.text)
    # print(json.dumps(today_data, indent=4))
    today_data = json.loads(response.text)["daily"][0]
    if float(today_data['weather'][0]['id']) == 800.0:
        icon = icon_set[9]
    else:
        icon = icon_set[round(float(today_data['weather'][0]['id']) / 100)]

    weather_message = f"Good morning, today's forecast is for {today_data['weather'][0]['description']} {icon} with temperatures between {round(float(today_data['temp']['min']))} and {round(float(today_data['temp']['max']))}°C.";

    update.message.reply_text(weather_message)
    # print(weather_message)

    # send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID +
    # '&parse_mode=Markdown&text=' + weather_message print(send_text) response = requests.get(send_text)

    # print(response.json())

    # requests.get(send_message_url)


def main():
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher
    jq = updater.job_queue
    dp.add_handler(CommandHandler("start", weather_command))
    dp.add_handler(CommandHandler("dourjob", weather_command))
    #jq.run_daily(weather_command, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(00, 3, 30))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
