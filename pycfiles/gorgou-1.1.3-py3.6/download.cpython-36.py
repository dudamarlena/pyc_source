# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/download.py
# Compiled at: 2018-02-03 08:38:19
# Size of source mod 2**32: 1749 bytes
import requests, threading

class downloader:

    def __init__(self, url, num, name):
        self.url = url
        self.num = num
        self.name = name
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        print(self.total)

    def get_range(self):
        ranges = []
        offset = int(self.total / self.num)
        for i in range(self.num):
            if i == self.num - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))

        return ranges

    def download(self, start, end):
        headers = {'Range':'Bytes=%s-%s' % (start, end), 
         'Accept-Encoding':'*'}
        res = requests.get((self.url), headers=headers)
        print('%s-%s download success' % (start, end))
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        self.fd = open(self.name, 'wb')
        thread_list = []
        n = 0
        for ran in self.get_range():
            start, end = ran
            n += 1
            thread = threading.Thread(target=(self.download), args=(start, end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()

        self.fd.close()