# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lehsuby/PycharmProjects/chatbotEORA/app/__init__.py
# Compiled at: 2019-08-26 17:41:34
# Size of source mod 2**32: 9453 bytes
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time as ttime
from datetime import datetime, timedelta
import pathlib, os, shutil
from subprocess import call
con = psycopg2.connect(dbname='db_chatbotEORA', user='tu', host='localhost', password='qwerty')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
MAIN_DIRECTORY = '/home/lehsuby/PycharmProjects/chatbotEORA/app/src'
NICKNAME = 'Привет! Меня зовут EORA. Как тебя зовут (введи user_id)?'
START_MESSAGE = 'Я помогу отличить кота от хлеба! Объект перед тобой квадратный?'
ITS_BREAD = 'Это хлеб, а не кот! Ешь его!'
ITS_CAT = 'Это кот, а не хлеб! Не ешь его!'
ADD_QUESTION = 'У него есть уши?'
WRONG_EXP = 'Я не понимаю вас'
POSITIVE_ANSWER = ['да', 'конечно', 'ага', 'пожалуй']
NEGATIVE_ANSWER = ['нет', 'нет, конечно', 'ноуп', 'найн']
START_COMMAND = ['/start']
CHECK_USER = 'SELECT *\n                    FROM public.users\n                    WHERE user_id = %s'
CHECK_MESSANGES = 'SELECT *\n                        FROM public.answers\n                        WHERE user_id = %s\n                        ORDER BY time_message'
INSERT_USER = 'INSERT INTO users VALUES (%s)'
INSERT_MESSAGE = 'INSERT INTO answers VALUES (%s,%s,%s,%s,%s)'
FIND_LAST_STATUS = 'SELECT task_status\n                        FROM public.answers\n                        WHERE time_message=(SELECT MAX(time_message)\n                                                FROM public.answers\n                                                WHERE user_id = %s)'
TAG_INPUT_WITH_ID = '</scroll-container></body>\n  <div style="float: left;">\n  <form action = "/eora/api/" method="get" class="input_message">\n    <input type="text" name="msg" required="required">\n    <input type="hidden" name="user_id" value=%s>\n    <input type="submit" value="Отправить">\n  </form>\n  </div>\n  <div style="float: right;">\n  <form action="/eora/api/" method="post" enctype="multipart/form-data" class="input_message">\n    <input type="file" name="file" accept="image/jpeg,image/png" required autofocus>\n    <input type="hidden" name="user_id" value=%s>\n    <input type="submit" value="Отправить на обработку"/>\n  </form>\n  </div>\n  <script type="text/javascript">\n  var messageBody = document.querySelector(\'scroll-container\');\n    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;\n</script>'
TAG_INPUT_WITOUT_ID = '</scroll-container></body>\n  <form action = "/eora/api/" method="get" class="input_message" class="input_file">\n    <input type="text" name="user_id" required="required">\n    <input type="submit" value="Отправить">\n  </form>\n  <script>\n  var messageBody = document.querySelector(\'scroll-container\');\n    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;\n</script>'
STYLES = '<style>#input_message{\n                    display: inline_block;\n                    position: fixed; \n                    margin-top: 10px;\n                    bottom: 0;\n                    }\n                    .name_bot{\n                    font: bold 2em Arial, Tahome, sans-serif;\n                    position: fixed;\n                    width: 100%;\n                    margin-bottom: 10px; \n                    text-align: center;\n                    top: 0;\n                    }\n                    scroll-container {\n                    outline: 2px solid #000;\n                    display: block;\n                    height: 90%;\n                    margin: 50px auto 20px;\n                    overflow-y: auto;\n                    }\n</style>\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>\n<body>\n<div class="name_bot">EORA - your personal bot</div>\n<scroll-container>\n'
UPLOAD_FILE = '\n<form action="/eora/api" method="post" enctype="multipart/form-data"">\n    <input type="file" name="file" accept="image/jpeg,image/png" required autofocus>\n    <input type="submit" value="Отправить на обработку"/>\n</form>'
app = Flask(__name__)

def get_history(user_id):
    cur = con.cursor()
    cur.execute(CHECK_MESSANGES, [user_id])
    rows = cur.fetchall()
    history = STYLES
    for row in rows:
        if row[4] == 0:
            history = history + row[0] + '<br />' + row[1].strftime('%Y-%m-%d %H:%M') + '<br />'
        else:
            history = history + "<p align='right'>" + row[0] + '<br />' + row[1].strftime('%Y-%m-%d %H:%M') + '</p><br />'

    return history


