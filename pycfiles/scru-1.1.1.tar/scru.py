# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/Datos/devel/hg-repos/scru/scru/scru.py
# Compiled at: 2011-06-17 00:32:26
import clipboard, imgur, screenshot, utils, os, subprocess, urllib
APP_ICON = '/usr/share/icons/hicolor/scalable/apps/scru.svg'
XDG_CACHE_HOME = os.environ['XDG_CACHE_HOME']
APP_CACHE = os.path.join(XDG_CACHE_HOME, 'scru')
if not os.path.isdir(APP_CACHE):
    os.makedirs(APP_CACHE)

def complete(url, notify):
    """Show a notify message when the upload was commpleted"""
    image = urllib.urlretrieve(url, os.path.join(APP_CACHE, 'notify.png'))[0]
    image_uri = 'file://' + image
    if notify:
        utils.show_notification('Scru', 'The screenshot was uploaded to imgur', image_uri)
    print 'The screenshot was uploaded to imgur'
    print 'Link was copied to the clipboard'


def screen_to_imgur(filename, link, select, sound, notify, quality, delay):
    """Take a screenshot and upload to imgur"""
    if not link:
        link = 'original'
    screen = screenshot.grab(filename, select, sound, quality, delay)
    print 'Uploading image to imgur...'
    data = imgur.upload(screen)
    screen.close()
    if link == 'html_clikeable_thumbail':
        thumb = data['upload']['links']['large_thumbnail']
        original = data['upload']['links']['original']
        url = '<a href="%s"><img src=%s/></a>' % (original, thumb)
    else:
        url = data['upload']['links'][link]
    notify_im = data['upload']['links']['small_square']
    clipboard.copy(url)
    if notify:
        complete(notify_im, notify)
    print link.upper() + ': ' + url
    return url