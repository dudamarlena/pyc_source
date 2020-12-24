# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/device/insight.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 1899 bytes
from datetime import datetime
from .switch import Switch

class Insight(Switch):

    def __repr__(self):
        return '<WeMo Insight "{name}">'.format(name=(self.name))

    @property
    def insight_params(self):
        params = self.insight.GetInsightParams().get('InsightParams')
        state, lastchange, onfor, ontoday, ontotal, timeperiod, _x, currentmw, todaymw, totalmw, powerthreshold = params.split('|')
        return {'state':state,  'lastchange':datetime.fromtimestamp(int(lastchange)), 
         'onfor':int(onfor), 
         'ontoday':int(ontoday), 
         'ontotal':int(ontotal), 
         'todaymw':int(float(todaymw)), 
         'totalmw':int(float(totalmw)), 
         'currentpower':int(float(currentmw))}

    @property
    def today_kwh(self):
        return self.insight_params['todaymw'] * 1.6666667e-08

    @property
    def current_power(self):
        """
        Returns the current power usage in mW.
        """
        return self.insight_params['currentpower']

    @property
    def today_on_time(self):
        return self.insight_params['ontoday']

    @property
    def on_for(self):
        return self.insight_params['onfor']

    @property
    def last_change(self):
        return self.insight_params['lastchange']

    @property
    def today_standby_time(self):
        return self.insight_params['ontoday']

    @property
    def ontotal(self):
        return self.insight_params['ontotal']

    @property
    def totalmw(self):
        return self.insight_params['totalmw']