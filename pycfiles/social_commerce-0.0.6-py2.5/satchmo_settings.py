# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/satchmo_settings.py
# Compiled at: 2009-10-31 23:19:40
import os, logging
SITE_DOMAIN = 'localhost'
MIDDLEWARE_CLASSES += ('satchmo_store.shop.SSLMiddleware.SSLRedirect', )
TEMPLATE_CONTEXT_PROCESSORS += ('satchmo_store.shop.context_processors.settings', )
INSTALLED_APPS += ('satchmo_store.shop', 'django.contrib.comments', 'django.contrib.sitemaps',
                   'registration', 'keyedcache', 'livesettings', 'l10n', 'sorl.thumbnail',
                   'satchmo_store.contact', 'tax', 'tax.modules.no', 'tax.modules.area',
                   'tax.modules.percent', 'shipping', 'product', 'payment', 'payment.modules.giftcertificate',
                   'satchmo_utils', 'app_plugins')
SATCHMO_SETTINGS = {'SHOP_BASE': '/', 
   'MULTISHOP': False}
CACHE_TIMEOUT = 300
ACCOUNT_ACTIVATION_DAYS = 7
CACHE_PREFIX = 'STORE'
LOGDIR = os.path.abspath(os.path.dirname(__file__))
LOGFILE = 'satchmo.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=os.path.join(LOGDIR, LOGFILE), filemode='w')
fileLog = logging.FileHandler(os.path.join(LOGDIR, LOGFILE), 'w')
fileLog.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
fileLog.setFormatter(formatter)
logging.getLogger('').addHandler(fileLog)
logging.getLogger('keyedcache').setLevel(logging.INFO)
logging.info('Satchmo Started')