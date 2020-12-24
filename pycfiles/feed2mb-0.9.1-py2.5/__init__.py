# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feed2mb/__init__.py
# Compiled at: 2010-10-19 17:39:01
import feedparser, pickle, os, sys, urllib
from ConfigParser import ConfigParser, NoOptionError
from options import Options
import re, time
from pprint import pprint
from config import MicroblogConfig
import microblog, os, tempfile, logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def update(**kwargs):
    global __version__
    if not kwargs:
        opt = Options()
        options = opt.parse()
        if options.show_version:
            print __version__
            sys.exit(1)
        if options.sample_config:
            from pkg_resources import resource_string
            foo_config = resource_string(__name__, '../docs/default.cfg.sample')
            print foo_config
            sys.exit(1)
        if options.log_filename:
            fh = logging.FileHandler(options.log_filename)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            log.addHandler(fh)
        else:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        conf = MicroblogConfig(options.config_filename)
        configs = conf.configs()
    else:
        configs = []
        kwargs['items'] = 5
        configs.append(kwargs)
        url = kwargs['url']
        shortener = kwargs['shortener']
        kwargs['interval'] = parsetime('00:05')
    pid = os.getpid()
    log.debug('Starting feed2mb with pid: ' + str(pid))
    if not configs[0]['pidfile']:
        pidfile = tempfile.NamedTemporaryFile()
    else:
        pidfile = open(configs[0]['pidfile'], 'w+b')
    pidfile.write(str(pid))
    pidfile.flush()
    log.debug('PID saved in: ' + pidfile.name)
    try:
        while True:
            interval = configs[0]['interval']
            for cf in configs:
                the_service = microblog.service(**cf).get()
                the_service.update()
                log.debug('next ' + cf['service'] + ' update in: ' + str(interval) + ' seconds')
                del the_service

            time.sleep(interval)

    finally:
        pidfile.close()
        try:
            os.remove(configs[0]['pidfile'])
        except:
            pass


__version__ = '0.9.1'