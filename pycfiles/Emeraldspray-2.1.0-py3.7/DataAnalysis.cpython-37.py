# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Es\DataAnalysis.py
# Compiled at: 2019-12-18 22:22:22
# Size of source mod 2**32: 10678 bytes
from bs4 import BeautifulSoup
from .WebGeter import WebGeter
from .BugReporter import BugReporter
import time, json

class steam250URLGeter:

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.num = len(self.raw_data.findAll(name='span', attrs={'class': 'title'}))
        self.data = []

    def dataHandle(self):
        for i in range(0, self.num):
            self.data.append([self.raw_data.findAll(name='span', attrs={'class': 'title'})[i].find(name='a').string, self.raw_data.findAll(name='span', attrs={'class': 'title'})[i].find(name='a')['href'].replace('\n', ''), self.raw_data.findAll(name='span', attrs={'class': 'score'})[i].string])

    def outputData(self):
        nowtime = str(time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime(time.time())))
        with open((nowtime + '.xuan2'), 'a', encoding='utf-8') as (outfile):
            for i in range(0, int(input('请输入分析个数最大为{}>'.format(len(self.data))))):
                outfile.write(self.data[i][0] + '\n')
                outfile.write(self.data[i][1] + '\n')
                outfile.write(self.data[i][2] + '\n')


class detailsDataGeter:

    def __init__(self, URL):
        self.URL = URL
        self.data = {}
        self.raw_data = WebGeter(self.URL).raw_data

    def ifBanGame(self):
        banlist = []
        for line in open('BannedGame.bin', 'r', encoding='utf-8'):
            banlist.append(line)

        for i in range(0, len(banlist)):
            if banlist[i] == self.data['Gamename']:
                print('由于已知的数据兼容问题，对此游戏的数据分析已经停止')
                quit()

    def whichClass(self):
        return self.raw_data.find(name='div', attrs={'class': 'game_area_sys_req sysreq_content active'}).find(name='div')['class'][0] == 'game_area_sys_req_full'

    def detailsGeter(self):
        self.data['Gamename'] = self.raw_data.find(name='div', attrs={'class': 'apphub_AppName'}).string
        self.ifBanGame()
        self.data['Developer'] = self.raw_data.find(name='div', attrs={'class': 'dev_row'}).find(name='a').string
        self.data['Recent Reviews'] = self.raw_data.findAll(name='div', attrs={'class': 'summary column'})[0].find(name='span').string
        self.data['Overall Reviews'] = self.raw_data.findAll(name='div', attrs={'class': 'summary column'})[1].find(name='span').string
        self.data['Description'] = self.raw_data.find(name='div', attrs={'class': 'game_description_snippet'}).string.strip('\t').strip('\t').strip('\r').strip('\n').strip('\t')
        if self.ifDiscount():
            self.data['Price'] = self.raw_data.find(name='div', attrs={'class': 'game_purchase_price price'}).string.strip('\t').strip('\r').strip('\n').strip('\t')
        else:
            self.data['Price'] = self.raw_data.find(name='div', attrs={'class': 'discount_final_price'}).string.strip('\t').strip('\r').strip('\n').strip('\t')
        temp = ''
        for i in range(0, len(self.raw_data.findAll(name='a', attrs={'class': 'app_tag'})) - 1):
            temp += self.raw_data.findAll(name='a', attrs={'class': 'app_tag'})[i].string.strip('\t').strip('\r').strip('\n').strip('\t').strip(',').strip('，') + ' '

        self.data['Tag'] = temp
        if self.whichClass():
            self.data['Old Game'] = self.whichClass()
        else:
            self.data['Old Game'] = self.whichClass()
            namelist = []
            iError = []
            for i in range(0, len(self.raw_data.find(name='div', attrs={'class': 'game_area_sys_req sysreq_content active'}).findAll(name='li'))):
                try:
                    namelist.append(self.raw_data.find(name='div', attrs={'class': 'game_area_sys_req sysreq_content active'}).findAll(name='li')[i].find(name='strong').string)
                except:
                    iError.append(i)
                    i += 1

            [s.extract() for s in self.raw_data('strong')]
            [s.extract() for s in self.raw_data('br')]
            errorFlag = False
            for i in range(0 + len(iError), len(self.raw_data.find(name='div', attrs={'class': 'game_area_sys_req sysreq_content active'}).findAll(name='li'))):
                try:
                    for ierror in iError:
                        if i == ierror:
                            i += 1
                            errorFlag = True

                    if errorFlag == True:
                        errorFlag = False
                        continue
                    self.data[namelist[i]] = self.raw_data.find(name='div', attrs={'class': 'game_area_sys_req sysreq_content active'}).findAll(name='li')[i].string
                except:
                    if os.path.exists('error.log'):
                        BugReporter()
                    else:
                        with open('error.log', 'a', encoding='utf-8') as (f):
                            f.write('errorcode:1002\n\ntime:' + str(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))) + '\n\n' + 'pwd:' + str(os.getcwd()) + '\n\n' + self.data['Gamename'] + '已经被加入黑名单，不再爬取')
                        with open('BannedGame.bin', 'a', encoding='utf-8') as (f):
                            f.write(self.data['Gamename'] + '\n')
                        BugReporter()

    def detailsGeterFixed(self):
        self.data['Gamename'] = self.raw_data.find(name='div', attrs={'class': 'apphub_AppName'}).string
        self.data['Developer'] = self.raw_data.find(name='div', attrs={'class': 'dev_row'}).find(name='a').string
        try:
            self.data['Recent Reviews'] = self.raw_data.findAll(name='div', attrs={'class': 'summary column'})[0].find(name='span').string
        except:
            self.data['Recent Reviews'] = 'Unknow'

        try:
            self.data['Overall Reviews'] = self.raw_data.findAll(name='div', attrs={'class': 'summary column'})[1].find(name='span').string
        except:
            self.data['Overall Reviews'] = 'Unknow'

        try:
            self.data['Description'] = self.raw_data.find(name='div', attrs={'class': 'game_description_snippet'}).string.strip('\t').strip('\t').strip('\r').strip('\n').strip('\t')
        except:
            self.data['Description'] = 'Unknow'

        try:
            self.data['Price'] = self.raw_data.find(name='div', attrs={'class': 'game_area_purchase_game_wrapper'}).find(name='div', attrs={'class': 'game_purchase_price price'}).string.strip('\t').strip('\r').strip('\n').strip('\t')
        except:
            try:
                self.data['Price'] = self.raw_data.find(name='div', attrs={'class': 'game_area_purchase_game_wrapper'}).find(name='div', attrs={'class': 'discount_final_price'}).string.strip('\t').strip('\r').strip('\n').strip('\t')
            except:
                try:
                    self.data['Price'] = self.raw_data.find(name='div', attrs={'class': 'game_area_purchase_game'}).find(name='div', attrs={'class': 'game_purchase_price price'}).string.strip('\t').strip('\r').strip('\n').strip('\t')
                except:
                    self.data['Price'] = 'Unknow'

        temp = ''
        for i in range(0, len(self.raw_data.findAll(name='a', attrs={'class': 'app_tag'})) - 1):
            temp += self.raw_data.findAll(name='a', attrs={'class': 'app_tag'})[i].string.strip('\t').strip('\r').strip('\n').strip('\t').strip(',').strip('，') + ' '

        self.data['Tag'] = temp

    def outputData(self):
        if not os.path.exists(str(datetime.date.today())):
            os.makedirs(str(datetime.date.today()))
        with open(str(datetime.date.today()) + '/' + data['Gamename'].replace(' ', '_').replace(':', '_').replace('\\', '_').replace('/', '_').replace('*', '_').replace('"', '_').replace('?', '_').replace('<', '_').replace('>', '_').replace('|', '_') + '.json', 'w') as (outfile):
            json.dump(self.data, outfile)


