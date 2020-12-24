# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/app/db.py
# Compiled at: 2019-04-07 10:59:32
# Size of source mod 2**32: 20293 bytes
import base64, json, logging, re, sqlite3, sys, time, traceback
logger = logging.getLogger('ssb_app_db')
init_sql = [
 'CREATE TABLE IF NOT EXISTS ssb_feed (\n            i integer primary key,\n            str text not null unique,\n            scan_low integer default -1,\n            front_seq integer default 0,\n            front_prev text\n);',
 'CREATE TABLE IF NOT EXISTS ssb_key_sha256 (\n            b blob primary key,\n            feed integer,\n            seqno integer,\n            foreign key (feed) references ssb_feed (i)\n);',
 'CREATE TABLE IF NOT EXISTS ssb_follow (\n            who integer,\n            whom integer,\n            state int default 0,\n            primary key (who, whom),\n            foreign key (who) references ssb_feed (i),\n            foreign key (whom) references ssb_feed (i)\n);',
 'CREATE TABLE IF NOT EXISTS ssb_about (\n            feed integer,\n            attr text,\n            val text,\n            primary key (feed, attr),\n            foreign key (feed) references ssb_feed (i)\n);',
 "CREATE TABLE IF NOT EXISTS ssb_pub (\n            feed integer,\n            host text default '',\n            port int default 8008,\n            success_count int,\n            last_success int,\n            error_count int,\n            last_error int,\n            foreign key (feed) references ssb_feed (i)\n);",
 'CREATE TABLE IF NOT EXISTS surfcity_config (\n            k text primary key unique,\n            v text\n);',
 "CREATE TABLE IF NOT EXISTS surfcity_thread (\n            ssbkey blob primary key,\n            autrs text default '[]',\n            recps text default '[]',\n            title text, \n            tips text default '[]',\n            created timestamp default CURRENT_TIMESTAMP,\n            newest int default 0,\n            lastread int default 0\n);",
 'CREATE TABLE IF NOT EXISTS surfcity_post (\n            feed integer,\n            seqno integer,\n            msgstr text,\n            ts int,\n            created timestamp default CURRENT_TIMESTAMP,\n            access timestamp default NULL,\n            foreign key (feed) references ssb_feed (i),\n            primary key (feed, seqno)\n);',
 "CREATE TABLE IF NOT EXISTS surfcity_msg_to_push (\n            seqno integer primary key,\n            contentstr text,\n            ts int default 0,\n            raw text default NULL,\n            key text default NULL,\n            confirmed text default '[]'\n);"]
pub_list = {}

