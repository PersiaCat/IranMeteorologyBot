from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from emoji import emojize
from uuid import uuid4
import Reports

USER = {}

def start(bot, update):
    global USER
    chat_id    = update.effective_user.id
    #aerodrome  = update.message.text

    USER[chat_id] = []
    msg = """به ربات هواشناسی هوانوردی ایران خوش آمدید.

جهت مشاهده گزارشات، روی دکمه مورد نظر کلیک فرمایید.
"""
    keyboard = []
    row = []
    row.append(InlineKeyboardButton('Metar', switch_inline_query_current_chat = 'OI'))
    keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    #msg = Reports.metar(bot, aerodrome, chat_id)
    bot.sendMessage(chat_id = chat_id,
                    text = msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)

def inlinequery(bot, update):
    query = update.inline_query.query
    chat_id = update.effective_user.id

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
            if query.upper() in aerodrome:
                result.append(InlineQueryResultArticle(
                id=uuid4(),
                title=aerodrome,
                description=aerodromes[aerodrome].split("-")[0],
                #http://s9.picofile.com/file/8365175892/3.png
                thumb_url=aerodromes[aerodrome].split("-")[1],
                thumb_width=512,
                thumb_height=512,
                input_message_content=InputTextMessageContent(
                    aerodrome)))
    except:
        pass
    update.inline_query.answer(result)

def button(bot, update):
    global USER
    #This part gets the user call backs on inline keyboard
    chat_id = update.effective_user.id  # chat_id of the user
    query = update.callback_query       # call back query of the inline keyboard
    option_name = query.data            # call back text
    USER[chat_id].append(option_name)   # adding this text to the USER to track different users status

    chat_id     = query.message.chat_id
    message_id  = query.message.message_id

    # Back
    if option_name == "back":
        USER[chat_id] = USER[chat_id][:-2]

    # Home
    if len(USER[chat_id]) == 0:
        #msg, reply_markup = home(chat_id)
        #bot.editMessageText(text=msg,
        #                      chat_id=chat_id,
        #                      message_id=message_id,
        #                      parse_mode=ParseMode.MARKDOWN,
        #                      reply_markup=reply_markup)
        pass

    # Account
    if len(USER[chat_id]) == 1 and USER[chat_id][0] == 'metar':
        msg = Reports.metar(bot, "OIII", chat_id, message_id)
        bot.editMessageText(text=msg,
                              chat_id=chat_id,
                              message_id=message_id,
                              parse_mode=ParseMode.MARKDOWN)

def message(bot, update):
    global USER

    chat_id     = update.effective_user.id              # chat_id of the user
    aerodrome   = update.effective_message.text         # chosen inline result by a user

    msg = Reports.metar(bot, aerodrome, chat_id)
    bot.sendMessage(text=msg,
                          chat_id=chat_id,
                          parse_mode=ParseMode.MARKDOWN)

def main():
    TOKEN = "873370289:AAEl2az5yYNkZg5cs57J2-_AThtpC_qOVso"

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    #Handlers
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(MessageHandler(Filters.text, message))
    #dispatcher.add_handler(MessageHandler(Filters.document, document))
    dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(CommandHandler("help", howto))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
