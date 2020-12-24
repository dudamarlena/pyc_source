# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_functest/bin.py
# Compiled at: 2011-01-13 01:48:00
import global_settings, sys
usage = "functest test framework.\n    functest [options] [test1.py] [test2.py] [filter=test]\n    \nAvailable Options:\n    (help, --help)  Print this help menu. \n    (pdb, --pdb)  Stop on failure and enter pdb debugger.\n    (nowrap, --nowrap)  Don't wrap output to print at end of test run for both stdout and stderr. \n        Allows output from tests as they run.\n    (stdout, --stdout)  Don't wrap stdout.\n    (stderr, --stderr)  Don't wrap stderr.\n    (bigtb, --bigtb)  Only available if pygments is installed. \n        This prints a much larger traceback, with the preceeding 4 lines of code in each line of the traceback.\n    (filter=)  Only run tests where the name contains this filter."

def main(test_args):
    from windmill.dep import functest
    functest.run_framework(test_args)


def process_args():
    from windmill.dep import functest
    functest.configure()
    functest.registry['functest_cli'] = True
    args = list(sys.argv)
    if args[0].endswith('functest') or args[0].endswith('functest.py') or args[0].endswith('functest.exe'):
        args.pop(0)

    def set_pdb(x):
        global_settings.pdb = True
        global_settings.wrap_stdout = False

    def set_nowrap(x):
        global_settings.wrap_stdout = False
        global_settings.wrap_stderr = False

    def set_stdout(x):
        global_settings.wrap_stdout = False

    def set_stdout(x):
        global_settings.wrap_stderr = False

    def set_bigtb(x):
        global_settings.bigtb = True

    def set_filter(x):
        global_settings.test_filter = x

    def set_help(x):
        print usage
        sys.exit()

    builtin_options = dict([ (k.replace('set_', ''), v) for (k, v) in locals().items() if k.startswith('set_') ])
    options = [ x.replace('--', '') for x in args ]
    for option in options:
        if option.find('=') is not -1:
            (key, value) = option.split('=')
        else:
            key = option
            value = None
        if key in builtin_options.keys():
            builtin_options[key](value)
        elif value is not None:
            functest.registry[key] = value
        else:
            functest.modules_passed.append(option)

    return functest.modules_passed


def cli():
    main(process_args())