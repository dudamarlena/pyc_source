# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-admin/phishdetectadmin/utils.py
# Compiled at: 2020-01-02 10:05:19
# Size of source mod 2**32: 2171 bytes
import re, smtplib
from urllib.parse import urlparse
from .config import load_config

def get_indicator_type(indicator):
    email_regex = re.compile('[^@]+@[^@]+\\.[^@]+')
    if email_regex.fullmatch(indicator):
        return 'email'
    domain_regex = re.compile('[a-zA-Z\\d-]{,63}(\\.[a-zA-Z\\d-]{,63})*')
    if domain_regex.fullmatch(indicator):
        return 'domain'


def clean_indicator(indicator):
    indicator = indicator.strip()
    indicator = indicator.lower()
    indicator = indicator.replace('[.]', '.')
    indicator = indicator.replace('[@]', '@')
    if get_indicator_type(indicator) == 'domain':
        if indicator.startswith('www.'):
            indicator = indicator[4:]
    return indicator


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def send_email(recipient, subject, message):
    config = load_config()
    if 'smtp_host' not in config or config['smtp_host'].strip() == '':
        return
    server = smtplib.SMTP(config['smtp_host'], 587)
    server.ehlo()
    server.starttls()
    server.login(config['smtp_user'], config['smtp_pass'])
    msg_text = 'From: PhishDetect <{}>\nTo: {}\nSubject: {}\n\n{}\n'.format(config['smtp_user'], recipient, subject, message)
    server.sendmail(config['smtp_user'], recipient, msg_text)
    server.close()