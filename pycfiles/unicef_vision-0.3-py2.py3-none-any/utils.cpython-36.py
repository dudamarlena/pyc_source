# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/vision/src/unicef_vision/utils.py
# Compiled at: 2019-02-05 15:36:21
# Size of source mod 2**32: 2030 bytes
import datetime, json, requests
from django.apps import apps
from django.conf import settings

def get_vision_logger_domain_model():
    get_model = apps.get_model
    return get_model(settings.VISION_LOGGER_MODEL)


def get_data_from_insight(endpoint, data={}):
    url = ('{}/{}'.format(settings.VISION_URL, endpoint).format)(**data)
    response = requests.get(url,
      headers={'Content-Type': 'application/json'},
      auth=(
     settings.VISION_USER, settings.VISION_PASSWORD),
      verify=False)
    if response.status_code != 200:
        return (
         False, 'Loading data from Vision Failed, status {}'.format(response.status_code))
    try:
        result = json.loads(response.json())
    except ValueError:
        return (
         False, 'Loading data from Vision Failed, no valid response returned for data: {}'.format(data))
    else:
        return (
         True, result)


def wcf_json_date_as_datetime(jd):
    if jd is None:
        return
    else:
        sign = jd[(-7)]
        if sign not in '-+' or len(jd) == 13:
            millisecs = int(jd[6:-2])
        else:
            millisecs = int(jd[6:-7])
            hh = int(jd[-7:-4])
            mm = int(jd[-4:-2])
            if sign == '-':
                mm = -mm
            millisecs += (hh * 60 + mm) * 60000
        return datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=(millisecs * 1000))


def wcf_json_date_as_date(jd):
    if jd is None:
        return
    else:
        sign = jd[(-7)]
        if sign not in '-+' or len(jd) == 13:
            millisecs = int(jd[6:-2])
        else:
            millisecs = int(jd[6:-7])
            hh = int(jd[-7:-4])
            mm = int(jd[-4:-2])
            if sign == '-':
                mm = -mm
            millisecs += (hh * 60 + mm) * 60000
        my_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=(millisecs * 1000))
        return my_date.date()


def comp_decimals(y, x):

    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    return isclose(float(x), float(y))