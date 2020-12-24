# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tools/steppermotor.py
# Compiled at: 2014-05-02 14:31:41
from __future__ import print_function
import os, sys, time, BinPy, threading
from BinPy import *
try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    raise ImportError('You need to install PyQt4 for GUI components')

class StepperMotor(threading.Thread):
    """
    Create a StepperMotor Simulation

    Description:
    ============

    This Class is used to simulate a stepper motor using the adequate inputs.

    Specifications:
    ===============

    Drive Method        : Bipolar ( Predefined )
    No. of Phases       : 2
    No. of rotor poles  : 100 ( Can be modified )
    Winding Per Phase   : 1
    Type                : Permanent magnet
    Maximum RPM         : 1200
    Output Leads        : A   B   A!  B!

    Examples
    ========

    >>> import time
    >>> from BinPy import *
    >>> from BinPy.tools.steppermotor import StepperMotor
    >>> a = Connector(); b = Connector(); c = Connector(); d = Connector()
    >>> sm = StepperMotor("Main Motor",a,b,c,d)
    >>> for i in range(100):
    ...     sm.rotate(0.5,1)
    ...     time.sleep(0.1)
    >>> # To rotate through a certain angle
    >>> sm.move_to(-90, rpm = 60)
    >>> sm.move_to(90, rpm = 60, shortest_path = False)
    >>> # To rotate by a certain angle
    >>> sm.move_by(90)
    >>> sm.move_by(-60)
    >>> # To update the leads externally
    >>> a.state = 0; b.state = 0; c.state = 0; d.state = 1
    >>> sm.trigger()
    >>> a.state = 1; b.state = 0; c.state = 0; d.state = 1
    >>> sm.trigger()

    Methods
    =======

    rotate(steps, direction, rpm, step_type)
    # To rotate steps in the direction with a speed of rpm rotations per minute with mode as step_type

    trigger()
    # To update changes in leads

    stop()
    # To terminate existing operation(s)

    kill()
    # To terminate this thread

    reset()
    # To reset the StepperMotor

    Attributes
    ==========

    ROTOR_POLES ; No of rotor poles.
    PHASES      ; No of phases.
    MAX_RPM     ; Max safe speed.
    SEQ         ; Sequence matrix.
    leads       ; Connector list.
    index       ; Serial Number of Stepper motor instance.
    name        ; Specified name of Stepper motor instance.

    angle       ; Current position in degrees of stepper motor.
    busy        ; Status of operation.
    status      ; Stack of pending operations.

    """
    index = 0

    def __init__(self, name, *inputs):
        self.ROTOR_POLES = 100
        self.PHASES = 2
        self.MAX_RPM = 1200
        self.SEQ = [[1, 0, 0, 0],
         [
          1, 1, 0, 0],
         [
          0, 1, 0, 0],
         [
          0, 1, 1, 0],
         [
          0, 0, 1, 0],
         [
          0, 0, 1, 1],
         [
          0, 0, 0, 1],
         [
          1, 0, 0, 1]]
        threading.Thread.__init__(self)
        self.name = str(name)
        self.rpm = self.MAX_RPM
        self.total_poles = self.ROTOR_POLES * self.PHASES
        self.step_angle = float(360) / float(self.total_poles)
        StepperMotor.index += 1
        self.index = StepperMotor.index
        self.leads = [
         None] * 4
        self._history = [0] * 4
        self.set_inputs(*inputs)
        self.step_type = 0
        self.step_resolution = 0.5
        self.angle = 0
        self.daemon = True
        self._disp = _SMDisplayApp(self, self.name, self.index)
        self.status = []
        self.busy = False
        self.exit_flag = False
        self.start()
        return

    def rotate(self, steps=1, direction=1, rpm=None, step_type=0):
        """
        Rotate the stepper motor by [steps] steps and in the specified direction.

        steps can Either be multiples of 0.5 ( Half Stepping ) .
        Default value is 1 ( Full stepping )

        direction 1 --> rotate right
        direction 0 --> rotate left

        rpm should be less than the MAX_RPM and greater than 0

        stepping = 0 --> Half Stepping
        stepping = 1 --> Full Stepping
        """
        if self.busy:
            raise Exception
            return
        else:
            self.status.append(1)
            self.busy = True
            self.direction = direction
            self.direction = 0 if steps < 0 else 1
            self.steps = abs(steps)
            self.step_type = step_type
            if self.step_type == 0:
                self.steps = float(round(2 * float(self.steps))) / float(2)
                self.step_resolution = 0.5
            else:
                self.steps = round(self.steps)
                self.step_resolution = 1
            if rpm is not None:
                if rpm > 0 and rpm < self.MAX_RPM:
                    self.rpm = rpm
            return

    def _rotate(self):
        """
        Internally called to realize rotation.
        """
        if self.steps > 0:
            self.steps -= self.step_resolution
            self.validate()
            updated_state = self.get_next_state() if self.direction == 1 else self.get_prev_state()
            self._update_leads(updated_state)
            time.sleep(float(60) / float(self.rpm * 360))
            self.status.append(2)
        else:
            self.status.pop()
            self.busy = False

    def move_to(self, angle, rpm=None, shortest_path=True):
        """
        Rotate the stepper motor in the specified rpm speed to reach the specified angle.
        The shortest_path when set forces rotation in the direction of minor arc.
        If shortest_path is not set the behaviour is in the direction of either the major
        or minor arc.
        """
        angle %= 360
        diff_angle = angle - self.angle
        if shortest_path and diff_angle > 180:
            diff_angle *= -1
        self.rotate(steps=diff_angle / self.step_angle, rpm=rpm)

    def move_by(self, angle, rpm=None):
        """
        Rotate the stepper motor by the specified angle at the specified rpm speed.
        """
        diff_angle = angle - self.angle
        self.rotate(steps=angle / self.step_angle, rpm=rpm)

    def _update_leads(self, data):
        for i in range(4):
            self.leads[i].state = data[i]

    def get_state(self):
        return [ int(i) for i in self.leads ]

    def get_next_state(self, state=None, step_type=0):
        if state is None:
            state = self.get_state()
        if state in self.SEQ:
            return self.SEQ[((self.SEQ.index(state) + step_type + 1) % 8)]
        else:
            raise Exception
            return

    def get_prev_state(self, state=None, step_type=0):
        if state is None:
            state = self.get_state()
        if state in self.SEQ:
            return self.SEQ[((self.SEQ.index(state) - step_type - 1) % 8)]
        else:
            raise Exception
            return

    def get_seq_no(self, state=None):
        if state is None:
            state = self.get_state()
        return self.SEQ.index(state)

    def _update_angle(self):
        state = self.get_state()
        if self._history == state:
            return
        seq_no = self.get_seq_no(state)
        old_seq_no = self.get_seq_no(self._history)
        if (old_seq_no + 1) % 8 == seq_no:
            self.angle += 0.5 * self.step_angle
        elif (old_seq_no + 2) % 8 == seq_no:
            self.angle += self.step_angle
        elif (old_seq_no - 1) % 8 == seq_no:
            self.angle -= 0.5 * self.step_angle
        elif (old_seq_no - 2) % 8 == seq_no:
            self.angle -= self.step_angle
        else:
            print('ERROR: Invalid configuration. Only single and half step changes are alowed. Refer to SEQ for table of allowed inputs')
            print('Restoring the current configuration from history')
            self._update_leads(self._history)
        self.angle %= 360

    def stop(self):
        self.busy = False
        self.status = []

    def reset(self, keep_connections=True):
        self.stop()
        for pin in self.leads:
            pin.state = 0

        if not keep_connections:
            self.disconnect()
        self.angle = 0
        self._history = [0] * 4
        self.step_type = 0
        self.step_resolution = 0.5

    def set_inputs(self, *values):
        """
        Connect all the connectors at once
        """
        for i in range(4):
            if not isinstance(values[i], Connector):
                self.leads = [
                 None] * 4
                self._history = [0] * 4
                raise Exception
            self.set_input(i, values[i])
            self._history[i] = values[i].state

        return

    def set_input(self, index, value):
        """
        Set the input based on the index and value.

        If the value is a Connector, then the respective input is connected to it.
        else the Connector at that index is updated with the value.
        """
        if isinstance(self.leads[index], Connector):
            self.leads[index].untap(self, 'input')
        if index <= 4:
            if isinstance(value, Connector):
                self.leads[index] = value
            else:
                self.leads[index].state = int(value) if isinstance(self.leads[index], Connector) else None
        if self.leads[index] is None:
            raise Exception
        else:
            self.leads[index].tap(self, 'input')
        return

    def disconnect(self):
        for pin in self.leads:
            pin.untap(self, 'input')

        self.leads = [
         None] * 4
        return

    def kill(self):
        """
        Use this method to kill the StepperMotor instance.
        """
        self.exit_flag = True

    def run(self):
        while not self.exit_flag and not self._disp.exit:
            if len(self.status) != 0:
                if self.status[(-1)] == 2:
                    self._trigger()
                    self.status.pop()
                elif self.status[(-1)] == 1:
                    self._rotate()

        self._disp.kill()
        sys.exit()

    def trigger(self):
        """
        Call trigger to notify the stepper motor instance of any changes in the input leads
        """
        while len(self.status) != 0:
            time.sleep(0.001)

        self.status.append(2)

    def _trigger(self):
        self.validate()
        self._update_angle()
        self._history = self.get_state()

    def validate(self):
        if False in [ isinstance(i, Connector) for i in self.leads ]:
            raise Exception
        if self.get_state() not in self.SEQ:
            print('ERROR: Current Configuration is invalid. Restoring valid state from history.')
            if self._history in self.SEQ:
                self._update_leads(self._history)
            else:
                print('ERROR: Restoration Failed, History invalid. Restoring history to 1000. Preserving the current angle')
                self._history = [1, 0, 0, 0]
                self._update_leads(self._history)
        elif self._history not in self.SEQ:
            self._history = self.get_state()


