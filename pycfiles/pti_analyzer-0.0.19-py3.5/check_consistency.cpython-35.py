# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/apps/check_consistency.py
# Compiled at: 2017-02-04 06:44:44
# Size of source mod 2**32: 850 bytes
import pymysql.cursors, os

def check_consistency(user, password, host, database):
    conn = pymysql.connect(user=user, password=password, host=host, database=database)
    try:
        with conn.cursor() as (cur):
            sql = 'SELECT id from articles_articles;'
            cur.execute(sql)
            ids = [r[0] for r in cur.fetchall()]
            for id in ids:
                if not os.path.exists('/var/pti/scrape/{}.txt'.format(id)):
                    print('Not found scraped text: id -> {}'.format(id))

    finally:
        conn.close()


if __name__ == '__main__':
    user = os.environ.get('PTI_USER')
    password = os.environ.get('PTI_PASSWORD')
    host = os.environ.get('PTI_HOST')
    db = os.environ.get('PTI_DB')
    check_consistency(user, password, host, db)