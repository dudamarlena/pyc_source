# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/khorne/.virtualenvs/paramark/lib/python3.7/site-packages/pytest_paramark.py
# Compiled at: 2020-01-10 16:15:05
# Size of source mod 2**32: 3006 bytes
import sys
from collections import defaultdict
from _pytest import fixtures, mark, outcomes

@fixtures.fixture
def paramark(request):
    kwargs = {}
    for marker in request.node.iter_markers(request.fixturename):
        tmp = dict(**marker.kwargs)
        tmp.update(kwargs)
        kwargs = tmp

    return kwargs


class ParameterSet(mark.ParameterSet):

    @classmethod
    def _for_parametrize(cls, argnames, argvalues, func, config, function_definition):
        args, params = super()._for_parametrize(argnames, argvalues, func, config, function_definition)
        argnames = {}
        parameters = []
        for param in params:
            markargs = defaultdict(dict)
            values = []
            for name, value in zip(args, param.values):
                try:
                    prefix, name = name.split('.', 1)
                    if name == '*':
                        if not isinstance(value, dict):
                            raise TypeError('{nodeid}: in "parametrize", when using "{prefix}.*" as the name, corresponding value must be a dictionary'.format(nodeid=(function_definition.nodeid),
                              prefix=prefix))
                        (markargs[prefix].update)(**value)
                    else:
                        markargs[prefix][name] = value
                except ValueError:
                    argnames[name] = None
                    values.append(value)

            marks = [mark.Mark(name=k, args=(), kwargs=v) for k, v in markargs.items()]
            parameters.append(cls(values=values, marks=(list(param.marks) + marks), id=(param.id)))

        return (argnames.keys(), parameters)


def pytest_fixture_setup(fixturedef, request):
    """ Execution of fixture setup. """
    kwargs = {}
    for argname in fixturedef.argnames:
        fixdef = request._get_active_fixturedef(argname)
        if argname == 'paramark':
            paramarkfunc = fixtures.resolve_fixture_function(fixdef, request)
            kwargs[argname] = fixtures.call_fixture_func(paramarkfunc, request, dict(request=request))
        else:
            result, arg_cache_key, exc = fixdef.cached_result
            request._check_scope(argname, request.scope, fixdef.scope)
            kwargs[argname] = result

    fixturefunc = fixtures.resolve_fixture_function(fixturedef, request)
    my_cache_key = request.param_index
    try:
        result = fixtures.call_fixture_func(fixturefunc, request, kwargs)
    except outcomes.TEST_OUTCOME:
        fixturedef.cached_result = (
         None, my_cache_key, sys.exc_info())
        raise

    fixturedef.cached_result = (
     result, my_cache_key, None)
    return result


def pytest_configure(config):
    mark.ParameterSet = ParameterSet