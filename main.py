import requests
import json
from stuffs import *
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import os
import psycopg2


def start(update, context):
    update.message.reply_text('Hi!')


def weather_command(update, context):
    icon_set = ['', '', '🌩', '🌦', '', '🌧', '🌨', '', '⛅', '☀']
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,alerts," \
          "hourly&appid=%s&units=metric" % (
              lat, lon, os.environ['OW_API_KEY'])

    # print(url)
    response = requests.get(url)
    today_data = json.loads(response.text)
    # print(json.dumps(today_data, indent=4))
    today_data = json.loads(response.text)["daily"][0]
    
    if float(today_data['weather'][0]['id']) == 800.0:
        icon = icon_set[9]
    else:
        icon = icon_set[round(float(today_data['weather'][0]['id']) / 100)]

    if  datetime.datetime.now().hour<12:
        greetings = "Good morning"
    elif datetime.datetime.now().hour<18:
        greetings = "Good day"
    else:
        greetings = "Good evening"
    
    weather_message = f"{greetings}, today's forecast is for {today_data['weather'][0]['description']} {icon} with temperatures between {round(float(today_data['temp']['min']))} and {round(float(today_data['temp']['max']))}°C."

    update.message.reply_text(weather_message)
    # print(weather_message)

    # send_text = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage?chat_id=' + bot_chatID +
    # '&parse_mode=Markdown&text=' + weather_message print(send_text) response = requests.get(send_text)

    # print(response.json())

    # requests.get(send_message_url)


def main():
    #DATABASE_URL = os.environ[DATABASE_URL]

    #conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    
    PORT = int(os.environ.get('PORT', 8443))

    updater = Updater(os.environ['TG_BOT_TOKEN'], use_context=True)

    dp = updater.dispatcher
    jq = updater.job_queue
    dp.add_handler(CommandHandler("start", weather_command))
    dp.add_handler(CommandHandler("forecast", weather_command))
    # jq.run_daily(weather_command, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(00, 3, 30))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=os.environ['TG_BOT_TOKEN'],
                          webhook_url='https://brizzle.herokuapp.com/' + os.environ['TG_BOT_TOKEN'])

    updater.idle()


if __name__ == '__main__':
    main()
