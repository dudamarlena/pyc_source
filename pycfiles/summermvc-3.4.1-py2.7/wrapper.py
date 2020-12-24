# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/wrapper.py
# Compiled at: 2018-05-30 07:41:17
__all__ = [
 'wrapper']
__authors__ = ['Tim Chow']
from functools import wraps
import inspect, sys, types
from .joint_point import JointPoint
from .exception import Return, InvalidAdviceUsageError

def wrapper(before_advices, around_advices, after_returning_advices, after_throwing_advices, after_advices):

    def _inner(f):

        @wraps(f)
        def _innest(*a, **kw):
            jp = JointPoint(f, a, kw)
            for before_advice in before_advices:
                formal_arguments = inspect.getargspec(before_advice).args
                try:
                    if 'joint_point' in formal_arguments:
                        before_advice(joint_point=jp)
                    else:
                        before_advice()
                except Return as e:
                    return e.get_return_value()

            new_around_advices = []
            for around_advice in around_advices:
                formal_arguments = inspect.getargspec(around_advice).args
                try:
                    if 'joint_point' in formal_arguments:
                        result = around_advice(joint_point=jp)
                    else:
                        result = around_advice()
                    if isinstance(result, types.GeneratorType):
                        try:
                            result.next()
                            new_around_advices.append(result)
                        except StopIteration:
                            pass

                except Return as e:
                    return e.get_return_value()

            uuid = object()
            returning = uuid
            exc_info = None
            try:
                returning = jp.proceed()
            except:
                exc_info = sys.exc_info()

            for around_advice in new_around_advices:
                try:
                    if exc_info is not None:
                        around_advice.throw(*exc_info)
                    else:
                        around_advice.send(returning)
                except StopIteration:
                    pass
                except Return as e:
                    return e.get_return_value()

            if returning is uuid:
                raise InvalidAdviceUsageError('if around adive catched the exception, it must return value by raise Return exception, or raise another exception.')
            if exc_info is None:
                for after_returning_advice in after_returning_advices:
                    formal_arguments = inspect.getargspec(after_returning_advice).args
                    kwargs = {}
                    if 'joint_point' in formal_arguments:
                        kwargs['joint_point'] = jp
                    if 'returning' in formal_arguments:
                        kwargs['returning'] = returning
                    try:
                        after_returning_advice(**kwargs)
                    except Return as e:
                        return e.get_return_value()

            else:
                for after_throwing_advice in after_throwing_advices:
                    formal_arguments = inspect.getargspec(after_throwing_advice).args
                    kwargs = {}
                    if 'joint_point' in formal_arguments:
                        kwargs['joint_point'] = jp
                    if 'exc_info' in formal_arguments:
                        kwargs['exc_info'] = exc_info
                    try:
                        after_throwing_advice(**kwargs)
                    except Return as e:
                        return e.get_return_value()

                for after_advice in after_advices:
                    formal_arguments = inspect.getargspec(after_advice).args
                    kwargs = {}
                    if 'joint_point' in formal_arguments:
                        kwargs['joint_point'] = jp
                    if 'returning' in formal_arguments:
                        kwargs['returning'] = None
                        if exc_info is None:
                            kwargs['returning'] = returning
                    if 'exc_info' in formal_arguments:
                        kwargs['exc_info'] = exc_info
                    try:
                        after_advice(**kwargs)
                    except Return as e:
                        return e.get_return_value()

            return returning

        return _innest

    return _inner