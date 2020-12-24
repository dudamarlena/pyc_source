# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\cocosnode.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 32622 bytes
"""
CocosNode: the basic element of cocos2d
"""
from __future__ import division, print_function, unicode_literals
from six import string_types
__docformat__ = 'restructuredtext'
import copy, math, weakref, pyglet
from pyglet import gl
import cocos.director as director
from cocos.camera import Camera
from cocos import euclid
__all__ = [
 'CocosNode']

class CocosNode(object):
    __doc__ = '\n    Cocosnode is the main element. Anything that gets drawn or contains things\n    that gets drawn is a :class:`CocosNode`.\n    The most popular :class:`CocosNode` are :class:`cocos.scene.Scene`, \n    :class:`cocos.layer.base_layers.Layer` and :class:`cocos.sprite.Sprite`.\n\n    The main features of a :class:`CocosNode` are:\n        - They can contain other :class:`CocosNode` (:meth:`add`, :meth:`get`, \n          :meth:`remove`, etc)\n        - They can schedule periodic callback (:meth:`schedule`, \n          :meth:`schedule_interval`, etc)\n        - They can execute actions (:meth:`do`, :meth:`pause`, :meth:`stop`, \n          etc)\n\n    Some :class:`CocosNode` provide extra functionality for them or their \n    children.\n\n    Subclassing a :class:`CocosNode` usually means (one/all) of:\n        - overriding ``__init__`` to initialize resources and schedule callbacks\n        - create callbacks to handle the advancement of time\n        - overriding :meth:`draw` to render the node\n    '

    def __init__(self):
        self.children = []
        self.children_names = {}
        self._parent = None
        self._x = 0
        self._y = 0
        self._scale = 1.0
        self._scale_x = 1.0
        self._scale_y = 1.0
        self._rotation = 0.0
        self.camera = Camera()
        self.transform_anchor_x = 0
        self.transform_anchor_y = 0
        self.visible = True
        self.grid = None
        self.actions = []
        self.to_remove = []
        self.skip_frame = False
        self.scheduled = False
        self.scheduled_calls = []
        self.scheduled_interval_calls = []
        self.is_running = False
        self.is_transform_dirty = False
        self.transform_matrix = euclid.Matrix3().identity()
        self.is_inverse_transform_dirty = False
        self.inverse_transform_matrix = euclid.Matrix3().identity()

    def make_property(attr):
        types = {'anchor_x':'int', 
         'anchor_y':'int',  'anchor':'(int, int)'}

        def set_attr():

            def inner(self, value):
                setattr(self, 'transform_' + attr, value)

            return inner

        def get_attr():

            def inner(self):
                return getattr(self, 'transform_' + attr)

            return inner

        return property((get_attr()),
          (set_attr()),
          doc=('a property to get fast access to transform_%s\n\n            :type: %s' % (attr, types[attr])))

    anchor = make_property('anchor')
    anchor_x = make_property('anchor_x')
    anchor_y = make_property('anchor_y')

    def make_property(attr):

        def set_attr():

            def inner(self, value):
                setattr(self, attr + '_x', value[0])
                setattr(self, attr + '_y', value[1])

            return inner

        def get_attr(self):
            return (
             getattr(self, attr + '_x'), getattr(self, attr + '_y'))

        return property(get_attr,
          (set_attr()),
          doc='a property to get fast access to "+attr+"_[x|y]\n\n            :type: (int, int)\n            ')

    transform_anchor = make_property('transform_anchor')
    del make_property

    def schedule_interval(self, callback, interval, *args, **kwargs):
        """
        Schedule a function to be called every ``interval`` seconds.

        Specifying an interval of 0 prevents the function from being
        called again (see :meth:`schedule` to call a function as often as 
        possible).

        The callback function prototype is the same as for :meth:`schedule`.

        This function is a wrapper to ``pyglet.clock.schedule_interval``.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not have to schedule things using pyglet by yourself.
        
        Arguments:
            callback (a function): 
                The function to call when the timer elapsed.
            interval (float): 
                The number of seconds to wait between each call.
            *args: Variable length argument list passed to the ``callback``.
            **kwargs: Arbitrary keyword arguments  passed to the ``callback``.

        """
        if self.is_running:
            (pyglet.clock.schedule_interval)(callback, interval, *args, **kwargs)
        self.scheduled_interval_calls.append((
         callback, interval, args, kwargs))

    def schedule(self, callback, *args, **kwargs):
        """
        Schedule a function to be called every frame.

        The function should have a prototype that includes ``dt`` as the
        first argument, which gives the elapsed time, in seconds, since the
        last clock tick.  Any additional arguments given to this function
        are passed on to the callback::

            def callback(dt, *args, **kwargs):
                pass

        This function is a wrapper to ``pyglet.clock.schedule``.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not have to schedule things using pyglet by yourself.

        Arguments:
            callback (a function):
                The function to call each frame.
            *args: Variable length argument list passed to the ``callback``.
            **kwargs: Arbitrary keyword arguments  passed to the ``callback``.
        """
        if self.is_running:
            (pyglet.clock.schedule)(callback, *args, **kwargs)
        self.scheduled_calls.append((
         callback, args, kwargs))

    def unschedule(self, callback):
        """
        Remove a function from the schedule.

        If the function appears in the schedule more than once, all occurances
        are removed. If the function was not scheduled, no error is raised.

        This function is a wrapper to pyglet.clock.unschedule.
        It has the additional benefit that all calllbacks are paused and
        resumed when the node leaves or enters a scene.

        You should not unschedule things using pyglet that where scheduled
        by :meth:`schedule`/:meth:`schedule_interval`.
        
        Arguments:
            callback (a function):
                The function to remove from the schedule.
        """
        self.scheduled_calls = [c for c in self.scheduled_calls if c[0] != callback]
        self.scheduled_interval_calls = [c for c in self.scheduled_interval_calls if c[0] != callback]
        if self.is_running:
            pyglet.clock.unschedule(callback)

    def resume_scheduler(self):
        """
        Time will continue/start passing for this node and callbacks
        will be called, worker actions will be called.
        """
        for c, i, a, k in self.scheduled_interval_calls:
            (pyglet.clock.schedule_interval)(c, i, *a, **k)

        for c, a, k in self.scheduled_calls:
            (pyglet.clock.schedule)(c, *a, **k)

    def pause_scheduler(self):
        """
        Time will stop for this node: scheduled callbacks will
        not be called, worker actions will not be called.
        """
        for f in set([x[0] for x in self.scheduled_interval_calls] + [x[0] for x in self.scheduled_calls]):
            pyglet.clock.unschedule(f)

        for arg in self.scheduled_calls:
            pyglet.clock.unschedule(arg[0])

    def _get_parent(self):
        if self._parent is None:
            return
        return self._parent()

    def _set_parent(self, parent):
        if parent is None:
            self._parent = None
        else:
            self._parent = weakref.ref(parent)

    parent = property(_get_parent, _set_parent, doc='The parent of this object.\n\n    Returns:\n        CocosNode or None\n    ')

    def get_ancestor(self, klass):
        """
        Walks the nodes tree upwards until it finds a node of the class
        ``klass`` or returns None.

        Returns:
            CocosNode or None
        """
        if isinstance(self, klass):
            return self
        parent = self.parent
        if parent:
            return parent.get_ancestor(klass)

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    x = property(_get_x, (lambda self, x: self._set_x(x)), doc='The x coordinate of the CocosNode')

    def _get_y(self):
        return self._y

    def _set_y(self, y):
        self._y = y
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    y = property(_get_y, (lambda self, y: self._set_y(y)), doc='The y coordinate of the CocosNode')

    def _get_position(self):
        return (
         self._x, self._y)

    def _set_position(self, pos):
        self._x, self._y = pos
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    position = property(_get_position, (lambda self, p: self._set_position(p)), doc='The (x, y) coordinates of the object.\n\n    :type: tuple[int, int]\n    ')

    def _get_scale(self):
        return self._scale

    def _set_scale(self, s):
        self._scale = s
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    scale = property(_get_scale, (lambda self, scale: self._set_scale(scale)), doc='The scaling factor of the object.\n\n    :type: float\n    ')

    def _get_scale_x(self):
        return self._scale_x

    def _set_scale_x(self, s):
        self._scale_x = s
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    scale_x = property(_get_scale_x, (lambda self, scale: self._set_scale_x(scale)), doc='The scale x of this object.\n\n    :type: float\n    ')

    def _get_scale_y(self):
        return self._scale_y

    def _set_scale_y(self, s):
        self._scale_y = s
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    scale_y = property(_get_scale_y, (lambda self, scale: self._set_scale_y(scale)), doc='The scale y of this object.\n\n    :type: float\n    ')

    def _get_rotation(self):
        return self._rotation

    def _set_rotation(self, a):
        self._rotation = a
        self.is_transform_dirty = True
        self.is_inverse_transform_dirty = True

    rotation = property(_get_rotation, (lambda self, angle: self._set_rotation(angle)), doc='The rotation of this object in degrees.\n    Defaults to 0.0.\n\n    :type: float\n    ')

    def add(self, child, z=0, name=None):
        """Adds a child and if it becomes part of the active scene, it calls
        its :meth:`on_enter` method.

        Arguments:
            child (CocosNode):
                object to be added
            z (Optional[float]):
                the child z index. Defaults to 0.
            name (Optional[str]):
                Name of the child. Defaults to ``None``

        Returns:
            CocosNode: self

        """
        if name:
            if name in self.children_names:
                raise Exception('Name already exists: %s' % name)
            self.children_names[name] = child
        child.parent = self
        elem = (
         z, child)
        lo = 0
        hi = len(self.children)
        a = self.children
        while lo < hi:
            mid = (lo + hi) // 2
            if z < a[mid][0]:
                hi = mid
            else:
                lo = mid + 1

        self.children.insert(lo, elem)
        if self.is_running:
            child.on_enter()
        return self

    def kill(self):
        """Remove this object from its parent, and thus most likely from
        everything.
        """
        self.parent.remove(self)

    def remove(self, obj):
        """Removes a child given its name or object

        If the node was added with name, it is better to remove by name, else
        the name will be unavailable for further adds (and will raise an 
        Exception if add with this same name is attempted)

        If the node was part of the active scene, its :meth:`on_exit` method 
        will be called.

        Arguments:
            obj (str or object):
                Name of the reference to be removed or object to be removed.
        """
        if isinstance(obj, string_types):
            if obj in self.children_names:
                child = self.children_names.pop(obj)
                self._remove(child)
            else:
                raise Exception('Child not found: %s' % obj)
        else:
            self._remove(obj)

    def _remove(self, child):
        l_old = len(self.children)
        self.children = [(z, c) for z, c in self.children if c != child]
        if l_old == len(self.children):
            raise Exception('Child not found: %s' % str(child))
        if self.is_running:
            child.on_exit()

    def get_children(self):
        """Return a list with the node's children, order is back to front.

        Returns:
            list[CocosNode]: children of this node, ordered back to front.

        """
        return [c for z, c in self.children]

    def __contains__(self, child):
        return child in self.get_children()

    def get(self, name):
        """Gets a child given its name.

        Arguments:
            name (str):
                name of the reference to retrieve.

        Returns:
            CocosNode: The child named 'name'. Will raise an ``Exception`` if 
            not present.

        Warning:
            If a node is added with name, then removing it differently
            than by name will prevent the name to be recycled: attempting to add 
            another node with this name will produce an Exception.
        """
        if name in self.children_names:
            return self.children_names[name]
        raise Exception('Child not found: %s' % name)

    def on_enter(self):
        """
        Called every time just before the node enters the stage.

        Scheduled calls and worker actions begin or continue to perform.

        Good point to do ``push_handlers()`` if you have custom ones
        
        Note:
            A handler pushed there is near certain to require a 
            ``pop_handlers()`` in the :meth:`on_exit` method (else it will be 
            called even after being removed from the active scene, or if going 
            on stage again it will be called multiple times for each event 
            ocurrences).
        """
        self.is_running = True
        self.resume()
        self.resume_scheduler()
        for c in self.get_children():
            c.on_enter()

    def on_exit(self):
        """
        Called every time just before the node leaves the stage.

        Scheduled calls and worker actions are suspended, that is, they will not
        be called until an :meth:`on_enter` event happens.

        Most of the time you will want to ``pop_handlers()`` for all explicit
        ``push_handlers()`` found in meth:`on_enter`.

        Consider to release here openGL resources created by this node, like
        compiled vertex lists.
        """
        self.is_running = False
        self.pause()
        self.pause_scheduler()
        for c in self.get_children():
            c.on_exit()

    def transform(self):
        """
        Apply ModelView transformations.

        You will most likely want to wrap calls to this function with
        ``glPushMatrix()``/``glPopMatrix()``
        """
        x, y = director.get_window_size()
        if not (self.grid and self.grid.active):
            self.camera.locate()
        gl.glTranslatef(self.position[0], self.position[1], 0)
        gl.glTranslatef(self.transform_anchor_x, self.transform_anchor_y, 0)
        if self.rotation != 0.0:
            gl.glRotatef(-self._rotation, 0, 0, 1)
        if self.scale != 1.0 or self.scale_x != 1.0 or self.scale_y != 1.0:
            gl.glScalef(self._scale * self._scale_x, self._scale * self._scale_y, 1)
        if self.transform_anchor != (0, 0):
            gl.glTranslatef(-self.transform_anchor_x, -self.transform_anchor_y, 0)

    def walk(self, callback, collect=None):
        """
        Executes callback on all the subtree starting at self.
        returns a list of all return values that are not ``None``.

        Arguments:
            callback (a function):
                Callable that takes a :class:`CocosNode` as an argument.
            collect (list):
                List of non-`None` returned values from visited nodes.

        Returns:
            list: The list of non-`None` return values.

        """
        if collect is None:
            collect = []
        r = callback(self)
        if r is not None:
            collect.append(r)
        for node in self.get_children():
            node.walk(callback, collect)

        return collect

    def visit(self):
        """
        This function *visits* its children in a recursive
        way.

        It will first *visit* the children that
        that have a z-order value less than 0.

        Then it will call the :meth:`draw` method to
        draw itself.

        And finally it will *visit* the rest of the
        children (the ones with a z-value bigger
        or equal than 0)

        Before *visiting* any children it will call
        the :meth:`transform` method to apply any possible
        transformations.
        """
        if not self.visible:
            return
            position = 0
            if self.grid:
                if self.grid.active:
                    self.grid.before_draw()
        else:
            if self.children:
                if self.children[0][0] < 0:
                    gl.glPushMatrix()
                    self.transform()
                    for z, c in self.children:
                        if z >= 0:
                            break
                        position += 1
                        c.visit()

                    gl.glPopMatrix()
            self.draw()
            if position < len(self.children):
                gl.glPushMatrix()
                self.transform()
                for z, c in self.children[position:]:
                    c.visit()

                gl.glPopMatrix()
            if self.grid and self.grid.active:
                self.grid.after_draw(self.camera)

    def draw(self, *args, **kwargs):
        """
        This is the function you will have to override if you want your
        subclassed :class:`CocosNode` to draw something on screen.

        You *must* respect the position, scale, rotation and anchor attributes.
        If you want OpenGL to do the scaling for you, you can::

            def draw(self):
                glPushMatrix()
                self.transform()
                # ... draw ..
                glPopMatrix()
        """
        pass

    def do(self, action, target=None):
        """Executes an :class:`.Action`.
        When the action is finished, it will be removed from the node's actions
        container.
        
        To remove an action you must use the :meth:`do` return value to
        call :meth:`remove_action`.

        Arguments:
            action (Action): 
                Action that will be executed.
        Returns:
            Action: A clone of ``action``

        """
        a = copy.deepcopy(action)
        if target is None:
            a.target = self
        else:
            a.target = target
        a.start()
        self.actions.append(a)
        if not self.scheduled:
            if self.is_running:
                self.scheduled = True
                pyglet.clock.schedule(self._step)
        return a

    def remove_action(self, action):
        """Removes an action from the node actions container, potentially 
        calling ``action.stop()``.

        If action was running, :meth:`.Action.stop` is called.
        Mandatory interface to remove actions in the node actions container.
        When skipping this there is the posibility to double call the 
        ``action.stop``

        Arguments:
            action (Action):
                Action to be removed.
                Must be the return value for a :meth:`do` call
        """
        assert action in self.actions
        if not action.scheduled_to_remove:
            action.scheduled_to_remove = True
            action.stop()
            action.target = None
            self.to_remove.append(action)

    def pause(self):
        """
        Suspends the execution of actions.
        """
        if not self.scheduled:
            return
        self.scheduled = False
        pyglet.clock.unschedule(self._step)

    def resume(self):
        """
        Resumes the execution of actions.
        """
        if self.scheduled:
            return
        self.scheduled = True
        pyglet.clock.schedule(self._step)
        self.skip_frame = True

    def stop(self):
        """
        Removes all actions from the running action list.

        For each action running, the stop method will be called,
        and the action will be removed from the actions container.
        """
        for action in self.actions:
            self.remove_action(action)

    def are_actions_running(self):
        """
        Determine whether any actions are running.
        """
        return bool(set(self.actions) - set(self.to_remove))

    def _step(self, dt):
        """pumps all the actions in the node actions container

            The actions scheduled to be removed are removed.
            Then a :meth:`.Action.step` is called for each action in the
            node actions container, and if the action doesn't need any more step
            calls, it will be scheduled to be removed. When scheduled to be
            removed, the :meth:`.Action.stop` method for the action is called.

        Arguments:
            dt (float):
                The time in seconds that elapsed since that last time this 
                function was called.
        """
        for x in self.to_remove:
            if x in self.actions:
                self.actions.remove(x)

        self.to_remove = []
        if self.skip_frame:
            self.skip_frame = False
            return
        if len(self.actions) == 0:
            self.scheduled = False
            pyglet.clock.unschedule(self._step)
        for action in self.actions:
            action.scheduled_to_remove or action.step(dt)
            if action.done():
                self.remove_action(action)

    def get_local_transform(self):
        """Returns an :class:`.euclid.Matrix3` with the local transformation matrix

        Returns:
            euclid.Matrix3
        """
        if self.is_transform_dirty:
            matrix = euclid.Matrix3().identity()
            matrix.translate(self._x, self._y)
            matrix.translate(self.transform_anchor_x, self.transform_anchor_y)
            matrix.rotate(math.radians(-self.rotation))
            matrix.scale(self._scale * self._scale_x, self._scale * self._scale_y)
            matrix.translate(-self.transform_anchor_x, -self.transform_anchor_y)
            self.is_transform_dirty = False
            self.transform_matrix = matrix
        return self.transform_matrix

    def get_world_transform(self):
        """Returns an :class:`.euclid.Matrix3` with the world transformation matrix

        Returns:
            euclid.Matrix3
        """
        matrix = self.get_local_transform()
        p = self.parent
        while p is not None:
            matrix = p.get_local_transform() * matrix
            p = p.parent

        return matrix

    def point_to_world(self, p):
        """Returns an :class:`.euclid.Vector2` converted to world space.

        Arguments:
            p (Vector2): Vector to convert

        Returns:
            Vector2: ``p`` vector converted to world coordinates.
        """
        v = euclid.Point2(p[0], p[1])
        matrix = self.get_world_transform()
        return matrix * v

    def get_local_inverse(self):
        """Returns an :class:`.euclid.Matrix3` with the local inverse 
        transformation matrix.

        Returns:
            euclid.Matrix3
        """
        if self.is_inverse_transform_dirty:
            matrix = self.get_local_transform().inverse()
            self.inverse_transform_matrix = matrix
            self.is_inverse_transform_dirty = False
        return self.inverse_transform_matrix

    def get_world_inverse(self):
        """returns an :class:`.euclid.Matrix3` with the world inverse 
        transformation matrix.

        Returns:
            euclid.Matrix3
        """
        matrix = self.get_local_inverse()
        p = self.parent
        while p is not None:
            matrix = matrix * p.get_local_inverse()
            p = p.parent

        return matrix

    def point_to_local(self, p):
        """returns an :class:`.euclid.Vector2` converted to local space.

        Arguments:
            p (Vector2): Vector to convert.

        Returns:
            Vector2: ``p`` vector converted to local coordinates.
        """
        v = euclid.Point2(p[0], p[1])
        matrix = self.get_world_inverse()
        return matrix * v