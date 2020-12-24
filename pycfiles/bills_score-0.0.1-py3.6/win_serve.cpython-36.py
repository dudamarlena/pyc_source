# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bills_scoring/win_serve.py
# Compiled at: 2018-02-22 23:19:03
# Size of source mod 2**32: 753 bytes
from waitress import serve
from . import hug_api, settings, user_schema_db
import fire

class WindowsServe:

    def server(self):
        serve((hug_api.__hug_wsgi__), listen=('*:{}'.format(settings.LOCAL_HTTPD_PORT)))


def check_if_db_exists():
    import os
    db_path = os.path.join(user_schema_db.file_path, settings.DB_NAME)
    if not os.path.isfile(db_path):
        data_engine = user_schema_db.UserWrapper()
        data_engine.create_db()
        data_engine.create_user('user', 'LOSASASA', 'a12-a23-a34')


def main():
    check_if_db_exists()
    fire.Fire(WindowsServe)


if __name__ == '__main__':
    main()