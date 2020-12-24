# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/processing.py
# Compiled at: 2010-10-14 14:04:21
__doc__ = '\nprocessing\n\nProcessing procblock blocks.  This is where the magic happens!\n'
import Queue, re, os, logging, procyaml, builtins
from unidist.log import log
PROCESSING_DEFAULT_TAGS = None
CONDITIION_DEFAULT_TAGS = None

class DoNotSaveTag(Exception):
    """Do not save tags that have this exception thrown.  They are not meant
  to be returned as data, they operate in the shadows."""


class UpdateBlockData(Exception):
    """Update the block data of the parent block with the target data."""

    def __init__(self, data):
        self.data = data


def LoadDefaultTagFunctions():
    """Load the default Tag Functions."""
    path = os.path.join(os.path.dirname(__file__), 'data', 'default_tag_functions.yaml')
    functions = procyaml.ImportYaml(path)
    return functions


def LoadDefaultConditionFunctions():
    """Load the default Condition Functions."""
    path = os.path.join(os.path.dirname(__file__), 'data', 'default_condition_functions.yaml')
    functions = procyaml.ImportYaml(path)
    return functions


def Init_ReEntrant():
    """Initialize our Default Tag Functions."""
    global CONDITIION_DEFAULT_TAGS
    global PROCESSING_DEFAULT_TAGS
    if PROCESSING_DEFAULT_TAGS == None:
        PROCESSING_DEFAULT_TAGS = {}
        PROCESSING_DEFAULT_TAGS.update(LoadDefaultTagFunctions())
    if CONDITIION_DEFAULT_TAGS == None:
        CONDITIION_DEFAULT_TAGS = {}
        CONDITIION_DEFAULT_TAGS.update(LoadDefaultConditionFunctions())
    return


def AddTagFunction(tag_name, tag_function_block):
    """Add a Tag Functions to our defaults."""
    PROCESSING_DEFAULT_TAGS[tag_name] = tag_function_block


def GetDefaultTagFunctionBlock(tag):
    if tag in PROCESSING_DEFAULT_TAGS:
        return PROCESSING_DEFAULT_TAGS[tag]
    else:
        for tag_function in PROCESSING_DEFAULT_TAGS:
            tag_search = tag_function
            regex = '^(%s)$' % tag_search
            found_list = re.findall(regex, tag)
            if found_list:
                return PROCESSING_DEFAULT_TAGS[tag_function]

        return


def Process(pipe_data, block, request_state, input_data, tag=None, cwd=None, env=None, block_parent=None):
    """Process this block.  This is where the magic happens!
  
  Args:
    data: dict, used as input
    state: dict, used as long running shared state, another kind of input.
    chain_output: dict, like state, but for a pipeline or chain of
        Process() calls.  chain_output is a dictionary that is updated()d at
        with the result of this function.
    env: dict (optional), if executing shell commands, all keys are set
        to the str() of their values in the shell environment.
    block_parent: dict (optional), if we know and want to pass along the parent,
        do it this way to avoid another piece of data to keep track of, as
        a given piece of data could think of parents in different ways.
  """
    if type(block) in (dict,):
        block = dict(block)
    Init_ReEntrant()
    tags = []
    for key in block:
        tags.append(key)

    tags.sort()
    prioritized_tags = Queue.PriorityQueue()
    for tag in tags:
        priority = 500
        tag_function_block = GetDefaultTagFunctionBlock(tag)
        if type(block[tag]) == type({}) and '__priority' in block[tag]:
            priority = int(block[tag]['__priority'])
        elif tag_function_block and '__priority' in tag_function_block:
            priority = tag_function_block['__priority']
        prioritized_tags.put((priority, tag))

    prioritized_list = []
    done = False
    while not done:
        try:
            (priority, tag) = prioritized_tags.get_nowait()
            prioritized_list.append((priority, tag))
        except Queue.Empty, e:
            done = True

    new_block = {}
    for (priority, tag) in prioritized_list:
        tag_function_block = GetDefaultTagFunctionBlock(tag)
        if tag_function_block:
            if '__builtin' in tag_function_block:
                function = builtins.GetFunctionByName(tag_function_block['__builtin'])
                if function == None:
                    raise Exception('Found tag function, but returned None: %s' % tag_function_block['__builtin'])
            else:
                raise Exception('No __builtin specified for Tag Function: %s' % tag)
            try:
                out_block = function(pipe_data, block[tag], request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block)
                new_block[tag] = out_block
            except DoNotSaveTag, e:
                pass
            except UpdateBlockData, e:
                new_block.update(e.data)

        elif type(block[tag]) == type({}):
            try:
                out_block = Process(pipe_data, block[tag], request_state, input_data, tag=tag, cwd=cwd, env=env, block_parent=block)
                new_block[tag] = out_block
            except DoNotSaveTag, e:
                pass
            except UpdateBlockData, e:
                print 'UpdateBlockData: %s: %s' % (tag, e.data)
                new_block.update(e.data)

        else:
            new_block[tag] = block[tag]

    if '__return_tag' in new_block:
        result = new_block.get(new_block['__return_tag'], None)
    else:
        result = new_block
    for key in result.keys():
        if key.startswith('__'):
            del result[key]

    return result