# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pytrack_analysis/profile.py
# Compiled at: 2017-07-25 14:07:28
# Size of source mod 2**32: 8150 bytes
import os, sys
from datetime import datetime as date
from functools import wraps
import tkinter as tk
from tkinter import messagebox, filedialog
from ._globals import *
PROFILE, NAME, OS = get_globals()

def get_profile(_name, _user, script=''):
    """
    Returns profile as dictionary. If the given project name or user name is not in the profile, it will create new entries.

    Arguments:
    * _name: project name or 'all' (all projects)
    * _user: username
    * script: scriptname
    """
    tk.Tk().withdraw()
    nowdate = date.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(PROFILE, 'r') as (stream):
        profile = yaml.load(stream)
    if _name == 'all':
        return profile
    if _name in profile['$PROJECTS']:
        NEW_PROJ = True
        project = profile[_name]
        project['last active'] = nowdate
        profile['active'] = _name
        try:
            systems = project['systems']
            if NAME not in systems.keys():
                if query_yn("System '{:}' does not seem to exist in the profile. DO you want to set up a new systems profile? (Opens TKinter GUI)".format(NAME)):
                    profile['activesys'] = NAME
                    systems[NAME] = {}
                    system = systems[NAME]
                    system['os'] = OS
                    system['python'] = sys.version
                    dbfile, viddir = set_database(forced=True)
                    if dbfile is not None:
                        if viddir is not None:
                            system['database'] = dbfile
                            system['videos'] = viddir
                    out, log, plot = set_output(forced=True)
                    if out is not None:
                        system['output'] = out
                        system['log'] = log
                        system['plot'] = plot
            else:
                profile['activesys'] = NAME
                system = systems[NAME]
                system['python'] = sys.version
        except (AttributeError, TypeError):
            project['systems'] = {}

    else:
        NEW_PROJ = query_yn('DO you want to create a new project: {:}?'.format(_name))
        if NEW_PROJ:
            profile['$PROJECTS'].append(_name)
            profile[_name] = {}
            project = profile[_name]
            project['users'] = []
            project['users'].append(_user)
            project['created'] = nowdate
            project['last active'] = nowdate
            profile['active'] = _name
            project['systems'] = {}
            systems = project['systems']
            systems[NAME] = {}
            system = systems[NAME]
            system['os'] = OS
            system['python'] = sys.version
            dbfile, viddir = set_database(forced=True)
            if dbfile is not None:
                if viddir is not None:
                    system['database'] = dbfile
                    system['videos'] = viddir
            out, log, plot = set_output(forced=True)
            if out is not None:
                system['output'] = out
                system['log'] = log
                system['plot'] = plot
            print('Created [PROJECT] {:}.'.format(_name))
        if NEW_PROJ:
            profile['activeuser'] = _user
            users = profile['$USERS']
            if _user not in users:
                if query_yn('DO you want to create a new user: {:}?'.format(_user)):
                    users.append(_user)
            if _user not in project['users']:
                if query_yn('DO you want to add user to project: {:}?'.format(_name)):
                    project['users'].append(_user)
            print('Loaded [PROJECT] {:}'.format(_name))
        with io.open(PROFILE, 'w+', encoding='utf8') as (outfile):
            yaml.dump(profile, outfile, default_flow_style=False, allow_unicode=True)
        return profile


def get_db(profile):
    """ Returns active system's database file location """
    return profile[profile['active']]['systems'][NAME]['database']


def get_out(profile):
    """ Returns active system's output path """
    return profile[profile['active']]['systems'][NAME]['output']


def get_log(profile):
    """ Returns active system's logfile location """
    return profile[profile['active']]['systems'][NAME]['log']


def get_plot(profile):
    """ Returns active system's plot path """
    return profile[profile['active']]['systems'][NAME]['plot']


def set_database(forced=False):
    """ Returns database file location and video directory chosen from TKinter filedialog GUI """
    if not forced:
        asksave = messagebox.askquestion('Set database path', 'Are you sure you want to set a new path for the database?', icon='warning')
        if asksave == 'no':
            return (None, None)
    print('Set database...')
    dbfile = filedialog.askopenfilename(title='Load database')
    print('Set raw videos location...')
    viddir = filedialog.askdirectory(title='Load directory with raw video files')
    return (dbfile, viddir)


def set_output(forced=False):
    """ Returns output, log and plot path chosen from TKinter filedialog GUI """
    if not forced:
        asksave = messagebox.askquestion('Set output path', 'Are you sure you want to set a new path for the output/logging?', icon='warning')
        if asksave == 'no':
            return (None, None, None)
    else:
        print('Set output location...')
        outfolder = filedialog.askdirectory(title='Load directory for output')
        if len(outfolder) > 0:
            out = outfolder
            log = os.path.join(outfolder, 'main.log')
            plot = os.path.join(outfolder, 'plots')
        else:
            out = os.path.join(USER_DATA_DIR, 'output')
        log = os.path.join(out, 'main.log')
        plot = os.path.join(out, 'plots')
    for each in [out, plot]:
        check_folder(each)

    return (out, log, plot)


def show_profile(profile):
    """ Command-line output of profile with colored formatting (active project is bold green) """
    RED = '\x1b[1;31m'
    CYAN = '\x1b[1;36m'
    MAGENTA = '\x1b[1;35m'
    RESET = '\x1b[0;0m'
    print()
    if profile is None:
        profile_dump = yaml.dump(profile, default_flow_style=False, allow_unicode=True)
        thisstr = profile_dump.split('\n')
        sys.stdout.write(RED)
        for lines in thisstr:
            if lines == '$PROJECTS:' or lines == '$USERS:':
                sys.stdout.write(RED)
            else:
                if lines.startswith('-'):
                    sys.stdout.write(CYAN)
                else:
                    sys.stdout.write(RESET)
            print(lines)

        sys.stdout.write(RESET)
    else:
        current = profile['active']
        profile_dump = yaml.dump(profile, default_flow_style=False, allow_unicode=True)
        thisstr = profile_dump.split('\n')
        sys.stdout.write(RED)
        for lines in thisstr:
            if lines == '$PROJECTS:' or lines == '$USERS:':
                sys.stdout.write(RED)
            else:
                if lines.startswith('-'):
                    sys.stdout.write(CYAN)
                elif current in lines:
                    if 'active' not in lines:
                        print()
                        sys.stdout.write(MAGENTA)
                else:
                    sys.stdout.write(RESET)
            print(lines)

        sys.stdout.write(RESET)