# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/racecar.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 6132 bytes
import os, copy, math, numpy as np

class Racecar:

    def __init__(self, bullet_client, urdfRootPath='', timeStep=0.01):
        self.urdfRootPath = urdfRootPath
        self.timeStep = timeStep
        self._p = bullet_client
        self.reset()

    def reset(self):
        car = self._p.loadURDF((os.path.join(self.urdfRootPath, 'racecar/racecar_differential.urdf')), [
         0, 0, 0.2],
          useFixedBase=False)
        self.racecarUniqueId = car
        for wheel in range(self._p.getNumJoints(car)):
            self._p.setJointMotorControl2(car, wheel,
              (self._p.VELOCITY_CONTROL),
              targetVelocity=0,
              force=0)
            self._p.getJointInfo(car, wheel)

        c = self._p.createConstraint(car, 9,
          car,
          11,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=1, maxForce=10000)
        c = self._p.createConstraint(car, 10,
          car,
          13,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), maxForce=10000)
        c = self._p.createConstraint(car, 9,
          car,
          13,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), maxForce=10000)
        c = self._p.createConstraint(car, 16,
          car,
          18,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=1, maxForce=10000)
        c = self._p.createConstraint(car, 16,
          car,
          19,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), maxForce=10000)
        c = self._p.createConstraint(car, 17,
          car,
          19,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), maxForce=10000)
        c = self._p.createConstraint(car, 1,
          car,
          18,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), gearAuxLink=15, maxForce=10000)
        c = self._p.createConstraint(car, 3,
          car,
          19,
          jointType=(self._p.JOINT_GEAR),
          jointAxis=[
         0, 1, 0],
          parentFramePosition=[
         0, 0, 0],
          childFramePosition=[
         0, 0, 0])
        self._p.changeConstraint(c, gearRatio=(-1), gearAuxLink=15, maxForce=10000)
        self.steeringLinks = [
         0, 2]
        self.maxForce = 20
        self.nMotors = 2
        self.motorizedwheels = [8, 15]
        self.speedMultiplier = 20.0
        self.steeringMultiplier = 0.5

    def getActionDimension(self):
        return self.nMotors

    def getObservationDimension(self):
        return len(self.getObservation())

    def getObservation(self):
        observation = []
        pos, orn = self._p.getBasePositionAndOrientation(self.racecarUniqueId)
        observation.extend(list(pos))
        observation.extend(list(orn))
        return observation

    def applyAction(self, motorCommands):
        targetVelocity = motorCommands[0] * self.speedMultiplier
        steeringAngle = motorCommands[1] * self.steeringMultiplier
        for motor in self.motorizedwheels:
            self._p.setJointMotorControl2((self.racecarUniqueId), motor,
              (self._p.VELOCITY_CONTROL),
              targetVelocity=targetVelocity,
              force=(self.maxForce))

        for steer in self.steeringLinks:
            self._p.setJointMotorControl2((self.racecarUniqueId), steer,
              (self._p.POSITION_CONTROL),
              targetPosition=steeringAngle)