from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from emoji import emojize
from uuid import uuid4
#import Reports
import os
import requests
from lxml import html
from bs4 import BeautifulSoup as bs

USER = {}
PORT = int(os.environ.get('PORT', '5000'))

def start(bot, update):
    global USER
    chat_id    = update.effective_chat.id
    #aerodrome  = update.message.text

    USER[chat_id] = []
    msg = """به ربات هواشناسی هوانوردی ایران خوش آمدید.

جهت مشاهده گزارشات، روی دکمه مورد نظر کلیک فرمایید.
"""
    keyboard = []
    row = []
    row.append(InlineKeyboardButton('METAR', switch_inline_query_current_chat = 'METAR/OI'))
    row.append(InlineKeyboardButton('TAF', switch_inline_query_current_chat = 'TAF/OI'))
    keyboard.append(row)
    row = []
    row.append(InlineKeyboardButton('Area Forcasts', callback_data = 'area'))
    keyboard.append(row)
    row = []
    row.append(InlineKeyboardButton('SIGMET', callback_data = 'sigmet'))
    row.append(InlineKeyboardButton('AIRMET', callback_data = 'airmet'))

    keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    #msg = Reports.metar(bot, aerodrome, chat_id)
    bot.sendMessage(chat_id = chat_id,
                    text = msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)

