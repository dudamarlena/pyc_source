# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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