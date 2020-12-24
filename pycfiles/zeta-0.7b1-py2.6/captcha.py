# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/captcha.py
# Compiled at: 2010-06-18 10:31:28
"""Generate and Manage captchas for Turing tests."""
import logging
from random import randint, choice
import os
from os.path import commonprefix, join, getmtime, basename, isfile, isdir
import time, sys, re
from hashlib import sha1
from skimpyGimpy import skimpyAPI
from pylons import session
import zeta.lib.helpers as h
from zeta.config.environment import envpath

class Captcha(object):

    def randomword(self, len=8, chars='ABCDEGHKLMNOPRSTUVWXYZ1234567890'):
        return ('').join(choice(chars) for i in range(len))

    def prunefile(self, path):
        """Remove captcha files that are older by 100000 seconds"""
        curtime = time.time()
        prune = map(lambda x: join(path, x[0]), filter(lambda x: curtime - x[1] > 100000, [ (f, os.path.getmtime(join(path, f))) for f in os.listdir(path)
                                                                                          ]))
        [ os.remove(f) for f in prune ]

    def captchafile(self, word):
        isdir(self.path) or os.mkdir(self.path)
        self.prunefile(self.path)
        return join(self.path, '%s.png' % word)

    def removefile(self):
        isfile(self.file) and os.remove(self.file)

    def __init__(self, word=None, wordsize=4, speckle=0.06, scale=2.0, color='00FFFF', test=False):
        """Generate image captcha for word (if word is None, randomly generate
        a word). place it under /public/captcha/<captchafile>.png.
        A hash digest is generated for the image file, which is used as
        `captchafile` name.
        """
        self.path = join(envpath, 'public', 'captcha')
        self.word = word or self.randomword(len=wordsize)
        self.wordsize = wordsize
        self.speckle = speckle
        self.scale = scale
        self.color = color
        self.file = self.captchafile(self.word)
        pngGenerator = skimpyAPI.Png(self.word, speckle=self.speckle, scale=self.scale, color=self.color)
        pngGenerator.data(self.file)
        self.urlpath = join('/captcha', basename(self.file))
        session['captcha'] = self
        session.save()

    def match(self, word):
        """Match user-input word with captcha"""
        return self.word == word

    def destroy(self):
        """Destroy all persistent storage created by this object"""
        self.removefile()
        c = session.get('captcha', None)
        if session.has_key('captcha'):
            del session['captcha']
        session.save()
        return


def sessioncaptcha():
    return session.get('captcha', None)