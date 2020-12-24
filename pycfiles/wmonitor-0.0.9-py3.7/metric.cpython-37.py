# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmonitor/metric.py
# Compiled at: 2019-10-16 09:02:56
# Size of source mod 2**32: 2557 bytes
import logging, os, time, requests
from requests import adapters
from wmonitor import constant
url = constant.Config.domain + '/adapter/metrics'
requests_log = logging.getLogger('WMonitor')
handler = logging.FileHandler(os.path.join(constant.Config.log_dir, 'wmonitor.log'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
requests_log.addHandler(handler)
print(constant.Config.logging_level)
requests_log.setLevel(constant.Config.logging_level)
session = requests.session()
session.mount('http://', adapters.HTTPAdapter(pool_connections=1, pool_maxsize=20, max_retries=3))
session.post(url)

class MetricSender:

    def send(self):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url=url, data=(self.__str__()), headers=headers)
            requests_log.info('发送成功, content: %s' % response.content)
            requests_log.debug('发送报文，data: %s' % self.__str__())
            response.close()
        except BaseException:
            requests_log.info('发送监控信息失败。data:%s' % self.__str__())


class Metric(MetricSender):

    @classmethod
    def gauge(cls, metric, value=1):
        entity = cls()
        entity._Metric__counterType = 'Gauge'
        entity._Metric__metric = metric
        entity._Metric__value = value
        entity._Metric__tags = ''
        return entity

    @classmethod
    def counter(cls, metric, value=1):
        entity = cls()
        entity._Metric__metric = metric
        entity._Metric__counterType = 'Counter'
        entity._Metric__value = value
        entity._Metric__tags = ''
        return entity

    @classmethod
    def state(cls, metric, value=1):
        entity = cls()
        entity._Metric__metric = metric
        entity._Metric__counterType = 'State'
        entity._Metric__value = value
        entity._Metric__tags = ''
        return entity

    def tags(self, tags):
        self._Metric__tags = tags
        return self

    def value(self, value):
        self._Metric__value = value
        return self

    def __str__(self):
        result = {}
        all_attribute = self.__dict__
        for key in all_attribute:
            key = str(key)
            real_name = key.replace('_Metric__', '')
            result[real_name] = self.__getattribute__(key)

        return result.__str__()

    def send(self):
        self._Metric__appName = constant.Config.app_code
        self._Metric__timestamp = time.time()
        super().send()


if __name__ == '__main__':
    Metric.gauge('test').send()