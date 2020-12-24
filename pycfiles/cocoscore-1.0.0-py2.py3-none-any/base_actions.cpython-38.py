# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\actions\base_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 34892 bytes
__doc__ = 'Foundation for all actions\n\nActions\n=======\n\nActions purpose is to modify along the time some trait of an object.\nThe object that the action will modify is the action\'s target.\nUsually the target will be an instance of some CocosNode subclass.\n\nExample::\n\n    MoveTo(position, duration)\n\nthe target will move smoothly over the segment\n(target.position, action position parameter), reaching the final position\nafter duration seconds have elapsed.\n\nCocos also provide some powerful operators to combine or modify actions, the\nmore important s being:\n\n**sequence operator:**   action_1 + action_2 -> action_result\n\nwhere action_result performs by first doing all that action_1 would do and\nthen perform all that action_2 would do\n\nExample use::\n\n    move_2 = MoveTo((100, 100), 10) + MoveTo((200, 200), 15)\n\nWhen activated, move_2 will move the target first to (100, 100), it will\narrive there 10 seconds after departure; then it will move to (200, 200),\nand will arrive there 10 seconds after having arrived to (100, 100)\n\n**spawn operator:**  action_1 | action_2 -> action_result\n\nwhere action_result performs by doing what would do action_1 in parallel with\nwhat would perform action_2\n\nExample use::\n\n    move_rotate = MoveTo((100,100), 10) | RotateBy(360, 5)\n\nWhen activated, move_rotate will move the target from the position at the\ntime of activation to (100, 100); also in the first 5 seconds target will\nbe rotated 360 degrees\n\n**loop operator:**   action_1 * n -> action_result\n\nWhere n non negative integer, and action result would repeat n times in a\nrow the same that action_1 would perform.\n\nExample use::\n\n    rotate_3 = RotateBy(360, 5) * 3\n\nWhen activated, rotate_3 will rotate target 3 times, spending 5 sec in each\nturn.\n\n\nAction instance roles\n+++++++++++++++++++++\n\nAction subclass: a detailed cualitative description for a change\n\nAn Action instance can play one of the following roles\n\nTemplate Role\n-------------\n\nThe instance knows all the details to perform,\nexcept a target has not been set.\nIn this role only __init__ and init should be called.\nIt has no access to the concrete action target.\nThe most usual way to obtain an action in the template mode is\nby calling the constructor of some Action subclass.\n\nExample::\n\n    position = (100, 100); duration = 10\n    move = MoveTo(position, duration)\n    move is playing here the template role.\n\n\nWorker role\n-----------\n\nCarry on with the changes desired when the action is initiated.\nYou obtain an action in the worker role by calling the method\ndo in a cocosnode instance, like::\n\n    worker_action = cocosnode.do(template_action, target=...)\n\nThe most usual is to call without the target kw-param, thus by default\nsetting target to the same cocosnode that performs the do.\nThe worker action begins to perform at the do call, and will carry on\nwith the desired modifications to target in subsequent frames.\nIf you want the capabilty to stop the changes midway, then you must\nretain the worker_action returned by the do and then, when you want stop\nthe changes, call::\n\n    cocosnode.remove_action(worker_action)\n    ( the cocosnode must be the same as in the do call )\n\nAlso, if your code need access to the action that performs the changes,\nhave in mind that you want the worker_action (but this is discouraged,\n\nExample::\n\n     position = (100, 100); duration = 10\n     move = MoveTo(position, duration)\n     blue_bird = Bird_CocosNode_subclass(...)\n     blue_move = blue_bird.do(move)\n\nHere move plays the template role and blue_move plays the worker role.\nThe target for blue_move has been set for the do method.\nWhen the do call omits the target parameter it defaults to the cocosnode where\nthe do is called, so in the example the target for blue_move is blue_bird.\nIn subsequents frames after this call, the blue_bird will move to the position\n(100, 100), arriving there 10 seconds after the do was executed.\n\nFrom the point of view of a worker role action, the actions life\ncan be mimicked by::\n\n    worker_action = deepcopy(template_action)\n    worker_action.target = some_obj\n    worker_action.start()\n    for dt in frame.next():\n        worker_action.step(dt)\n        if premature_termination() or worker_action.done():\n            break\n    worker_action.stop()\n\nComponent role\n--------------\n\nSuch an instance is created and stored into an Action class instance\nthat implements an Action operator (a composite action).\nCarries on with the changes desired on behalf of the composite action.\nWhen the composite action is not instance of IntervalAction, the\nperceived life can be mimicked as in the worker role.\nWhen the composite action is instance of IntervalAction, special rules apply.\nFor examples look at code used in the implementation of any operator, like\nSequence_Action or Sequence_IntervalAction.\n\nRestrictions and Capabilities for the current design and implementation\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\nWorker Independence\n-------------------\n\nMultiple worker actions can be obtained from a single template action, and\nthey wont interfere between them when applied to different targets.\n\nExample::\n\n     position = (100, 0); duration = 10\n     move = MoveBy(position, duration)\n\n     blue_bird = Sprite("blue_bird.png")\n     blue_bird.position = (0, 100)\n     blue_move = blue_bird.do(move)\n\n     red_bird = Sprite("red_bird.png")\n     red_bird.position = (0, 200)\n     red_move = blue_bird.do(move)\n\n    Here we placed two birds at the left screen border, separated vertically\n    by 100.\n    move is the template_action: full details on changes, still no target\n    blue_move, red_move are worker_action \'s: obtained by a node.do, have all\n    the details plus the target; they will perform the changes along the time.\n    What we see is both birds moving smooth to right by 100, taking 10 seconds\n    to arrive at final position.\n    Note that even if both worker actions derive for the same template, they\n    don\'t interfere one with the other.\n\n\nA worker action instance should not be used as a template\n---------------------------------------------------------\n\nYou will not get tracebacks, but the second worker action most surelly will\nhave a corrupt workspace, that will produce unexpected behavior.\n\nPosible fights between worker actions over a target member\n----------------------------------------------------------\n\nIf two actions that are active at the same time try to change the same\ntarget\'s member(s), the resulting change is computationally well defined, but\ncan be somewhat unexpected by the programmer.\n\nExample::\n\n    guy = Sprite("grossini.png")\n    guy.position = (100, 100)\n    worker1 = guy.do(MoveTo((400, 100), 3))\n    worker2 = guy.do(MoveBy((0, 300), 3))\n    layer.add(guy)\n\nHere the worker1 action will try to move to (400, 100), while the worker2 action\nwill try to move 300 in the up direction.\nBoth are changing guy.position in each frame.\n\nWhat we see on screen, in the current cocos implementation, is the guy moving up,\nlike if only worker2 were active.\nAnd, by physics, the programmer expectation probably guessed more like a\ncombination of both movements.\n\nNote that the unexpected comes from two actions trying to control the same target\nmember. If the actions were changing diferent members, like position and\nrotation, then no unexpected can happen.\n\nThe fighting can result in a behavior that is a combination of both workers, not one\na \'winning\' one. It entirely depends on the implementation from each action.\nIt is possible to write actions than in a fight will show additive behavoir,\nby example::\n\n    import cocos.euclid as eu\n    class MoveByAdditive(ac.Action):\n        def init( self, delta_pos, duration ):\n            try:\n                self.delta_pos = eu.Vector2(*delta_pos)/float(duration)\n            except ZeroDivisionError:\n                duration = 0.0\n                self.delta_pos = eu.Vector2(*delta_pos)\n            self.duration = duration\n\n        def start(self):\n            if self.duration==0.0:\n                self.target.position += self.delta_pos\n                self._done = True\n\n        def step(self, dt):\n            old_elapsed = self._elapsed\n            self._elapsed += dt\n            if self._elapsed > self.duration:\n                dt = self.duration - old_elapsed\n                self._done = True\n            self.target.position += dt*self.delta_pos\n\n    guy = Sprite("grossini.png")\n    guy.position = (100, 100)\n    worker1 = guy.do(MoveByAdditive((300, 0), 3))\n    worker2 = guy.do(MoveByAdditive((0, 300), 3))\n    layer.add(guy)\n\nHere the guy will mode in diagonal, ending 300 right and 300 up, the two\nactions have combined.\n\n\nAction\'s instances in the template role must be (really) deepcopyiable\n----------------------------------------------------------------------\n\nBeginers note: if you pass in init only floats, ints, strings, dicts or tuples\nof the former you can skip this section and revisit later.\n\nIf the action template is not deepcopyiable, you will get a deepcopy exception,\ncomplaining it can\'t copy something\n\nIf you cheat deepcopy by overriding __deepcopy__ in your class like::\n\n    def __deepcopy__(self):\n        return self\n\nyou will not get a traceback, but the Worker Independence will broke, the Loop\nand Repeat operators will broke, and maybe some more.\n\nThe section name states a precise requeriment, but it is a bit concise. Let see\nsome common situations where you can be in trouble and how to manage them.\n\n  - you try to pass a CocosNode instance in init, and init stores that in an\n    action member\n\n  - you try to pass a callback f = some_cocosnode.a_method, with the idea that\n    it shoud be called when some condition is meet, and init stores it in an\n    action member\n\n  - You want the action access some big decision table, static in the sense it\n    will not change over program execution. Even if is deepcopyable, there\'s\n    no need to deepcopy.\n\nWorkarounds:\n\n    - store the data that you do not want to deepcopy in some member in the\n      cocosnode\n\n    - use an init2 fuction to pass the params you want to not deepcopy::\n\n        worker = node.do(template)\n        worker.init2(another_cocosnode)\n\n      (see test_action_non_interval.py for an example)\n\n\nFuture:\nNext cocos version probably will provide an easier mechanism to designate some\nparameters as references.\n\n\nOverview main subclasses\n++++++++++++++++++++++++\n\nAll action classes in cocos must be subclass of one off the following:\n\n    - Action\n    - IntervalAction (is itself subclass of Action)\n    - InstantAction  (is itself subclass of IntervalAction)\n\nInstantAction\n-------------\n\nThe task that must perform happens in only one call, the start method.\nThe duration member has the value zero.\nExamples::\n\n    Place(position) : does target.position <- position\n    CallFunc(f, *args, **kwargs) : performs the call f(*args,**kwargs)\n\nIntervalAction\n--------------\n\nThe task that must perform is spanned over a number of frames.\nThe total time needed to complete the task is stored in the member duration.\nThe action will cease to perform when the time elapsed from the start call\nreachs duration.\nA proper IntervalAction must adhere to extra rules, look in the details section\nExamples::\n\n    MoveTo(position, duration)\n    RotateBy(angle, duration)\n\nAction\n------\n\nThe most general posible action class.\nThe task that must perform is spanned over a number of frames.\nThe time that the action would perfom is undefined, and member duration has\nvalue None.\nExamples::\n\n    RandomWalk(fastness)\n\nPerforms:\n\n  - selects a random point in the screen\n  - moves to it with the required fastness\n  - repeat\n\nThis action will last forever.\n\n::\n\n    Chase(fastness, chasee)\n\nPerforms:\n\n  - at each frame, move the target toward the chasee with the specified\n    fastness.\n  - Declare the action as done when the distance from target to\n    chasee is less than 10.\n\nIf fastness is greather than the chasee fastness this action will certainly\nterminate, but we dont know how much time when the action starts.\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import copy
__all__ = [
 'Action',
 'IntervalAction', 'InstantAction',
 'sequence', 'spawn', 'loop', 'Repeat',
 'Reverse', '_ReverseTime']

