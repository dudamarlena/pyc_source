# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyano/config.py
# Compiled at: 2010-11-11 18:17:01
import ConfigParser, pkgutil

class Config:
    pass


conf = Config()
PYANO = 'Pyano'
NONE = ''
RANDOM = 'RANDOM'
POST = 'Post'

class ConfigError(Exception):
    pass


def _get_html(config, conf_name, pkg_name):
    param = config.get(PYANO, conf_name)
    if not param:
        return pkgutil.get_data(__name__, pkg_name)
    try:
        return open(param).read()
    except IOError:
        raise ConfigError('Error reading ' + param + '.')


def parse_config(config_file=None):
    config = ConfigParser.SafeConfigParser()
    config.add_section(PYANO)
    config.set(PYANO, 'mixmaster', '/usr/bin/mixmaster')
    config.set(PYANO, 'remailer_addr', '')
    config.set(PYANO, 'remailer_mx', 'localhost')
    config.set(PYANO, 'mlist2', '')
    config.set(PYANO, 'allow_from', '')
    config.set(PYANO, 'hist_file', '')
    config.set(PYANO, 'hist_window', '15')
    config.set(PYANO, 'hist_max_uses', '5')
    config.set(PYANO, 'banned_file', '')
    config.set(PYANO, 'chain_max_length', '5')
    config.set(PYANO, 'max_copies', '5')
    config.set(PYANO, 'mail_html', '')
    config.set(PYANO, 'news_html', '')
    config.set(PYANO, 'block_html', '')
    config.set(PYANO, 'mail_form_html', '')
    config.set(PYANO, 'news_form_html', '')
    config.set(PYANO, 'mail2news', 'mail2news@dizum.com, mail2news@mixmin.net, mail2news@m2n.mixmin.net, mail2news@reece.net.au, mail2news@tioat.net, ' + POST)
    config.set(PYANO, 'bad_mail2news', '')
    try:
        if config_file != None:
            config.read(config_file)
    except:
        raise ConfigError('Error parsing configuration file.')

    conf.mixmaster = config.get(PYANO, 'mixmaster')
    conf.remailer_addr = config.get(PYANO, 'remailer_addr')
    conf.remailer_mx = config.get(PYANO, 'remailer_mx')
    conf.mlist2 = config.get(PYANO, 'mlist2')
    conf.allow_from = config.get(PYANO, 'allow_from')
    conf.hist_file = config.get(PYANO, 'hist_file')
    conf.hist_window = config.getint(PYANO, 'hist_window')
    conf.hist_max_uses = config.getint(PYANO, 'hist_max_uses')
    conf.banned_file = config.get(PYANO, 'banned_file')
    conf.chain_max_length = config.getint(PYANO, 'chain_max_length')
    conf.max_copies = config.getint(PYANO, 'max_copies')
    conf.mail2news = [ gateway.strip() for gateway in config.get(PYANO, 'mail2news').split(',') ]
    conf.bad_mail2news = config.get(PYANO, 'bad_mail2news')
    conf.mail_html = _get_html(config, 'mail_html', 'html/mail.html')
    conf.news_html = _get_html(config, 'news_html', 'html/news.html')
    conf.block_html = _get_html(config, 'block_html', 'html/block.html')
    conf.mail_form_html = _get_html(config, 'mail_form_html', 'html/mail_form.html')
    conf.news_form_html = _get_html(config, 'news_form_html', 'html/news_form.html')
    return