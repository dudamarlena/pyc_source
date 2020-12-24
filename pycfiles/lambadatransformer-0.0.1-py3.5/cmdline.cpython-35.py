# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lambadalib/cmdline.py
# Compiled at: 2017-10-10 17:04:43
# Size of source mod 2**32: 1522 bytes
import argparse, imp, traceback
from lambadalib import lambada

def execute():
    parser = argparse.ArgumentParser(description='Lambada - Automated Deployment of Python Methods to the (Lambda) Cloud')
    parser.add_argument('modules', metavar='module', type=str, nargs='+', help='module file(s) to move to the cloud')
    parser.add_argument('--local', dest='local', action='store_const', const=True, default=False, help='only local conversion (default: remote deployment)')
    parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False, help='debugging mode (default: none)')
    parser.add_argument('--endpoint', metavar='ep', type=str, nargs='?', help='service endpoint when not using AWS Lambda but e.g. Snafu')
    parser.add_argument('--annotations', dest='annotations', action='store_const', const=True, default=False, help='only consider decorated functions')
    args = parser.parse_args()
    for module in args.modules:
        basemodule = module.replace('.py', '')
        lambada.printlambada('track module: {:s}'.format(basemodule))
        fileobj, filename, desc = imp.find_module(basemodule, ['.'])
        mod = imp.load_module(basemodule, fileobj, filename, desc)
        fileobj.close()
        try:
            lambada.move(mod.__dict__, local=args.local, module=filename, debug=args.debug, endpoint=args.endpoint, annotations=args.annotations)
        except Exception as e:
            print('Exception: {:s}'.format(str(e)))
            if args.debug:
                traceback.print_exc()
            return 1

    return 0