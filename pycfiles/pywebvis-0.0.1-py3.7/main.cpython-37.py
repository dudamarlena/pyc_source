# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/main.py
# Compiled at: 2019-11-15 00:11:41
# Size of source mod 2**32: 350 bytes
import trio, time
with open('./front/teet.t') as (f):
    a = f.read()
from .VisWorker import Vis

def main():
    vis = Vis(ws_port=8000,
      vis_port=80)
    vis.show()
    N = [
     42, 12]
    vis.vars['test'] = N
    while True:
        N[1] += 1
        N[0] *= 2
        time.sleep(0.4)


if __name__ == '__main__':
    main()