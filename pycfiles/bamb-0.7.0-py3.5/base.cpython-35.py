# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/domain/base.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 27887 bytes
from common import constants
from common import utils
from domain import exceptions
import copy

class Invokable(object):

    def __init__(self, *arg, **kwargs):
        self.executor_name = ''
        self.target = None
        self.parameters = None
        self.result = None
        self.native_execution = True
        self._Invokable__flags = constants.MASK_INVOKABLE_TARGET_MANDATORY

    def invoke(self, *args, **kwargs):
        self.result = Result()
        try:
            self.result.content = self.on_invoking(*args, **kwargs)
            self.result.state = constants.MASK_RESULT_SUCCESS
        except RuntimeError as e:
            self.result.state = constants.MASK_RESULT_FAILED
            self.result.content = str(e)

    def on_invoking(self, *args, **kwargs):
        pass

    def copy_execution_info(self, oth, target=None, parameters=None):
        if not isinstance(oth, Invokable):
            return
        if target is None and oth.target is not None:
            target = oth.target.clone()
        if parameters is None:
            parameters = {}
            if oth.parameters is not None:
                for k, p in oth.parameters.items():
                    parameters[k] = p.clone()

        if target is not None:
            self.target = target
        if parameters is not None:
            self.parameters = parameters
        if len(oth.executor_name) > 0:
            self.executor_name = oth.executor_name

    @property
    def is_target_sensitive(self):
        return self._Invokable__flags & constants.MASK_INVOKABLE_TARGET_MANDATORY

    @is_target_sensitive.setter
    def is_target_sensitive(self, value):
        if value:
            self._Invokable__flags |= constants.MASK_INVOKABLE_TARGET_MANDATORY
        else:
            self._Invokable__flags &= ~constants.MASK_INVOKABLE_TARGET_MANDATORY

    @property
    def ignore_result(self):
        return self._Invokable__flags & constants.MASK_INVOKABLE_IGNORE_RESULT

    @ignore_result.setter
    def ignore_result(self, value):
        if value:
            self._Invokable__flags |= constants.MASK_INVOKABLE_IGNORE_RESULT
        else:
            self._Invokable__flags &= ~constants.MASK_INVOKABLE_IGNORE_RESULT