class _SMDisplayApp(threading.Thread):

    def __init__(self, bound_to, name, index):
        threading.Thread.__init__(self)
        self.daemon = False
        self.app = QtGui.QApplication(sys.argv)
        self.window = _SMDisplay(bound_to, name, index)
        self.window.show()
        self.window.raise_()
        self.bound_to = bound_to
        self.index = index
        self.name = name
        self.exit = False
        self.start()

    def run(self):
        self.app.exec_()
        while not self.exit:
            if not self.window.isVisible():
                print('STEPPERMOTOR: ' + str(self.index) + ' ' + str(self.name) + ' : Simulation window has been closed. Terminating simulation.\n')
                self.bound_to.reset()
                self.exit = True
            else:
                time.sleep(0.1)

        self.window.close()
        sys.exit()

    def kill(self):
        self.exit = True


class _SMDisplay(QtGui.QMainWindow):
    """
    Internal GUI module to display the stepper motor simulation
    """

    def __init__(self, bound_to, name, index):
        super(_SMDisplay, self).__init__(None)
        self.bound_to = bound_to
        self.name = name
        self.index = index
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet('QWidget{background-color: #FFFFFF;}')
        self.setWindowTitle('BinPy : StepperMotor - ' + str(self.index) + ' - ' + str(self.name))
        self.path = os.path.join(str(BinPy.__file__).replace('__init__.pyc', '').replace('__init__.py', ''), 'res', 'stepper_motor.jpg')
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(150, 150, 300, 300)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.pixmap = QtGui.QPixmap(self.path).scaled(self.label.size(), 1)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.refresh)
        self.timer.start(1)
        return

    def refresh(self, angle=None):
        if not self.isVisible():
            self.timer.stop()
            return
        else:
            if angle is None:
                angle = self.bound_to.angle
            rotated = self.pixmap.transformed(QtGui.QTransform().rotate(angle))
            self.label.setPixmap(rotated)
            return