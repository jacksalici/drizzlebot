import requests
import json
from stuffs import *
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import os
import psycopg2


def start_command(update, context):
    update.message.reply_text('Hi!')

    conn = None
    try:

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(os.environ['DATABASE_URL'])

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




def weather_command(update, context):
    icon_set = ['', '', '🌩', '🌦', '', '🌧', '🌨', '', '⛅', '☀']
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,alerts," \
          "hourly&appid=%s&units=metric" % (
              lat, lon, os.environ['OW_API_KEY'])

    response = requests.get(url)
    today_data = json.loads(response.text)["daily"][0]

    if float(today_data['weather'][0]['id']) == 800.0:
        icon = icon_set[9]
    else:
        icon = icon_set[round(float(today_data['weather'][0]['id']) / 100)]

    if datetime.datetime.now().hour < 12:
        greetings = "Good morning"
    elif datetime.datetime.now().hour < 18:
        greetings = "Good day"
    else:
        greetings = "Good evening"

    weather_message = f"{greetings}, today's forecast is for {today_data['weather'][0]['description']} {icon} with temperatures between {round(float(today_data['temp']['min']))} and {round(float(today_data['temp']['max']))}°C."

    update.message.reply_text(weather_message)






def main():
    PORT = int(os.environ.get('PORT', 8443))

    updater = Updater(os.environ['TG_BOT_TOKEN'], use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("forecast", weather_command))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=os.environ['TG_BOT_TOKEN'],
                          webhook_url='https://brizzle.herokuapp.com/' + os.environ['TG_BOT_TOKEN'])

    updater.idle()


if __name__ == '__main__':
    main()