class steamTop100URLGeter:

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.data = []

    def dataHandle(self):
        self.data.append(self.raw_data.findAll(name='td', attrs={'class': 'users_count'})[0].string)
        self.data.append(self.raw_data.findAll(name='td', attrs={'class': 'users_count'})[1].string)
        for i in range(0, len(self.raw_data.find(id='detailStats').findAll(name='a', attrs={'class': 'gameLink'}))):
            self.data.append([self.raw_data.find(id='detailStats').findAll(name='a', attrs={'class': 'gameLink'})[i].string, self.raw_data.find(id='detailStats').findAll(name='span', attrs={'class': 'currentServers'})[(2 * i)].string, self.raw_data.find(id='detailStats').findAll(name='span', attrs={'class': 'currentServers'})[(2 * i + 1)].string, self.raw_data.find(id='detailStats').findAll(name='a', attrs={'class': 'gameLink'})[i]['href']])

    def outputData(self):
        nowtime = str(time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime(time.time())))
        with open((nowtime + '.xuan'), 'a', encoding='utf-8') as (outfile):
            outfile.write(self.data[0] + '\n')
            outfile.write(self.data[1] + '\n')
            for i in range(2, len(self.data)):
                outfile.write(self.data[i][0] + '\n')
                outfile.write(self.data[i][1] + '\n')
                outfile.write(self.data[i][2] + '\n')
                outfile.write(self.data[i][3] + '\n')