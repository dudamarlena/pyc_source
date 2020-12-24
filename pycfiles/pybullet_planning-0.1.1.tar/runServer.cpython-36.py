# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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