# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/update.py
# Compiled at: 2018-12-07 04:32:38
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
import locale, os, re, subprocess, time
from pocsuite.lib.core.common import dataToStdout
from pocsuite.lib.core.common import poll_process
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import paths
from pocsuite.lib.core.revision import getRevisionNumber
from pocsuite.lib.core.settings import GIT_REPOSITORY
from pocsuite.lib.core.settings import IS_WIN
from pocsuite.lib.core.settings import SITE

def update():
    if not conf.update:
        return
    success = False
    if not os.path.exists(os.path.join(os.path.dirname(paths.POCSUITE_ROOT_PATH), '.git')):
        err_msg = "not a git repository. Please checkout the 'pocsuite' repository from GitHub (e.g. 'git clone --depth 1https://github.com/knownsec/Pocsuite.git pocsuite')"
        logger.error(err_msg)
    else:
        info_msg = 'updating pocsuite to the latest development version from the GitHub repository'
        logger.info(info_msg)
        debug_msg = "pocsuite will try to update itself using 'git' command"
        logger.debug(debug_msg)
        dataToStdout('\r[%s] [INFO] update in progress ' % time.strftime('%X'))
        try:
            process = subprocess.Popen('git checkout . && git pull %s HEAD' % GIT_REPOSITORY, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=paths.POCSUITE_ROOT_PATH.encode(locale.getpreferredencoding()))
            poll_process(process, True)
            stdout, stderr = process.communicate()
            success = not process.returncode
        except (IOError, OSError) as ex:
            success = False
            stderr = ('{}').format(ex)

        if success:
            info_msg = ("{0} the latest revision '{1}'").format('already at' if 'Already' in stdout else 'updated to', getRevisionNumber())
            logger.info(info_msg)
        elif 'Not a git repository' in stderr:
            err_msg = "not a valid git repository. Please checkout the 'pocsuite' repository from GitHub (e.g. 'git clone --depth 1 https://github.com/knownsec/Pocsuite.git pocsuite')"
            logger.error(err_msg)
        else:
            err_msg = ("update could not be completed ('{}')").format(re.sub('\\W+', ' ', stderr).strip())
            logger.error(err_msg)
    if not success:
        if IS_WIN:
            info_msg = ("for Windows platform it's recommended to use a Githubfor Windows client for updating purposes (http://windows.github.com/) or just download the latest snapshot from {}").format(SITE)
        else:
            info_msg = "for Linux platform it's required to install a standard 'git' package (e.g.: 'sudo apt-get install git')"
        logger.info(info_msg)