class SURFCITY_DB:

    def __init__(self):
        self.conn = None
        self.max_msgs = 500
        self.max_keys = 5000

    def open(self, fname, defaultFeed):
        self.fname = fname
        try:
            self.conn = sqlite3.connect(fname)
            for stmt in init_sql:
                self.conn.execute(stmt)

            self.conn.commit()
            if defaultFeed:
                feed = self.get_config('id')
                if not feed:
                    self.set_config('id', defaultFeed)
                    self.add_feedID(defaultFeed)
            if self.conn.execute('SELECT Count(*) FROM ssb_pub').fetchone()[0] == 0:
                for pub in pub_list:
                    pass

        except sqlite3.Error as e:
            try:
                raise e
            finally:
                e = None
                del e

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def forget_posts(self, frontier_window):
        limit = int(time.time()) - frontier_window
        sql = 'DELETE FROM surfcity_post WHERE ts < ? AND created < ?;'
        try:
            self.conn.execute(sql, (limit, limit))
        except:
            return
        else:
            self.conn.commit()
            sql = 'VACUUM;'
            self.conn.execute(sql)

    def get_config(self, k):
        sql = 'SELECT v FROM surfcity_config WHERE k = ? LIMIT 1;'
        try:
            return self.conn.execute(sql, (k,)).fetchone()[0]
        except:
            return

    def set_config(self, k, v):
        sql = 'INSERT OR REPLACE INTO surfcity_config (k,v) VALUES (?,?);'
        self.conn.execute(sql, (k, v))
        self.conn.commit()

    def _get_feed_ndx(self, author):
        try:
            sql = 'SELECT i FROM ssb_feed WHERE str = ? LIMIT 1;'
            res = self.conn.execute(sql, (author,)).fetchone()
            return res[0]
        except Exception as e:
            try:
                sql = 'INSERT INTO ssb_feed (str) VALUES (?);'
                self.conn.execute(sql, (author,))
                self.conn.commit()
                sql = 'SELECT i FROM ssb_feed WHERE str = ? LIMIT 1;'
                return self.conn.execute(sql, (author,)).fetchone()[0]
            finally:
                e = None
                del e

    def add_feedID(self, feedId):
        self._get_feed_ndx(feedId)

    def update_about(self, feedId, attr, val):
        i = self._get_feed_ndx(feedId)
        sql = 'INSERT OR REPLACE INTO ssb_about (feed,attr,val) VALUES (?,?,?);'
        self.conn.execute(sql, (i, attr, val))
        self.conn.commit()

    def get_about(self, feedId, attr):
        i = self._get_feed_ndx(feedId)
        sql = 'SELECT val FROM ssb_about WHERE feed=? AND attr=?'
        val = self.conn.execute(sql, (i, attr)).fetchone()
        if not val or len(val) == 0:
            return
        return val[0]

    def match_about_name(self, regex):
        try:
            pattern = re.compile(regex)
        except:
            return []
            lst = []
            sql = 'SELECT str,val,attr FROM ssb_feed INNER JOIN ssb_about ON feed = i'
            for c in self.conn.execute(sql):
                if c[2] in ('myname', 'name'):
                    if pattern.search(c[0]):
                        lst.append(c[0])
                        continue
                    try:
                        for s in json.loads(c[1]):
                            if pattern.search(s):
                                lst.append(c[0])
                                break

                    except:
                        pass

            return lst

    def update_id_front(self, feedId, front, prev):
        i = self._get_feed_ndx(feedId)
        sql = 'UPDATE ssb_feed SET front_seq = ?, front_prev = ? WHERE i = ?'
        self.conn.execute(sql, (front, prev, i))
        self.conn.commit()

    def update_id_low(self, feedId, low):
        i = self._get_feed_ndx(feedId)
        sql = 'UPDATE ssb_feed SET scan_low = ? WHERE i = ?'
        self.conn.execute(sql, (low, i))
        self.conn.commit()

    def get_id_front(self, feedId):
        i = self._get_feed_ndx(feedId)
        sql = 'SELECT front_seq, front_prev FROM ssb_feed WHERE i = ? LIMIT 1'
        return self.conn.execute(sql, (i,)).fetchone()

    def get_id_low(self, feedId):
        i = self._get_feed_ndx(feedId)
        sql = 'SELECT scan_low FROM ssb_feed WHERE i = ? LIMIT 1'
        return self.conn.execute(sql, (i,)).fetchone()[0]

    def add_pub(self, feedId, host, port):
        i = self._get_feed_ndx(feedId)
        sql = 'INSERT OR REPLACE INTO ssb_pub (feed, host, port) VALUES (?,?,?)'
        self.conn.execute(sql, (i, host, port))
        self.conn.commit()

    def get_thread_newest(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT newest FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        return self.conn.execute(sql, (key,)).fetchone()[0]

    def get_thread_lastread(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT lastread FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        return self.conn.execute(sql, (key,)).fetchone()[0]

    def update_thread_newest(self, key, ts):
        key = base64.b64decode(key.split('.')[0])
        sql = 'UPDATE surfcity_thread SET newest = ? WHERE ssbkey = ?'
        self.conn.execute(sql, (ts, key))
        self.conn.commit()

    def update_thread_lastread(self, key):
        key = base64.b64decode(key.split('.')[0])
        t = int(time.time())
        sql = 'UPDATE surfcity_thread SET lastread = ? WHERE ssbkey = ?'
        self.conn.execute(sql, (t, key))
        self.conn.commit()

    def update_follow(self, who, whom, state, only_if_absent=False):
        i = self._get_feed_ndx(who)
        j = self._get_feed_ndx(whom)
        sql = 'SELECT state FROM ssb_follow WHERE who=? AND whom = ?;'
        if self.conn.execute(sql, (i, j)).fetchone() != None:
            if only_if_absent:
                return
        sql = 'INSERT OR REPLACE INTO ssb_follow (who, whom, state) VALUES (?,?,?)'
        self.conn.execute(sql, (i, j, state))
        self.conn.commit()

    def get_following(self, who, state=0):
        lst = []
        i = self._get_feed_ndx(who)
        sql = 'SELECT str FROM ssb_feed INNER JOIN ssb_follow ON whom = i WHERE who = ? and state = ?;'
        cur = self.conn.execute(sql, (i, state)).fetchall()
        for rec in cur:
            lst.append(rec[0])

        return lst

    def get_followers(self, who):
        lst = []
        i = self._get_feed_ndx(who)
        sql = 'SELECT str FROM ssb_feed INNER JOIN ssb_follow ON who = i WHERE whom = ? and state = 0;'
        cur = self.conn.execute(sql, (i,)).fetchall()
        for rec in cur:
            lst.append(rec[0])

        return lst

    def get_friends(self, who):
        lst = []
        i = self._get_feed_ndx(who)
        sql = 'SELECT str FROM ssb_feed AS i  INNER JOIN ssb_follow AS ff  ON ff.who = i.i  INNER JOIN ssb_follow AS f  ON f.whom = ff.who WHERE f.who = ? AND f.state = 0 AND ff.state = 0 AND f.who = ff.whom'
        cur = self.conn.execute(sql, (i,)).fetchall()
        for rec in cur:
            lst.append(rec[0])

        return lst

    def get_follofollowing(self, who):
        lst = [
         who]
        i = self._get_feed_ndx(who)
        sql = 'SELECT str FROM ssb_feed AS i  INNER JOIN ssb_follow AS ff  ON ff.whom = i.i  INNER JOIN ssb_follow AS f  ON f.whom = ff.who WHERE f.who = ? AND f.state = 0 AND ff.state = 0'
        cur = self.conn.execute(sql, (i,)).fetchall()
        for rec in cur:
            if rec[0] not in lst:
                lst.append(rec[0])

        return lst[1:]

    def add_key(self, key, msgName):
        key = base64.b64decode(key.split('.')[0])
        i = self._get_feed_ndx(msgName[0])
        try:
            sql = 'INSERT INTO ssb_key_sha256 (b,feed,seqno) VALUES (?,?,?);'
            self.conn.execute(sql, (key, i, msgName[1]))
            self.conn.commit()
        except:
            pass

        return i

    def get_msgName(self, key):
        key2 = base64.b64decode(key.split('.')[0])
        try:
            sql = 'SELECT str,seqno FROM ssb_feed INNER JOIN ssb_key_sha256 ON ssb_feed.i = ssb_key_sha256.feed WHERE b = ? LIMIT 1;'
            return self.conn.execute(sql, (key2,)).fetchone()
        except:
            return

    def add_post(self, msgstr, msgName, ts, key=None):
        if key:
            self.add_key(key, msgName)
        i = self._get_feed_ndx(msgName[0])
        try:
            sql = 'INSERT INTO surfcity_post (feed,seqno,msgstr,ts) VALUES (?,?,?,?);'
            self.conn.execute(sql, (i, int(msgName[1]), msgstr, ts))
            self.conn.commit()
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e

    def get_post(self, msgName):
        i = self._get_feed_ndx(msgName[0])
        try:
            sql = 'SELECT msgstr, ts FROM surfcity_post INNER JOIN ssb_feed ON feed = i WHERE str = ? and seqno = ? LIMIT 1;'
            return self.conn.execute(sql, msgName).fetchone()
        except:
            return

    def add_thread(self, recps, key, timestamp):
        key = base64.b64decode(key.split('.')[0])
        if not recps:
            recps = []
        recps = json.dumps(recps)
        sql = 'INSERT INTO surfcity_thread (ssbkey,recps,newest) VALUES (?,?,?);'
        try:
            self.conn.execute(sql, (key, recps, timestamp))
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e

    def add_tip_to_thread(self, tkey, bkey):
        tkey = base64.b64decode(tkey.split('.')[0])
        sql = 'SELECT tips FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        s = self.conn.execute(sql, (tkey,)).fetchone()[0]
        tips = json.loads(s)
        if bkey not in tips:
            tips.append(bkey)
            s = json.dumps(tips)
            sql = 'UPDATE surfcity_thread SET tips=? WHERE ssbkey=?'
            self.conn.execute(sql, (s, tkey))
            self.conn.commit()

    def get_thread_tips(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT tips FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        return json.loads(self.conn.execute(sql, (key,)).fetchone()[0])

    def add_author_to_thread(self, tkey, a):
        tkey = base64.b64decode(tkey.split('.')[0])
        sql = 'SELECT autrs FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        lst = json.loads(self.conn.execute(sql, (tkey,)).fetchone()[0])
        if a not in lst:
            lst.append(a)
            sql = 'UPDATE surfcity_thread SET autrs=? WHERE ssbkey=?'
            self.conn.execute(sql, (json.dumps(lst), tkey))
            self.conn.commit()

    def get_thread_authors(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT autrs FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        authors = self.conn.execute(sql, (key,)).fetchone()[0]
        return json.loads(authors)

    def get_thread_recps(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT recps FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        recps = self.conn.execute(sql, (key,)).fetchone()[0]
        return json.loads(recps)

    def get_thread_title(self, key):
        key = base64.b64decode(key.split('.')[0])
        sql = 'SELECT title FROM surfcity_thread WHERE ssbkey = ? LIMIT 1'
        return self.conn.execute(sql, (key,)).fetchone()[0]

    def update_thread_title(self, key, title):
        key = base64.b64decode(key.split('.')[0])
        sql = 'UPDATE surfcity_thread SET title=? WHERE ssbkey=?'
        self.conn.execute(sql, (title, key))
        self.conn.commit()

    def add_push_msg(self, seqno, raw_str, meta_dict):
        sql = 'INSERT OR REPLACE INTO surfcity_msg_to_push (seqno,msg,meta) VALUES (?,?,?);'
        self.conn.execute(sql, (seqno, raw_str, json.dumps(meta_dict)))
        self.conn.commit()

    def get_push_msg(self, seqno):
        sql = 'SELECT msg_val, msg_meta FROM surfcity_msg_to_push WHERE seqno = ? LIMIT 1'
        msg = self.conn.execute(sql, (seqno,)).fetchone()
        if msg:
            msg = (
             msg[0], json.loads(meta))
        return msg

    def list_pubs(self):
        lst = []
        sql = 'SELECT str,host,port FROM ssb_pub INNER JOIN ssb_feed ON i = feed'
        cur = self.conn.execute(sql, ()).fetchall()
        result = {}
        for rec in cur:
            result[rec[0]] = {'host':rec[1], 
             'port':rec[2]}

        return result

    def list_newest_threads(self, limit=20, public=True):
        lst = []
        sql = 'SELECT ssbkey FROM surfcity_thread '
        if public:
            sql += "WHERE recps == '[]' "
        else:
            sql += "WHERE recps <> '[]' "
        sql += 'ORDER BY newest DESC LIMIT ?;'
        cur = self.conn.execute(sql, (limit,)).fetchall()
        for rec in cur:
            x = base64.b64encode(rec[0]).decode('ascii')
            lst.append(f"%{x}.sha256")

        return lst

    def list_newest_post(self, limit=20):
        lst = []
        sql = 'SELECT msg FROM surfcity_post ORDER BY ts DESC LIMIT ?;'
        cur = self.conn.execute(sql, (limit,)).fetchall()
        for rec in cur:
            lst.append(json.loads(rec[0]))

        return lst

    def get_stats(self):
        result = {'counts': {}}
        for tbl in ('ssb_feed', 'ssb_key_sha256', 'ssb_follow', 'ssb_about', 'ssb_pub',
                    'surfcity_config', 'surfcity_thread', 'surfcity_post'):
            sql = 'SELECT Count(*) FROM '
            cnt = self.conn.execute(sql + tbl, ()).fetchone()[0]
            result['counts'][tbl] = cnt

        return result

    def push_add(self, contentstr, ts):
        pass

    def push_get_fresh(self):
        pass

    def push_setraw(self, id, raw, key):
        pass

    def push_del(i):
        pass

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    store = SURFCITY_DB()
    store.open('alice.sq3')
    store.set_config('id', 'alice.id')
    print('id', store.get_config('id'))
    store.add_key(b'\x01\x02\x00', ['alice.id', 1])
    print('get_msgName', store.get_msgName(b'\x01\x02\x00'))
    store.add_msg({'this':[
      'alice.id', 3], 
     'content':'blahblah UU'})
    print('msg', store.get_post(['alice.id', 1]))
    print('msg', store.get_post(['alice.id', 3]))
    store.add_feedID('bob.id')
    store.add_feedID('carole.id')
    store.add_follow('alice.id', 'bob.id')
    store.add_follow('alice.id', 'carole.id')
    print('follow', store.get_following('alice.id'))
    store.close()