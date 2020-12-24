# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_mozrunner/install.py
# Compiled at: 2011-04-09 01:50:00
import sys, os
if sys.platform != 'win32':
    import pwd
import tempfile, subprocess, commands, shutil, tempfile, zipfile
from time import sleep
try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree

from distutils import dir_util
copytree = dir_util.copy_tree
from windmill.dep import json

def set_preferences(profile, prefs, enable_default_prefs=True):
    """Set all the preferences from dict in the profile's prefs.py"""
    from windmill.dep import mozrunner
    prefs_file = os.path.join(profile, 'user.js')
    f = open(prefs_file, 'w+')
    f.write('\n#MozRunner Prefs Start\n')
    if enable_default_prefs and hasattr(mozrunner, 'settings'):
        default_prefs = mozrunner.settings.get('MOZILLA_DEFAULT_PREFS')
        pref_lines = [ 'user_pref(%s, %s);' % (json.dumps(k), json.dumps(v)) for (k, v) in default_prefs.items()
                     ]
        f.write('#MozRunner Default Prefs\n')
        for line in pref_lines:
            f.write(line + '\n')

    pref_lines = [ 'user_pref(%s, %s);' % (json.dumps(k), json.dumps(v)) for (k, v) in prefs.items() ]
    f.write('#MozRunner Preferences\n')
    for line in pref_lines:
        f.write(line + '\n')

    f.write('#MozRunner Prefs End\n')
    f.flush()
    f.close()


def clean_prefs_file(prefs_file):
    """Removed the preferences added by mozrunner from prefs.py in the given prefs_file."""
    lines = open(prefs_file, 'r').read().splitlines()
    s = lines.index('#MozRunner Prefs Star')
    e = lines.index('#MozRunner Prefs End')
    cleaned_prefs = ('\n').join(lines[:s] + lines[e:])
    f = open(prefs_file, 'w')
    f.write(cleaned_prefs)
    f.flush()
    f.close()


def create_tmp_profile(settings):
    """Create a new profile in tmp from default mozilla profile."""
    process = subprocess.Popen([settings['MOZILLA_BINARY'], '-version'], shell=False, stdout=subprocess.PIPE)
    version = process.communicate()
    if version[0].find('3.') != -1 or version[0].find('2.') != -1:
        default_profile = settings['MOZILLA_DEFAULT_PROFILE']
        tmp_profile = tempfile.mkdtemp(suffix='.mozrunner')
        if sys.platform == 'linux2':
            try:
                login = os.getlogin()
            except OSError:
                login = pwd.getpwuid(os.geteuid())[0]
            else:
                output = commands.getoutput('chown -R %s:%s %s' % (login, login, tmp_profile))
                if output != '':
                    print output
        if os.path.exists(tmp_profile) is True:
            shutil.rmtree(tmp_profile)
        copytree(default_profile, tmp_profile, preserve_symlinks=1)
        settings['MOZILLA_PROFILE'] = tmp_profile
    else:
        process = subprocess.Popen([settings['MOZILLA_BINARY'], '-createprofile', 'mozrunner'], shell=False, stderr=subprocess.PIPE)
        out = process.communicate()
        arr = out[1].replace("'", '').replace('\n', '').split(' at ')
        tmp_profile = arr[1].replace('prefs.js', '')
        settings['MOZILLA_PROFILE'] = tmp_profile


def install_plugin(path_to_plugin, profile_path):
    """Install a given extracted plugin in to the given profile_path."""
    tree = ElementTree.ElementTree(file=os.path.join(path_to_plugin, 'install.rdf'))
    about = [ e for e in tree.findall('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description') if e.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about') == 'urn:mozilla:install-manifest'
            ]
    if len(about) is 0:
        plugin_element = tree.find('.//{http://www.mozilla.org/2004/em-rdf#}id')
        plugin_id = plugin_element.text
    else:
        plugin_id = about[0].get('{http://www.mozilla.org/2004/em-rdf#}id')
    plugin_path = os.path.join(profile_path, 'extensions', plugin_id)
    copytree(path_to_plugin, plugin_path, preserve_symlinks=1)


def install_plugins(settings, runner_class):
    """Install all plugins defined in settings to the profile defined in settings. 
    
    Uses the runner_class to start and stop the browser after plugins are installed to run through any plugin initialization code."""
    binary = settings['MOZILLA_BINARY']
    profile = settings['MOZILLA_PROFILE']
    for plugin_path in settings['MOZILLA_PLUGINS']:
        if plugin_path.endswith('.xpi'):
            tmpdir = tempfile.mkdtemp(suffix='.mozrunner_plugins')
            compressed_file = zipfile.ZipFile(plugin_path, 'r')
            for name in compressed_file.namelist():
                pardir = os.path.join(tmpdir, os.path.dirname(name))
                if not os.path.exists(pardir):
                    os.makedirs(pardir)
                if not name.endswith('/'):
                    data = compressed_file.read(name)
                    f = open(os.path.join(tmpdir, name), 'w')
                    f.write(data)
                    f.close()

            install_plugin(tmpdir, profile)
        else:
            install_plugin(plugin_path, profile)