class EasySerializable(object):

    def __init__(self, *args, **kwargs):
        self._id = None
        self._EasySerializable__class_name = ''
        self._EasySerializable__module_name = ''
        self._EasySerializable__froms = []
        self._EasySerializable__dwi = [[]]
        self._EasySerializable__dict_updated = False
        self.es_update_by_definition()
        self.es_update_by_parameters(*args, **kwargs)

    def es_update_by_definition(self):
        self._EasySerializable__class_name = self.__class__.__name__
        module_names = self.__module__.split('.')
        self._EasySerializable__module_name = module_names[(-1)]
        if len(module_names) > 1:
            self._EasySerializable__froms = module_names[0:-1]
        self._EasySerializable__dwi = self.dwi

    @staticmethod
    def is_wrapped_dict(d):
        if isinstance(d, dict):
            return len(constants.KEYWORDS_ES_MANDATORY & set(d.keys())) == len(constants.KEYWORDS_ES_MANDATORY)
        else:
            return False

    def clone(self):
        d = self.es_to_dict()
        return EasySerializable.es_load(d)

    @property
    def object_id(self):
        return self._id

    def es_update_by_parameters(self, *args, **kwargs):
        for arg in args:
            if EasySerializable.is_wrapped_dict(arg):
                EasySerializable.es_update_by_dict(self, arg)
                return

        for arg in kwargs.values():
            if EasySerializable.is_wrapped_dict(arg):
                EasySerializable.es_update_by_dict(self, arg)
                return

    def es_update_by_dict(self, d, ignore_children=False):
        if not isinstance(d, dict):
            return
        for dk, dv in d.items():
            if dk not in constants.KEYWORDS_ES_ALL and (not ignore_children or dk != constants.FIELD_CHILDREN):
                self.__dict__[dk] = EasySerializable.es_load(dv)
                self._EasySerializable__dict_updated = True

    @staticmethod
    def es_load(d, cls=None, ignore_children=False):
        t = type(d)
        if t in utils.PRIMARY_SIMPLE_TYPES:
            return d
        if EasySerializable.is_wrapped_dict(d):
            class_name = d.get(constants.KEYWORD_CLASS_NAME)
            module_name = d.get(constants.KEYWORD_MODULE_NAME)
            froms = d.get(constants.KEYWORD_FROM_LIST)
            try:
                if len(froms) > 0:
                    module = __import__(froms[0])
                    if len(froms) > 1:
                        for sm in froms[1:]:
                            module = getattr(module, sm)

                    module = getattr(module, module_name)
                else:
                    module = __import__(module_name)
                class_ = getattr(module, class_name)
            except Exception as err:
                raise exceptions.FailedToLoadException('failed to load class froms = ', froms, ', module = ', module_name, ', class = ', class_name, '. exception is ', err)

            inst = class_()
            if isinstance(inst, EasySerializable):
                inst.es_update_by_dict(d, ignore_children)
            if isinstance(inst, ListTree):
                inst.lt_refresh()
            return inst
        if t in (list, tuple, set):
            dl = []
            for v in d:
                dl.append(EasySerializable.es_load(v, cls))

            if isinstance(d, list):
                return dl
            if isinstance(d, tuple):
                return tuple(dl)
            if isinstance(d, set):
                pass
            return set(dl)
        if isinstance(d, dict):
            dd = {}
            for k, v in d.items():
                dd[k] = EasySerializable.es_load(v, cls)

            return dd
        return d

    @staticmethod
    def dwi_build(*args, **kwargs):
        dwi = [[]]
        if len(args) > 0:
            dwi[0] = args[0]
        dwi[0] = kwargs.get(constants.KEYWORD_SKIPKEYS, dwi[0])
        return dwi

    @staticmethod
    def es_any_to_primary(arg):
        if arg is None:
            return
        t = type(arg)
        if t in utils.PRIMARY_SIMPLE_TYPES:
            return arg
        if isinstance(arg, EasySerializable):
            return arg.es_to_dict()
        if t in (list, tuple, set):
            vl = []
            for v in arg:
                vl.append(EasySerializable.es_any_to_primary(v))

            if isinstance(arg, list):
                return vl
            if isinstance(arg, tuple):
                return tuple(vl)
            if isinstance(arg, set):
                pass
            return set(vl)
        if isinstance(arg, dict):
            d = {}
            for k, v in arg.items():
                d[k] = EasySerializable.es_any_to_primary(v)

            return d

    def es_to_dict(self, deny_keys=[], allow_keys=[]):
        d = {constants.KEYWORD_CLASS_NAME: self._EasySerializable__class_name, 
         constants.KEYWORD_MODULE_NAME: self._EasySerializable__module_name, 
         constants.KEYWORD_FROM_LIST: self._EasySerializable__froms}
        dk = self._EasySerializable__dwi[0]
        if len(allow_keys) == 0 and len(deny_keys) > 0:
            dk = deny_keys
        for k, v in self.__dict__.items():
            if len(allow_keys) == 0 and k not in dk and k not in constants.DEFAULT_SKIPKEYS or len(allow_keys) > 0 and k in allow_keys:
                d[k] = EasySerializable.es_any_to_primary(v)

        return d

    def es_copy(self, ignore_children=False):
        return EasySerializable.es_load(self.es_to_dict(), ignore_children=ignore_children)

    @property
    def dwi(self):
        return self._EasySerializable__dwi

    def dwi_add_skipkeys(self, skipkeys):
        if isinstance(skipkeys, list):
            self._EasySerializable__dwi[0].extend(skipkeys)
        elif isinstance(skipkeys, str):
            self._EasySerializable__dwi[0].append(skipkeys)

    def dwi_remove_skipkeys(self, skipkeys):
        if isinstance(skipkeys, list):
            for s in skipkeys:
                try:
                    self._EasySerializable__dwi[0].remove(s)
                finally:
                    pass

        elif isinstance(skipkeys, str):
            try:
                self._EasySerializable__dwi[0].remove(skipkeys)
            finally:
                pass

    @property
    def es_dict_updated(self):
        return self._EasySerializable__dict_updated


