# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/update.py
# Compiled at: 2019-08-28 02:03:12
# Size of source mod 2**32: 3535 bytes
import sys, time, os, re, subprocess
from pocsuite3.lib.core.common import data_to_stdout
from pocsuite3.lib.core.common import get_latest_revision
from pocsuite3.lib.core.common import poll_process
from pocsuite3.lib.core.data import conf
from pocsuite3.lib.core.data import logger
from pocsuite3.lib.core.data import paths
from pocsuite3.lib.core.revision import get_revision_number
from pocsuite3.lib.core.settings import GIT_REPOSITORY
from pocsuite3.lib.core.settings import IS_WIN
from pocsuite3.lib.core.settings import UNICODE_ENCODING
from pocsuite3.lib.core.settings import VERSION

def update():
    if not conf.update_all:
        return
        success = False
        warn_msg = os.path.exists(os.path.join(paths.POCSUITE_ROOT_PATH, '../', '.git')) or "not a git repository. It is recommended to clone the 'knownsec/pocsuite3' repository "
        warn_msg += "from GitHub (e.g. 'git clone --depth 1 {} pocsuite3')".format(GIT_REPOSITORY)
        logger.warn(warn_msg)
        if VERSION == get_latest_revision():
            logger.info("already at the latest revision '{}'".format(get_revision_number()))
            return
        else:
            pass
    else:
        info_msg = 'updating pocsuite3 to the latest development revision from the '
        info_msg += 'GitHub repository'
        logger.info(info_msg)
        debug_msg = "pocsuite3 will try to update itself using 'git' command"
        logger.debug(debug_msg)
        data_to_stdout('\r[{0}] [INFO] update in progress '.format(time.strftime('%X')))
        cwd_path = os.path.join(paths.POCSUITE_ROOT_PATH, '../')
        try:
            process = subprocess.Popen(('git checkout . && git pull %s HEAD' % GIT_REPOSITORY), shell=True,
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE),
              cwd=(cwd_path.encode(sys.getfilesystemencoding() or UNICODE_ENCODING)))
            poll_process(process, True)
            stdout, stderr = process.communicate()
            success = not process.returncode
        except (IOError, OSError) as ex:
            try:
                success = False
                stderr = str(ex)
            finally:
                ex = None
                del ex

        if success:
            logger.info("{0} the latest revision '{1}'".format('already at' if b'Already' in stdout else 'updated to', get_revision_number()))
        else:
            if 'Not a git repository' in stderr:
                err_msg = "not a valid git repository. Please checkout the 'knownsec/pocsuite3' repository "
                err_msg += "from GitHub (e.g. 'git clone --depth 1 %s pocsuite3')" % GIT_REPOSITORY
                logger.error(err_msg)
            else:
                logger.error("update could not be completed ('%s')" % re.sub('\\W+', ' ', stderr).strip())
    if not success:
        if IS_WIN:
            info_msg = "for Windows platform it's recommended "
            info_msg += 'to use a GitHub for Windows client for updating '
            info_msg += 'purposes (http://windows.github.com/) or just '
            info_msg += 'download the latest snapshot from '
            info_msg += 'https://github.com/knownsec/pocsuite3/downloads'
        else:
            info_msg = "for Linux platform it's recommended "
            info_msg += "to install a standard 'git' package (e.g.: 'sudo apt-get install git')"
        logger.info(info_msg)
    sys.exit()