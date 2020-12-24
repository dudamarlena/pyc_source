# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/tasks.py
# Compiled at: 2010-05-30 13:30:03
from decorator import decorator
from pysutils import tolist, OrderedDict
from pysmvt.utils import gather_objects

def _attributes(f, *args, **kwargs):
    """
        does the work of calling the function decorated by `attributes`
    """
    return f(*args, **kwargs)


def attributes(*args):
    """
        a decorator to add an "attribute" to an action, which can be used
        as a filtering mechanism to control what actions in given task are run.
        If we have the following in tasks.init_data:
        
            @attributes('test', 'dev')
            def action_020_a_little_data():
                pass
            
            @attributes('prod')
            def action_020_a_lot_of_data():
                pass
            
        Given the above, then:
            
            run_tasks('init-data') # both functions called
            run_tasks('init-data:prod') # only action_020_a_lot_of_data
            run_tasks('init-data:test') # only action_020_a_little_data
            run_tasks('init-data:dev') # only action_020_a_little_data
            run_tasks('init-data:foo') # neither function called
        
    """

    def decorate_func(f):
        if args:
            f.__pysmvt_task_attrs = args
        return decorator(_attributes, f)

    return decorate_func


def run_tasks(tasks, print_call=True, test_only=False, *args, **kwargs):
    tasks = tolist(tasks)
    retval = OrderedDict()
    for task in tasks:
        if ':' in task:
            (task, attr) = task.split(':', 1)
            if attr.startswith('~'):
                soft_attribute_matching = True
                attr = attr[1:]
            else:
                soft_attribute_matching = False
        else:
            attr = None
        underscore_task = task.replace('-', '_')
        modlist = gather_objects('tasks.%s' % underscore_task)
        callables = []
        for modobjs in modlist:
            for (k, v) in modobjs.iteritems():
                if k.startswith('action_'):
                    plus_exit = False
                    callable_attrs = getattr(v, '__pysmvt_task_attrs', tuple())
                    for cattr in callable_attrs:
                        if cattr.startswith('+') and cattr[1:] != attr:
                            plus_exit = True
                            break

                    if plus_exit:
                        continue
                    if attr is not None:
                        if soft_attribute_matching:
                            if '-' + attr in callable_attrs:
                                continue
                        elif attr not in callable_attrs and '+' + attr not in callable_attrs:
                            continue
                    callables.append((k, modobjs['__name__'], v, None))

        retval[task] = []
        for call_tuple in sorted(callables):
            if print_call == True:
                print '--- Calling: %s:%s ---' % (call_tuple[1], call_tuple[0])
            if test_only:
                callable_retval = 'test_only=True'
            else:
                callable_retval = call_tuple[2]()
            retval[task].append((
             call_tuple[0],
             call_tuple[1],
             callable_retval))

    if print_call and test_only:
        print '*** NOTICE: test_only=True, no actions called ***'
    return retval