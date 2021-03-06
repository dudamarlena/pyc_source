# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eschool/eschool_base.py
# Compiled at: 2019-10-01 15:29:44
# Size of source mod 2**32: 3047 bytes
import hashlib, json
from requests import Session
from requests.cookies import cookiejar_from_dict
import getpass
PERIOD = '145625'
m = hashlib.sha256()

class EschoolBase:

    def __init__(self, cookies=None, handled_homeworks=None, handled_msgs=None, handled_marks=None, period=PERIOD):
        self.session = Session()
        if cookies:
            self.session.cookies = cookies
        self.handled_marks = handled_marks or []
        self.handled_msgs = handled_msgs or []
        self.handled_homeworks = handled_homeworks or []
        self.period = period
        self.homework_handler = None
        self.mark_handler = None
        self.message_handler = None

    @classmethod
    def login(cls, login, password=None, period=None):
        """
        Login to the account
        """
        self = cls(period=period)
        password = password or getpass.getpass('Eschool password: ')
        m.update(password.encode())
        password = m.hexdigest()
        self.session.post('https://app.eschool.center/ec-server/login', data={'username':login, 
         'password':password})
        return self

    def save(self, filename='eschool_account'):
        """
        Save account to file
        :param filename: filename
        """
        filename = filename
        with open(filename, 'w') as (f):
            f.write(json.dumps((
             self.session.cookies.get_dict(), self.handled_homeworks, self.handled_msgs, self.handled_marks)))

    @classmethod
    def from_file(cls, filename):
        """
        Restore from file
        :param filename: filename
        :return: session
        """
        with open(filename) as (f):
            cookies, homeworks, msgs, marks = json.loads(f.read())
            cookies = cookiejar_from_dict(cookies)
        self = cls(cookies, homeworks, msgs, marks)
        return self

    def get(self, method, **kwargs):
        resp = self.session.get(f"https://app.eschool.center/ec-server/{kwargs.get('prefix', 'student')}/{method}/?userId=108217&eiId={self.period}" + ('&' if kwargs else '') + '&'.join([key + '=' + str(kwargs[key]) for key in kwargs.keys() if key != 'prefix']))
        resp.raise_for_status()
        return resp.json()

    def on_homework(self, func):
        """
        Decorator for handling event (adding homework)
        """
        self.homework_handler = func

    def on_mark(self, func):
        """
        Decorator for handling event (adding mark)
        """
        self.mark_handler = func

    def on_message(self, func):
        """
        Decorator for handling event (adding message)
        """
        self.message_handler = func

    def download_file(self, file_id):
        """
        Download file with file_id
        :param file_id: file id
        :return: raw file content (bytes)
        """
        result = self.session.get(f"https://app.eschool.center/ec-server/files/{file_id}")
        return result.content