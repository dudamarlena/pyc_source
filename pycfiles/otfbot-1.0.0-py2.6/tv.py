# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/tv.py
# Compiled at: 2011-04-22 06:35:42
from otfbot.lib import chatMod, urlutils
from otfbot.lib.pluginSupport.decorators import callback
import time, os, sys, traceback
HAS_PYXMLTV = True
try:
    import xmltv
except ImportError:
    HAS_PYXMLTV = False

class Meta:
    service_depends = [
     'scheduler']


class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.tv = None
        self.source = self.bot.config.get('source', 'otr', 'tv')
        if self.source == 'otr':
            self.tvdatadir = datadir
            self.dataurl = 'http://www.onlinetvrecorder.com/epg/csv/'
            self.days = int(self.bot.config.get('days', 5, 'tv'))
        elif self.source == 'xmltv':
            if not HAS_PYXMLTV:
                self.bot.depends('xmltv python module')
            self.xmltvfile = datadir + '/' + self.bot.config.get('xmltvfile', 'tv.xml.txt', 'tv')
            self.dataurl = 'http://xmltv.info/xw/default/run/xmltv?offset=-1'
            self.bot.root.getServiceNamed('scheduler').callLater(1, self.update_data, dataurl)
        else:
            self.logger.info("no allowed datasource choosen. availiable sources: 'otr' and 'xmltv'. See docs for more info.")
        if not os.path.isdir(self.tvdatadir):
            os.makedirs(self.tvdatadir)
        standardsender = self.bot.config.get('standardsender', 'ard,zdf,rtl,sat1,n24,pro7,vox', 'tv')
        ignore = self.bot.config.get('ignoresender', '9live,bibeltv,ukbbc4,ukbbc3,uswxtv,ukchannel4,uslivewell,uswfut,usports,ukbbc,nickelodeon,sixx,anixe,uswpix,yavido,tvpinfo,uswwor,deluxemusic,erf,ukitv,ukcbsaction,uswabc,tv5,bbcworld,gotv,tvpolonia,ukfive,usnjn,uswnyw,tvphistoria,uswnye,drdishtv,ukbbc2,ukfilm4,uswcbs,ktv,stv,cnbc,uswnju,tele5,imusic,uswnbc,usnjn2,ukitv3,ukitv4,ukitv2,tvpkultura,uke4', 'tv')
        self.standardsender = []
        for i in standardsender.split(','):
            self.standardsender.append(i.lower().replace(' ', ''))

        self.ignoresender = []
        for i in ignore.split(','):
            self.ignoresender.append(i.lower().replace(' ', ''))

        self.download_data()
        return

    @callback
    def command(self, user, channel, command, options):
        try:
            user = user.getNick()
            public = False
            all = False
            filterstandard = False
            programm = []
            ltime = time.localtime()
            if not self.tv and command in ['tv', 'tvsearch']:
                self.bot.sendmsg(channel, 'no tvdata, yet!')
                return
            if command == 'tv':
                o = options.split(' ')
                o1 = o[0].replace('.', '').replace(':', '')
                if o[(len(options.split(' ')) - 1)] == 'public':
                    public = True
                    o.remove('public')
                if o[(len(options.split(' ')) - 1)] == 'all':
                    all = True
                    public = False
                    o.remove('all')
                if options == '':
                    o = []
                if len(o) != 0 and o[0].lower() == 'help':
                    self.bot.sendmsg(user, " !tv <- Zeigt das aktuelle TV-Programm an. An dieses Kommando kann 'all' angehaengt werden, dann werden alle bekannten Sender ausgegeben.")
                    self.bot.sendmsg(user, " !tv <uhrzeit> <- Zeigt das Programm fuer <uhrzeit> (hh:mm) an. An dieses Kommando kann 'all' angehaengt werden, dann werden alle bekannten Sender ausgegeben.")
                    self.bot.sendmsg(user, ' !tv <uhrzeit> <sendername> <- zeigt das Programm fuer <uhrzeit> auf <sendername> an.')
                    self.bot.sendmsg(user, ' !tv <sendername> <- zeigt das aktuelle Programm auf <sendername>.')
                    self.bot.sendmsg(user, ' !tv liststations <- zeigt alle verfuegbaren Sender an.')
                    self.bot.sendmsg(user, ' !tvsearch <begriff> <- sucht auf allen Sendern nach <begriff>. Optional kann noch der Sender, auf dem gesucht werden soll, als letztes Wort angehaengt werden.')
                    self.bot.sendmsg(user, " Wenn die Ausgabe nicht im Query, sondern im Channel erfolgen soll: 'public' ans Ende des Kommandos anhaengen (nicht moeglich mit Option 'all').")
                elif len(o) != 0 and o[0].lower() == 'liststations':
                    stations = []
                    for i in self.tv.stations:
                        if self.tv.stations[i][0].lower().replace(' ', '') not in self.ignoresender:
                            stations.append(self.tv.stations[i][0])

                    self.bot.sendmsg(channel, 'bekannte Sender: ' + (', ').join(stations))
                    return
                if o1 != 'public' and len(o) == 1:
                    try:
                        int(o1)
                        if int(o1) > 2400 or int(o1[2:4]) > 59:
                            self.bot.sendmsg(channel, 'corrupted time!')
                            return False
                        programm = self.tv.get_programm_at_time(o1 + '00')
                        filterstandard = not all
                    except ValueError:
                        if not self.tv.get_station(o1) and o1 != 'help':
                            self.bot.sendmsg(channel, 'Station not found! See !tv help')
                        else:
                            programm = self.tv.get_programm_at_time_and_station(o1, str(ltime[3]) + str(ltime[4]) + '00')
                    else:
                        programm = self.parse_programm(programm)
                elif len(o) == 2:
                    if not self.tv.get_station(o[1]):
                        self.bot.sendmsg(channel, 'Station not found! See !tv help')
                        return 0
                    else:
                        if o1 == 'now':
                            o1 = str(ltime[3]) + str(ltime[4])
                        try:
                            int(o1)
                            if int(o1) > 2400 or int(o1[2:4]) > 59:
                                self.bot.sendmsg(channel, 'corrupted time! See !tv help')
                            programm = self.tv.get_programm_at_time_and_station(o[1], o1 + '00')
                        except ValueError:
                            if not self.tv.get_station(o1) and o1 != 'help':
                                self.bot.sendmsg(channel, 'Station not found! See !tv help')
                            else:
                                programm = self.tv.get_programm_at_time_and_station(o1, str(ltime[3]) + str(ltime[4]) + '00')

                        programm = self.parse_programm(programm)
                elif self.tv:
                    programm = self.tv.get_programm_now()
                    programm = self.parse_programm(programm)
                    filterstandard = not all
                for i in programm:
                    if not filterstandard or not i['station'][0].lower().replace(' ', '') not in self.standardsender.encode('UTF-8'):
                        if not public:
                            if i['language'] != '':
                                self.bot.sendmsg(user, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title'] + ' (' + i['language'] + ')').encode('utf8'))
                            else:
                                self.bot.sendmsg(user, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title']).encode('utf8'))
                        elif i['language'] != '':
                            self.bot.sendmsg(channel, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title'] + ' (' + i['language'] + ')').encode('utf8'))
                        else:
                            self.bot.sendmsg(channel, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title']).encode('utf8'))

            elif command.lower() == 'tvsearch':
                o = options.split(' ')
                if not self.tv.get_station(o[(len(options.split(' ')) - 1)]):
                    result = self.tv.search(options)
                else:
                    result = self.tv.search((' ').join(o[:-1]))
                t_result = self.parse_programm(result)
                result = []
                ltime = time.localtime()
                for i in t_result:
                    if len(str(ltime[3])) == 1:
                        h = '0' + str(ltime[3])
                    else:
                        h = str(ltime[3])
                    if len(str(ltime[4])) == 1:
                        m = '0' + str(ltime[4])
                    else:
                        m = str(ltime[4])
                    if int(i['stop'][4:12]) > int(str(ltime[1]) + str(ltime[2]) + h + m):
                        if not self.tv.get_station(o[(len(options.split(' ')) - 1)]):
                            result.append(i)
                        elif i['station'][0].lower().replace(' ', '') == o[(len(options.split(' ')) - 1)].lower():
                            result.append(i)

                for i in result[:3]:
                    if i['language'] != '':
                        self.bot.sendmsg(channel, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][6:8]) + '.' + str(i['start'][4:6]) + '., ' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title'] + ' (' + i['language'] + ')').encode('utf8'))
                    else:
                        self.bot.sendmsg(channel, unicode(str(chr(2)) + i['station'][0] + str(chr(2)) + ' (' + str(i['start'][6:8]) + '.' + str(i['start'][4:6]) + '., ' + str(i['start'][8:10]) + ':' + str(i['start'][10:12]) + '-' + str(i['stop'][8:10]) + ':' + str(i['stop'][10:12]) + '): ' + i['title']).encode('utf8'))

                if result == []:
                    self.bot.sendmsg(channel, 'keine passende Sendung gefunden!')
        except Exception, e:
            self.logger.error(e)
            tb_list = traceback.format_tb(sys.exc_info()[2])[1:]
            for entry in tb_list:
                for line in entry.strip().split('\n'):
                    self.logger.error(line)

    def parse_programm(self, programm):
        output = []
        for i in programm:
            try:
                if i['title'][0] != 'D':
                    start = i['start']
                    stop = i['stop']
                    titel = i['title'][0][0]
                    language = i['title'][0][1]
                    station = self.tv.get_station_name(i['channel'])
                    if station[0].lower().replace(' ', '') not in self.ignoresender:
                        output.append({'start': start, 'stop': stop, 'title': titel, 'language': language, 'station': station})
            except:
                self.logger.info(sys.exc_info())

        return output

    def download_data(self):
        if self.source == 'otr':
            for i in os.listdir(self.tvdatadir):
                try:
                    date = i.split('_')[1] + i.split('_')[2] + i.split('_')[3].split('.')[0]
                    if int(date) < int(time.strftime('%Y%m%d', time.localtime())):
                        os.remove(self.tvdatadir + '/' + i)
                except IndexError:
                    pass

            for i in range(self.days):
                filename = time.strftime('epg_%Y_%m_%d.csv', time.gmtime(time.time() + 86400 * i))
                try:
                    if os.stat(self.tvdatadir + '/' + filename).st_mtime + 43200 < time.time():
                        urlutils.download(self.dataurl + filename, self.tvdatadir + '/' + filename)
                except OSError:
                    urlutils.download(self.dataurl + filename, self.tvdatadir + '/' + filename)

        else:
            if self.source == 'xmltv':
                urlutils.download(self.dataurl, self.xmltvfile)
            self.bot.root.getServiceNamed('scheduler').callLater(10, self.processUpdatedData)

    def processUpdatedData(self):
        del self.tv
        if self.source == 'otr':
            complete = True
            for i in range(self.days):
                try:
                    if not self.is_complete(datadir + '/' + time.strftime('epg_%Y_%m_%d.csv', time.gmtime(time.time() + 86400 * i))):
                        complete = False
                except OSError:
                    complete = False

            if not complete:
                self.tv = None
                self.bot.root.getServiceNamed('scheduler').callLater(30, self.processUpdatedData)
                self.bot.logger.info("tvdata is not loaded completely yet. TV-Plugin will be aviable as it's loading is done.")
            else:
                try:
                    self.tv = tv_otr(datadir, self.days, self.bot)
                except:
                    self.bot.logger.info(sys.exec_info())

        elif self.source == 'xmltv':
            try:
                self.tv = tv_xmltv(self.xmltvfile)
                self.bot.root.getServiceNamed('scheduler').callLater(86400, self.download_data)
            except IOError:
                self.logger.info("xmltv-file is not loaded completely yet. TV-Plugin will be aviable as it's loading is done.")
                self.bot.root.getServiceNamed('scheduler').callLater(30, self.processUpdatedData)

        return

    def is_complete(self, filename):
        return time.time() - 1 > os.stat(filename).st_mtime


class tv:

    def get_stations(self, xmlstations):
        stations = {}
        for i in xmlstations:
            stations[i['id']] = i['display-name'][0]

        return stations

    def get_station(self, name):
        for i in self.stations:
            if self.stations[i][0].lower().replace(' ', '').replace('.', '').replace('-', '') == name.lower().replace(' ', '').replace('.', '').replace('-', ''):
                return i

        return 0

    def get_station_name(self, stationid):
        return self.stations[stationid]

    def get_programm_at_time(self, zeit, datum='today'):
        if datum == 'today':
            ltime = time.localtime()
            datum = str(ltime[0]) + '0' * ((len(str(ltime[1])) - 2) * -1) + str(ltime[1]) + '0' * ((len(str(ltime[2])) - 2) * -1) + str(ltime[2])
            del ltime
        sendungen = []
        for i in self.programm:
            if int(i['start'].split(' ')[0]) <= int(datum + zeit) and int(datum + zeit) < int(i['stop'].split(' ')[0]):
                sendungen.append(i)

        return sendungen

    def get_programm_at_time_and_station(self, station, zeit, datum='today'):
        sendungen_all = self.get_programm_at_time(zeit, datum)
        sendungen = []
        station_id = self.get_station(station)
        for i in sendungen_all:
            if i['channel'] == station_id:
                sendungen.append(i)

        return sendungen

    def search(self, begriff):
        result = []
        for i in self.programm:
            if begriff.encode('UTF-8').lower() in i['title'][0][0].lower():
                result.append(i)

        return result

    def get_programm_now(self):
        ltime = time.localtime()
        zeit = str(ltime[3]) + str(ltime[4]) + '00'
        programm = self.get_programm_at_time(zeit)
        return programm


class tv_xmltv(tv):

    def __init__(self, xmltvfile):
        self.stations = xmltv.read_channels(xmltvfile)
        self.programm = xmltv.read_programmes(xmltvfile)
        self.stations = self.get_stations(self.stations)


class tv_otr(tv):

    def __init__(self, datadir, days, bot):
        self.stations = []
        self.programm = []
        self.bot = bot
        for i in range(days):
            self.programm.extend(self.parse(datadir + '/' + time.strftime('epg_%Y_%m_%d.csv', time.gmtime(time.time() + 86400 * i))))

        self.stations = self.get_stations(self.stations)

    def parse(self, filename):
        a = open(filename)
        a = a.readlines()
        programm = []
        for i in a:
            b = i.split(';')
            try:
                t1 = b[1].split('.')
                t2 = b[2].split('.')
                start = t1[2].split(' ')[0] + t1[1] + t1[0] + t1[2].split(' ', 1)[1].replace(':', '')
                stop = t2[2].split(' ')[0] + t2[1] + t2[0] + t2[2].split(' ', 1)[1].replace(':', '')
                channel = b[4].replace(' ', '').lower()
                title = b[5]
                language = b[10]
                programm.append({'start': start, 'stop': stop, 'channel': channel, 'title': [(title, language)]})
                if not self.stations.count({'id': channel, 'display-name': [(b[4].replace(' ', ''), '')]}):
                    self.stations.append({'id': channel, 'display-name': [(b[4].replace(' ', ''), '')]})
            except IndexError:
                pass

        return programm