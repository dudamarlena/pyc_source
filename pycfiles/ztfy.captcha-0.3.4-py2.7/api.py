# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/captcha/api.py
# Compiled at: 2015-02-06 06:53:19
__docformat__ = 'restructuredtext'
import hashlib, logging, os, random, string, sys
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from ztfy.cache.interfaces import IPersistentCacheProxyHandler
from zope.component import queryUtility
from ztfy.utils import request as request_utils, session
SHA_SEED = str(random.randint(0, sys.maxint))

def getShaSeed():
    proxy = queryUtility(IPersistentCacheProxyHandler)
    if proxy is None:
        logging.getLogger('ztfy.captcha').warning('No cache handler defined! You may get captcha errors in multi-process environments...')
        return SHA_SEED
    else:
        cache = proxy.getCache()
        seed = cache.query('ztfy.captcha', 'SHA_SEED')
        if seed is None:
            seed = SHA_SEED
            cache.set('ztfy.captcha', 'SHA_SEED', SHA_SEED)
        return seed


FONTS = {}
FONTS_PATH = os.path.join(os.path.dirname(__file__), 'fonts')
for f in os.listdir(FONTS_PATH):
    try:
        FONTS[f] = ImageFont.truetype(os.path.join(FONTS_PATH, f), random.randint(30, 40))
    except:
        logging.getLogger('ztfy.captcha').error("Can't load font from file '%s'" % f)

def getCaptchaImage(text, format='JPEG'):
    """Generate new captcha"""
    img = Image.new('RGB', (30 * len(text), 100), 16777215)
    img.format = format
    d = ImageDraw.Draw(img)
    x = y = 2
    height = random.randint(0, 35)
    for c in text:
        font = FONTS[random.choice(FONTS.keys())]
        w, h = font.getsize(c)
        height = max(height, h)
        y = random.randint(2, max(height - h, 2) + 10)
        d.text((x, y + 5), c, font=font, fill=3355443)
        x += w

    height += 15
    for _i in range(5):
        d.line((random.randint(0, x / 2),
         random.randint(0, height),
         random.randint(x / 2, x),
         random.randint(0, height)), width=1, fill=8947848)

    return img.crop((0, 0, x + 4, height + 4)).filter(ImageFilter.SMOOTH_MORE)


CHARS = string.ascii_uppercase + string.digits[1:]

def getDigest(text):
    return hashlib.sha256(getShaSeed() + '-----' + (text or '')).hexdigest()


def getCaptcha(id, length=5, format='JPEG', request=None):
    """Create a new random captcha"""
    text = ('').join([ random.choice(CHARS) for _i in range(length) ])
    image = getCaptchaImage(text, format)
    if request is None:
        try:
            request = request_utils.getRequest()
        except RuntimeError:
            pass

    if request is not None:
        session.setData(request, 'ztfy.captcha', id, getDigest(text))
    return (
     text, image)


def checkCaptcha(id, text, request=None):
    if request is None:
        try:
            request = request_utils.getRequest()
        except RuntimeError:
            return False

    digest = session.getData(request, 'ztfy.captcha', id)
    return getDigest(text) == digest