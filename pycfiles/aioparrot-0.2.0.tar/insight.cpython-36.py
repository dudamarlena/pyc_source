# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/device/insight.py
# Compiled at: 2018-11-10 21:59:50
# Size of source mod 2**32: 2538 bytes
from datetime import datetime
from .switch import Switch
import asyncio as aio

class Insight(Switch):

    def __init__(self, url):
        super().__init__(url)
        self.measurements = {'state':0,  'last change':0, 
         'current on time':0, 
         'today on time':0, 
         'total on time':0, 
         'today consumption':0, 
         'total consumption':0, 
         'current power':0}

    def __repr__(self):
        return '<WeMo Insight "{}">'.format(self.name)

    @property
    def insight_params(self):
        xx = aio.ensure_future(self._insight_params())
        return self.measurements

    async def _insight_params(self):
        params = await self.insight.GetInsightParams()
        params = params.get('InsightParams')
        state, lastchange, onfor, ontoday, ontotal, timeperiod, _x, currentmw, todaymw, totalmw, powerthreshold = params.split('|')
        self.measurements = {'state':state,  'last change':datetime.fromtimestamp(int(lastchange)).strftime('%Y-%m-%d %H:%M:%S'), 
         'current on time':int(onfor), 
         'today on time':int(ontoday), 
         'total on time':int(ontotal), 
         'today consumption':int(float(todaymw)), 
         'total consumption':int(float(totalmw)), 
         'current power':int(float(currentmw))}

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