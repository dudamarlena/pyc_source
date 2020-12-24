# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\discord\config.py
# Compiled at: 2020-03-30 02:47:10
# Size of source mod 2**32: 1770 bytes
import os, logging.config
from colorama import Fore
signal = os.getenv('DISCORD_SIGNAL_CHAR') or '!'
max_workers = os.getenv('DISCORD_MAX_WORKERS', 10)
public_ip = os.getenv('PUBLIC_ADDRESS', None)
public_path = os.getenv('PUBLIC_DATA_PATH', None)
os.makedirs('logs', exist_ok=True)
logging.config.dictConfig({'version':1, 
 'disable_existing_loggers':True, 
 'formatters':{'console':{'format':Fore.CYAN + '%(asctime)s' + Fore.RESET + ' ' + Fore.GREEN + '%(levelname)-8s' + Fore.RESET + ' %(message)s', 
   'datefmt':'%H:%M:%S'}, 
  'file':{'format':'%(asctime)s [%(process)d] %(levelname)s\n%(name)s: %(message)s\n', 
   'datefmt':'%Y-%m-%d %H:%M:%S'}}, 
 'handlers':{'console':{'formatter':'console', 
   'class':'logging.StreamHandler', 
   'stream':'ext://sys.stdout'}, 
  'file':{'formatter':'file', 
   'class':'logging.handlers.RotatingFileHandler', 
   'filename':'logs/discord-bot.log', 
   'maxBytes':10485760, 
   'backupCount':5, 
   'encoding':'utf-8'}}, 
 'loggers':{'': {'handlers':[
        'console', 'file'], 
       'level':logging.INFO}}})