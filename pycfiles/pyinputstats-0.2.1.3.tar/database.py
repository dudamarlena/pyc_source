# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Desktop/pyInputStats/pyinputstatsmodules/database.py
# Compiled at: 2011-03-28 13:49:02
import os, helpers, sqlite3, time, datetime

class Cursor(object):

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.cursor.close()


class DatabaseConnector(object):

    def __enter__(self):
        path = helpers.get_data_dir()
        self.db_path = os.path.join(path, 'data.db')
        if not os.path.exists(self.db_path):
            self.create_database()
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def create_database(self):
        sql = '\n            CREATE TABLE IF NOT EXISTS data (\n                id INTEGER PRIMARY KEY,\n                pixels INT,\n                clicks INT,\n                keys INT,\n                time INT\n            )'
        sql2 = 'CREATE TABLE IF NOT EXISTS keys (\n                id INTEGER PRIMARY KEY,\n                key STRING UNIQUE,\n                count INT)'
        connection = sqlite3.connect(self.db_path)
        with Cursor(connection) as (cursor):
            cursor.execute(sql)
            cursor.execute(sql2)
        connection.close()

    def get_char_stats(self):
        sql = 'SELECT key, count FROM keys ORDER BY count DESC'
        with Cursor(self.connection) as (cursor):
            return cursor.execute(sql).fetchall()

    def get_stats(self, date=None):
        if not date:
            sql = 'SELECT sum(pixels), sum(clicks), sum(keys) FROM data'
            with Cursor(self.connection) as (cursor):
                return cursor.execute(sql).fetchone()
        elif date == 'today':
            today = datetime.date.today()
            timestamp = time.mktime(today.timetuple())
            sql = '\n            SELECT sum(pixels), sum(clicks), sum(keys) \n            FROM data\n            WHERE time > ?\n            '
            with Cursor(self.connection) as (cursor):
                return cursor.execute(sql, (timestamp,)).fetchone()
        elif isinstance(date, datetime.date):
            timestamp_start = time.mktime(date.timetuple())
            timestamp_end = timestamp_start + 86400
            sql = '\n            SELECT sum(pixels), sum(clicks), sum(keys) \n            FROM data\n            WHERE time > ? AND time < ?\n            '
            with Cursor(self.connection) as (cursor):
                return cursor.execute(sql, (timestamp_start, timestamp_end)).fetchone()
        else:
            (year, month) = date
            timestamp_start = time.mktime(datetime.date(year, month, 1).timetuple())
            if month < 12:
                timestamp_end = time.mktime(datetime.date(year, month + 1, 1).timetuple())
            else:
                timestamp_end = time.mktime(datetime.date(year + 1, 1, 1).timetuple())
            sql = '\n            SELECT sum(pixels), sum(clicks), sum(keys) \n            FROM data\n            WHERE time > ? AND time < ?\n            '
            with Cursor(self.connection) as (cursor):
                return cursor.execute(sql, (timestamp_start, timestamp_end)).fetchone()

    def get_month_data(self, date, day, step=1):
        (year, month) = date
        timestamp_start = time.mktime(datetime.date(year, month, 1).timetuple()) + day * 60 * 60 * 24
        timestamp_end = timestamp_start + step * 60 * 60 * 24
        sql = '\n            SELECT sum(pixels), sum(clicks), sum(keys)\n            FROM data\n            WHERE time > ? AND time < ?\n            '
        with Cursor(self.connection) as (cursor):
            return cursor.execute(sql, (timestamp_start, timestamp_end)).fetchall()

    def get_day_data(self, date, hour, step=1):
        timestamp_start = time.mktime(date.timetuple()) + hour * 60 * 60
        timestamp_end = timestamp_start + step * 60 * 60
        sql = '\n            SELECT sum(pixels), sum(clicks), sum(keys)\n            FROM data\n            WHERE time > ? AND time < ?\n            '
        with Cursor(self.connection) as (cursor):
            return cursor.execute(sql, (timestamp_start, timestamp_end)).fetchall()

    def insert(self, data):
        sql = 'INSERT OR IGNORE INTO data (\n            pixels,\n            clicks,\n            keys,\n            time\n        ) VALUES (?, ?, ?, ?)'
        sql2 = 'INSERT OR IGNORE INTO keys (\n            key,\n            count\n        ) VALUES (?, 0)'
        sql3 = ' UPDATE keys SET count = count+? WHERE key=?'
        with Cursor(self.connection) as (cursor):
            cursor.execute(sql, (data['distance'], data['buttons'], data['keys'], data['time']))
            cursor.executemany(sql2, ((i[0],) for i in data['keys_pressed']))
            cursor.executemany(sql3, (i[::-1] for i in data['keys_pressed']))
        self.connection.commit()

    def get_num_days(self):
        sql = 'SELECT time FROM data ORDER BY time ASC'
        with Cursor(self.connection) as (cursor):
            first = cursor.execute(sql).fetchone()
            if first:
                first = first[0]
                last = time.time()
                s = last - first
                (d, s) = divmod(s, 86400)
                (h, s) = divmod(s, 3600)
                res = d + h / 24.0
                if res == 0:
                    return 1
                return d + h / 24.0
            return 1

    def get_months(self):
        months = []
        sql = 'SELECT time FROM data'
        with Cursor(self.connection) as (cursor):
            timestamps = cursor.execute(sql).fetchall()
            for timestamp in timestamps:
                d = datetime.date.fromtimestamp(timestamp[0])
                t = (d.year, d.month)
                if t not in months:
                    months.append(t)

            today = datetime.date.today()
            if (today.year, today.month) not in months:
                months.append((today.year, today.month))
            months.sort()
            return months

    def get_days(self):
        days = []
        sql = 'SELECT time FROM data'
        with Cursor(self.connection) as (cursor):
            timestamps = cursor.execute(sql).fetchall()
            for timestamp in timestamps:
                d = datetime.date.fromtimestamp(timestamp[0])
                if d not in days:
                    days.append(d)

            return days