def inlinequery(bot, update):
    query = update.inline_query.query

    try:
        aerodromes = {
        'OIII': 'مهرآباد-http://s9.picofile.com/file/8365204700/OIII.png',
        'OITT': 'تبریز-http://s9.picofile.com/file/8365205050/OITT.png',
        'OIMM': 'مشهد-http://s8.picofile.com/file/8365204892/OIMM.png',
        'OISS': 'شیراز-http://s9.picofile.com/file/8365204984/OISS.png',
        'OIFM': 'اصفهان-http://s8.picofile.com/file/8365204584/OIFM.png',
        'OIAA': 'آبادان-http://s8.picofile.com/file/8365204300/OIAA.png',
        'OIAW': 'اهواز-http://s8.picofile.com/file/8365204334/OIAW.png',
        'OITR': 'ارومیه-http://s8.picofile.com/file/8365205034/OITR.png',
        'OITP': 'پارس آباد مغان-http://s9.picofile.com/file/8365175892/3.png',
        'OITM': 'سهند مراغه-http://s9.picofile.com/file/8365175892/3.png',
        'OITL': 'اردبیل-http://s8.picofile.com/file/8365205018/OITL.png',
        'OITZ': 'زنجان-http://s8.picofile.com/file/8365205084/OITZ.png',
        'OIGG': 'رشت-http://s9.picofile.com/file/8365204626/OIGG.png',
        'OINR': 'رامسر-http://s9.picofile.com/file/8365204968/OINR.png',
        'OINN': 'نوشهر-http://s9.picofile.com/file/8365175892/3.png',
        'OINZ': 'ساری-http://s9.picofile.com/file/8365204976/OINZ.png',
        'OING': 'گرگان-http://s9.picofile.com/file/8365204942/OING.png',
        'OINE': 'کلاله-http://s9.picofile.com/file/8365175892/3.png',
        'OIAG': 'آغاجاری-http://s9.picofile.com/file/8365175892/3.png',
        'OIAH': 'گچساران-http://s9.picofile.com/file/8365175892/3.png',
        'OIAI': 'مسجد سلیمان-http://s9.picofile.com/file/8365175892/3.png',
        'OIAM': 'بندر ماهشهر-http://s9.picofile.com/file/8365175892/3.png',
        'OIBA': 'ابوموسی-http://s9.picofile.com/file/8365175892/3.png',
        'OIBB': 'بوشهر-http://s9.picofile.com/file/8365204368/OIBB.png',
        'OIBJ': 'جام جم-http://s9.picofile.com/file/8365175892/3.png',
        'OIBK': 'کیش-http://s9.picofile.com/file/8365204384/OIBK.png',
        'OIBL': 'بندر لنگه-http://s9.picofile.com/file/8365204426/OIBL.png',
        'OIBP': 'عسلویه / خلیج فارس-http://s9.picofile.com/file/8365175892/3.png',
        'OIBQ': 'خارک-http://s9.picofile.com/file/8365175892/3.png',
        'OIBS': 'سیری-http://s9.picofile.com/file/8365175892/3.png',
        'OIBV': 'لاوان-http://s9.picofile.com/file/8365175892/3.png',
        'OICC': 'کرمانشاه-http://s9.picofile.com/file/8365204450/OICC.png',
        'OICI': 'ایلام-http://s8.picofile.com/file/8365204476/OICI.png',
        'OICK': 'خرم آباد-http://s9.picofile.com/file/8365204492/OICK.png',
        'OICS': 'سنندج-http://s9.picofile.com/file/8365204526/OICS.png',
        'OIFK': 'کاشان-http://s8.picofile.com/file/8365204550/OIFK.png',
        'OIFS': 'شهرکرد-http://s9.picofile.com/file/8365204600/OIFS.png',
        'OIHH': 'همدان-http://s8.picofile.com/file/8365204642/OIHH.png',
        'OIHR': 'اراک-http://s8.picofile.com/file/8365204668/OIHR.png',
        'OIIE': 'امام خمینی (ره)-http://s9.picofile.com/file/8365175892/3.png',
        'OIIK': 'قزوین-http://s9.picofile.com/file/8365204726/OIIK.png',
        'OIIP': 'پیام کرج-http://s8.picofile.com/file/8365204734/OIIP.png',
        'OIIS': 'سمنان-http://s8.picofile.com/file/8365204742/OIIS.png',
        'OIKB': 'بندر عباس-http://s9.picofile.com/file/8365204776/OIKB.png',
        'OIKK': 'کرمان-http://s9.picofile.com/file/8365204800/OIKK.png',
        'OIKQ': 'قشم-http://s8.picofile.com/file/8365204834/OIKQ.png',
        'OIMB': 'بیرجند-http://s9.picofile.com/file/8365204868/OIMB.png',
        'OIMC': 'سرخس-http://s9.picofile.com/file/8365175892/3.png',
        'OIMN': 'بجنورد-http://s9.picofile.com/file/8365175892/3.png',
        'OIMQ': 'کاشمر-http://s9.picofile.com/file/8365175892/3.png',
        'OIMT': 'طبس-http://s9.picofile.com/file/8365204918/OIMT.png',
        'OISF': 'فسا-http://s9.picofile.com/file/8365175892/3.png',
        'OISL': 'لار-http://s9.picofile.com/file/8365175892/3.png',
        'OISR': 'لامرد-http://s9.picofile.com/file/8365175892/3.png',
        'OISY': 'یاسوج-http://s9.picofile.com/file/8365205000/OISY.png',
        'OITU': 'ماکو-http://s9.picofile.com/file/8365175892/3.png',
        'OIYY': 'یزد-http://s9.picofile.com/file/8365205100/OIYY.png',
        'OIZB': 'زابل-http://s8.picofile.com/file/8365205134/OIZB.png',
        'OIZC': 'چابهار-http://s9.picofile.com/file/8365205150/OIZC.png',
        'OIZH': 'زاهدان-http://s8.picofile.com/file/8365205192/OIZH.png',
        'OIZJ': 'جاسک-http://s9.picofile.com/file/8365175892/3.png',
        'OIZI': 'ایرانشهر-http://s9.picofile.com/file/8365175892/3.png'
        }
        result = []
        for aerodrome in sorted(aerodromes.keys()):
            if query.split("/")[1].upper() in aerodrome:
                result.append(InlineQueryResultArticle(
                id=uuid4(),
                title=aerodrome,
                description=aerodromes[aerodrome].split("-")[0],
                #http://s9.picofile.com/file/8365175892/3.png
                thumb_url=aerodromes[aerodrome].split("-")[1],
                thumb_width=512,
                thumb_height=512,
                input_message_content=InputTextMessageContent(
                    query.split('/')[0].upper() + "/" + aerodrome)))
    except:
        pass
    update.inline_query.answer(result)


def message(bot, update):
    global USER

    chat_id     = update.effective_chat.id              # chat_id of the user
    aerodrome   = update.effective_message.text         # chosen inline result by a user

    if 'METAR' in aerodrome.upper():
        msg = metar(bot, aerodrome.split("/")[1], chat_id)
    elif 'TAF' in aerodrome.upper():
        msg = taf(bot, aerodrome.split("/")[1], chat_id)
    bot.sendMessage(text=msg,
                          chat_id=chat_id,
                          parse_mode=ParseMode.MARKDOWN)

