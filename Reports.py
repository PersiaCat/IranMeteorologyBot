from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from emoji import emojize
import requests
from lxml import html
from bs4 import BeautifulSoup as bs

def metar(bot, aerodrome, chat_id):
    bot.sendMessage(chat_id = chat_id,
                    text = "Getting METAR Data ...")
    r = requests.get("https://www.aviationweather.gov/metar/data?ids=%s&format=decoded&hours=0&taf=off&layout=on" % aerodrome)
    soup = bs(r.content, "html.parser")
    table = soup.findAll("td")
    station = date = time = temperature = pressure_hPa = pressure_inch = dew_point = wind_direction = wind_speed_mph = wind_speed_knot = RH = visibility = weather = clouds = ""
    for td in range(len(table)):
        if ":" in table[td].text:
            if "METAR" in table[td].text:
                station = table[td + 1].text
            if "Text" in table[td].text:
                text = table[td + 1].text
                date = text.split(" ")[1][:2]
                time = text.split(" ")[1][2:6]
                if "CAVOK" in text:
                    weather = "Cloud and Visibility OK"
            if "Temperature" in table[td].text:
                temperature = table[td + 1].text.split(" (")[0].strip()
            if "Pressure" in table[td].text:
                pressure_hPa  = table[td + 1].text.split(" (")[1][:-1].strip()
                pressure_inch = table[td + 1].text.split(" (")[0].strip()
            if "Dewpoint" in table[td].text:
                dew_point = table[td + 1].text.split(" (")[0].strip()
                RH        = table[td + 1].text.split(" [")[1][:-1]
            if "Winds" in table[td].text:
                if "00000KT" in text:
                    wind = "calm"
                else:
                    wind_direction  = table[td + 1].text.split(" degrees")[0].split("(")[1].strip()
                    wind_speed_knot = table[td + 1].text.split(" at ")[1].split(" knots")[0].split("(")[1].strip()
                    wind_speed_mph  = table[td + 1].text.split(" at ")[1].split(" MPH")[0].strip()
                    wind = "from " + wind_direction + " degrees at " + wind_speed_knot + " knots ( " + wind_speed_mph + " MPH )"
            if "Visibility" in table[td].text:
                visibility = table[td + 1].text.split(" (")[1][:-1].strip()
            if "Weather" in table[td].text:
                weather = table[td + 1].text.split(" (")[1][:-1].strip()
            if "Clouds" in table[td].text:
                if "NSC" in text:
                    clouds = "No Significant Cloud"
                else:
                    clouds = table[td + 1].text.strip()
        else:
            pass
    msg = """%s *METAR Data:*
        _%s_

%s *Airport:*
        _%s_

%s *Date and Time:*
        _%s_

%s *Wind:*
        _%s_

%s *Visibility:*
        _%s_

%s *Weather:*
        _%s_

%s *Clouds:*
        _%s_

%s *Temperature:*
        _%s_

%s *Dew Point:*
        _%s_

%s *Pressure:*
        _%s_""" % (emojize(":information_source:", use_aliases=True),
                text,
                emojize(":world_map:", use_aliases=True),
                station,
                emojize(":date:", use_aliases=True),
                date + "th at " + time[:2] +":" + time[2:] + " UTC",
                emojize(":wind_blowing_face:", use_aliases=True),
                wind,
                emojize(":candle:", use_aliases=True),
                visibility,
                emojize(":rainbow:", use_aliases=True),
                weather,
                emojize(":thunder_cloud_and_rain:", use_aliases=True),
                clouds,
                emojize(":thermometer:", use_aliases=True),
                temperature,
                emojize(":droplet:", use_aliases=True),
                dew_point + " ( " + RH + " )",
                emojize(":compression:", use_aliases=True),
                pressure_hPa + " ( " + pressure_inch + " )")
    return msg
