# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/himawaripy/utils.py
# Compiled at: 2019-04-24 17:25:39
# Size of source mod 2**32: 9325 bytes
import os, re, sys, subprocess
from distutils.version import LooseVersion

def set_background(file_path):
    de = get_desktop_environment()
    if de == 'mac':
        subprocess.call(['osascript', '-e',
         'tell application "System Events"\nset theDesktops to a reference to every desktop\nrepeat with aDesktop in theDesktops\nset the picture of aDesktop to "' + file_path + '"\nend repeat\nend tell'])
    else:
        fetch_envvar('DBUS_SESSION_BUS_ADDRESS')
        fetch_envvar('DISPLAY')
    if de in ('gnome', 'unity', 'cinnamon', 'pantheon', 'gnome-classic'):
        if de == 'unity':
            subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'draw-background', 'false'])
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + file_path])
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-options', 'scaled'])
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'primary-color', '#000000'])
        if de == 'unity':
            assert os.system('bash -c "gsettings set org.gnome.desktop.background draw-background true"') == 0
    else:
        if de == 'mate':
            subprocess.call(['gsettings', 'set', 'org.mate.background', 'picture-filename', file_path])
        else:
            if de == 'i3':
                subprocess.call(['feh', '--bg-max', file_path])
            else:
                if de == 'xfce4':
                    displays = subprocess.getoutput('xfconf-query --channel xfce4-desktop --list | grep last-image').split()
                    for display in displays:
                        subprocess.call(['xfconf-query', '--channel', 'xfce4-desktop', '--property', display, '--set', file_path])

                else:
                    if de == 'lxde':
                        subprocess.call(['pcmanfm', '--set-wallpaper', file_path, '--wallpaper-mode=fit'])
                    else:
                        if de == 'kde':
                            if plasma_version() > LooseVersion('5.7'):
                                script = 'var a = desktops();for (i = 0; i < a.length; i++) {{d = a[i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");d.writeConfig("Image", "file://{}");d.writeConfig("FillMode", 1);d.writeConfig("Color", "#000");}}'
                                try:
                                    subprocess.check_output(['qdbus', 'org.kde.plasmashell', '/PlasmaShell',
                                     'org.kde.PlasmaShell.evaluateScript', script.format(file_path)])
                                except subprocess.CalledProcessError as e:
                                    if 'Widgets are locked' in e.output.decode('utf-8'):
                                        print('Cannot change the wallpaper while widgets are locked! (unlock the widgets)')
                                    else:
                                        raise e

                            else:
                                print("Couldn't detect plasmashell 5.7 or higher.")
                        else:
                            if has_program('feh'):
                                print("Couldn't detect your desktop environment ('{}'), but you have 'feh' installed so we will use it...".format(de))
                                subprocess.call(['feh', '--bg-max', file_path])
                            else:
                                if has_program('nitrogen'):
                                    print("Couldn't detect your desktop environment ('{}'), but you have 'nitrogen' installed so we will use it...".format(de))
                                    subprocess.call(['nitrogen', '--restore'])
                                else:
                                    return False
        return True


def get_desktop_environment():
    if sys.platform in ('win32', 'cygwin'):
        return 'windows'
    else:
        if sys.platform == 'darwin':
            return 'mac'
        else:
            fetch_envvar('DESKTOP_SESSION')
            desktop_session = os.environ.get('DESKTOP_SESSION')
            if desktop_session is not None:
                desktop_session = desktop_session.lower()
                if desktop_session in ('gnome', 'unity', 'cinnamon', 'mate', 'xfce4',
                                       'lxde', 'fluxbox', 'blackbox', 'openbox',
                                       'icewm', 'jwm', 'afterstep', 'trinity', 'kde',
                                       'pantheon', 'gnome-classic', 'i3'):
                    return desktop_session
                if 'xfce' in desktop_session or desktop_session.startswith('xubuntu'):
                    return 'xfce4'
                if desktop_session.startswith('ubuntu'):
                    return 'unity'
                if desktop_session.startswith('lubuntu'):
                    return 'lxde'
                if desktop_session.startswith('kubuntu'):
                    return 'kde'
                if desktop_session.startswith('razor'):
                    return 'razor-qt'
                if desktop_session.startswith('wmaker'):
                    return 'windowmaker'
                if desktop_session.startswith('peppermint'):
                    return 'gnome'
            fetch_envvar('KDE_FULL_SESSION')
            fetch_envvar('GNOME_DESKTOP_SESSION_ID')
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                return 'kde'
            if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                if 'deprecated' not in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    return 'gnome2'
            else:
                if is_running('xfce-mcs-manage'):
                    return 'xfce4'
            if is_running('ksmserver'):
                return 'kde'
            fetch_envvar('XDG_CURRENT_DESKTOP')
            current_desktop = os.environ.get('XDG_CURRENT_DESKTOP')
            if current_desktop:
                current_desktop = current_desktop.lower()
                if current_desktop in ('gnome', 'unity', 'kde', 'gnome-classic', 'mate'):
                    return current_desktop
                if current_desktop == 'xfce':
                    return 'xfce4'
                if current_desktop == 'x-cinnamon':
                    return 'cinnamon'
        return 'unknown'


def has_program(program):
    try:
        subprocess.check_output(['which', '--', program])
        return True
    except subprocess.CalledProcessError:
        return False


def plasma_version():
    try:
        output = subprocess.Popen(['plasmashell', '-v'], stdout=(subprocess.PIPE)).communicate()[0].decode('utf-8')
        print("Plasma version '{}'.".format(output))
        version = re.match('plasmashell (.*)', output).group(1)
        return LooseVersion(version)
    except (subprocess.CalledProcessError, IndexError):
        return LooseVersion('')


def is_running(process):
    try:
        subprocess.check_output(['pidof', '--', process])
        return True
    except subprocess.CalledProcessError:
        return False


def fetch_envvar(varname):
    """
    When himawaripy is called by cron or an init, the environment variables that
    are available to us is severely limited, causing problems with some
    processes we call (such as gsetings [due to lack of
    $DBUS_SESSION_BUS_ADDRESS for instance]).

    To try fix this issue as much as we can, without resorting to additional
    shell scripts, we try fetching values of the environment variables we are
    interested in (before we access them!) from another process. pulseauido
    seemed to me a good choice, for it's available virtually on all desktop
    installations (regardless of DE), and seem to have all the environment
    variables that we are (potentially) interested in (*e.g.* gdm does NOT have
    $DISPLAY whereas pulseaudio do!)
    """
    if varname in os.environ:
        return
    else:
        val = os.popen('bash -c "grep -z ^{}= /proc/$(pgrep -n pulseaudio)/environ | cut -d= -f2-"'.format(varname)).read().strip('\x00\n')
        if val:
            print('Fetched env. var. {} as `{}`'.format(varname, val))
            os.environ[varname] = val
        else:
            print('Could NOT retrieve env. var. {}'.format(varname))