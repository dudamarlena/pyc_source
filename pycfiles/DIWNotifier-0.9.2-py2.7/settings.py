# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/settings.py
# Compiled at: 2014-02-05 13:50:25
from utils import os, ShortLinksCollector, MyConfigParser
import getpass
stuff_dir = os.getenv('HOME') + unicode('/.diwnotifier/')
conf_path = stuff_dir + unicode('etc/diwnotifier.conf')
if os.path.isdir(stuff_dir + unicode('etc/')):
    try:
        with open(conf_path):
            pass
    except IOError:
        print 'Userid/Email:',
        user = raw_input()
        pswd = getpass.getpass('Password:')
        write = '[credentials]\nuser = ' + user + '\npasswd = ' + pswd + '\n\n[notifications]\nfriends=True\nmessages=True\nnotifications=True\nshoutbox=True\n\n#MILLISECONDS\n#########################\n[time]\nrefresh=90000\n#NOTIFICATION TIMEOUT\n#########################\nmain=5000\nmessage=10000'
        conf = open(conf_path, 'w+')
        conf.write(write)
        conf.close()
        print '[*] ' + conf_path + ' created...'

class Settings:
    APP_NAME = 'DIW Notifier'
    APP_VERSION = '0.9.2'
    EMAIL = 'am0n@clandiw.it'
    HOME_URL = 'http://clandiw.it'
    LOGIN_URL = 'http://clandiw.it/index.php?app=core\\&module=global&section=login'
    SHOUTBOX_URL = 'http://clandiw.it/index.php?/shoutbox/'
    app_home = unicode('/usr/local/lib/python2.7/dist-packages/DIWNotifier-0.9.2-py2.7.egg/diwnotifier/')
    icons_path = app_home + unicode('data/images/icons/')
    TRAY_ICON_MAIN = icons_path + 'clandiw.xpm'
    TRAY_ICON = icons_path + 'clandiw.xpm'
    TRAY_ICON_OFF = icons_path + 'clandiw_off.xpm'
    links_collector_uri = stuff_dir + unicode('var/cache/short_links_collector.txt')
    collector = ShortLinksCollector(links_collector_uri)
    collector.load()
    MSG_URL = collector.add('http://clandiw.it/index.php?app=members&module=messaging')
    FRIENDS_URL = collector.add('http://clandiw.it/index.php?app=members&module=friendsonline')
    NOTIFICATIONS_URL = collector.add('http://clandiw.it/index.php?app=core&module=usercp&tab=core&area=notificationlog')
    NEW_CONTENT = collector.add('http://clandiw.it/index.php?app=core&module=search&do=viewNewContent&search_app=forums&sid=2a4e1257c3e3566f5f623a86709fa4f8&search_app_filters[forums][searchInKey]=&change=1&period=week&userMode=all&followedItemsOnly=0')
    PCM_URL = 'http://clandiw.it/index.php?app=core\\&module=modcp'
    PIWIK_URL = HOME_URL + '/analytics'
    avatars_path = stuff_dir + unicode('var/cache/avatars/')
    image_uri = avatars_path + unicode('default_large.png')
    conf_path = stuff_dir + unicode('etc/diwnotifier.conf')
    autostart_path = os.getenv('HOME') + unicode('/.config/autostart/diwnotifier.py.desktop')
    log_dir = stuff_dir + unicode('var/log/')
    LOG_LEVEL = 'INFO'
    LOG_FORMATTING = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    BROWSER = 'chromium-browser'
    EDITOR = 'xdg-open'
    config = MyConfigParser(conf_path)
    REFRESH_TIME = int(config.read_field('time', 'refresh'))
    T1 = int(config.read_field('time', 'main'))
    T2 = int(config.read_field('time', 'message'))
    NOTIFICATIONS = True
    ABOUT_ICON = app_home + 'data/images/clandiw.png'
    LICENSE = APP_NAME + ' is free software; you can redistribute it and/or modify it\nunder the terms of the GNU General Public Licence as published\nby the Free Software Foundation; either version 3 of the Licence,\nor (at your option) any later version.\n\n' + APP_NAME + ' is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.'
    DESCRIPTION = APP_NAME + ' - A featureful web crawler\nfor http://clandiw.it site'
    WEBSITE = 'http://tinyurl.com/diwnotifier'
    COPYRIGHT = '(C) 2013 - 2014 Marco Vespo'
    DEVELOPER = 'Marco Vespo <am0n@clandiw.it>'
    ARTIST = 'The DIW crew <http://clandiw.it>'