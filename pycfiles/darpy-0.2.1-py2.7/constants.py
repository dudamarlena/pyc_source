# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/darpy/constants.py
# Compiled at: 2017-11-03 15:38:57
PIP_CMD = 'pip --isolated --no-cache-dir'
_PIP_DOWNLOAD_CMD = PIP_CMD + ' download --dest "{}"'
PIP_DOWNLOAD_SRC_CMD = PIP_CMD + ' download --dest "{}" -e "{}"'
PIP_DOWNLOAD_REQ_CMD = PIP_CMD + ' download --dest "{}" -r "{}"'
PIP_INSTALL_CMD = PIP_CMD + ' install --no-index --find-links "{0}" --ignore-installed "{0}"/*'