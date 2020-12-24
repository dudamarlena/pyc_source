# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/3.7/site-packages/tripgo_parser/get.py
# Compiled at: 2020-01-31 20:22:28
# Size of source mod 2**32: 5366 bytes
import os, requests, json, datetime, time

class Response:

    def __init__(self, key, origlat, origlon, destlat, destlon, startime, date, tripid='', modes=None, allModes=False, bestOnly=False):
        self.tripid = tripid
        self.origlat = origlat
        self.origlon = origlon
        self.destlat = destlat
        self.destlon = destlon
        self.startime = startime
        self.orig = '(' + str(origlat) + ',' + str(origlon) + ')'
        self.dest = '(' + str(destlat) + ',' + str(destlon) + ')'
        self.startime = startime
        self.allModes = allModes
        self.bestOnly = bestOnly
        self.modes = modes if modes is not None else []
        self.startimeTimestamp = self.dateToTimestamp(date) + int(startime) * 60
        self.fileExists = False
        self.usageExceeded = False
        self.parameters = self.create_parameters()
        self.headers = {'X-TripGo-Key': key}

    def create_parameters(self):
        parameters = {'v':11, 
         'from':self.orig, 
         'to':self.dest, 
         'departAfter':int(self.startimeTimestamp), 
         'bestOnly':self.bestOnly}
        if len(self.modes) != 0:
            parameters.update({'modes': self.modes})
        else:
            parameters.update({'allModes': True})
        return parameters

    def fetch(self):
        while True:
            try:
                results = requests.get('https://api.tripgo.com/v1/routing.json', params=(self.parameters),
                  headers=(self.headers))
                data = results.json()
                print('Successful fetch from %s' % results.url)
                self.checkUsageLimit(data)
                if self.usageExceeded:
                    print('Error: API usage exceeded. Waiting 60 seconds...')
                    time.sleep(60)
                    continue
                return data
            except Exception as e:
                try:
                    print('Error: ' + str(e.message))
                    print('Retrying in 5...')
                    time.sleep(5)
                    continue
                finally:
                    e = None
                    del e

    def save(self, destination_folder, unique_id=''):
        directory = self.dir_path(destination_folder)
        path, id, file_exists = self.file_path(directory, unique_id)
        if file_exists:
            print('File {} already exists.'.format(str(id)))
        else:
            data = self.fetch()
            with open(path, 'w') as (f):
                json.dump(data, f)
        return True

    def dir_path(self, destination_folder):
        cwd = os.getcwd()
        directory = os.path.join(cwd, destination_folder)
        dirExists = os.path.exists(directory)
        if not dirExists:
            os.mkdir(destination_folder)
        return directory

    def file_path(self, directory, unique_id=''):
        md = '-'.join(self.modes) if self.modes is not [] else ''
        if unique_id == '' and self.tripid == '':
            olt = self.origlat[-4:]
            oln = self.origlon[-4:]
            dlt = self.destlat[-4:]
            dln = self.destlon[-4:]
            unique_id = '{}-{}-{}-{}-{}{}.json'.format(olt, oln, dlt, dln, self.startime, md)
        else:
            if unique_id == '':
                if self.tripid != '':
                    if self.modes == []:
                        unique_id = '{}-{}.json'.format(self.tripid, self.startime)
                else:
                    unique_id = '{}-{}-{}.json'.format(self.tripid, self.startime, md)
            else:
                unique_id = ''.join([unique_id, '.json'])
        path = os.path.join(directory, unique_id)
        pathExists = os.path.exists(path)
        return (
         path, unique_id, pathExists)

    def dateToTimestamp(self, dateString):
        dateArray = dateString.split('/')
        dateArray = [int(i) for i in dateArray]
        currentYear = datetime.datetime.now().year
        timestamp = datetime.datetime(currentYear + 1, dateArray[1], dateArray[0]).timestamp()
        return int(timestamp) + 36000

    def checkUsageLimit(self, data):
        try:
            if 'usage' in data['error']:
                self.usageExceeded = True
        except:
            self.usageExceeded = False