class ListTree(object):

    def __init__(self, *args, **kwargs):
        self._ListTree__lt_parent_element = None
        self._ListTree__lt_children = []

    @property
    def lt_children(self):
        return self._ListTree__lt_children

    @property
    def lt_parent(self):
        return self._ListTree__lt_parent_element

    def lt_path(self):
        n = self
        l = []
        while isinstance(n, ListTree):
            p = n._ListTree__lt_parent_element
            if isinstance(p, ListTree):
                l.append(p._ListTree__lt_children.index(n))
            n = p

        l.reverse()
        return l

    def lt_root(self):
        r = self
        n = self._ListTree__lt_parent_element
        while isinstance(n, ListTree):
            r = n
            n = n._ListTree__lt_parent_element

        return r

    def child(self, path, default=None, separator='.'):
        p = path
        if isinstance(p, str):
            if p.find(separator) >= 0:
                p = p.split(separator)
            else:
                p = [
                 p]
            for i, v in enumerate(p):
                if v.isnumeric():
                    p[i] = int(v)
                else:
                    raise exceptions.IllegalArgumentException('invalid path : ' + path)

        if isinstance(p, tuple):
            p = list(p)
        if isinstance(p, list):
            n = self
            if len(p) == 0:
                return self
            for i, v in enumerate(p):
                if isinstance(n, ListTree):
                    if 0 <= v < len(n._ListTree__lt_children):
                        n = n._ListTree__lt_children[v]
                    else:
                        return default
                else:
                    return default

            if i == len(p) - 1:
                pass
            return n
        return default

    def lt_add_child(self, child):
        if isinstance(child, ListTree):
            if child in self._ListTree__lt_children:
                raise RuntimeError(constants.MSG_DUPLICATED)
            self._ListTree__lt_children.append(child)
            child._ListTree__lt_parent_element = self
        else:
            raise RuntimeError(constants.MSG_INVALID_TYPE)

    def lt_extend_children(self, children):
        if isinstance(children, list):
            for c in children:
                self.lt_add_child(c)

    def lt_remove(self, path=None, separator='.'):
        if path is None:
            child = self
        else:
            child = self.child(path, None, separator)
        if child is None or child._ListTree__lt_parent_element is None:
            return
        p = child._ListTree__lt_parent_element
        p._ListTree__lt_children.remove(child)

    def lt_insert_child(self, child, before=-1):
        if isinstance(child, tuple):
            child = list(child)
        if isinstance(child, list):
            for c in child:
                self.lt_insert_child(c, before)
                if before >= 0:
                    before += 1

            return
        if isinstance(child, ListTree):
            if before < 0 or before >= len(self._ListTree__lt_children):
                self.lt_add_child(child)
                return
            if child in self._ListTree__lt_children:
                raise exceptions.DuplicatedException(constants.MSG_DUPLICATED)
            child._ListTree__lt_parent_element = self
            self._ListTree__lt_children.insert(before, child)
        else:
            raise exceptions.IllegalArgumentException(constants.MSG_INVALID_TYPE)

    def lt_refresh(self):
        for n in self._ListTree__lt_children:
            if isinstance(n, ListTree):
                n._ListTree__lt_parent_element = self
                n.lt_refresh()

    @property
    def is_leaf(self):
        return len(self._ListTree__lt_children) == 0

    @property
    def is_root(self):
        return self._ListTree__lt_parent_element is None

    def get_all_leaves(self, reverse=False):
        leaves = []
        if reverse:
            l = self.lt_last_leaf()
        else:
            l = self.lt_first_leaf()
        while 1:
            leaves.append(l)
            if reverse:
                l = l.lt_prev_leaf()
            else:
                l = l.lt_next_leaf()
            if not isinstance(l, ListTree):
                break

        return leaves

    def lt_next(self, matcher=None, try_self=False):
        return self._ListTree__lt_next_inner(try_self=try_self, backward=False, matcher=matcher)

    def lt_prev(self, matcher=None, try_self=False):
        return self._ListTree__lt_next_inner(try_self=try_self, backward=True, matcher=matcher)

    def lt_first(self, matcher=None):
        if matcher is None:
            matcher = Matcher.leaf_matcher
        if not matcher(self) > 0:
            if len(self._ListTree__lt_children) > 0:
                return self._ListTree__lt_children[0].lt_first(matcher)
            else:
                return
        else:
            return self

    def lt_last(self, matcher=None):
        if matcher is None:
            matcher = Matcher.leaf_matcher
        if not matcher(self):
            if len(self._ListTree__lt_children) > 0:
                return self._ListTree__lt_children[(-1)].lt_last(matcher)
            else:
                return
        else:
            return self

    def __lt_next_inner(self, try_self=False, backward=False, matcher=None):
        if matcher is None:
            matcher = Matcher.leaf_matcher
        if try_self:
            if matcher(self):
                return self
            if backward:
                lt = self.lt_last(matcher)
            else:
                lt = self.lt_first(matcher)
            if lt is not None:
                pass
            return lt
        return self._ListTree__find_next(backward=backward, matcher=matcher)

    def __find_next(self, backward=False, matcher=None):
        if matcher is None:
            matcher = Matcher.leaf_matcher
        p = self._ListTree__lt_parent_element
        if isinstance(p, ListTree):
            i = p._ListTree__lt_children.index(self)
            if i < 0:
                raise exceptions.InternalErrorException('Fatal exception: element does not belongs to its parent')
            if backward:
                if i == 0:
                    return p._ListTree__lt_next_inner(try_self=False, backward=True, matcher=matcher)
                else:
                    return p._ListTree__lt_children[(i - 1)]._ListTree__lt_next_inner(try_self=True, backward=True, matcher=matcher)
            else:
                if i >= len(p._ListTree__lt_children) - 1:
                    return p._ListTree__lt_next_inner(try_self=False, backward=False, matcher=matcher)
                else:
                    return p._ListTree__lt_children[(i + 1)]._ListTree__lt_next_inner(try_self=True, backward=False, matcher=matcher)
        else:
            return

    def lt_first_leaf(self):
        if len(self._ListTree__lt_children) > 0:
            return self._ListTree__lt_children[0].lt_first_leaf()
        else:
            return self

    def lt_next_leaf(self):
        return self._ListTree__lt_next_leaf_inner(try_self=False, backward=False)

    def lt_last_leaf(self):
        if len(self._ListTree__lt_children) > 0:
            return self._ListTree__lt_children[(-1)].lt_last_leaf()
        else:
            return self

    def lt_prev_leaf(self):
        return self._ListTree__lt_next_leaf_inner(try_self=False, backward=True)

    def __lt_next_leaf_inner(self, try_self=False, backward=False):
        if try_self:
            if len(self._ListTree__lt_children) == 0:
                return self
            else:
                if backward:
                    return self.lt_last_leaf()
                return self.lt_first_leaf()
        else:
            return self._ListTree__find_next_in_parent(backward)

    def __find_next_in_parent(self, backward=False):
        p = self._ListTree__lt_parent_element
        if isinstance(p, ListTree):
            i = p._ListTree__lt_children.index(self)
            if i < 0:
                raise exceptions.InternalErrorException('Fatal exception: element does not belongs to its parent')
            if backward:
                if i == 0:
                    return p._ListTree__lt_next_leaf_inner(try_self=False, backward=True)
                else:
                    return p._ListTree__lt_children[(i - 1)]._ListTree__lt_next_leaf_inner(try_self=True, backward=True)
            else:
                if i >= len(p._ListTree__lt_children) - 1:
                    return p._ListTree__lt_next_leaf_inner(try_self=False, backward=False)
                else:
                    return p._ListTree__lt_children[(i + 1)]._ListTree__lt_next_leaf_inner(try_self=True, backward=False)
        else:
            return

    def lt_iterator(self, matcher=None):
        if matcher is None:
            matcher = Matcher.always_true_matcher
        start = self
        path = []
        while start is not None:
            if matcher(start):
                yield start
            if len(start._ListTree__lt_children) > 0:
                start = start._ListTree__lt_children[0]
                path.append(0)
            else:
                p = start
                while True:
                    if len(path) == 0:
                        start = None
                        break
                    p = p._ListTree__lt_parent_element
                    i = path[(-1)]
                    path.pop()
                    if i < len(p._ListTree__lt_children) - 1:
                        start = p._ListTree__lt_children[(i + 1)]
                        path.append(i + 1)
                        break

    def lt_copy(self, matcher=None, match_with=None, **kwargs):
        if matcher is None:
            matcher = Matcher.always_true_matcher
        if matcher is None or matcher(self, match_with, **kwargs):
            if len(self._ListTree__lt_children) == 0:
                if isinstance(self, EasySerializable):
                    return self.es_copy()
                else:
                    return copy.copy(self)
            else:
                if isinstance(self, EasySerializable):
                    lt = self.es_copy(ignore_children=True)
                else:
                    lt = copy.copy(self)
                if not isinstance(lt, ListTree):
                    raise exceptions.AppException('instance copied is not a ListTree')
                lt._ListTree__lt_children = []
                for i, v in enumerate(self._ListTree__lt_children):
                    m = None
                    if isinstance(match_with, ListTree):
                        if i < len(match_with._ListTree__lt_children):
                            m = match_with._ListTree__lt_children[i]
                    v1 = v.lt_copy(matcher, m, **kwargs)
                    if v1 is not None:
                        lt.lt_add_child(v1)

                return lt
        else:
            return


