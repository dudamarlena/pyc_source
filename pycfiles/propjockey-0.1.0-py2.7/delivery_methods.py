# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/passwordless/delivery_methods.py
# Compiled at: 2017-11-22 16:02:35
import abc, logging, sys
from propjockey.mailers import Mailgun
SUCCESS, INFO, WARNING, ERROR = ('success', 'info', 'warning', 'danger')

class DeliveryMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, login_url, **kwargs):
        pass


class DeliverByNull(DeliveryMethod):

    def __init__(self, config):
        pass

    def __call__(self, login_url, email, permitted):
        if permitted['success']:
            return (('Deliver: {} to {}').format(login_url, email), SUCCESS)
        else:
            return (
             ('Deliver: no permission to {}').format(email), WARNING)


class DeliverByLog(DeliveryMethod):

    def __init__(self, config):
        """ just log that we tried to deliver. """
        self.logs = logging.getLogger(__name__)
        self.logs.setLevel(logging.DEBUG)
        log = logging.StreamHandler(sys.stdout)
        log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log.setFormatter(formatter)
        self.logs.addHandler(log)

    def __call__(self, login_url, email, permitted):
        if permitted['success']:
            self.logs.debug('Deliver: ' + login_url + ' to ' + email)
            return (
             ('Deliver: {} to {}').format(login_url, email), SUCCESS)
        else:
            self.logs.debug('Deliver: no permission to ' + email)
            return (('Deliver: no permission to {}').format(email), WARNING)


class DeliverByMailgun(DeliveryMethod):

    def __init__(self, config):
        config = config['MAILGUN']
        self.mailgun = Mailgun(config)
        self.from_email = config['DELIVER_LOGIN_URL']['FROM']
        self.subject = config['DELIVER_LOGIN_URL']['SUBJECT']

    def __call__(self, login_url, email, permitted):
        if permitted['success']:
            text = ("Here's your login link:\n{}\n").format(login_url)
        else:
            text = permitted['text']
        message = {'text': text, 'from': self.from_email, 
           'to': [
                email], 
           'subject': self.subject}
        response = self.mailgun.send(message)
        if response.status_code == 200:
            return (('Sent login link to {}').format(email), SUCCESS)
        else:
            return (
             'Failed to send login link.', ERROR)


DELIVERY_METHODS = {'log': DeliverByLog, 
   'null': DeliverByNull, 
   'mailgun': DeliverByMailgun}