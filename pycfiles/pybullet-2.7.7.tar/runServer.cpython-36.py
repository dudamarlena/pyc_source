# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_utils/runServer.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 571 bytes
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
import pybullet_data, pybullet as p, time
p.connect(p.GUI_SERVER)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
while True:
    p.setPhysicsEngineParameter()
    time.sleep(0.01)