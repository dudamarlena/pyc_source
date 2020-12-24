# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/formatter.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.i18n import _, ngettext
NB_CHANNEL_NAME = {1: _('mono'), 2: _('stereo')}

def humanAudioChannel(value):
    return NB_CHANNEL_NAME.get(value, unicode(value))


def humanFrameRate(value):
    if isinstance(value, (int, long, float)):
        return _('%.1f fps') % value
    else:
        return value


def humanComprRate(rate):
    return '%.1fx' % rate


def humanAltitude(value):
    return ngettext('%.1f meter', '%.1f meters', value) % value


def humanPixelSize(value):
    return ngettext('%s pixel', '%s pixels', value) % value


def humanDPI(value):
    return '%s DPI' % value