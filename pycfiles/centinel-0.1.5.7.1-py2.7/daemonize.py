# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/daemonize.py
# Compiled at: 2016-07-14 15:16:59
import os, shutil, stat, tempfile

def create_script_for_location(content, destination):
    """Create a script with the given content, mv it to the
    destination, and make it executable

    Parameters:
    content- the content to put in the script
    destination- the directory to copy to

    Note: due to constraints on os.rename, destination must be an
    absolute path to a file, not just a directory

    """
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    temp.write(content)
    temp.close()
    shutil.move(temp.name, destination)
    cur_perms = os.stat(destination).st_mode
    set_perms = cur_perms | stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR
    os.chmod(destination, set_perms)


def daemonize(package, bin_loc, user):
    """Create crontab entries to run centinel every hour and
    autoupdate every day

    Parameters:

    package- name of the currently installed package (will be used for
        autoupdate). If this parameter is None, the autoupdater will
        not be used

    bin_loc- location of the centinel binary/script.

    Note: this works by creating temporary files, adding the content
    of the cron scripts to these temporary files, moving these files
    into the appropriate cron folders, and making these scripts
    executable

    Note: if the script already exists, this will delete it

    """
    path = '/etc/cron.hourly/centinel-' + user
    if user != 'root':
        hourly = ('').join(['#!/bin/bash\n',
         '# cron job for centinel\n',
         'su ', user, " -c '", bin_loc, " --sync'\n",
         'su ', user, " -c '", bin_loc, "'\n",
         'su ', user, " -c '", bin_loc, " --sync'\n"])
    else:
        hourly = ('').join(['#!/bin/bash\n',
         '# cron job for centinel\n',
         bin_loc, ' --sync\n',
         bin_loc, '\n',
         bin_loc, ' --sync\n'])
    create_script_for_location(hourly, path)
    if package is None:
        return
    else:
        updater = ('').join(['#!/bin/bash\n',
         '# autoupdater for centinel\nsudo pip install --upgrade ',
         package, '\n'])
        create_script_for_location(updater, '/etc/cron.daily/centinel-autoupdate')
        print 'Successfully created cron jobs for user ' + user
        return