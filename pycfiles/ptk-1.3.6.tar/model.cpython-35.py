# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/analyzer/model.py
# Compiled at: 2017-02-04 11:29:39
# Size of source mod 2**32: 3617 bytes
import pymysql.cursors, pickle

class Author(object):
    """Author"""

    @classmethod
    def load_from_mysql(cls, user, password, host, database):
        conn = pymysql.connect(user=user, password=password, host=host, database=database)
        try:
            with conn.cursor() as (cur):
                sql = 'SELECT id,name,rate from articles_authors;'
                cur.execute(sql)
                ret = [Author(r[0], r[1], r[2]) for r in cur.fetchall()]
        finally:
            conn.close()

        return ret

    def save(self, user, password, host, database):
        conn = pymysql.connect(user=user, password=password, host=host, database=database)
        try:
            with conn.cursor() as (cur):
                sql = 'UPDATE articles_authors   SET rate=%s   WHERE id=%s;'
                cur.execute(sql, (str(self.rate), self.id))
        finally:
            conn.close()

    def __init__(self, id, name, rate):
        self.id = id
        self.name = name
        self.rate = rate

    def __eq__(self, other):
        assert type(other) is Author
        return self.name == other.name and self.id == other.id

    def __ne__(self, other):
        assert type(other) is Author
        return self.name != other.name and self.id == other.id

    def __hash__(self):
        return self.id.__hash__()


class Article(object):
    """Article"""

    @classmethod
    def load_from_mysql(cls, user, password, host, database, pkl_base_dir):
        conn = pymysql.connect(user=user, password=password, host=host, database=database)
        ret = []
        try:
            with conn.cursor() as (cur):
                sql = 'select   art.id,  art.pub_date,  art.url,  auh.id,  auh.name,  auh.rate from   articles_articles art JOIN   articles_authors auh on art.author_id = auh.id;'
                cur.execute(sql)
                for r in cur.fetchall():
                    try:
                        topics = Article.load_from_pickel(pkl_base_dir, r[0])
                        a = Article(r[0], Author(r[3], r[4], r[5]), r[1], r[2], topics)
                        ret.append(a)
                    except FileNotFoundError as e:
                        print('File Not Found', e)

        finally:
            conn.close()

        return ret

    @classmethod
    def load_from_pickel(cls, base_dir, id):
        return pickle.load(open('{}/{}.pkl'.format(base_dir, id), 'rb'))

    def __init__(self, id, author, pub_time, url, topics):
        self.id = id
        self.author = author
        self.pub_time = pub_time
        self.url = url
        self.topics = topics

    def get_topic_prob(self, t_id):
        """
        Get probability of given topic id
        :param t_id:
        :return: probability
        """
        for t in self.topics:
            if t[0] == t_id:
                return t[1]