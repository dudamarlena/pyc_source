# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/daniel/Desktop/pyInputStats/pyinputstatsmodules/helpers.py
# Compiled at: 2011-03-28 13:49:02
import sys, os
from distutils import dir_util
from xdg import BaseDirectory
import gtk, time, datetime, subprocess, re
from textwrap import dedent

def strip_data(data):
    """Strips off None-Tuples at the beginning and at the end of a given list.
    
    Also trims chunks of None-Tuples in between and replaces them through
    [(0, 0, 0), (-1, -1, -1)*n, (0, 0, 0)].
    """
    for (i, datum) in enumerate(data):
        (pix, clicks, keys) = datum
        if pix is None and clicks is None and keys is None:
            data[i] = (-1, -1, -1)
        else:
            break

    l = len(data) - 1
    for (i, datum) in enumerate(data[::-1]):
        (pix, clicks, keys) = datum
        if pix is None and clicks is None and keys is None:
            data[l - i] = (-1, -1, -1)
        else:
            break

    start = None
    length = 0
    chunks = []
    for (i, datum) in enumerate(data):
        (pix, clicks, keys) = datum
        if pix is None and clicks is None and keys is None:
            if start:
                length += 1
            else:
                start = i
                length = 1
        elif start:
            chunks.append((start, i))
            start = None

    for (s, l) in chunks:
        if l == 1:
            data[s] == (0, 0, 0)
        elif l == 2:
            data[s:l] == [(0, 0, 0), (0, 0, 0)]
        else:
            data[(s + 1):l] = [
             (-1, -1, -1)] * (l - s - 1)
            data[s] = (0, 0, 0)
            data[l - 1] = (0, 0, 0)

    return data


def get_data_dir():
    d = os.path.join(BaseDirectory.xdg_data_home, 'pyinputstats')
    if not os.path.exists(d):
        dir_util.mkpath(d)
    return d


def get_autostart_entry():
    """Returns path of our autostart entry or None if no such entry exists
    
    In order to avoid problems, the autostart-entry will be removed, if it
    was disabled via GNOME-Startup-Apps-Dialog."""
    d = os.path.join(BaseDirectory.xdg_config_home, 'autostart')
    if not os.path.exists(d):
        return
    else:
        for f in os.listdir(d):
            found = False
            disabled = False
            p = os.path.join(d, f)
            with open(p, 'r') as (fh):
                for line in fh:
                    if 'Exec' in line and 'pyinputstats' in line:
                        found = True
                    if 'gnome-autostart' in line.lower() and 'false' in line.lower():
                        disabled = True

            if found and not disabled:
                return p
            if found and disabled:
                os.remove(p)
                return

        return


def disable_autostart():
    """Deletes the autostart entry"""
    path = get_autostart_entry()
    if path:
        os.remove(path)


def enable_autostart():
    """Creates the autostart entry"""
    d = os.path.join(BaseDirectory.xdg_config_home, 'autostart')
    if not os.path.exists(d):
        dir_util.mkpath(d)
    autostart_file = get_autostart_entry()
    if autostart_file:
        return autostart_file
    fname = 'pyinputstats-{0}.desktop'
    counter = 1
    while os.path.exists(fname.format(counter)):
        counter += 1

    fname = fname.format(counter)
    entry = ("\n[Desktop Entry]\nType=Application\nExec=python '{0}'\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName[de_DE]=pyInputStats\nName=pyInputStats\nComment[de_DE]=\nComment=\n").format(os.path.abspath(sys.argv[0]))
    p = os.path.join(d, fname)
    with open(p, 'w') as (fh):
        fh.write(entry)
    return p


def month_days(month):
    (year, month) = month
    timestamp_start = time.mktime(datetime.date(year, month, 1).timetuple())
    if month < 12:
        timestamp_end = time.mktime(datetime.date(year, month + 1, 1).timetuple())
    else:
        timestamp_end = time.mktime(datetime.date(year + 1, 1, 1).timetuple())
    return int(round((timestamp_end - timestamp_start) / 86400))


def translate_keys(keycode, state):
    (keyval, group, level, mods) = gtk.gdk.Keymap.translate_keyboard_state(gtk.gdk.keymap_get_default(), keycode, state, 0)
    return gtk.gdk.keyval_name(gtk.gdk.keyval_to_lower(keyval))


def get_char(name):
    uc = gtk.gdk.keyval_to_unicode(gtk.gdk.keyval_from_name(str(name)))
    if uc:
        if uc <= 32:
            return name
        else:
            if str(name).startswith('KP_'):
                return name
            return unichr(uc)
    else:
        return name


def get_dpi(fallback=96):
    p = subprocess.Popen(['xdpyinfo'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ret = p.stdout.read()
    rg = re.compile('resolution: *(?P<x>[0-9]*)x(?P<y>[0-9]*)')
    res = rg.search(ret)
    if res:
        x, y = res.group('x'), res.group('y')
        if x >= y:
            return int(x)
        return int(y)
    return fallback