def get_last_status(user_id):
    cur = con.cursor()
    cur.execute(FIND_LAST_STATUS, [user_id])
    return cur.fetchone()[0]


def prediction(name_file, user_id):
    f = open('src/%s_logfile_1.txt' % user_id, 'w')
    call_string = 'python scripts/label_image.py --image src/%s' % name_file
    call(call_string, stdout=f, shell=True)
    with open('src/%s_logfile_1.txt' % user_id, 'r') as (f):
        data = f.readlines()
    cat = data[3]
    cat = float(cat[12:19])
    bread = data[4]
    bread = float(bread[13:20])
    os.remove('src/%s_logfile_1.txt' % user_id)
    os.remove('src/%s' % name_file)
    if cat > bread:
        return ITS_CAT
    else:
        return ITS_BREAD


@app.route('/eora/api/', methods=['GET', 'POST'])
def get_bot_response():
    cur = con.cursor()
    t = datetime.fromtimestamp(ttime.time())
    if request.method == 'POST':
        static_file = request.files['file']
        full_name_file = static_file.filename
        name_file = full_name_file.replace(' ', '')
        static_file.save('src/' + name_file)
        user_id = request.form['user_id'].strip()
        answer = prediction(name_file, user_id)
        cur.execute(INSERT_MESSAGE, (full_name_file, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 0, '1'))
        t = datetime.fromtimestamp(ttime.time())
        cur.execute(INSERT_MESSAGE, (answer, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 0, '0'))
        history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id, user_id)
        return history
    if not request.args.get('msg'):
        if not request.args.get('user_id'):
            history = get_history('') + NICKNAME + TAG_INPUT_WITOUT_ID
            return history
        else:
            user_id = request.args.get('user_id').strip()
            cur.execute(CHECK_USER, [user_id])
            if cur.rowcount == 0:
                cur.execute(INSERT_USER, [user_id])
                message = 'Привет, ' + user_id + '!!! ' + START_MESSAGE
                cur.execute(INSERT_MESSAGE, (message, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 0, '0'))
                history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id, user_id)
                return history
            message = 'И снова здравствуй, ' + user_id + '!!! ' + START_MESSAGE
            cur.execute(INSERT_MESSAGE, (message, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 0, '0'))
            history = get_history(user_id) + TAG_INPUT_WITH_ID % (user_id, user_id)
            return history
    else:
        user_id = request.args.get('user_id').strip()
        last_status = get_last_status(user_id)
        print(last_status)
        message = request.args.get('msg').strip().lower()
        cur.execute(INSERT_MESSAGE, (message, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, last_status, '1'))
        history = get_history(user_id)
        t = datetime.fromtimestamp(ttime.time())
        if message in START_COMMAND:
            cur.execute(INSERT_MESSAGE, (START_MESSAGE, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 0, '0'))
            history += START_MESSAGE + '<br />' + t.strftime('%Y-%m-%d %H:%M')
        else:
            if last_status == 2:
                cur.execute(INSERT_MESSAGE, (WRONG_EXP, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 2, '0'))
                history += WRONG_EXP + '<br />' + t.strftime('%Y-%m-%d %H:%M')
            else:
                if message in POSITIVE_ANSWER:
                    if last_status == 0:
                        cur.execute(INSERT_MESSAGE, (ADD_QUESTION, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 1, '0'))
                        history += ADD_QUESTION + '<br />' + t.strftime('%Y-%m-%d %H:%M')
                    elif last_status == 1:
                        cur.execute(INSERT_MESSAGE, (ITS_CAT, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 2, '0'))
                        history += ITS_CAT + '<br />' + t.strftime('%Y-%m-%d %H:%M')
                else:
                    if message in NEGATIVE_ANSWER:
                        if last_status == 0:
                            cur.execute(INSERT_MESSAGE, (ITS_CAT, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 2, '0'))
                            history += ITS_CAT + '<br />' + t.strftime('%Y-%m-%d %H:%M')
                        elif last_status == 1:
                            cur.execute(INSERT_MESSAGE, (ITS_BREAD, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, 2, '0'))
                            history += ITS_BREAD + '<br />' + t.strftime('%Y-%m-%d %H:%M')
                    else:
                        cur.execute(INSERT_MESSAGE, (WRONG_EXP, t.strftime('%Y-%m-%d %H:%M:%S.%f'), user_id, last_status, '0'))
                        history += WRONG_EXP + '<br />' + t.strftime('%Y-%m-%d %H:%M')
            history += TAG_INPUT_WITH_ID % (user_id, user_id)
            return history


if __name__ == '__main__':
    app.run(debug=False)