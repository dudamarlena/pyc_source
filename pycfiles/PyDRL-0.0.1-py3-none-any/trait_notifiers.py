# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\trait_notifiers.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import traceback
from types import MethodType
from trait_base import TraitNotifier
from trait_delegates import TraitEvent

class TraitChangeNotifier:

    def __init__(self, object, name, anytrait_notifiers):
        self.trait_notifiers = []
        self.anytrait_notifiers = anytrait_notifiers
        cls = object.__class__
        cls_notifier = cls.__dict__.get(TraitNotifier)
        self.trait_notifier = self.anytrait_notifier = None
        trait_notifier = getattr(cls, name + '_changed', None)
        if trait_notifier is not None:
            if cls_notifier is not None:
                notifier = cls_notifier.notifiers.get(name)
                if notifier is not None:
                    self.trait_notifier = notifier.notifier
            if self.trait_notifier is None:
                self.trait_notifier = StaticTraitChangeNotifyWrapper(trait_notifier)
        anytrait_notifier = getattr(cls, 'anytrait_changed', None)
        if anytrait_notifier is not None:
            if cls_notifier is not None:
                self.anytrait_notifier = cls_notifier.anytrait_notifier
            else:
                self.anytrait_notifier = StaticAnyTraitChangeNotifyWrapper(anytrait_notifier)
        return

    def add(self, handler):
        trait_notifiers = self.trait_notifiers
        for cur_notifier in trait_notifiers:
            if handler == cur_notifier.handler:
                return 0

        trait_notifiers.append(TraitChangeNotifyWrapper(handler))
        return 1

    def remove(self, handler):
        trait_notifiers = self.trait_notifiers
        for cur_notifier in trait_notifiers:
            if handler == cur_notifier.handler:
                trait_notifiers.remove(cur_notifier)
                return 1

        return 0

    def __call__(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                if self.trait_notifier is not None:
                    self.trait_notifier(object, name, old_value, value)
                for notifier in self.trait_notifiers[:]:
                    notifier(object, name, old_value, value)

                if self.anytrait_notifier is not None:
                    self.anytrait_notifier(object, name, old_value, value)
                for notifier in self.anytrait_notifiers[:]:
                    notifier(object, name, old_value, value)

                return value
            obj_dict[name] = value
            return value
        except:
            obj_dict[name] = value
            if self.trait_notifier is not None:
                self.trait_notifier(object, name, old_value, value)
            for notifier in self.trait_notifiers[:]:
                notifier(object, name, old_value, value)

            if self.anytrait_notifier is not None:
                self.anytrait_notifier(object, name, old_value, value)
            for notifier in self.anytrait_notifiers[:]:
                notifier(object, name, old_value, value)

            return value

        return

    def deferred(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                tnotifier = getattr(object, TraitNotifier)
                if self.trait_notifier is not None:
                    tnotifier.defer_notify(self.trait_notifier, object, name, old_value, value)
                for notifier in self.trait_notifiers:
                    tnotifier.defer_notify(notifier, object, name, old_value, value)

                if self.anytrait_notifier is not None:
                    tnotifier.defer_notify(self.anytrait_notifier, object, name, old_value, value)
                for notifier in self.anytrait_notifiers:
                    tnotifier.defer_notify(notifier, object, name, old_value, value)

                return value
            obj_dict[name] = value
            return value
        except:
            obj_dict[name] = value
            tnotifier = getattr(object, TraitNotifier)
            if self.trait_notifier is not None:
                tnotifier.defer_notify(self.trait_notifier, object, name, old_value, value)
            for notifier in self.trait_notifiers:
                tnotifier.defer_notify(notifier, object, name, old_value, value)

            if self.anytrait_notifier is not None:
                tnotifier.defer_notify(self.anytrait_notifier, object, name, old_value, value)
            for notifier in self.anytrait_notifiers:
                tnotifier.defer_notify(notifier, object, name, old_value, value)

            return value

        return


class EventChangeNotifier(TraitChangeNotifier):

    def __call__(self, object, name, value, default):
        if self.trait_notifier is not None:
            self.trait_notifier(object, name, None, value)
        for notifier in self.trait_notifiers[:]:
            notifier(object, name, None, value)

        if self.anytrait_notifier is not None:
            self.anytrait_notifier(object, name, None, value)
        for notifier in self.anytrait_notifiers[:]:
            notifier(object, name, None, value)

        return value

    def deferred(self, object, name, value, default):
        tnotifier = getattr(object, TraitNotifier)
        if self.trait_notifier is not None:
            tnotifier.defer_notify(self.trait_notifier, object, name, None, value)
        for notifier in self.trait_notifiers:
            tnotifier.defer_notify(notifier, object, name, None, value)

        if self.anytrait_notifier is not None:
            tnotifier.defer_notify(self.anytrait_notifier, object, name, None, value)
        for notifier in self.anytrait_notifiers:
            tnotifier.defer_notify(notifier, object, name, None, value)

        return value


class TraitChangeNotifyWrapper:

    def __init__(self, handler):
        self.handler = handler
        adjust = 0
        func = handler
        if type(handler) is MethodType:
            func = handler.im_func
            adjust = 1
        self.__call__ = getattr(self, 'call_%d' % (func.func_code.co_argcount - adjust))

    def call_0(self, object, trait_name, old, new):
        try:
            self.handler()
        except:
            traceback.print_exc()

    def call_1(self, object, trait_name, old, new):
        try:
            self.handler(new)
        except:
            traceback.print_exc()

    def call_2(self, object, trait_name, old, new):
        try:
            self.handler(trait_name, new)
        except:
            traceback.print_exc()

    def call_3(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name, new)
        except:
            traceback.print_exc()

    def call_4(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name, old, new)
        except:
            traceback.print_exc()


class StaticAnyTraitChangeNotifyWrapper:

    def __init__(self, handler):
        self.handler = handler
        self.__call__ = getattr(self, 'call_%d' % handler.func_code.co_argcount)

    def call_0(self, object, trait_name, old, new):
        try:
            self.handler()
        except:
            traceback.print_exc()

    def call_1(self, object, trait_name, old, new):
        try:
            self.handler(object)
        except:
            traceback.print_exc()

    def call_2(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name)
        except:
            traceback.print_exc()

    def call_3(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name, new)
        except:
            traceback.print_exc()

    def call_4(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name, old, new)
        except:
            traceback.print_exc()


class StaticTraitChangeNotifyWrapper:

    def __init__(self, handler):
        self.handler = handler
        self.__call__ = getattr(self, 'call_%d' % handler.func_code.co_argcount)

    def call_0(self, object, trait_name, old, new):
        try:
            self.handler()
        except:
            traceback.print_exc()

    def call_1(self, object, trait_name, old, new):
        try:
            self.handler(object)
        except:
            traceback.print_exc()

    def call_2(self, object, trait_name, old, new):
        try:
            self.handler(object, new)
        except:
            traceback.print_exc()

    def call_3(self, object, trait_name, old, new):
        try:
            self.handler(object, old, new)
        except:
            traceback.print_exc()

    def call_4(self, object, trait_name, old, new):
        try:
            self.handler(object, trait_name, old, new)
        except:
            traceback.print_exc()


class InstanceTraitNotifier:

    def __init__(self, object, class_notifier):
        TraitNotifier.__init__(self)
        self.object = object
        self.deferrals = None
        self.deferral_level = 0
        self.active_notifiers = 0
        self.notifiers = {}
        self.anytrait_notifiers = []
        self.binder = InstanceTraitNotifierBinder(self, '_notifier_for', TraitChangeNotifier)
        self.event_binder = InstanceTraitNotifierBinder(self, '_event_notifier_for', EventChangeNotifier)
        if class_notifier is not None:
            obj_id = id(object)
            info = class_notifier.deferrals.get(obj_id)
            if info is not None:
                self.deferral_level, deferrals = info
                self.deferrals = {}
                for trait_name in deferrals.keys():
                    notifiers, old_value, new_value = deferrals[trait_name]
                    for notifier in notifiers.values():
                        self.defer_notify(notifier, object, trait_name, old_value, new_value)

                del class_notifier.deferrals[obj_id]
        return

    def _set_trait_value(self, object, name, value, default):
        return self.notifiers.get(name, self.binder)(object, name, value, default)

    def _set_trait_value_deferred(self, object, name, value, default):
        return self.notifiers.get(name, self.binder).deferred(object, name, value, default)

    def _set_event_value(self, object, name, value, default):
        return self.notifiers.get(name, self.event_binder)(object, name, value, default)

    def _set_event_value_deferred(self, object, name, value, default):
        return self.notifiers.get(name, self.event_binder).deferred(object, name, value, default)

    def add(self, handler, name):
        if name == 'anytrait':
            anytrait_notifiers = self.anytrait_notifiers
            if len(anytrait_notifiers) == 0:
                notifiers = self.notifiers
                for name, notifier in notifiers.items():
                    if not isinstance(notifier, TraitChangeNotifier):
                        mutates_to = TraitChangeNotifier
                        if isinstance(self.object._trait(name).setter, TraitEvent):
                            mutates_to = EventChangeNotifier
                        notifiers[name] = mutates_to(self.object, name, anytrait_notifiers)

            anytrait_notifiers.append(TraitChangeNotifyWrapper(handler))
        else:
            notifier = self.notifiers.get(name, None)
            if not isinstance(notifier, TraitChangeNotifier):
                mutates_to = TraitChangeNotifier
                if isinstance(self.object._trait(name).setter, TraitEvent):
                    mutates_to = EventChangeNotifier
                self.notifiers[name] = notifier = mutates_to(self.object, name, self.anytrait_notifiers)
            self.active_notifiers += notifier.add(handler)
        return

    def remove(self, handler, name):
        if name == 'anytrait':
            anytrait_notifiers = self.anytrait_notifiers
            for notifier in anytrait_notifiers:
                if handler == notifier.handler:
                    anytrait_notifiers.remove(notifier)
                    if len(anytrait_notifiers) == 0:
                        object = self.object
                        if self.active_notifiers == 0:
                            self.move_deferrals_to_class()
                        else:
                            notifiers = self.notifiers
                            for name, notifier in notifiers.items():
                                if len(notifier.trait_notifiers) == 0:
                                    notifiers[name] = object._notifier_for(name)

        else:
            notifiers = self.notifiers
            notifier = notifiers.get(name, None)
            if isinstance(notifier, TraitChangeNotifier):
                self.active_notifiers -= notifier.remove(handler)
                if len(notifier.trait_notifiers) == 0 and len(self.anytrait_notifiers) == 0:
                    object = self.object
                    notifiers[name] = object._notifier_for(name)
                    if self.active_notifiers == 0:
                        self.move_deferrals_to_class()
        return

    def reset_trait_value(self, object):
        obj_dict = object.__dict__
        if self.deferral_level == 0:
            obj_dict['_set_trait_value'] = self._set_trait_value
            obj_dict['_set_event_value'] = self._set_event_value
        else:
            obj_dict['_set_trait_value'] = self._set_trait_value_deferred
            obj_dict['_set_event_value'] = self._set_event_value_deferred

    def defer_trait_change(self, object, defer=True):
        if defer:
            self.deferral_level += 1
            if self.deferral_level == 1:
                self.deferrals = {}
                object._reset_trait_value()
        else:
            self.deferral_level -= 1
            if self.deferral_level == 0:
                deferrals = self.deferrals
                for trait_name in deferrals.keys():
                    notifiers, old_value, new_value = deferrals[trait_name]
                    for notifier in notifiers.values():
                        notifier(object, trait_name, old_value, new_value)

                self.deferrals = None
                object._reset_trait_value()
        return

    def defer_notify(self, notifier, object, trait_name, old, new):
        info = self.deferrals.setdefault(trait_name, [{}, old, new])
        info[0].setdefault(id(notifier), notifier)
        info[2] = new

    def move_deferrals_to_class(self):
        object = self.object
        del object.__dict__[TraitNotifier]
        deferrals = self.deferrals
        if deferrals is not None:
            cls_notifier = object._class_notifier()
            info = cls_notifier.deferrals.setdefault(id(object), [0, {}])
            info[0] = self.deferral_level
            for trait_name in deferrals.keys():
                notifiers, old_value, new_value = deferrals[trait_name]
                for notifier in notifiers.values():
                    cls_notifier.defer_notify(notifier, object, trait_name, old_value, new_value)

            self.deferrals = None
        self.object = self.notifiers = None
        object._reset_trait_value()
        return


class InstanceTraitNotifierBinder:

    def __init__(self, tnotifier, notifier_for, notifier_factory):
        self.tnotifier = tnotifier
        self.notifier_for = getattr(tnotifier.object, notifier_for)
        self.notifier_factory = notifier_factory

    def __call__(self, object, name, value, default):
        tnotifier = self.tnotifier
        if len(tnotifier.anytrait_notifiers) == 0:
            notifier = self.notifier_for(name)
        else:
            notifier = self.notifier_factory(object, name, tnotifier.anytrait_notifiers)
        tnotifier.notifiers[name] = notifier
        return notifier(object, name, value, default)

    def deferred(self, object, name, value, default):
        tnotifier = self.tnotifier
        if len(tnotifier.anytrait_notifiers) == 0:
            notifier = self.notifier_for(name)
        else:
            notifier = self.notifier_factory(object, name, tnotifier.anytrait_notifiers)
        tnotifier.notifiers[name] = notifier
        return notifier.deferred(object, name, value, default)


class ClassTraitNotifier:

    def __init__(self, cls):
        TraitNotifier.__init__(self)
        self.cls = cls
        self.notifiers = {}
        self.deferrals = {}
        self.bind_factory = self.no_anytrait_changed
        self.event_bind_factory = self.event_no_anytrait_changed
        handler = getattr(cls, 'anytrait_changed', None)
        if handler is not None:
            self.anytrait_notifier = StaticAnyTraitChangeNotifyWrapper(handler)
            self.bind_factory = self.has_anytrait_changed
            self.event_bind_factory = self.event_has_anytrait_changed
        self.binder = ClassTraitNotifierBinder(self.notifiers, self.bind_factory)
        self.event_binder = ClassTraitNotifierBinder(self.notifiers, self.event_bind_factory)
        return

    def _set_trait_value(self, object, name, value, default):
        return self.notifiers.get(name, self.binder)(object, name, value, default)

    def _set_trait_value_deferred(self, object, name, value, default):
        return self.notifiers.get(name, self.binder).deferred(object, name, value, default)

    def notifier_for(self, name):
        notifier = self.notifiers.get(name, None)
        if notifier is None:
            self.notifiers[name] = notifier = self.bind_factory(name)
        return notifier

    def no_anytrait_changed(self, name):
        notifier = getattr(self.cls, name + '_changed', None)
        if notifier is None:
            return simple_set_trait_value
        else:
            return SpecificTraitNotifier(StaticTraitChangeNotifyWrapper(notifier))

    def has_anytrait_changed(self, name):
        notifier = getattr(self.cls, name + '_changed', None)
        if notifier is None:
            return SpecificTraitNotifier(self.anytrait_notifier)
        else:
            return AnyAndSpecificTraitNotifier(self.anytrait_notifier, notifier)

    def _set_event_value(self, object, name, value, default):
        return self.notifiers.get(name, self.event_binder)(object, name, value, default)

    def _set_event_value_deferred(self, object, name, value, default):
        return self.notifiers.get(name, self.event_binder).deferred(object, name, value, default)

    def event_notifier_for(self, name):
        notifier = self.notifiers.get(name, None)
        if notifier is None:
            self.notifiers[name] = notifier = self.event_bind_factory(name)
        return notifier

    def event_no_anytrait_changed(self, name):
        notifier = getattr(self.cls, name + '_changed', None)
        if notifier is None:
            return ignore_set_trait_value
        else:
            return SpecificEventNotifier(StaticTraitChangeNotifyWrapper(notifier))

    def event_has_anytrait_changed(self, name):
        notifier = getattr(self.cls, name + '_changed', None)
        if notifier is None:
            return SpecificEventNotifier(self.anytrait_notifier)
        else:
            return AnyAndSpecificEventNotifier(self.anytrait_notifier, notifier)

    def event_anytrait_changed(self, object, name, value, default):
        self.anytrait_notifier(object, name, None, value)
        return value

    def reset_trait_value(self, object):
        obj_dict = object.__dict__
        if self.deferrals.get(id(object)) is None:
            obj_dict['_set_trait_value'] = self._set_trait_value
            obj_dict['_set_event_value'] = self._set_event_value
        else:
            obj_dict['_set_trait_value'] = self._set_trait_value_deferred
            obj_dict['_set_event_value'] = self._set_event_value_deferred
        return

    def defer_trait_change(self, object, defer=True):
        obj_id = id(object)
        if defer:
            info = self.deferrals.setdefault(obj_id, [0, {}])
            info[0] += 1
            if info[0] == 1:
                object._reset_trait_value()
        else:
            info = self.deferrals.get(obj_id)
            if info is not None:
                info[0] -= 1
                if info[0] == 0:
                    deferrals = info[1]
                    for trait_name in deferrals.keys():
                        notifiers, old_value, new_value = deferrals[trait_name]
                        for notifier in notifiers.values():
                            notifier(object, trait_name, old_value, new_value)

                    del self.deferrals[obj_id]
                    object._reset_trait_value()
        return

    def defer_notify(self, notifier, object, trait_name, old, new):
        info = self.deferrals[id(object)][1].setdefault(trait_name, [{}, old, new])
        info[0].setdefault(id(notifier), notifier)
        info[2] = new


class ClassTraitNotifierBinder:

    def __init__(self, notifiers, bind_factory):
        self.notifiers = notifiers
        self.bind_factory = bind_factory

    def __call__(self, object, name, value, default):
        self.notifiers[name] = notifier = self.bind_factory(name)
        return notifier(object, name, value, default)

    def deferred(self, object, name, value, default):
        self.notifiers[name] = notifier = self.bind_factory(name)
        return notifier.deferred(object, name, value, default)


class SimpleSetTraitValue:

    def __call__(self, object, name, value, default):
        object.__dict__[name] = value
        return value

    def deferred(self, object, name, value, default):
        object.__dict__[name] = value
        return value


simple_set_trait_value = SimpleSetTraitValue()

class IgnoreSetTraitValue:

    def __call__(self, object, name, value, default):
        pass

    def deferred(self, object, name, value, default):
        pass


ignore_set_trait_value = IgnoreSetTraitValue()

class SpecificTraitNotifier:

    def __init__(self, notifier):
        self.notifier = notifier

    def __call__(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                self.notifier(object, name, old_value, value)
                return value
            else:
                obj_dict[name] = value
                return value

        except:
            obj_dict[name] = value
            self.notifier(object, name, old_value, value)
            return value

    def deferred(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                getattr(object.__class__, TraitNotifier).defer_notify(self.notifier, object, name, old_value, value)
                return value
            else:
                obj_dict[name] = value
                return value

        except:
            obj_dict[name] = value
            getattr(object.__class__, TraitNotifier).defer_notify(self.notifier, object, name, old_value, value)
            return value


class SpecificEventNotifier:

    def __init__(self, notifier):
        self.notifier = notifier

    def __call__(self, object, name, value, default):
        self.notifier(object, name, None, value)
        return value

    def deferred(self, object, name, value, default):
        getattr(object.__class__, TraitNotifier).defer_notify(self.notifier, object, name, None, value)
        return value


class AnyAndSpecificTraitNotifier:

    def __init__(self, anytrait_notifier, notifier):
        self.anytrait_notifier = anytrait_notifier
        self.notifier = StaticTraitChangeNotifyWrapper(notifier)

    def __call__(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                self.notifier(object, name, old_value, value)
                self.anytrait_notifier(object, name, old_value, value)
                return value
            else:
                obj_dict[name] = value
                return value

        except:
            obj_dict[name] = value
            self.notifier(object, name, old_value, value)
            self.anytrait_notifier(object, name, old_value, value)
            return value

    def deferred(self, object, name, value, default):
        obj_dict = object.__dict__
        old_value = obj_dict.get(name, default)
        try:
            if old_value != value:
                obj_dict[name] = value
                tnotifier = getattr(object.__class__, TraitNotifier)
                tnotifier.defer_notify(self.notifier, object, name, old_value, value)
                tnotifier.defer_notify(self.anytrait_notifier, object, name, old_value, value)
                return value
            else:
                obj_dict[name] = value
                return value

        except:
            obj_dict[name] = value
            tnotifier = getattr(object.__class__, TraitNotifier)
            tnotifier.defer_notify(self.notifier, object, name, old_value, value)
            tnotifier.defer_notify(self.anytrait_notifier, object, name, old_value, value)
            return value


class AnyAndSpecificEventNotifier:

    def __init__(self, anytrait_notifier, notifier):
        self.anytrait_notifier = anytrait_notifier
        self.notifier = StaticTraitChangeNotifyWrapper(notifier)

    def __call__(self, object, name, value, default):
        self.notifier(object, name, None, value)
        self.anytrait_notifier(object, name, None, value)
        return value

    def deferred(self, object, name, value, default):
        tnotifier = getattr(object.__class__, TraitNotifier)
        tnotifier.defer_notify(self.notifier, object, name, None, value)
        tnotifier.defer_notify(self.anytrait_notifier, object, name, None, value)
        return value