class Action(object):
    """Action"""

    def __init__(self, *args, **kwargs):
        """dont override - use init"""
        self.duration = None
        (self.init)(*args, **kwargs)
        self.target = None
        self._elapsed = 0.0
        self._done = False
        self.scheduled_to_remove = False

    def init(*args, **kwargs):
        """
        Gets called by __init__ with all the parameteres received,
        At this time the target for the action is unknown.
        Typical use is store parameters needed by the action.
        """
        pass

    def start(self):
        """
        External code sets self.target and then calls this method.
        Perform here any extra initialization needed.
        """
        pass

    def stop(self):
        """
        When the action must cease to perform this function is called by
        external code; after this call no other method should be called.
        """
        self.target = None

    def step(self, dt):
        """
        Gets called every frame. `dt` is the number of seconds that elapsed
        since the last call.
        """
        self._elapsed += dt

    def done(self):
        """
        False while the step method must be called.
        """
        return self._done

    def __add__(self, action):
        """sequence operator - concatenates actions
            action1 + action2 -> action_result
            where action_result performs as:
            first do all that action1 would do; then
            perform all that action2 would do
        """
        return sequence(self, action)

    def __mul__(self, other):
        """repeats ntimes the action
        action * n -> action_result
        where action result performs as:
        repeat n times the changes that action would do
        """
        if not isinstance(other, int):
            raise TypeError('Can only multiply actions by ints')
        if other <= 1:
            return self
        return Loop_Action(self, other)

    def __or__(self, action):
        """spawn operator -  runs two actions in parallel
        action1 | action2 -> action_result
        """
        return spawn(self, action)

    def __reversed__(self):
        raise Exception('Action %s cannot be reversed' % self.__class__.__name__)


