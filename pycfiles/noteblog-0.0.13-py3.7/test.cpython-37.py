# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/test.py
# Compiled at: 2019-04-29 08:24:23
# Size of source mod 2**32: 2860 bytes
import multiprocessing, time, requests
from bs4 import BeautifulSoup
success_num = 0
CONSTANT = 0

def getProxyIp(count=12):
    proxy = []
    for index in range(0, count):
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
        r = requests.get(('http://www.xicidaili.com/nt/{0}'.format(index)), headers=header)
        html = r.text
        soup = BeautifulSoup(html)
        table = soup.find('table', attrs={'id': 'ip_list'})
        tr = table.find_all('tr')[1:]
        for item in tr:
            tds = item.find_all('td')
            temp_dict = {}
            kind = tds[5].get_text().lower()
            if 'http' in kind:
                temp_dict['http'] = 'http://{0}:{1}'.format(tds[1].get_text(), tds[2].get_text())
            if 'https' in kind:
                temp_dict['https'] = 'https://{0}:{1}'.format(tds[1].get_text(), tds[2].get_text())
            proxy.append(temp_dict)

    return proxy


class BrashRead:

    def __init__(self, url=None, nums=10):
        if not url:
            url = 'https://blog.csdn.net/n1007530194/article/details/78369429'
        self.url = url
        self.nums = nums

    def brash(self, proxy_dict):
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
        try:
            requests.get((self.url), headers=header, proxies=proxy_dict, timeout=10)
        except Exception as e:
            try:
                print('failed' + str(e))
            finally:
                e = None
                del e

        else:
            print('successful')
        time.sleep(0.5)

    def run(self):
        for _ in range(0, self.nums):
            proxies = getProxyIp()
            for i in range(5):
                i += 1
                pool = multiprocessing.Pool(processes=32)
                results = []
                for i in range(len(proxies)):
                    results.append(pool.apply_async(brash, (proxies[i],)))

                for i in range(len(proxies)):
                    results[i].get()

                pool.close()
                pool.join()

            time.sleep(20)


br = BrashRead()
br.run()
# global CONSTANT ## Warning: Unused global