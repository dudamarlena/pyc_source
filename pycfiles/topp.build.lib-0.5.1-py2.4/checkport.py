# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topp/build/lib/checkport.py
# Compiled at: 2007-09-27 13:07:36
""" 
tasks for checking and setting port availability
"""
from topp.utils.filesystem import which
from buildit.task import Task

def getporttasks(variables, portsfile=True):
    nmap = which('nmap')
    retval = []
    for i in variables:
        if nmap:
            retval.append(Task('checking port availability via nmap', commands=['nmap localhost -p ${%s} | grep "${%s}.*closed"' % (i, i)]))
        if portsfile:
            app = ('').join([ j.strip('_') for j in i.split('port') ])
            if not app:
                app = '${app}'
                retval.append(Task('checking port availability via ports file', workdir='${basedir}', commands=['touch ${portsfile}', '! grep -v "^${%s}[[:space:]]%s$" ${portsfile} | grep "^${%s}[[:space:]]"' % (i, app, i)]))
                retval.append(Task('setting port number', workdir='${basedir}', commands=['cp ${portsfile} ${portsfile}.TMP', 'echo "${%s} %s" >> ${portsfile}.TMP' % (i, app), 'sort -g ${portsfile}.TMP | uniq > ${portsfile}', 'rm ${portsfile}.TMP'], dependencies=(retval[(len(retval) - 1)],)))

    return retval