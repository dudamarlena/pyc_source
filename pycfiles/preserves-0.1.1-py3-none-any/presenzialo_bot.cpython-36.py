# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/presenzialo_bot.py
# Compiled at: 2020-01-27 05:59:20
# Size of source mod 2**32: 6290 bytes
import os, re, sys, datetime, configparser
from threading import Thread
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=(logging.INFO))
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from .presenzialo_auth import PRauth, config_auth
from .presenzialo_web import PRweb
from .presenzialo_day import PRday
from .presenzialo_address import PRaddress

def get_token(config_file):
    parser = configparser.ConfigParser()
    parser.read(config_file)
    return parser.get('PRbot', 'token')


token = get_token(config_auth)
logging.info('found token %s', token)
bot = Bot(token=token)
updater = Updater(token=token)

def get_prweb():
    logging.info('getting PRweb')
    return PRweb(PRauth())


def _message_format(msg):
    return re.sub('[.\\.]+', ' ', msg)


def bot_wakeup(bot, update):
    keyboard = [
     [
      KeyboardButton('/time', True, True), KeyboardButton('/stamp', True, True)]]
    keyboard = [
     [
      InlineKeyboardButton('time', callback_data='time'),
      InlineKeyboardButton('stamp', callback_data='stamp')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('inline button commands', reply_markup=reply_markup)
    update.message.reply_text('type /help for more commands')


def bot_print(bot, update, msg):
    bot.sendMessage(parse_mode='HTML',
      chat_id=(update.message.chat.id),
      text=('<pre>' + msg + '</pre>'))


def call_prlo(func):

    def wrapped(bot, update, *args, **kwargs):
        logging.info('calling %s', func.__name__)
        ret = func(bot, update, *args, **kwargs)
        bot_wakeup(bot, update)
        logging.info('well done %s', func.__name__)
        return ret

    return wrapped


def get_today():
    today = datetime.date.today()
    logging.info('day arg %s', today)
    pr_day = PRday(get_prweb().timecard(today, today))
    day = pr_day.days[0]
    return day


@call_prlo
def time(bot, update):
    """bot command for uptime"""
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    day = get_today()
    msg = 'Today  {}\n'.format(day.date().date())
    msg += 'Uptime {}\n'.format(day.uptime())
    bot_print(bot, update, msg)


@call_prlo
def stamp(bot, update):
    """bot command for time stamps"""
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    day = get_today()
    msg = 'Today  {}\n'.format(day.date().date())
    msg += 'Stamps {}\n'.format(', '.join([i.time().strftime('%H:%M') for i in day.logs()]))
    bot_print(bot, update, msg)


@call_prlo
def present(bot, update, args):
    """bot command for worker's presence"""
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    address = PRaddress(get_prweb())
    workers = address.present(args)
    msg = "Workers' status:\n"
    msg += str(address)
    bot_print(bot, update, msg)


@call_prlo
def phone(bot, update, args):
    """bot command for worker's phone"""
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    address = PRaddress(get_prweb())
    workers = address.phone(args)
    msg = "Worker's phone:\n"
    msg += str(workers)
    bot_print(bot, update, msg)


@call_prlo
def help(bot, update):
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    msg = 'HRbot help\n\n/bot\n   inline button command\n\n/time\n   today uptime\n/stamp\n   today time stamps\n\n/in name [name ...]\n   worker status\n/phone 12345 [12345 ...]\n   phone from phone number\n\n/restart\n   restart HRbot\n\n/help\n   print this help\n    '
    update.message.reply_text(msg)


def button(bot, update):
    query = update.callback_query
    globals()[query.data](bot, query)


def stop(bot, update):
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    bot.send_message(chat_id=(update.message.chat_id), text='stop me please')
    updater.stop()


def stop_and_restart():
    updater.stop()
    (os.execl)(sys.executable, sys.executable, *sys.argv)


def restart(bot, update):
    bot.send_chat_action(chat_id=(update.message.chat_id), action=(ChatAction.TYPING))
    update.message.reply_text('bot is restarting ...')
    Thread(target=stop_and_restart).start()


def main():
    updater.dispatcher.add_handler(MessageHandler(Filters.text, bot_wakeup))
    updater.dispatcher.add_handler(CommandHandler('bot', bot_wakeup))
    updater.dispatcher.add_handler(CommandHandler('stamp', stamp))
    updater.dispatcher.add_handler(CommandHandler('time', time))
    updater.dispatcher.add_handler(CommandHandler('in', present, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('phone', phone, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(CommandHandler('restart', restart))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()