class IntervalAction(Action):
    """IntervalAction"""

    def step(self, dt):
        """
        Dont customize this method: it will not be called when in the component
        role for certain composite actions (like Sequence_IntervalAction).
        In such situation the composite will calculate the suitable t and
        directly call .update(t)
        You customize the action stepping by overriding .update
        """
        self._elapsed += dt
        try:
            self.update(min(1, self._elapsed / self.duration))
        except ZeroDivisionError:
            self.update(1.0)

    def update(self, t):
        """Gets called on every frame
        't' is the time elapsed normalized to [0, 1]
        If this action takes 5 seconds to execute, `t` will be equal to 0
        at 0 seconds. `t` will be 0.5 at 2.5 seconds and `t` will be 1 at 5sec.
        This method must not use self._elapsed, which is not guaranted to be
        updated.
        """
        pass

    def done(self):
        """
        When in the worker role, this method is reliable.
        When in the component role, if the composite spares the call to
        step this method cannot be relied (an then the composite must decide
        by itself when the action is done).
        Example of later situation is Sequence_IntervalAction.
        """
        return self._elapsed >= self.duration

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Can only multiply actions by ints')
        if other <= 1:
            return self
        return Loop_IntervalAction(self, other)


def Reverse(action):
    """Reverses the behavior of the action

    Example::

        # rotates the sprite 180 degrees in 2 seconds counter clockwise
        action = Reverse( RotateBy( 180, 2 ) )
        sprite.do( action )
    """
    return action.__reversed__()


