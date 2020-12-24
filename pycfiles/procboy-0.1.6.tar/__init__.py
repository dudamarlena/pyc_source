# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/procblock/__init__.py
# Compiled at: 2010-10-14 14:04:21
__doc__ = '\nprocblock\n\nby Geoff Howland\n\n\nprocblock is a Data Based Logic Structure.\n\nprocblock intentionally blurs the line between data and code.  Use procblock\nlightly for flow control, or heavily as the framework for your applications\nand systems.  procblock includes many tools to decrease the amount of code\nyou need to write, by using powerful distributed system mechanisms to allow\na tiny bit of custom code to interact in a way normally reserved for\nenterprise level applications.  Enterprise level applications, which already\nhandle distributed problems themselves, can use procblock as a way to create\nlightweight interfaces with operating system oriented tasks, which change too\nfrequently to warrant re-designing the enterprise level application code base.\n\nIt is a not a programming language, though it could be useful to treat it that\nway at times, as it is a software development tool.  procblock uses hierarchical\ndata structures (Python dictionaries and lists) to sturcture data which can be\nprocessed through a series of rules and scripts.  A basic set of functions is\nprovided to conditionally return data, or run scripts, but from this much\nricher functionality can be created by programmers using this structure to\ncreate simpler custom logic to perform their specific intensions.\n\nprocblock is a Hardened Execution Environment.\n\nIt runs code with a common interface, and can run shell commands.  It can\nrun code in serial, simultaneously in threads, or caching while periodically\nrunning in threads.  Many controls can be applied to running code and commands\ndue to procblock being dedicated to servicing logic, but only providing\nminimal logic.\n\nprocblock intends to facilitate simpler programming and design,\nand tries to provide structure which lends to simpler pieces of code being\nconnected together through procblock.\n\nprocblock was built to facilitate Pipe Oriented Design programming.\n\nUnix shells have provided Pipe based programming for decades, and it\'s power\nis undeniable in being able to stream output from one program as input to\nanother program.  Through a common interface, procblock executes scripts\nand shell commands in a manner similar to pipes, but works with Python\ndictionaries instead of character streams.\n\nprocblock provides Aspect Oriented Design.\n\nDue to procblock\'s Pipe Oriented Design, Aspects are possible by inspecting\npipe data and modifying it, at any point in the pipeline.  By providing Flow\nBlocks overrides, a programmer can add Aspect logic at any or every stage\nof the execution pipeline.  This differentiates it from many frameworks which\nrequire new code to fit into an existing object model.  Create your own object\nmodel, procblock does not need to know or care.\n\nprocblock is Object Oriented Design agnostic.\n\nIt neither promotes or prevents working with Object Orientation, and so can\nbe used by heavy OO advocates, even though it is was not itself created with\na heavy OO orientation.\n\nprocblock provides long running and shared state.\n\nShare state between sessions or over many executions of scripts, procblock\nstays running and keeps a global state, which can be passed to different\nscripts for sharing state, or providing input.  Use this for storing HTTP\nsession information, caching requests, resource locking or any other purpose.\nState is a modified Python dictionary which provides thread safety on setting\nkeys for the top level of your state dictionary.  Optionally, all Python\ndictionaries that procblock creates or converts are turned into thread safe\ndictionaries.  (TODO(g): Add option to specify this.)\n\nprocblock is designed as a message and queueing system.\n\nAny block tagged to be delivered to a previously registered listening block\nwill be delivered to a queue, which can be processed at the programmer\'s\nleisure.  Many listeners can receive the same message, and code can be added\nto remotely pass those messages to networked nodes which can procress the\nblock or result.  Shared state is useful for some activities, and message\npassing is useful for a different set of activities, providing more coverage\nbetween your simpler scripts and logic.\n\nprocblock can be used an a main() or library, or both.\n\nBecause procblock can run long running code or simultaneous threads, it can\nbe used as run control and glue for long running programs or daemons.  Because\nprocblock can be imported as a library and pass in any Python dictionary\nformat data, it can be used as a lightweight logic processer.\n\nprocblock is extendable.\n\nAdd your own Tag Functions, and any data you give that tag will be processed by\nyour Tag Function (just another block itself).\n\nprocblock can be a cross-language logic processor.\n\nI\'m not going to do it, but port the procblock engine to your favorite language.\nSince procblock works on data primitives (Python dictionaries, lists and\nstrings), it is transferable to any other language which either has these\nnatively or uses libraries to acquire them.  Besides natively running Python\nscripts, instead of your desired language, nothing about procblock is specific\nto Python.  Your "scripts" may be Java classes you create instead of Python\nmodules with Execute() functions, but that is just the final implementation\nstep of procblock, not the core of what makes procblock useful.\n\nprocblock is a conditional data storage system.\n\nWhen trying to retrieve data, where some data should be conditionally based\non a check against input or state information, procblock formatted data can be\nused to reduce custom code and retrieve the conditional data.  Useful for\nrequest configuration, where different configuration information will be\nprovided based on input state (like a HTTP Host Header returning a different\nHTTP server configuration block).\n\nprocblock processes things recursively.\n\nWith the exception of some built-in (but overridable) functions, procblock\nprocesses data blocks using other procblock formatted data blocks.  Even the\nstandard procblock Tag Functions are really just default Custom Tag Functions\nthat use the underlaying built-in functions, but process their tagged blocked\nthe same way you might create your own Tag Function.\n\nYou don\'t have to understand procblock to use procblock.\n\nGrokking all the mechanisms of what makes procblock work, or how to overload it\nand add your own Tag Functions is not necessary to use procblock effectively.\nprocblock is designed to be used by either careful construction of logic and\ndata flow, or casually placing data in a hierarchy and processing it to see\nthe result.  Both ways are effective, and while I don\'t encourage random\nattempts to create solid logic, it can be useful to prototype and play with\nan idea, and procblock tries to facilitate this easy and compact way to\nhierarchically layer and play with the structure of both data and logic.\n\n\n#TODO(g): Load ".procblock.yaml" for default procblock options.  Can easily\n#   create development and production environments this way.  Cool.\n\n#TODO(g): ALlow procblock to execute a procblock python file from the command\n#   line the same way it would launch a YAML procblock.  This way there is\n#   truly no difference between them.  Code or YAML is the same to procblock.\n#     Benefits?\n'
import sys, os, processing, procyaml, mainfunctions, run

