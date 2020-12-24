# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/kuka.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 8661 bytes
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
import pybullet as p, numpy as np, copy, math, pybullet_data

class Kuka:

    def __init__(self, urdfRootPath=pybullet_data.getDataPath(), timeStep=0.01):
        self.urdfRootPath = urdfRootPath
        self.timeStep = timeStep
        self.maxVelocity = 0.35
        self.maxForce = 200.0
        self.fingerAForce = 2
        self.fingerBForce = 2.5
        self.fingerTipForce = 2
        self.useInverseKinematics = 1
        self.useSimulation = 1
        self.useNullSpace = 21
        self.useOrientation = 1
        self.kukaEndEffectorIndex = 6
        self.kukaGripperIndex = 7
        self.ll = [
         -0.967, -2, -2.96, 0.19, -2.96, -2.09, -3.05]
        self.ul = [
         0.967, 2, 2.96, 2.29, 2.96, 2.09, 3.05]
        self.jr = [
         5.8, 4, 5.8, 4, 5.8, 4, 6]
        self.rp = [
         0, 0, 0, 0.5 * math.pi, 0, -math.pi * 0.5 * 0.66, 0]
        self.jd = [
         1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05,
         1e-05, 1e-05, 1e-05, 1e-05]
        self.reset()

    def reset(self):
        objects = p.loadSDF(os.path.join(self.urdfRootPath, 'kuka_iiwa/kuka_with_gripper2.sdf'))
        self.kukaUid = objects[0]
        p.resetBasePositionAndOrientation(self.kukaUid, [-0.1, 0.0, 0.07], [
         0.0, 0.0, 0.0, 1.0])
        self.jointPositions = [
         0.006418, 0.413184, -0.011401, -1.589317, 0.005379, 1.137684, -0.006539, 4.8e-05,
         -0.299912, 0.0, -4.3e-05, 0.29996, 0.0, -0.0002]
        self.numJoints = p.getNumJoints(self.kukaUid)
        for jointIndex in range(self.numJoints):
            p.resetJointState(self.kukaUid, jointIndex, self.jointPositions[jointIndex])
            p.setJointMotorControl2((self.kukaUid), jointIndex,
              (p.POSITION_CONTROL),
              targetPosition=(self.jointPositions[jointIndex]),
              force=(self.maxForce))

        self.trayUid = p.loadURDF(os.path.join(self.urdfRootPath, 'tray/tray.urdf'), 0.64, 0.075, -0.19, 0.0, 0.0, 1.0, 0.0)
        self.endEffectorPos = [0.537, 0.0, 0.5]
        self.endEffectorAngle = 0
        self.motorNames = []
        self.motorIndices = []
        for i in range(self.numJoints):
            jointInfo = p.getJointInfo(self.kukaUid, i)
            qIndex = jointInfo[3]
            if qIndex > -1:
                self.motorNames.append(str(jointInfo[1]))
                self.motorIndices.append(i)

    def getActionDimension(self):
        if self.useInverseKinematics:
            return len(self.motorIndices)
        else:
            return 6

    def getObservationDimension(self):
        return len(self.getObservation())

    def getObservation(self):
        observation = []
        state = p.getLinkState(self.kukaUid, self.kukaGripperIndex)
        pos = state[0]
        orn = state[1]
        euler = p.getEulerFromQuaternion(orn)
        observation.extend(list(pos))
        observation.extend(list(euler))
        return observation

    def applyAction(self, motorCommands):
        if self.useInverseKinematics:
            dx = motorCommands[0]
            dy = motorCommands[1]
            dz = motorCommands[2]
            da = motorCommands[3]
            fingerAngle = motorCommands[4]
            state = p.getLinkState(self.kukaUid, self.kukaEndEffectorIndex)
            actualEndEffectorPos = state[0]
            self.endEffectorPos[0] = self.endEffectorPos[0] + dx
            if self.endEffectorPos[0] > 0.65:
                self.endEffectorPos[0] = 0.65
            if self.endEffectorPos[0] < 0.5:
                self.endEffectorPos[0] = 0.5
            self.endEffectorPos[1] = self.endEffectorPos[1] + dy
            if self.endEffectorPos[1] < -0.17:
                self.endEffectorPos[1] = -0.17
            if self.endEffectorPos[1] > 0.22:
                self.endEffectorPos[1] = 0.22
            self.endEffectorPos[2] = self.endEffectorPos[2] + dz
            self.endEffectorAngle = self.endEffectorAngle + da
            pos = self.endEffectorPos
            orn = p.getQuaternionFromEuler([0, -math.pi, 0])
            if self.useNullSpace == 1:
                if self.useOrientation == 1:
                    jointPoses = p.calculateInverseKinematics(self.kukaUid, self.kukaEndEffectorIndex, pos, orn, self.ll, self.ul, self.jr, self.rp)
                else:
                    jointPoses = p.calculateInverseKinematics((self.kukaUid), (self.kukaEndEffectorIndex),
                      pos,
                      lowerLimits=(self.ll),
                      upperLimits=(self.ul),
                      jointRanges=(self.jr),
                      restPoses=(self.rp))
            else:
                if self.useOrientation == 1:
                    jointPoses = p.calculateInverseKinematics((self.kukaUid), (self.kukaEndEffectorIndex),
                      pos,
                      orn,
                      jointDamping=(self.jd))
                else:
                    jointPoses = p.calculateInverseKinematics(self.kukaUid, self.kukaEndEffectorIndex, pos)
                if self.useSimulation:
                    for i in range(self.kukaEndEffectorIndex + 1):
                        p.setJointMotorControl2(bodyUniqueId=(self.kukaUid), jointIndex=i,
                          controlMode=(p.POSITION_CONTROL),
                          targetPosition=(jointPoses[i]),
                          targetVelocity=0,
                          force=(self.maxForce),
                          maxVelocity=(self.maxVelocity),
                          positionGain=0.3,
                          velocityGain=1)

                else:
                    for i in range(self.numJoints):
                        p.resetJointState(self.kukaUid, i, jointPoses[i])

                p.setJointMotorControl2((self.kukaUid), 7,
                  (p.POSITION_CONTROL),
                  targetPosition=(self.endEffectorAngle),
                  force=(self.maxForce))
                p.setJointMotorControl2((self.kukaUid), 8,
                  (p.POSITION_CONTROL),
                  targetPosition=(-fingerAngle),
                  force=(self.fingerAForce))
                p.setJointMotorControl2((self.kukaUid), 11,
                  (p.POSITION_CONTROL),
                  targetPosition=fingerAngle,
                  force=(self.fingerBForce))
                p.setJointMotorControl2((self.kukaUid), 10,
                  (p.POSITION_CONTROL),
                  targetPosition=0,
                  force=(self.fingerTipForce))
                p.setJointMotorControl2((self.kukaUid), 13,
                  (p.POSITION_CONTROL),
                  targetPosition=0,
                  force=(self.fingerTipForce))
        else:
            for action in range(len(motorCommands)):
                motor = self.motorIndices[action]
                p.setJointMotorControl2((self.kukaUid), motor,
                  (p.POSITION_CONTROL),
                  targetPosition=(motorCommands[action]),
                  force=(self.maxForce))