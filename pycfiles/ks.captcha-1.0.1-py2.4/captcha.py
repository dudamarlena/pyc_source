# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/captcha/captcha.py
# Compiled at: 2008-12-22 08:21:48
from zope.interface import implements
from interfaces import ICaptcha
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from zope.app.container.contained import Contained
from persistent import Persistent
from StringIO import StringIO
import random, os, time
from zope.schema.fieldproperty import FieldProperty
from logging import getLogger
logger = getLogger('captcha')
keydict = {}
timekeydict = {}

class Captcha(Contained, Persistent):
    __module__ = __name__
    implements(ICaptcha)
    width = FieldProperty(ICaptcha['width'])
    height = FieldProperty(ICaptcha['height'])
    noise = FieldProperty(ICaptcha['noise'])
    fontsize = FieldProperty(ICaptcha['fontsize'])
    font = FieldProperty(ICaptcha['font'])
    keypos = None
    secret = FieldProperty(ICaptcha['secret'])
    min = FieldProperty(ICaptcha['min'])
    max = FieldProperty(ICaptcha['max'])
    format = FieldProperty(ICaptcha['format'])
    mimetype = FieldProperty(ICaptcha['mimetype'])
    interval = FieldProperty(ICaptcha['interval'])
    mode = FieldProperty(ICaptcha['mode'])

    def __init__(self, min=1000, max=9999, width=80, height=80, noise=20, font='/', fontsize=4, keypos=(10, 10), secret=20, format='PNG', mimetype='image/png', interval=3600, mode='RGB'):
        u""" Конструктор класса Captcha
        """
        self.width = width
        self.height = height
        self.noise = noise
        self.fontsize = fontsize
        self.font = font
        self.keypos = keypos
        self.secret = secret
        self.min = min
        self.max = max
        self.format = format
        self.mimetype = mimetype
        self.interval = interval
        self.mode = mode

    def banner(self, key):
        u""" Генерирует картинку, на которой изображён указанный в параметре key
            (слово, набор цифр или нечто подобное) font - путь к шрифту, fontsize - размер шрифта
            keypos - tuple (x,y) - позиция с которой будет печататься текст

        """
        key = self.decrypt(key)
        bg = (
         random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        image = Image.new(self.mode, (self.width, self.height), bg)
        fg = tuple([ 255 - x for x in bg ])
        font = ImageFont.truetype(os.path.join(p, self.font), int(self.fontsize))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), '%u' % key, font=font, fill=fg)
        for item in range(0, (self.width + self.height) * self.noise / 100):
            draw.line(((random.randint(0, self.width), random.randint(0, self.height)), (random.randint(0, self.width), random.randint(0, self.height))), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        for item in range(0, self.height * self.width * self.noise / 100):
            draw.point((random.randint(0, self.width), random.randint(0, self.height)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        del draw
        buf = StringIO()
        image.save(buf, self.format)
        return buf.getvalue()

    def getkey(self):
        for a in timekeydict.keys():
            if a < time.time() - self.interval:
                try:
                    del keydict[timekeydict[a]]
                except KeyError:
                    pass
                else:
                    del timekeydict[a]

        key = random.choice(tuple(set(range(self.min, self.max)).difference(set(keydict.keys()))))
        if keydict.has_key(key):
            raise ValueError, 'Эта ошибка никогда не возникает'
        keydict[key] = random.choice(range(self.min, self.max))
        timekeydict[time.time()] = key
        return key

    def decrypt(self, key):
        u""" Принимает ключ в зашифрованном виде, расшифровывает его и
            возвращает результат расшифровки
        """
        key = int(key)
        if keydict.has_key(key) == False:
            keydict[key] = random.choice(range(self.min, self.max))
        return keydict[key]

    def check(self, key, x):
        u""" Проверяет, соответствуют ли данные, введённые пользователем,
            данным, изображённым на картинке
        """
        try:
            key = int(key)
            x = int(x)
        except ValueError, msg:
            logger.warning('Captcha.check', exc_info=True)
            return False

        if keydict.has_key(key):
            res = keydict[key] == x
            del keydict[key]
            return res
        else:
            return False