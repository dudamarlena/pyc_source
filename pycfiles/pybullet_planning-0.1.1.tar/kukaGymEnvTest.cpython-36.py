# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/examples/kukaGymEnvTest.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 1566 bytes
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
from pybullet_envs.bullet.kukaGymEnv import KukaGymEnv
import time

def main():
    environment = KukaGymEnv(renders=True, isDiscrete=False, maxSteps=10000000)
    motorsIds = []
    dv = 0.01
    motorsIds.append(environment._p.addUserDebugParameter('posX', -dv, dv, 0))
    motorsIds.append(environment._p.addUserDebugParameter('posY', -dv, dv, 0))
    motorsIds.append(environment._p.addUserDebugParameter('posZ', -dv, dv, 0))
    motorsIds.append(environment._p.addUserDebugParameter('yaw', -dv, dv, 0))
    motorsIds.append(environment._p.addUserDebugParameter('fingerAngle', 0, 0.3, 0.3))
    done = False
    while not done:
        action = []
        for motorId in motorsIds:
            action.append(environment._p.readUserDebugParameter(motorId))

        state, reward, done, info = environment.step2(action)
        obs = environment.getExtendedObservation()


if __name__ == '__main__':
    main()