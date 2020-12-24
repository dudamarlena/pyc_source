# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/armor/validatorexc.py
# Compiled at: 2006-08-02 05:57:49
from inspect import getargspec
from harold.armor.basetypes import basetypes
from harold.lib import keys, make_annotated, ValidationError, DecorationError
validation_anno_template = '\ndef %(name)s%(signature)s:\n    %(docstring)r\n    return %(name)s.func_validation_anno%(values)s\n'

def add(names, *validators):
    """ decorator for annotating functions with validators

    @param names parameter name as string or tuple of names
    @param *validators one or more validators to associate with the parameter names
    @return decorator function that adds 'func_validators' attribute to decorated function
    """
    try:
        names + ''
        names = (names,)
    except (TypeError,):
        names = tuple(names)

    def add_deco(original):
        """ add_deco(original) -> decorate original with validator mapping

        @param original function to decorate with validators
        @return original with 'func_validators' list attribute
        """
        (args, varargs, varkw, defaults) = getargspec(original)
        for value in (varargs, varkw):
            if value is not None:
                args.append(varargs)

        for name in names:
            if name not in args:
                raise DecorationError('cannot validate missing argument')

        try:
            valmap = original.func_validators
        except (AttributeError,):
            valmap = original.func_validators = []

        try:
            valseq = valmap[valmap.index(names)]
        except (ValueError,):
            valseq = []
            valmap.append((names, valseq))

        valseq.extend([ basetypes.get(v, v) for v in validators ])
        return original

    return add_deco


def fuse(original):
    """ Decorator function to finalize the validator list and enforce calling them.

    @param original function previously decorated with the 'add' decorator
    @return replacement function that calls each validator before calling the original
    """
    get_validators(original)

    def enforcer_anno(*varparams, **keyparams):
        """ enforcer_anno(...) -> annotation called instead of (and before) original

        """
        (orignames, origvarargs, origvarkw, origdefaults) = getargspec(original)
        varparams = list(varparams)
        valid = {}
        invalid = {}
        for (vkeys, validators) in get_validators(original):
            (idxs, vals) = indexed_values(vkeys, orignames, varparams, keyparams)
            for vcall in validators:
                (vcargnames, vcvarargs, vcvarkw, vcdefaults) = getargspec(vcall)
                kwds = {}
                if keys.env in vcargnames or vcvarkw:
                    if keys.env in keyparams:
                        kwds[keys.env] = keyparams[keys.env]
                    elif keys.env in orignames:
                        kwds[keys.env] = varparams[orignames.index(keys.env)]
                try:
                    results = vcall(*vals, **kwds)
                    if len(vals) == 1:
                        results = (
                         results,)
                except (Exception,), exc:
                    for key in vkeys:
                        prepend_item(invalid, key, exc.args)

                else:
                    for (idx, val) in enumerate(results):
                        vals[idx] = val

                    for ((idx, name), res) in zip(idxs, results):
                        if idx is None:
                            keyparams[name] = res
                        else:
                            varparams[idx] = res
                        prepend_item(valid, name, results)

        if invalid:
            raise ValidationError(invalid, valid)
        return original(*varparams, **keyparams)

    replacement = make_annotated(original, validation_anno_template)
    replacement.func_validation_anno = enforcer_anno
    return replacement


def prepend_item(mapping, key, value):
    """ prepend_item(mapping, key, value) -> insert value at mapping[key][0]

    """
    try:
        mapping[key].insert(0, value)
    except (KeyError,):
        mapping[key] = [
         value]


def indexed_values(keys, names, paramseq, parammap):
    """ indexed_values(...) -> returns indexes and values for named keys

    """
    indexes = []
    values = []
    for key in keys:
        try:
            index = names.index(key)
            value = paramseq[index]
        except (ValueError,):
            index = None
            value = parammap[key]

        indexes.append((index, key))
        values.append(value)

    return (
     indexes, values)


def get_validators(func):
    """ get_validators(func) -> returns validator mapping on func

    """
    try:
        return func.func_validators
    except (AttributeError,):
        raise DecorationError('Function does not have validators')