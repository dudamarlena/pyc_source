# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/test/decorators.py
# Compiled at: 2019-02-12 09:35:28
# Size of source mod 2**32: 1256 bytes
import os
from djangoplus import test
from django.conf import settings

def parametrized(dec):

    def layer(*args, **kwargs):

        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def testcase(func, title, username=settings.DEFAULT_SUPERUSER, password=settings.DEFAULT_PASSWORD, record=True):

    def wrapper(self):
        if username:
            if username != self.current_username:
                self.login(username, password)
            self.back()
        else:
            if test.CACHE['RECORD']:
                if record:
                    print('Start recording {}'.format(func.__name__))
                    self.recorder.start()
                    if title:
                        self.subtitle.display(title)
            func(self)
            if test.CACHE['RECORD'] and record:
                self.wait(6)
                output_dir = os.path.join(settings.BASE_DIR, 'videos')
                self.recorder.stop(title, output_dir, self.AUDIO_FILE_PATH)
                print('Stoped recording {}'.format(func.__name__))
        self.dump(func.__name__)

    test.CACHE['SEQUENCE'] += 1
    wrapper._sequence = test.CACHE['SEQUENCE']
    wrapper._funcname = func.__name__
    test.CACHE['RECORDING'] = False
    return wrapper