# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgcaptcha/model.py
# Compiled at: 2007-06-02 01:56:45
from datetime import datetime
import calendar, cPickle

class Captcha(object):
    """Pertinent data about a Captcha.
    
    Exposed properties are:
    plaintext: (read/write) a string representing the text of the captcha 
                (i.e. what is it supposed to say)
    created: (read only) the UTC date when the captcha was created. This 
                data is updated when the plaintext property is updated.
                
    Exposed methods:
    serialize(): returns a binary representation of the object
    deseralize(obj): creates a Captcha object given the output of the
                serialize() method. This is a classmethod.
    """
    __module__ = __name__
    _plaintext = None
    _created = None

    def __init__(self, plaintext=''):
        super(Captcha, self).__init__()
        self.plaintext = plaintext

    def get_plaintext(self):
        return self._plaintext

    def set_plaintext(self, text):
        self._plaintext = text
        self._created = datetime.utcnow()

    plaintext = property(get_plaintext, set_plaintext)
    c = lambda s: s._created
    created = property(lambda s: s._created)

    def serialize(self):
        """Get a serialized binary representation of the object."""
        secs = int(calendar.timegm(self.created.utctimetuple()))
        t = (self.plaintext, secs)
        return cPickle.dumps(t, cPickle.HIGHEST_PROTOCOL)

    def deserialize(cls, serialized_obj):
        """Create a new Captcha object given output from the serialize method."""
        t = cPickle.loads(serialized_obj)
        scp = cls()
        scp._plaintext = t[0]
        scp._created = datetime.utcfromtimestamp(t[1])
        return scp

    deserialize = classmethod(deserialize)