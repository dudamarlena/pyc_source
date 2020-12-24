# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_captcha/models.py
# Compiled at: 2014-06-13 14:34:59
# Size of source mod 2**32: 5826 bytes
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.captcha.helpers import get_challenge
from flask import current_app
import datetime, random, time, unicodedata, six
db = SQLAlchemy()
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
MAX_RANDOM_KEY = 18446744073709551616
import hashlib

def get_cache():
    from werkzeug.contrib.cache import SimpleCache
    return SimpleCache()


def get_safe_now():
    return datetime.datetime.utcnow()


class CaptchaSequenceCache:
    instance = None

    def __init__(self, max_value):
        self.max_value = max_value
        self.cache = get_cache()

    @classmethod
    def get(cls):
        if cls.instance is None:
            cls.instance = CaptchaSequenceCache(current_app.config['CAPTCHA_PREGEN_MAX'])
        return cls.instance

    def current(self):
        seq = self.cache.get('seq')
        if seq is not None:
            return seq
        else:
            return 0
            return

    def next(self):
        seq = self.cache.get('seq')
        if seq is not None:
            seq = (seq + 1) % self.max_value
            self.cache.set('seq', seq)
        else:
            self.cache.set('seq', 0)
            seq = 0
        return seq


class CaptchaSequence(db.Model):
    __tablename__ = 'captcha_sequence'
    value = db.Column(db.Integer, primary_key=True)
    max_value = db.Column(db.Integer)

    def __init__(self, start, max_value):
        self.value = start
        self.max_value = max_value

    @classmethod
    def init(cls):
        start = current_app.config['CAPTCHA_PREGEN_START']
        max_value = current_app.config['CAPTCHA_PREGEN_MAX']
        sequence = CaptchaSequence(start, max_value)
        db.session.add(sequence)
        db.session.commit()

    @classmethod
    def get(cls):
        row = db.session.query(CaptchaSequence).first()
        if row is not None:
            ret = row.value
        else:
            cls.init()
            ret = 0
        return ret

    @classmethod
    def next(cls):
        row = db.session.query(CaptchaSequence).first()
        if row is not None:
            row.value = (row.value + 1) % row.max_value
            ret = row.value
            db.session.commit()
        else:
            cls.init()
            ret = 0
        return ret


class CaptchaStore(db.Model):
    __tablename__ = 'captcha_store'
    __table_args__ = {'sqlite_autoincrement': True}
    index = db.Column(db.Integer, index=True)
    challenge = db.Column(db.String(32))
    response = db.Column(db.String(32))
    hashkey = db.Column(db.String(40), primary_key=True)
    expiration = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.response = six.text_type(self.response).lower()
        if not self.expiration:
            self.set_expiration()
        if not self.hashkey:
            key_ = unicodedata.normalize('NFKD', str(randrange(0, MAX_RANDOM_KEY)) + str(time.time()) + six.text_type(self.challenge)).encode('ascii', 'ignore') + unicodedata.normalize('NFKD', six.text_type(self.response)).encode('ascii', 'ignore')
            if hashlib:
                self.hashkey = hashlib.sha1(key_).hexdigest()
            else:
                self.hashkey = sha.new(key_).hexdigest()
            del key_
        db.session.add(self)
        db.session.commit()

    def set_expiration(self):
        timeout = current_app.config['CAPTCHA_TIMEOUT']
        self.expiration = get_safe_now() + datetime.timedelta(minutes=int(timeout))

    @classmethod
    def validate(cls, hashkey, response):
        """
        Returns true or false if key validates or not
        """
        find = db.session.query(CaptchaStore).filter(CaptchaStore.hashkey == hashkey, CaptchaStore.expiration > get_safe_now())
        if find.count() == 0:
            return False
        ret = find.first().response == response
        if not current_app.config['CAPTCHA_PREGEN']:
            db.session.delete(find.first())
        db.session.commit()
        return ret

    def __unicode__(self):
        return self.challenge

    @classmethod
    def remove_expired(cls):
        items = db.session.query(CaptchaStore).filter(CaptchaStore.expiration <= get_safe_now())
        for i in items:
            db.session.delete(i)

        db.session.commit()

    @classmethod
    def generate_key(cls):
        c = cls.generate()
        return c.hashkey

    @classmethod
    def generate(cls, index=0):
        challenge, response = get_challenge()()
        c = CaptchaStore()
        c.challenge = challenge
        c.response = response
        c.index = index
        c.save()
        return c

    @classmethod
    def get_all(cls):
        items = db.session.query(CaptchaStore)
        ret = []
        for i in items:
            ret.append({'key': i.hashkey, 
             'index': i.index, 
             'challenge': i.challenge, 
             'response': i.response, 
             'expiration': i.expiration})

        return ret

    @classmethod
    def delete_all(cls):
        ret = items = db.session.query(CaptchaStore).delete()
        db.session.commit()
        return ret