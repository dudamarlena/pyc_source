# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\exm\sections\java.py
# Compiled at: 2019-03-10 13:35:48
import os, shlex, subprocess

def process(ctx):
    ensureJavaVersion(ctx)
    if not ctx['java'].get('bin'):
        ctx['java']['bin'] = '%s/bin/java' % ctx['env']['JAVA_HOME']


def ensureJavaVersion(ctx):
    javaHome = ctx['env']['JAVA_HOME']
    version = str(ctx['java']['version'])
    shell_cmd = '"%s/bin/java" -version' % javaHome
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line.startswith('java version'):
            if line.find(version) == -1:
                raise Exception('Java version is incorrect: %s, expected: %s' % (line, version))

    if p.returncode != 0:
        raise Exception('Detect java version failed, java: %s' % javaHome)
    return