# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/SendTaskToTrello.py
# Compiled at: 2020-05-12 23:12:16
# Size of source mod 2**32: 1637 bytes
from trello import TrelloClient
from polical import connectSQLite
from polical import configuration
from datetime import datetime
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def SendTaskToTrello(username, user_dict):
    client = TrelloClient(api_key=(user_dict['api_key']),
      api_secret=(user_dict['api_secret']),
      token=(user_dict['oauth_token']),
      token_secret=(user_dict['oauth_token_secret']))
    member_id = user_dict['owner_id']
    subjectsBoard = client.get_board(user_dict['board_id'])
    tasks = connectSQLite.getTasks(username)
    if len(tasks) == 0:
        logging.info('No existen tareas nuevas, verifique consultando el calendario')
        print('No existen tareas nuevas, verifique consultando el calendario')
    else:
        for x in tasks:
            logging.info('Agregando Tarea:' + x.subjectID + ' ' + x.title + ' ' + x.description + ' ' + x.due_date)
            print('Agregando Tarea:')
            x.print()
            subjectList = subjectsBoard.get_list(x.subjectID)
            card = subjectList.add_card(x.title, x.description.replace('\\n', '\n'))
            card.assign(member_id)
            x.due_date = x.due_date[0:10] + ' 07:00:00'
            card.set_due(datetime.strptime(x.due_date, '%Y-%m-%d %H:%M:%S'))
            connectSQLite.addTarTID(x.id, subjectList.list_cards()[(-1)].id, username)