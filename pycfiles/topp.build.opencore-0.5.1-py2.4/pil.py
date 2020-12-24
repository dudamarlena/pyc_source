# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topp/build/opencore/tasks/pil.py
# Compiled at: 2007-09-27 10:29:29
"""Tasks to download, compile and install Python Imaging Library."""
from buildit.task import Task
from topp.build.lib.commands import DistUtilInstaller
install = Task('Install Python Imaging Library', namespaces='pil', workdir='${srcdir}', targets='${deploydir}/bin/pilconvert.py', commands=[DistUtilInstaller('${./download_url}')])