# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webbridge\client.py
# Compiled at: 2016-09-02 12:59:33
import multiprocessing
try:
    import webview
except:
    raise ImportError('webview not found')

class Client:

    def __init__(self, title, url, borderless=False):
        self.title = title
        self.url = url
        self.borderless = borderless
        self.process = None
        self.running = False
        return

    def run(self):
        self.process = multiprocessing.Process(target=self._handle_webview, args=(self._cleanup,))
        self.process.start()
        self.running = lambda : self.process.is_alive()

    def kill(self):
        if self.running != False:
            self.process.terminate()
            self.process.join()

    def _handle_webview(self, cleanup_callback):
        try:
            webview.create_window(self.title, self.url)
        except Exception as e:
            with open('error-log.txt', 'w') as (f):
                f.write(e)

        cleanup_callback()

    def _cleanup(self):
        self.process.terminate()
        self.process.join()