class Result(EasySerializable, ListTree):

    def __init__(self, copy_from=None, init_dict=None):
        self._Result__state = constants.MASK_RESULT_UNKNOWN
        self._Result__content = ''
        ListTree.__init__(self)
        EasySerializable.__init__(self, init_dict)
        if isinstance(copy_from, Invokable):
            self.copy_result(copy_from)

    def copy_result(self, invocable):
        if isinstance(invocable, Invokable):
            self._Result__state = invocable.result._Result__state
            self._Result__content = invocable.result._Result__content

    @property
    def state(self):
        if self._Result__state == constants.MASK_RESULT_UNKNOWN:
            children = self.lt_children
            if len(children) > 0:
                succ_count = 0
                current_state = constants.MASK_RESULT_UNKNOWN
                for i, r in enumerate(children):
                    if isinstance(r, Result):
                        if r.state == constants.MASK_RESULT_UNKNOWN:
                            return constants.MASK_RESULT_UNKNOWN
                        if r.state == constants.MASK_RESULT_SUCCESS:
                            succ_count += 1
                        elif r.state == constants.MASK_RESULT_PARTIAL_SUCCESS:
                            current_state = constants.MASK_RESULT_PARTIAL_SUCCESS

                if current_state == constants.MASK_RESULT_UNKNOWN:
                    if succ_count == len(children):
                        current_state = constants.MASK_RESULT_SUCCESS
                    else:
                        if succ_count == 0:
                            current_state = constants.MASK_RESULT_FAILED
                        else:
                            current_state = constants.MASK_RESULT_PARTIAL_SUCCESS
                        self._Result__state = current_state
                    return self._Result__state

    @state.setter
    def state(self, value):
        if len(self.lt_children) == 0:
            self._Result__state = value
        else:
            raise exceptions.IllegalOperationException('can not set state for a result belongs to parent task!')

    @property
    def all_content(self):
        c = []
        for r in self.lt_iterator():
            c.append(r.content)

        return c

    @property
    def content(self):
        return self._Result__content

    @content.setter
    def content(self, value):
        self._Result__content = value