class InstantAction(IntervalAction):
    """InstantAction"""

    def __init__(self, *args, **kwargs):
        (super(IntervalAction, self).__init__)(*args, **kwargs)
        self.duration = 0.0

    def step(self, dt):
        """does nothing - dont override"""
        pass

    def start(self):
        """
        Here we must do out stuff
        """
        pass

    def done(self):
        return True

    def update(self, t):
        """does nothing - dont override
        """
        pass

    def stop(self):
        """does nothing - dont override
        """
        pass

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Can only multiply actions by ints')
        if other <= 1:
            return self
        return Loop_InstantAction(self, other)


def loop(action, times):
    return action * times


class Loop_Action(Action):
    """Loop_Action"""

    def init(self, one, times):
        self.one = one
        self.times = times

    def start(self):
        self.current_action = copy.deepcopy(self.one)
        self.current_action.target = self.target
        self.current_action.start()

    def step(self, dt):
        self._elapsed += dt
        self.current_action.step(dt)
        if self.current_action.done():
            self.current_action.stop()
            self.times -= 1
            if self.times == 0:
                self._done = True
            else:
                self.current_action = copy.deepcopy(self.one)
                self.current_action.target = self.target
                self.current_action.start()

    def stop(self):
        if not self._done:
            self.current_action.stop()


class Loop_InstantAction(InstantAction):
    """Loop_InstantAction"""

    def init(self, one, times):
        self.one = one
        self.times = times

    def start(self):
        for i in range(self.times):
            cpy = copy.deepcopy(self.one)
            cpy.start()


