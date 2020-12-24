# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/LossInfo.py
# Compiled at: 2018-11-05 10:41:30
# Size of source mod 2**32: 1968 bytes
import numpy as np, psycopg2
import astropy.units as u
import astropy.units.astrophys as ua

class LossInfo:

    def __init__(self, atom, lifetime, aplanet, database):
        self.photo = 0.0
        self.eimp = 0.0
        self.chX = 0.0
        self.reactions = []
        if lifetime.value < 0:
            self.photo = np.abs(1.0 / lifetime.value)
            self.reactions = 'Generic photo reaction.'
        else:
            con = psycopg2.connect(host='localhost', database=database)
            cur = con.cursor()
            cur.execute('SELECT reaction, kappa\n                           FROM photorates\n                           WHERE species=%s and bestvalue=True', (
             atom,))
            if cur.rowcount == 0:
                print('No photoreactions found')
            else:
                rows = cur.fetchall()
                for r in rows:
                    self.reactions.append(r[0])
                    self.photo += r[1] / aplanet ** 2

        if len(self.reactions) == 0:
            self.reactions = None

    def __len__(self):
        if self.reactions is not None:
            return len(self.reactions)
        return 0

    def __str__(self):
        if len(self) == 0:
            print('No reactions included')
        else:
            if len(self) == 1:
                print('Included Reaction: {}'.format(self.reactions[0]))
            else:
                print('\tIncluded Reactions: {}'.format(tuple(self.reactions)))
        if self.photo != 0:
            print('Photo Rate = {:0.2e} s'.format(self.photo))
        if self.eimp != 0:
            print('Electron Impact Rate = {:0.2e} UNIT'.format(self.eimp))
        if self.chX != 0:
            print('Charge Exchange Rate = {:0.2e} UNIT'.format(self.chX.value))
        return ''