# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: BrickBreaker/highscore.py
# Compiled at: 2017-12-20 17:29:08
import fileinput, hashlib, operator, getpass, platform

class Highscore:

    def __init__(self):
        self._highscore = self.load()

    def get_scores(self):
        return self._highscore

    @staticmethod
    def load():
        user = getpass.getuser()
        highscore = []
        if platform.system() == 'Linux':
            try:
                f = open('/var/tmp/highscore.dat', 'r')
            except IOError:
                f = open('/var/tmp/highscore.dat', 'w')

            for line in fileinput.input('/var/tmp/highscore.dat'):
                name, score, md5 = line.split('[::]')
                md5 = md5.replace('\n', '')
                if str(hashlib.md5(str.encode(str(name + score + 'pygame'))).hexdigest()) == str(md5):
                    highscore.append([str(name), int(score), str(md5)])

            highscore.sort(key=operator.itemgetter(1), reverse=True)
            highscore = highscore[0:10]
            f.close()
        elif platform.system() == 'Darwin':
            try:
                f = open('/var/tmp/highscore.dat', 'r')
            except IOError:
                f = open('/var/tmp/highscore.dat', 'w')

            for line in fileinput.input('/var/tmp/highscore.dat'):
                name, score, md5 = line.split('[::]')
                md5 = md5.replace('\n', '')
                if str(hashlib.md5(str.encode(str(name + score + 'pygame'))).hexdigest()) == str(md5):
                    highscore.append([str(name), int(score), str(md5)])

            highscore.sort(key=operator.itemgetter(1), reverse=True)
            highscore = highscore[0:10]
            f.close()
        return highscore

    def add(self, name, score):
        user = getpass.getuser()
        hash = hashlib.md5(str(name + str(score) + 'pygame').encode('utf-8'))
        self._highscore.append([name, str(score), hash.hexdigest()])
        if platform.system() == 'Linux':
            with open('/var/tmp/highscore.dat', 'w') as (f):
                for name, score, md5 in self._highscore:
                    f.write(str(name) + '[::]' + str(score) + '[::]' + str(md5) + '\n')

        elif platform.system() == 'Darwin':
            with open('/var/tmp/highscore.dat', 'w') as (f):
                for name, score, md5 in self._highscore:
                    f.write(str(name) + '[::]' + str(score) + '[::]' + str(md5) + '\n')