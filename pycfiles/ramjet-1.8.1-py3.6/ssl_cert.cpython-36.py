# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/monitors/ssl_cert.py
# Compiled at: 2017-11-07 01:37:57
# Size of source mod 2**32: 1936 bytes
import socket, datetime, ssl
from textwrap import dedent
from ramjet.engines import ioloop, thread_executor
from ramjet.utils import send_mail
from .base import logger as monitor_logger
ALERT_RECEIVERS = [
 'ppcelery@gmail.com']
DOMAINS = [
 'blog.laisky.com']
logger = monitor_logger.getChild('ssl_cert')

def bind_task():

    def run():
        logger.info('running...')
        thread_executor.submit(main)
        ioloop.call_later(86400, run)

    run()


def main():
    try:
        for domain in DOMAINS:
            expired_at = load_ssl_expiry_datetime(domain)
            if is_need_to_alert(expired_at):
                send_alert_email(domain, expired_at)

    except Exception as err:
        logger.exception(err)


def send_alert_email(domain, expired_at):
    logger.info('send_alert_email for domain %s', domain)
    content = dedent("\n        These domains' cert is goging to expired!\n\n        {domain}: will expired at {expired_at}\n    ".format(domain=domain, expired_at=expired_at))
    send_mail(to_addrs=ALERT_RECEIVERS, subject='HTTPS cert going to expired!', content=content)


def load_ssl_expiry_datetime(hostname):
    logger.debug('load_ssl_expiry_datetime for hostname: %s', hostname)
    ssl_date_fmt = '%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket((socket.socket(socket.AF_INET)),
      server_hostname=hostname)
    conn.settimeout(3.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def is_need_to_alert(valid_to):
    return valid_to - datetime.datetime.utcnow() < datetime.timedelta(days=7)


if __name__ == '__main__':
    print(load_ssl_expiry_datetime('laisky.com'))