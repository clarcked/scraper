import urllib.request
import threading
from typing import Any

from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
import telegram_send
from telegram.update import Update


def send_msg(bot, update, message):
    chat_id = update.message.chat_id
    print(chat_id)
    bot.send_message(chat_id=chat_id, text=message)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def hay_turno():
    host = 'https://titulosvalidez.educacion.gob.ar/validez/v_turnos/inicio12.php'
    test = 'Disculpe por favor. Por el momento no hay'
    print("checking to target....")
    html = urllib.request.urlopen(host).read().decode('iso-8859-1')
    print('testing: {}'.format(test))
    passed = test not in str(html)
    print('test passed: {}'.format(passed))
    return passed


def start(update=None, context=None):
    hay = hay_turno()
    if hay:
        print("hay turno enviamos la notification")
        message = 'sí, hay turnos appurate...'
        if context:
            bot = context.bot
            send_msg(bot=bot, update=update, message=message)
        else:
            telegram_send.send(messages=[message])
    else:
        print("no hay turno")
        if context:
            bot = context.bot
            send_msg(bot=bot, update=update, message="no hay turnos...")


def main():
    token = '1787635419:AAFy_1HCK0usZ5KtDXNTTWP6PdS1D49HlQg'
    print('starting telegram clarcked bot')
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('titulos', start))
    print('bot is ready ...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    process = set_interval(main, 20)
