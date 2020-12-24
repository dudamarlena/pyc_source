# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/dns/dnspod.py
# Compiled at: 2017-03-20 03:08:12
import logging, os, requests
logger = logging.getLogger(__name__)

class DNSPod(object):

    def __init__(self, root='https://dnsapi.cn', api_format='json', domain=None):
        super(DNSPod, self).__init__()
        self.logger = logger
        self.root = root
        self.format = api_format
        self.domain = domain

    def get_token(self):
        """
        currently we get dnspod token from OS environment.
        :return:
        """
        return os.environ.get('DNSPOD_LOGIN_TOKEN')

    def validated_data(self, response, excepted_code):
        """
        check dnspod api response

        :param response:
        :param excepted_code:
        :return:
        """
        try:
            rtn = response.json()
            if rtn.get('status') and rtn['status'].get('code') == '1':
                self.logger.debug('request success,json data:%s' % rtn)
                return rtn
            log_msg = 'request fail.\n\turl:\t\t\t%s\n\trequest:\t\t%s\n\tresponse:\t\t%s' % (
             response.url,
             response.request.body,
             response.text)
            if rtn['status']['code'] in excepted_code:
                logger_handler = self.logger.warning
            else:
                logger_handler = self.logger.error
                rtn = None
            logger_handler(log_msg)
            return rtn
        except Exception as e:
            self.logger.error('parse json fail, url:%s, rtn:%s, exception:%s' % (
             response.url, response.text, e))
            return

        return

    def request(self, api_path, data={}, excepted_code=[]):
        """
        generic request method
        :param api:
        :param data:
        :return:
        """
        api = self.root + api_path
        token = self.get_token()
        if not token:
            raise ValueError("please set `DNSPOD_LOGIN_TOKEN' environment")
        data.update({'login_token': token, 
           'format': 'json'})
        response = requests.post(api, data)
        return self.validated_data(response, excepted_code)

    def get_version(self):
        """
        get dnspod api version
        :return: version or raise ValueError
        """
        rtn = self.request('/Info.Version')
        if not rtn:
            raise ValueError
        return rtn['status']['message']

    def bind_domain(self, domain=None):
        """
        if domain is exist,we consider it is works.

        if user set domain, after bind progress, self.domain will set to domain

        :param domain:
        :return:
        """
        domain = domain or self.domain
        if not domain:
            raise ValueError('please set domain or self.domain value')
        rtn = self.request('/Domain.Create', {'domain': domain}, [
         '7'])
        if rtn['status']['code'] in ('1', '7'):
            self.domain = domain
            return True
        else:
            return False

    def get_record(self, query, length=32):
        """
        get domain record.
        :param data:
        :param length: currently,only support max 32 sub domain
        :return: record, if not exist return None
        """
        if not self.domain:
            raise ValueError("please set `self.domain' or use `bind_domain' to rebind domain")
        rtn = self.request('/Record.List', {'domain': self.domain, 
           'sub_domain': query['sub_domain'], 
           'length': length})
        if rtn:
            for record in rtn['records']:
                compared = [True if record['value'] == query['value'] else False,
                 True if record['line'].encode('utf-8') == query['record_line'] else False,
                 True if record['type'] == query['record_type'] else False]
                if False not in compared:
                    return record

    def get_record_id(self, query, length=32):
        """
        get domain record id named by dnspod
        :param query:
        :param length:
        :return: record id.if not exist,return None
        """
        record = self.get_record(query, length)
        if record:
            return record['id']

    def remove_domain(self):
        """

        :param api_data:
        :return:
        """
        if not self.domain:
            raise ValueError("please set `self.domain' or use `bind_domain' to rebind domain")
        return self.request('/Domain.Remove', {'domain': self.domain})

    def remove_record(self, api_data):
        """
        only exist record will be deleted
        :param api_data:
        :return:
        """
        if not self.domain:
            raise ValueError("please set `self.domain' or use `bind_domain' to rebind domain")
        record_id = self.get_record_id(api_data)
        if record_id:
            return self.request('/Record.Remove', {'domain': self.domain, 
               'record_id': record_id})

    def modify_record(self, record_id, api_data):
        """
        modify record

        :param record_id: dnspod record id
        :param api_data:
        :return:
        """
        if not self.domain:
            raise ValueError("please set `self.domain' or use `bind_domain' to rebind domain")
        api_data.update({'domain': self.domain, 
           'record_id': record_id})
        return self.request('/Record.Modify', api_data)

    def bind_record(self, value, record_type, sub_domain='@', record_line='默认', weight=None, mx_order=5, ttl=600, active=True, overwrite=True, **kwargs):
        """
        :param value:
        :param record_type:
        :param sub_domain:
        :param record_line:
        :param weight: your account must be VIP account
        :param mx_order:
        :param ttl:
        :param active:
        :param overwrite: rewrite if record is exist. default is True
        :param kwargs:
        :return: dict or None if fail
        """
        if not self.domain:
            raise ValueError("please set `self.domain' or use `bind_domain' to rebind domain")
        data = {'domain': self.domain, 
           'record_type': record_type.upper(), 
           'sub_domain': sub_domain, 
           'record_line': record_line, 
           'value': value, 
           'ttl': ttl, 
           'status': 'enable' if active else 'disable'}
        if data['record_type'] == 'MX':
            data['mx'] = mx_order
        if weight:
            data['weight'] = weight
        rtn = self.request('/Record.Create', data, excepted_code=['104'])
        if rtn:
            if rtn['status']['code'] == '104':
                if overwrite is True:
                    record_id = self.get_record_id(data)
                    self.modify_record(record_id, data)
            return rtn