def Main():
    """Execute to process command line options and arguments to run a block.
  
  Uses __usage tag in block, if available, otherwise does default processing
  of options and passes args raw and in order.
  """
    request_state = {}
    pipe_data = {}
    if len(sys.argv) >= 2:
        if sys.argv[1] not in ('-h', '--help'):
            yaml_import = sys.argv[1]
        else:
            print 'error: no procblock YAML file was specified'
            print 'usage: %s <procblock.yaml|procblock.py> <options> <args>' % os.path.basename(sys.argv[0])
            sys.exit(1)
        if not yaml_import.endswith('.py'):
            block = dict(procyaml.ImportYaml(yaml_import))
            code = False
        else:
            block = {}
            code = True
            code_block = run.code_python.GetPythonScriptModule(yaml_import)
        try:
            if 'data' in block:
                input_data = dict(block['data'])
            else:
                input_data = {}
            options_and_args = mainfunctions.ProcessOptionsAndArgs(block)
            input_data.update(options_and_args)
            if '__usage' in block:
                usage = block['__usage']
                del block['__usage']
            else:
                usage = None
            if input_data:
                pipe_data.update(input_data)
            output = mainfunctions.PrintStartup(block)
        except mainfunctions.OptionsAndArgsFailure, e:
            output = mainfunctions.PrintUsage(block, error=e)
            print output
            sys.exit(1)
        else:
            code or mainfunctions.ProcessAndLoop(usage, block, input_data, request_state, pipe_data)
    else:
        result = code_block.ProcessBlock(pipe_data, usage, {}, input_data, tag=None, cwd=None, env=None, block_parent=None)
        import pprint
        pprint.pprint(result)
    return


if __name__ == '__main__':
    Main()