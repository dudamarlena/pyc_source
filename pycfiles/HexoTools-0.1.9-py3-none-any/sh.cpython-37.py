# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\projects\hexotools\hexotools\sh\sh.py
# Compiled at: 2019-10-09 06:13:39
# Size of source mod 2**32: 1951 bytes
import os, webbrowser, subprocess, json, time
PKG_PATH = os.path.dirname(os.path.dirname(__file__))
config_path = os.path.join(PKG_PATH, 'config.json')
with open(config_path, 'r', encoding='utf-8') as (fo):
    config = json.load(fo)
sh = {'cd':'{0} && cd {1} '.format(config['disk'], config['blog_path']), 
 'generate':'hexo g', 
 'deploy':'hexo g -d', 
 'server':'hexo server', 
 'clean':'hexo clean'}

def mCmd(iterable):
    """os.system()执行多条指令
    """
    return subprocess.Popen(('&& '.join(iterable)), shell=True)


def startServer(port=4000):
    cmd = [
     sh['cd'],
     '{0} -p {1}'.format(sh['server'], port)]
    popen = mCmd(cmd)
    time.sleep(4)
    webbrowser.open('http://localhost:{0}'.format(port))
    return popen


def stopNodeProcess(pid):
    if os.system('taskkill /pid {0} /f'.format(pid)) in (0, 1):
        if os.system('taskkill /F /IM node.exe'.format(pid)) in (0, 1):
            return True
    return False


def deploy():
    cmd = [
     sh['cd'],
     sh['deploy']]
    mCmd(cmd)


def executeCommand(command, *args):
    try:
        with open(config_path, 'r', encoding='utf-8') as (fo):
            config = json.load(fo)
        print('Run_CWD: {0}...'.format(config['cwd']))
        sp = subprocess.Popen(command, shell=True,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          cwd=(config['cwd']))
        out, err = sp.communicate()
        if out:
            print(out.decode('gbk'))
        if err:
            print(err.decode('gbk'))
    except BaseException as e:
        try:
            print(e)
        finally:
            e = None
            del e


def webReadme():
    webbrowser.open('https://github.com/ShoorDay/HexoTools')