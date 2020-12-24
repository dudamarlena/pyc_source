# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: J:\workspace\python\haf\haf\common\httprequest.py
# Compiled at: 2020-03-21 04:58:55
# Size of source mod 2**32: 6529 bytes
"""
file name : httpreqeust
description : http request all need this
others :
    support GET POST PUT DELETE method
    support with headers, data
"""
import json, traceback
import urllib.error as urlerror
import urllib.parse
import urllib.request as ur
import requests
from haf.common.log import Log
logger = Log.getLogger(__name__)

class HttpController(object):
    __doc__ = '\n    HttpController\n    using to the get/post/others\n    '

    def __init__(self):
        pass

    @staticmethod
    def getdata(data):
        """
        getdata: using to make data to the url type

        :param data: the origin data
        :return the url type data
        """
        datastr = '?'
        if isinstance(data, bytes):
            data = str(data, encoding='utf-8')
        elif isinstance(data, str):
            try:
                data = json.loads(data)
                for d in data.keys():
                    datastr = datastr + str(d) + '=' + str(data[d]) + '&'

            except:
                return data

        else:
            if isinstance(data, dict):
                for d in data.keys():
                    datastr = datastr + str(d) + '=' + str(data[d]) + '&'

        return datastr[:-1]

    @staticmethod
    def get(url, data=None, headers=None, **kwargs):
        """
        get of http

        :param url the request url
        :param data the origin data
        :param headers the get headers

        :return the response of get
        """
        key = kwargs.get('key')
        try:
            url = url + HttpController.getdata(data)
            if 'application/json' in headers.values():
                if 'using_data' in kwargs:
                    data = bytes((json.dumps(data if data is not None else {})), encoding='utf-8')
                elif 'using_origin_data' in kwargs:
                    pass
                else:
                    data = None
            elif 'using_data' in kwargs:
                data = bytes((urllib.parse.urlencode(data)), encoding='utf-8')
            else:
                if 'using_origin_data' in kwargs:
                    pass
                else:
                    data = None
            logger.debug(f"{key} GET [url] {url}", __name__)
            response = requests.get(url, json=data, headers=headers, timeout=10)
            if response is None:
                return {'result': 'None'}
            logger.debug(f"{key} {str(response)}", __name__)
            return response
        except requests.HTTPError as e:
            try:
                logger.error(f"{key}{str(e)}", __name__)
                logger.error(f"{key}{traceback.format_exc()}", __name__)
                return e
            finally:
                e = None
                del e

        except Exception as ee:
            try:
                logger.error(f"{key}{str(ee)}")
                logger.error(f"{key}{traceback.format_exc()}", __name__)
                return ee
            finally:
                ee = None
                del ee

    @staticmethod
    def post(url, data=None, headers=None, **kwargs):
        """
        post of http

        :param url the request url
        :param data the origin data
        :param headers the post headers

        :return the response of post
        """
        key = kwargs.get('key')
        try:
            if 'application/json' in headers.values():
                data = bytes((json.dumps(data)), encoding='utf-8')
            else:
                data = bytes((urllib.parse.urlencode(data)), encoding='utf-8')
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response is None:
                return {'result': 'None'}
            logger.debug(f"{key} POST {str(response)}", __name__)
            return response
        except requests.HTTPError as e:
            try:
                logger.error(f"{key} {str(e)}", __name__)
                return e
            finally:
                e = None
                del e

        except urlerror.HTTPError as httpe:
            try:
                logger.error(f"{key} {str(httpe)}", __name__)
                return httpe
            finally:
                httpe = None
                del httpe

        except Exception as ee:
            try:
                logger.error(f"{key} {str(ee)}", __name__)
                return ee
            finally:
                ee = None
                del ee

    def put(self, url, data=None, headers=None, **kwargs):
        """
        put of http

        :param url the request url
        :param data the origin data
        :param headers the put headers

        :return the response of put
        """
        key = kwargs.get('key')
        try:
            if 'application/json' in headers.values():
                data = bytes((json.dumps(data)), encoding='utf-8')
            else:
                data = bytes((urllib.parse.urlencode(data)), encoding='utf-8')
            response = requests.put(url, json=data, headers=headers, timeout=10)
            if response is None:
                return {'result': 'None'}
            logger.debug(f"{key} PUT {str(response)}", __name__)
            return response
        except requests.HTTPError as e:
            try:
                logger.error(f"{key} {str(e)}", __name__)
                return e
            finally:
                e = None
                del e

        except urlerror.HTTPError as httpe:
            try:
                logger.error(f"{key} {str(httpe)}", __name__)
                return httpe
            finally:
                httpe = None
                del httpe

        except Exception as ee:
            try:
                logger.error(f"{key} {str(ee)}", __name__)
                return ee
            finally:
                ee = None
                del ee

    def delete(self, url, data=None, headers=None, **kwargs):
        """
        delete of http

        :param url the request url
        :param data the origin data
        :param headers the delete headers

        :return the response of delete
        """
        key = kwargs.get('key')
        try:
            if 'application/json' in headers.values():
                data = bytes((json.dumps(data)), encoding='utf-8')
            else:
                data = bytes((urllib.parse.urlencode(data)), encoding='utf-8')
            response = requests.delete(url, json=data, headers=headers, timeout=10)
            if response is None:
                return {'result': 'None'}
            logger.debug(f"{key} DELETE {str(response)}", __name__)
            return response
        except requests.HTTPError as e:
            try:
                logger.error(f"{key} {str(e)}", __name__)
                return e
            finally:
                e = None
                del e

        except urlerror.HTTPError as httpe:
            try:
                logger.error(f"{key} {str(httpe)}", __name__)
                return httpe
            finally:
                httpe = None
                del httpe

        except Exception as ee:
            try:
                logger.error(f"{key} {str(ee)}", __name__)
                return ee
            finally:
                ee = None
                del ee