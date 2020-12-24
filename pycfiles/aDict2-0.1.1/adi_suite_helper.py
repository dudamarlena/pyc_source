# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/suite/browser/adi_suite_helper.py
# Compiled at: 2013-01-01 06:05:34
from Products.Five import BrowserView
from Acquisition import aq_inner

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''


class View(BrowserView):

    def embedUrl(self):
        context = aq_inner(self.context)
        destUrl = self.context.getRemoteUrl()
        if 'youtu' in destUrl or 'vimeo' in destUrl:
            movieCode = destUrl.split('/')[(-1)]
            if 'v=' in movieCode:
                if '&' in movieCode:
                    movieCode = find_between(movieCode, 'v=', '&')
                else:
                    movieCode = movieCode[8:]
            if 'youtu' in destUrl:
                transUrl = 'http://www.youtube.com/embed/' + movieCode
                return transUrl
            if 'vimeo' in destUrl:
                transUrl = 'http://player.vimeo.com/video/' + movieCode
                return transUrl
        else:
            return destUrl