class Parameter(EasySerializable):

    def __init__(self, parm_name='', parm_expression='', parm_variables={}, *args, **kwargs):
        self.name = ''
        self._Parameter__expression = ''
        self._Parameter__variables = {}
        self._Parameter__value = 0
        self._Parameter__value_settled = False
        EasySerializable.__init__(self, *args, **kwargs)
        if not self.es_dict_updated:
            self.name = parm_name
            self._Parameter__expression = parm_expression
            self._Parameter__variables = parm_variables
            if 'parm_value' in kwargs.keys():
                self._Parameter__value = kwargs.get('parm_value')
                self._Parameter__value_settled = True

    @property
    def value(self):
        if not self._Parameter__value_settled:
            raise RuntimeError('parameter value is currently not available!')
        return self._Parameter__value

    @value.setter
    def value(self, v):
        self._Parameter__value = v
        self._Parameter__value_settled = True

    @property
    def expression(self):
        return self._Parameter__expression

    @expression.setter
    def expression(self, v):
        self._Parameter__expression = v
        self._Parameter__value_settled = False

    @property
    def variables(self):
        return self._Parameter__variables

    @variables.setter
    def variables(self, v):
        self._Parameter__variables = v
        self._Parameter__value_settled = False

    @property
    def value_available(self):
        return self._Parameter__value_settled