class Loop_IntervalAction(IntervalAction):
    """Loop_IntervalAction"""

    def init(self, one, times):
        """Init method

        :Parameters:
            `one` : `Action`
                Action to be repeated
            `times` : int
                Number of times that the action will be repeated
        """
        self.one = one
        self.times = times
        if not hasattr(self.one, 'duration'):
            raise Exception('You can only loop actions with finite duration, not repeats or others like that')
        self.duration = self.one.duration * times
        self.current = None
        self.last = None

    def start(self):
        self.duration = self.one.duration * self.times
        self.last = 0
        self.current_action = copy.deepcopy(self.one)
        self.current_action.target = self.target
        self.current_action.start()

    def __repr__(self):
        return '( %s * %i )' % (self.one, self.times)

    def update(self, t):
        current = int(t * float(self.times))
        new_t = (t - current * (1.0 / self.times)) * self.times
        if current >= self.times:
            return
        elif current == self.last:
            self.current_action.update(new_t)
        else:
            self.current_action.update(1)
            self.current_action.stop()
            for i in range(self.last + 1, current):
                self.current_action = copy.deepcopy(self.one)
                self.current_action.target = self.target
                self.current_action.start()
                self.current_action.update(1)
                self.current_action.stop()

            self.current_action = copy.deepcopy(self.one)
            self.current_action.target = self.target
            self.last = current
            self.current_action.start()
            self.current_action.update(new_t)

    def stop(self):
        self.current_action.update(1)
        self.current_action.stop()

    def __reversed__(self):
        return Loop_IntervalAction(Reverse(self.one), self.times)


def sequence(action_1, action_2):
    """Returns an action that runs first action_1 and then action_2
       The returned action will be instance of the most narrow class
       posible in InstantAction, IntervalAction, Action
    """
    if isinstance(action_1, InstantAction) and isinstance(action_2, InstantAction):
        cls = Sequence_InstantAction
    elif isinstance(action_1, IntervalAction) and isinstance(action_2, IntervalAction):
        cls = Sequence_IntervalAction
    else:
        cls = Sequence_Action
    return cls(action_1, action_2)


class Sequence_Action(Action):
    """Sequence_Action"""

    def init(self, one, two, **kwargs):
        self.one = copy.deepcopy(one)
        self.two = copy.deepcopy(two)
        self.first = True

    def start(self):
        self.one.target = self.target
        self.two.target = self.target
        self.current_action = self.one
        self.current_action.start()

    def step(self, dt):
        self._elapsed += dt
        self.current_action.step(dt)
        if self.current_action.done():
            self._next_action()

    def _next_action(self):
        self.current_action.stop()
        if self.first:
            self.first = False
            self.current_action = self.two
            self.current_action.start()
            if self.current_action.done():
                self._done = True
        else:
            self.current_action = None
            self._done = True

    def stop(self):
        if self.current_action:
            self.current_action.stop()

    def __reversed__(self):
        return sequence(Reverse(self.two), Reverse(self.one))


class Sequence_InstantAction(InstantAction):
    """Sequence_InstantAction"""

    def init(self, one, two, **kwargs):
        self.one = copy.deepcopy(one)
        self.two = copy.deepcopy(two)

    def start(self):
        self.one.target = self.target
        self.two.target = self.target
        self.one.start()
        self.two.start()

    def __reversed__(self):
        return Sequence_InstantAction(Reverse(self.two), Reverse(self.one))


class Sequence_IntervalAction(IntervalAction):
    """Sequence_IntervalAction"""

    def init(self, one, two, **kwargs):
        """Init method

        :Parameters:
            `one` : `Action`
                The first action to execute
            `two` : `Action`
                The second action to execute
        """
        self.one = copy.deepcopy(one)
        self.two = copy.deepcopy(two)
        self.actions = [self.one, self.two]
        if not (hasattr(self.one, 'duration') and hasattr(self.two, 'duration')):
            raise Exception('You can only sequence actions with finite duration, not repeats or others like that')
        self.duration = float(self.one.duration + self.two.duration)
        try:
            self.split = self.one.duration / self.duration
        except ZeroDivisionError:
            self.split = 0.0
        else:
            self.last = None

    def start(self):
        self.one.target = self.target
        self.two.target = self.target
        self.one.start()
        self.last = 0
        if self.one.duration == 0.0:
            self.one.update(1.0)
            self.one.stop()
            self.two.start()
            self.last = 1

    def __repr__(self):
        return '( %s + %s )' % (self.one, self.two)

    def update(self, t):
        current = t >= self.split
        if current != self.last:
            self.actions[self.last].update(1.0)
            self.actions[self.last].stop()
            self.last = current
            self.actions[self.last].start()
        elif current == 0:
            try:
                sub_t = t / self.split
            except ZeroDivisionError:
                sub_t = 1.0

        else:
            try:
                sub_t = (t - self.split) / (1.0 - self.split)
            except ZeroDivisionError:
                sub_t = 1.0

        self.actions[current].update(sub_t)

    def stop(self):
        if self.last:
            self.two.stop()
        else:
            self.one.stop()

    def __reversed__(self):
        return Sequence_IntervalAction(Reverse(self.two), Reverse(self.one))


