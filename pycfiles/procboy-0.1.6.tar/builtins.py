# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/builtins.py
# Compiled at: 2010-10-14 14:04:21
__doc__ = '\nbuiltins\n\nprocblock built-in functions.\n\nThese are the foundational functions required to process our conditions,\nstate setting, message passing, thread management and code and script execution.\n'
from unidist.log import log
import logging
from run import running
import processing
from unidist import messagequeue
from unidist import sharedlock
from unidist import dotinspect
WORKER_THREAD_MINIMUM_DEFAULT = 5
WORKER_THREAD_MAXIMUM_DEFAULT = 20

def GetFunctionByName(name):
    """Return the built-in function, by it's name."""
    FUNCTIONS = {'Set': Set, 
       'RunBlock': RunBlock, 
       'RunSimultaneousBlock': RunSimultaneousBlock, 
       'RunSimultaneousWorkerThreadsBlock': RunSimultaneousWorkerThreadsBlock, 
       'ConditionIf': ConditionIf, 
       'Conditions': Conditions, 
       'Template': Template, 
       'Control_PutTagResultInQueue': Control_PutTagResultInQueue, 
       'Control_PreProcessLockAcquire': Control_PreProcessLockAcquire, 
       'Control_FinalProcessLockRelease': Control_FinalProcessLockRelease, 
       'List_Add': List_Add, 
       'List_Remove': List_Remove, 
       'EqualTo': EqualTo, 
       'GreaterThan': GreaterThan, 
       'LessThan': LessThan, 
       'GreaterThanOrEqualTo': GreaterThanOrEqualTo, 
       'LessThanOrEqualTo': LessThanOrEqualTo, 
       'NotEqualTo': NotEqualTo, 
       'InSet': InSet, 
       'NotInSet': NotInSet, 
       'SetIsEmpty': SetIsEmpty, 
       'SetIsNotEmpty': SetIsNotEmpty, 
       'SetHas': SetHas, 
       'SetHasNo': SetHasNo}
    function = FUNCTIONS.get(name, None)
    if function == None:
        raise Exception('Function not found: %s' % name)
    return function