class Target(EasySerializable, ListTree):

    def __init__(self, ip='', priority=1, name='', concurrency=0, init_list=[], init_dict={}):
        self.priority = 1
        self.ip = ''
        self.name = ''
        self.concurrency = 0
        ListTree.__init__(self)
        EasySerializable.__init__(self, init_dict)
        if not self.es_dict_updated:
            if len(init_list) > 0:
                self.lt_extend_children(init_list)
                self.priority = 1
                for t in self.lt_children:
                    if t.priority > self.priority:
                        self.priority = t.priority

        else:
            self.priority = priority
            self.ip = ip
            self.name = name
            self.concurrency = concurrency
        self.lt_refresh()

    def hosts(self):
        h = []
        for t in self.lt_children:
            if t.is_leaf():
                inserted = False
                for i, h1 in enumerate(h):
                    if t.priority > h1.priority:
                        h.insert(i, t)
                        inserted = True

                if not inserted:
                    h.append(t)

        return h

    def clusters(self):
        c = []
        for t in self.lt_children:
            if not t.is_leaf():
                c.append(t)

        return c

    def all_as_clusters(self):
        a = self.clusters()
        h = self.hosts()
        if len(h) > 0:
            t = Target(init_list=h)
            t.name = self.name
            t.concurrency = self.concurrency
            a.append(t)
        return a

    def filter_by_host_ips(self, ips, clone=False):
        if clone:
            d = self.es_to_dict()
            t = EasySerializable.es_load(d)
            if isinstance(t, Target):
                return t.filter_by_host_ips(ips, False)
        else:
            to_be_removed = []
            for t in self.lt_iterator():
                if len(t.ip) > 0 and t.ip not in ips:
                    to_be_removed.append(t)

            for t in to_be_removed:
                if isinstance(t, ListTree):
                    t.lt_remove()

            return self


class Event(dict):

    def __init__(self, source_tag=None, event_id='', data=None, init_dict=None):
        dict.__init__(self)
        if isinstance(init_dict, dict):
            for k, v in init_dict.items():
                self[k] = v

        else:
            self[constants.PARM_EVENT_ID] = event_id
            self[constants.PARM_EVENT_TAG] = source_tag
            self[constants.PARM_EVENT_DATA] = data

    @property
    def source_tag(self):
        return self.get(constants.PARM_EVENT_TAG, None)

    @source_tag.setter
    def source_tag(self, value):
        self[constants.PARM_EVENT_TAG] = value

    @property
    def event_id(self):
        return self.get(constants.PARM_EVENT_ID, '')

    @event_id.setter
    def event_id(self, value):
        self[constants.PARM_EVENT_ID] = value

    @property
    def data(self):
        return self.get(constants.PARM_EVENT_DATA, '')

    @data.setter
    def data(self, value):
        self[constants.PARM_EVENT_DATA] = value

    @property
    def is_command(self):
        return len(self.command) > 0

    @property
    def command(self):
        return self.get(constants.PARM_EVENT_CMD, '')

    @command.setter
    def command(self, value):
        self[constants.PARM_EVENT_CMD] = value


class Listener(object):

    @property
    def filters(self):
        return []

    def on_event(self, e, queue=''):
        pass

    @property
    def queue_suffix(self):
        return ''

    @property
    def callback_name(self):
        return ''


class EventFilter(object):

    def match(self, e):
        return False


class SimpleEventFilter(EventFilter):

    def __init__(self, topics=[], source_tags=[]):
        self._SimpleEventFilter__topics = []
        self._SimpleEventFilter__topics.extend(topics)
        self._SimpleEventFilter__source_tags = []
        self._SimpleEventFilter__source_tags.extend(source_tags)

    @property
    def topics(self):
        return self._SimpleEventFilter__topics

    @property
    def source_tags(self):
        return self._SimpleEventFilter__source_tags

    def match(self, e):
        if not isinstance(e, Event):
            return False
        if len(self._SimpleEventFilter__topics) > 0 and e.event_id not in self._SimpleEventFilter__topics:
            return False
        if len(self._SimpleEventFilter__source_tags) > 0 and e.source_tag not in self._SimpleEventFilter__source_tags:
            return False
        return True


class CommandProcessor(object):

    def on_command(self, cmd, **kwargs):
        pass


class Matcher(object):

    @staticmethod
    def always_true_matcher(o, *args, **kwargs):
        return True

    @staticmethod
    def leaf_matcher(lt, *args, **kwargs):
        if not isinstance(lt, ListTree):
            return False
        else:
            if len(lt.lt_children) > 0:
                return False
            return True