# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Goap/Automaton.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 5535 bytes
from datetime import datetime
from automat import MethodicalMachine
from Goap.Sensor import Sensors
from Goap.Action import Actions
import Goap.Planner as Planner
import Goap.WorldState as WorldState
from rx import Observable
from time import sleep

class Fact(object):

    def __init__(self, sensor, data, binding):
        self.binding = binding
        self.data = data
        self.time_stamp = datetime.now()
        self.parent_sensor = sensor

    def __str__(self):
        return '{}: {}'.format(self.binding, self.data)

    def __repr__(self):
        return self.__str__()


class AutomatonPriorities:

    def __init__(self, items: list):
        self._items = items

    def __iter__(self):
        return self._items

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return self.__repr__()


class Automaton:
    __doc__ = ' A 3 State Machine Automaton: observing (aka monitor or patrol), planning and acting '
    machine = MethodicalMachine()

    def __init__(self, name: str, sensors: Sensors, actions: Actions, world_state: dict):
        self.world_state = WorldState(world_state)
        self.working_memory = []
        self.name = name
        self.sensors = sensors
        self.actions = actions
        self.planner = Planner(actions=actions)
        self.action_plan = []
        self.action_plan_response = None
        self.sensors_responses = {}
        self.actions_response = []
        self.goal = {}

    def __sense_environment(self):
        Observable.from_(self.sensors).subscribe(lambda sensor: self.working_memory.append(Fact(sensor=(sensor.name), data=(sensor.exec()), binding=(sensor.binding))))
        Observable.from_(self.working_memory).subscribe(lambda fact: setattr(self.world_state, fact.binding, fact.data.response))

    def __set_action_plan(self):
        self.action_plan = self.planner.plan(self.world_state, self.goal)
        return self.action_plan

    def __execute_action_plan(self):
        self.actions_response = [action[2]['object'].exec() for action in self.action_plan]
        return 'Action planning execution results: {}'.format(self.action_plan_response)

    @machine.state(initial=True)
    def waiting_orders(self):
        """ Waiting goal / orders """
        pass

    @machine.state()
    def sensing(self):
        """ Running sensors and assimilating sensor's responses """
        pass

    @machine.state()
    def planning(self):
        """ Generating action plan to change actual world state to achieve goal """
        pass

    @machine.state()
    def acting(self):
        """ Executing action plan"""
        pass

    @machine.input()
    def wait(self):
        """ Input waiting_orders state """
        pass

    @machine.input()
    def sense(self):
        """ Input sense state """
        pass

    @machine.output()
    def __sense(self):
        """ Execute sensors """
        self._Automaton__sense_environment()

    @machine.input()
    def plan(self):
        """ Input for planning state """
        pass

    @machine.output()
    def __plan(self):
        """ Generate action plan """
        self._Automaton__set_action_plan()

    @machine.input()
    def act(self):
        """ Input for acting state"""
        pass

    @machine.output()
    def __act(self):
        """ Execute action plan """
        self._Automaton__execute_action_plan()

    @machine.input()
    def input_goal(self, goal):
        """ Change / Set AI goal """
        pass

    @machine.output()
    def __input_goal(self, goal):
        """ Actually sets goal """
        self.goal = goal

    @machine.output()
    def __reset_working_memory(self):
        self.working_memory = []

    waiting_orders.upon(sense, enter=sensing, outputs=[_Automaton__sense])
    sensing.upon(plan, enter=planning, outputs=[_Automaton__plan])
    planning.upon(act, enter=acting, outputs=[_Automaton__act])
    acting.upon(sense, enter=sensing, outputs=[_Automaton__reset_working_memory, _Automaton__sense])
    waiting_orders.upon(input_goal, enter=waiting_orders, outputs=[_Automaton__input_goal])
    planning.upon(input_goal, enter=waiting_orders, outputs=[_Automaton__input_goal])
    acting.upon(input_goal, enter=waiting_orders, outputs=[_Automaton__input_goal])
    sensing.upon(wait, enter=waiting_orders, outputs=[_Automaton__reset_working_memory])


class AutomatonController(object):

    def __init__(self, actions: Actions, sensors: Sensors, name: str, world_state: dict):
        self.automaton = Automaton(actions=actions, sensors=sensors, name=name, world_state=world_state)

    @property
    def world_state(self):
        return self.automaton.world_state

    @world_state.setter
    def world_state(self, value):
        self.automaton.world_state = value

    @property
    def goal(self):
        return self.automaton.goal

    @goal.setter
    def goal(self, value):
        self.automaton.input_goal(value)

    def start(self):
        while True:
            self.automaton.sense()
            if self.automaton.world_state != self.goal:
                print('World state differs from goal: \nState: {}\nGoal: {}'.format(self.automaton.world_state, self.goal))
                print('Need to find an action plan')
                self.automaton.plan()
                print('Plain found. Will execute the action plan: {}'.format(self.automaton.action_plan))
                self.automaton.act()
            else:
                print('World state equals to goal: {}'.format(self.goal))
                self.automaton.wait()
            sleep(5)