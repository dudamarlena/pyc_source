# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jcrack/jcrack.py
# Compiled at: 2012-02-06 22:05:35
from celery.task import task
from subprocess import Popen, PIPE
from crackchars import getCharset
import tempfile, os, jconfig
config = jconfig.getConfig()

def checkCwd():
    os.chdir('/tmp')
    if not os.path.exists('/tmp/charset.txt'):
        f = open('/tmp/charset.txt', 'w')
        f.write(getCharset())
        f.close()


@task
def rcrack(hashtype, hashval):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    checkCwd()
    args = [
     'rcracki_mt',
     '-h', hashval,
     '-o', tmp.name,
     '-t', config.get('tune', 'threads_per_proc'),
     '/mnt/lmtables/' + hashtype]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate('')
    f = open(tmp.name, 'r')
    for line in f.readlines():
        words = line.split(':')
        return (hashtype, hashval, words[1])

    f.close()


@task
def hashcat(hashtype, hashval):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    checkCwd()
    args = [
     '/opt/oclHashcat-lite-0.09/cudaHashcat-lite64.bin',
     '--quiet',
     '-m', hashtype,
     '--outfile-format=2',
     '--outfile=' + tmp.name,
     hashval]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate('')
    f = open(tmp.name, 'r')
    for line in f.readlines():
        words = line.strip()
        if len(words) > 0:
            return (hashtype, hashval, words)

    f.close()