def taf(bot, aerodrome, chat_id):
    bot.sendMessage(chat_id = chat_id,
                    text = "Getting TAF Data ...")
    try:
        taf_data    = requests.get("https://www.aviationweather.gov/taf/data?ids=%s&format=raw&date=&submit=Get+TAF+data" % aerodrome)
        taf_soup    = bs(taf_data.content, "html.parser")
        taf_code    = taf_soup.findAll("code")[0].text
    except:
        taf_code = "..."

    msg = """%s *TAF Data:*
        _%s_
    """ % (emojize(":information_source:", use_aliases=True),
        taf_code)

    return msg

def metar(bot, aerodrome, chat_id):
    bot.sendMessage(chat_id = chat_id,
                    text = "Getting METAR Data ...")
    metar_data  = requests.get("https://www.aviationweather.gov/metar/data?ids=%s&format=decoded&hours=0&taf=off&layout=on" % aerodrome)
    metar_soup  = bs(metar_data.content, "html.parser")
    table       = metar_soup.findAll("td")
    station = date = time = temperature = pressure_hPa = pressure_inch = dew_point = wind_direction = wind_speed_mph = wind_speed_knot = RH = visibility = weather = clouds = "..."
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
                pressure_hPa  = table[td + 1].text.split(" (")[1][:-1].strip().replace("mb", "hPa")
                if " A2" in text:
                    pressure_inch = text[text.index(" A2") + 2:text.index(" A2") + 4] + "." + text[text.index(" A2") + 4: text.index(" A2") + 6] + " inches Hg"
                if " A3" in text:
                    pressure_inch = text[text.index(" A3") + 2:text.index(" A3") + 4] + "." + text[text.index(" A3") + 4: text.index(" A3") + 6] + " inches Hg"
                #pressure_inch = table[td + 1].text.split(" (")[0].strip()
            if "Dewpoint" in table[td].text:
                dew_point = table[td + 1].text.split(" (")[0].strip()
                RH        = table[td + 1].text.split(" [")[1][:-1]
            if "Winds" in table[td].text:
                if "00000KT" in text:
                    wind = "calm"
                else:
                    wind_direction  = table[td + 1].text.split(" degrees")[0].split("(")[1].strip()
                    wind_speed_knot = table[td + 1].text.split(" at ")[1].split(" knots")[0].split("(")[1].strip()
                    #wind_speed_mph  = table[td + 1].text.split(" at ")[1].split(" MPH")[0].strip()
                    wind = """direction:   %s degrees
        speed:       %s knots ( %s m/s)""" % (wind_direction,
                                    wind_speed_knot,
                                    str(int(wind_speed_knot) / 2))

            if "Visibility" in table[td].text:
                visibility = table[td + 1].text.split(" (")[1][:-1].strip()
                try:
                    visibility = visibility.replace("km", "")
                    visibility = visibility.replace("+", "")
                except:
                    pass
                visibility = round(float(visibility))
                if visibility == 10:
                    visibility = "more than 10 km"
                elif visibility >= 5:
                    visibility = str(visibility) + " km"
                else:
                    visibility = str(visibility * 1000) + " m"
            if "Weather" in table[td].text:
                weather = table[td + 1].text.split(" (")[1][:-1].strip()
            if "Clouds" in table[td].text:
                if "NSC" in text:
                    clouds = "Nill Significant Cloud"
                elif "unknown" in table[td + 1].text:
                    clouds = "..."
                else:
                    clouds = table[td + 1].text.strip()
        else:
            pass

    msg = """%s *METAR Data:*
        _%s_

*------* _METAR Decode_ *-----*

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

def main():
    #676428333:AAEYXfSt7tDKsqSzEloCwUDlgFdv-2tq3UU  debug
    #873370289:AAEl2az5yYNkZg5cs57J2-_AThtpC_qOVso  main
    TOKEN = "873370289:AAEl2az5yYNkZg5cs57J2-_AThtpC_qOVso"

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    #Handlers
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(MessageHandler(Filters.text, message))
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.setWebhook("https://iranmeteorologybot.herokuapp.com/" + TOKEN)
    #updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