def spawn(action_1, action_2):
    """Returns an action that runs action_1 and action_2 in paralel.
       The returned action will be instance of the most narrow class
       posible in InstantAction, IntervalAction, Action
    """
    if isinstance(action_1, InstantAction) and isinstance(action_2, InstantAction):
        cls = Spawn_InstantAction
    elif isinstance(action_1, IntervalAction) and isinstance(action_2, IntervalAction):
        cls = Spawn_IntervalAction
    else:
        cls = Spawn_Action
    return cls(action_1, action_2)


class Spawn_Action(Action):
    """Spawn_Action"""

    def init(self, one, two):
        one = copy.deepcopy(one)
        two = copy.deepcopy(two)
        self.actions = [one, two]

    def start(self):
        for action in self.actions:
            action.target = self.target
            action.start()

    def step(self, dt):
        if len(self.actions) == 2:
            self.actions[0].step(dt)
            if self.actions[0].done():
                self.actions[0].stop()
                self.actions = self.actions[1:]
        if self.actions:
            self.actions[(-1)].step(dt)
            if self.actions[(-1)].done():
                self.actions[(-1)].stop()
                self.actions = self.actions[:-1]
        self._done = len(self.actions) == 0

    def stop(self):
        for e in self.actions:
            e.stop()

    def __reversed__(self):
        return Reverse(self.actions[0]) | Reverse(self.actions[1])


class Spawn_IntervalAction(IntervalAction):
    """Spawn_IntervalAction"""

    def init(self, one, two):
        from cocos.actions.interval_actions import Delay
        one = copy.deepcopy(one)
        two = copy.deepcopy(two)
        self.duration = max(one.duration, two.duration)
        if one.duration > two.duration:
            two = two + Delay(one.duration - two.duration)
        elif two.duration > one.duration:
            one = one + Delay(two.duration - one.duration)
        self.actions = [one, two]

    def start(self):
        for a in self.actions:
            a.target = self.target
            a.start()

    def update(self, t):
        self.actions[0].update(t)
        self.actions[1].update(t)
        self._done = t >= 1.0
        if self._done:
            self.actions[0].stop()
            self.actions[1].stop()

    def __reversed__(self):
        return Reverse(self.actions[0]) | Reverse(self.actions[1])


class Spawn_InstantAction(InstantAction):
    """Spawn_InstantAction"""

    def init(self, one, two):
        one = copy.deepcopy(one)
        two = copy.deepcopy(two)
        self.actions = [one, two]

    def start(self):
        for action in self.actions:
            action.target = self.target
            action.start()


class Repeat(Action):
    """Repeat"""

    def init(self, action):
        """Init method.

        :Parameters:
            `action` : `Action` instance
                The action that will be repeated
        """
        self.duration = None
        self.original = action
        self.action = copy.deepcopy(action)

    def start(self):
        self.action.target = self.target
        self.action.start()

    def step(self, dt):
        self.action.step(dt)
        if self.action.done():
            self.action.stop()
            self.action = copy.deepcopy(self.original)
            self.start()

    def done(self):
        return False


class _ReverseTime(IntervalAction):
    """_ReverseTime"""

    def init(self, other, *args, **kwargs):
        (super(_ReverseTime, self).init)(*args, **kwargs)
        self.other = other
        self.duration = self.other.duration

    def start(self):
        self.other.target = self.target
        super(_ReverseTime, self).start()
        self.other.start()

    def stop(self):
        super(_ReverseTime, self).stop()

    def update(self, t):
        self.other.update(1 - t)

    def __reversed__(self):
        return self.other