def Set(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """"Set a pipe_data variable.  Format:  set <variable name>: <data>"""
    add_to = tag.split(' ')[(-1)]
    if add_to in pipe_data:
        pipe_data[add_to] = block
    return block


def RunBlock(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Run this block of functions serially."""
    output = running.RunScriptBlock(pipe_data, block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent)
    return output


def RunSimultaneousBlock(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Run this block of functions in their own control threads.
  
  Returns: dict of RunThread objects, keyed on name
  """
    thread_handler = running.RunThreadHandler()
    pipe_data['_thread_handler'] = thread_handler
    threads = {}
    for key in block:
        run_block = block[key]
        run_thread = running.RunThread(thread_handler.GetNextRunThreadId(), pipe_data, run_block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block)
        threads[key] = run_thread
        run_thread.start()

    return threads


def RunSimultaneousWorkerThreadsBlock(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Run this block of functions in their own worker control threads.
  
  Keeps a minimum of worker threads, and up to the maximum, so that work can be
  handled simultaneously, and by a number of threads at once.  Provides more
  flexibility for running code.
  
  Returns: dict of RunThread objects, keyed on name
  """
    thread_handler = running.RunThreadHandler()
    pipe_data['_thread_handler'] = thread_handler
    threads = {}
    for key in block:
        run_block = block[key]
        minimum = pipe_data.get('minimum', WORKER_THREAD_MINIMUM_DEFAULT)
        maximum = pipe_data.get('maximum', WORKER_THREAD_MAXIMUM_DEFAULT)
        for count in range(0, maximum):
            thread_data = dict(pipe_data)
            log('Worker: %s: %s' % (key, pipe_data))
            thread_data['__worker_id'] = count
            thread_data['__worker_name'] = '%s_%s' % (key, count)
            run_thread = running.RunThread(thread_handler.GetNextRunThreadId(), thread_data, run_block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block)
            threads[key] = run_thread
            run_thread.start()

    return threads


def _ParseConditionTag(tag, inspect_data):
    data = {}
    chunks = tag.split(' ')
    data['condition'] = chunks[0]
    data['operator'] = chunks[2]
    data['left'] = dotinspect.Inspect(chunks[1], inspect_data)
    text = (' ').join(chunks[3:])
    data['right'] = dotinspect.Inspect(text, inspect_data)
    return data


def _ConditionTest(left, operator, right):
    processing.Init_ReEntrant()
    operator_function = processing.CONDITIION_DEFAULT_TAGS[operator]['compare']
    function = GetFunctionByName(operator_function)
    success = function(left, right)
    if success:
        return True
    else:
        return False


def ConditionIf(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """If conditional statement."""
    condition = _ParseConditionTag(tag, pipe_data)
    left = condition['left']
    right = condition['right']
    remove_else = False
    if left != None and _ConditionTest(left, condition['operator'], right):
        if 'else' in block:
            block = dict(block)
            del block['else']
    elif 'else' in block:
        block = block['else']
    else:
        raise processing.DoNotSaveTag('If')
    result = processing.Process(pipe_data, block, request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block_parent)
    raise processing.UpdateBlockData(result)
    return


def Conditions(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Ordered list of if/elif/else.
  
  ##NOTE(g): Not currently in use!  :P   Broken.
  
  Otherwise elif will not be ordered.  (TODO(g): Add priority to elif to fix.)
  """
    new_if = True
    if_scan = False
    elif_scan = False
    for item in block:
        style = item.keys()[0].split(' ', 1)[0]
        if style == 'if':
            new_if = True
            if_scan = False
            elif_scan = False
        result = processing.Process(item)

    return pipe_data


def _PopulateTemplate(text, data):
    """Use data keys to populate data."""
    for key in data:
        var = '%%(%s)s' % key
        if var in text:
            text = text.replace(var, str(data[key]))

    return text


def Template(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Use __output (if set) or block data and fill out template and store in
      __output Copy __output to __output_raw first.
  """
    fp = open(block['path'])
    path_text = fp.read()
    fp.close()
    output = _PopulateTemplate(path_text, pipe_data)
    return output


def Control_PutTagResultInQueue(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Puts the appropriate message in the message queue."""
    for item in block:
        tag_data = block_parent.get(item['tag'], None)
        messagequeue.AddMessage(item['queue'], tag_data)

    if '__control_PutTagResultInQueue' in block_parent:
        del block_parent['__control_PutTagResultInQueue']
    return


def Control_PreProcessLockAcquire(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    sharedlock.Acquire(block['name'], block.get('timeout', None))
    return


def Control_FinalProcessLockRelease(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    sharedlock.Release(block['name'])


def List_Add(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Add this to a list."""
    add_to = tag.split(' ')[(-1)]
    if add_to in pipe_data:
        pipe_data[add_to].append(block)
    raise processing.DoNotSaveTag('List_Add')


def List_Remove(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Remove this from a list."""
    log('LIST REMOVE: %s' % block)
    block_parent['list_remove'] = tag
    raise processing.DoNotSaveTag('List_Add')


def GetBlockOutput(block):
    if '__output' in block:
        return block['__output']
    else:
        return block


def EqualTo(left, right):
    return left == right


def GreaterThan(left, right):
    return left > right


def LessThan(left, right):
    return left < right


def GreaterThanOrEqualTo(left, right):
    return left >= right


def LessThanOrEqualTo(left, right):
    return left <= right


def NotEqualTo(left, right):
    return left != right


def InSet(left, right):
    return right in left


def NotInSet(left, right):
    return right not in left


def SetIsEmpty(left, right):
    return len(left) == 0


def SetIsNotEmpty(left, right):
    return len(left) > 0


def SetHas(left, right):
    return right in left


def SetHasNo(left, right):
    return right not in left