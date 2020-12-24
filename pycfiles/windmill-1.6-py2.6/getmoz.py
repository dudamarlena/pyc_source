# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_mozrunner/getmoz.py
# Compiled at: 2011-01-13 01:48:00
build_url_map = {'mozilla-central-win32': '/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-win32/firefox-4.0a1pre.en-US.win32.zip', 
   'mozilla-central-linux': '/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux/firefox-4.0a1pre.en-US.linux-i686.tar.bz2', 
   'mozilla-central-macosx': '/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-macosx/firefox-4.0a1pre.en-US.mac.dmg', 
   'firefox-trunk-win32': '/pub/mozilla.org/firefox/tinderbox-builds/FX-WIN32-TBOX-trunk/firefox-3.0pre.en-US.win32.zip', 
   'firefox-trunk-linux': '/pub/mozilla.org/firefox/tinderbox-builds/fx-linux-tbox-trunk/firefox-3.0pre.en-US.linux-i686.tar.bz2', 
   'firefox-trunk-macosx': '/pub/mozilla.org/firefox/tinderbox-builds/bm-xserve08-trunk/firefox-3.0pre.en-US.mac.dmg'}
import sys, urllib, termutil

class StdoutReportHook(object):

    def __init__(self, filename):
        self.term = termutil.TerminalController()
        self.progress = termutil.ProgressBar(self.term, 'Downloading ' + filename)
        self.percent_complete = 0

    def __call__(self, block, blocksize, target_size):
        if target_size is not -1:
            percent = round(float(block * blocksize) / target_size, 2)
            if percent != self.percent_complete:
                upper_percent = int(str(percent).split('.')[(-1)])
                self.progress.update(percent, 'Downloading ')
                self.percent_complete = percent


def wget(url):
    i = url.rfind('/')
    f = url[i + 1:]
    print url, '->', f
    urllib.urlretrieve(url, f, StdoutReportHook(f))


if __name__ == '__main__':
    wget('http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/bm-xserve08-trunk/firefox-3.0pre.en-US.mac.dmg')