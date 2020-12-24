# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\base.py
# Compiled at: 2011-11-04 04:58:46


def is_subclass(sub, sup):
    try:
        if sup in sub.__bases__:
            return True
    except:
        return False
    else:
        for klass in sub.__bases__:
            if is_subclass(klass, sup):
                return True


class Parser:

    def parse(self, exp):
        try:
            exp_parse = exp.___parse___
        except:
            if isinstance(exp, list):
                return [ self.parse(e) for e in exp ]
            else:
                if isinstance(exp, tuple):
                    return tuple(self.parse(e) for e in exp)
                return exp

        try:
            return exp_parse(self)
        except TypeError:
            return exp


def preparse(exp):
    return Parser().parse(exp)


class LoopExitNextTagger:
    """ use tagger to preprocess before solve expression"""
    surfix = '$'

    def __init__(self):
        self.new_label_id = 1
        self.labels = {}

    def make_label(self, label):
        if label is None:
            label = '$' + str(self.new_label_id)
            self.new_label_id += 1
        return label

    def push_label(self, control_struct_type, label):
        self.labels.setdefault(control_struct_type, []).append(label)
        self.labels.setdefault(None, []).append(label)
        return

    def pop_label(self, control_struct_type):
        self.labels[control_struct_type].pop()
        self.labels[None].pop()
        return

    def tag_loop_label(self, exp):
        try:
            exp_tag_loop_label = exp.tag_loop_label
        except:
            if isinstance(exp, list):
                return [ self.tag_loop_label(e) for e in exp ]
            else:
                if isinstance(exp, tuple):
                    return tuple(self.tag_loop_label(e) for e in exp)
                return exp

        try:
            return exp_tag_loop_label(self)
        except TypeError:
            return exp


def tag_loop_label(exp):
    return LoopExitNextTagger().tag_loop_label(exp)


def dao_repr(exp):
    try:
        exp_____repr____ = exp.____repr____
    except:
        if isinstance(exp, list) or isinstance(exp, tuple):
            return (',').join([ dao_repr(e) for e in exp ])
        else:
            return repr(exp)

    try:
        return exp_____repr____()
    except TypeError:
        return repr(exp)


def apply_generators(generators):
    length = len(generators)
    if length == 0:
        yield True
        return
    if length == 1:
        for _ in generators[0]:
            yield True

        return
    i = 0
    while i < length:
        try:
            generators[i].next()
            if i == length - 1:
                yield True
                return
            i += 1
        except StopIteration:
            if i == 0:
                return
            i -= 1
        except GeneratorExit:
            raise


def unify(x, y, env, occurs_check=False):
    try:
        x_unify = x.unify
    except AttributeError:
        try:
            y_unify = y.unify
        except AttributeError:
            if (isinstance(x, list) or isinstance(x, tuple)) and (isinstance(y, list) or isinstance(y, tuple)):
                for _ in unify_list(x, y, env, occurs_check):
                    yield True

            if x == y:
                yield True
            return
        else:
            for _ in y_unify(x, env, occurs_check):
                yield True

        return
    else:
        for _ in x_unify(y, env, occurs_check):
            yield True


def unify_list(list1, list2, env, occurs_check=False):
    """unify list1 with list2 in env."""
    if len(list1) != len(list2):
        return
    for _ in apply_generators(tuple(unify(x, y, env, occurs_check) for (x, y) in zip(list1, list2))):
        yield True


def deref(x, env):
    try:
        x_deref = x.deref
    except AttributeError:
        if isinstance(x, list):
            return [ deref(e, env) for e in x ]
        else:
            if isinstance(x, tuple):
                return tuple(deref(e, env) for e in x)
            return x

    return x_deref(env)


def getvalue(x, env):
    try:
        x_getvalue = x.getvalue
    except AttributeError:
        if isinstance(x, list):
            return [ getvalue(e, env) for e in x ]
        else:
            if isinstance(x, tuple):
                return tuple(getvalue(e, env) for e in x)
            return x

    return x_getvalue(env)


def apply_generators_list(generators):
    length = len(generators)
    if length == 0:
        yield []
        return
    i = 0
    result = []
    while i < length:
        try:
            result.append(generators[i].next())
            if i == length - 1:
                yield result
                return
            i += 1
        except StopIteration:
            if i == 0:
                return
            i -= 1
        except GeneratorExit:
            raise


def peek_value(exp, env):
    try:
        exp_take_value = exp.peek_value
    except AttributeError:
        if isinstance(exp, list):
            return [ peek_value(e) for e in exp ]
        else:
            if isinstance(exp, tuple):
                return tuple(peek_value(e) for e in exp)
            return exp

    return exp_take_value(env)


def copy(exp, memo):
    try:
        exp_copy = exp.copy
    except AttributeError:
        if isinstance(exp, list):
            return [ getvalue(e, memo) for e in exp ]
        else:
            if isinstance(exp, tuple):
                return tuple(getvalue(e, memo) for e in exp)
            return exp

    return exp_copy(memo)


def copy_rule_head(arg_exp, env):
    try:
        arg_exp_copy_rule_head = arg_exp.copy_rule_head
    except AttributeError:
        if isinstance(arg_exp, list):
            return [ copy_rule_head(e, env) for e in arg_exp ]
        else:
            if isinstance(arg_exp, tuple):
                return tuple(copy_rule_head(e, env) for e in arg_exp)
            return arg_exp

    return arg_exp_copy_rule_head(env)


def match_list(list1, list2):
    if len(list1) != len(list2):
        return False
    for (x, y) in zip(list1, list2):
        if not match(x, y):
            return False

    return True


def match(x, y):
    try:
        x_match = x.match
    except AttributeError:
        if isinstance(x, list) or isinstance(x, tuple) or isinstance(y, list) and isinstance(y, tuple):
            return match_list(x, y)
        else:
            return x == y

    return x_match(y)


def contain_var(x, y):
    try:
        return x.contain_var(x, y)
    except:
        return False


def closure(exp, env):
    try:
        exp_closure = exp.closure
    except AttributeError:
        if isinstance(exp, list) or isinstance(exp, tuple):
            return tuple(closure(e, env) for e in exp)
        else:
            return exp

    return exp_closure(env)