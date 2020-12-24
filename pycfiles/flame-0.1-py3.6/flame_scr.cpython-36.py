# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/flame_scr.py
# Compiled at: 2018-06-21 06:50:39
# Size of source mod 2**32: 4474 bytes
import argparse
from flame.util import utils
import flame.context as context, flame.manage as manage

def sensitivity(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tp / (tp + fn)


def specificity(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn / (tn + fp)


def manage_cmd(args):
    """
    Instantiates a Build object to build a model using the given input
    file (training series) and model (name of endpoint, eg. 'CACO2')
    """
    version = utils.intver(args.version)
    if args.action == 'new':
        success, results = manage.action_new(args.endpoint)
    else:
        if args.action == 'kill':
            success, results = manage.action_kill(args.endpoint)
        else:
            if args.action == 'remove':
                success, results = manage.action_remove(args.endpoint, version)
            else:
                if args.action == 'publish':
                    success, results = manage.action_publish(args.endpoint)
                else:
                    if args.action == 'list':
                        success, results = manage.action_list(args.endpoint)
                    else:
                        if args.action == 'import':
                            success, results = manage.action_import(args.endpoint)
                        else:
                            if args.action == 'export':
                                success, results = manage.action_export(args.endpoint)
                            else:
                                if args.action == 'refactoring':
                                    success, results = manage.action_refactoring(args.file)
                                else:
                                    if args.action == 'dir':
                                        success, results = manage.action_dir()
                                    else:
                                        if args.action == 'info':
                                            success, results = manage.action_info(args.endpoint, version)
    print('flame : ', success, results)


def main():
    parser = argparse.ArgumentParser(description='Use Flame to either build a model from or apply a model to the input file.')
    parser.add_argument('-f', '--infile', help='Input file.',
      required=False)
    parser.add_argument('-e', '--endpoint', help='Endpoint model name.',
      required=False)
    parser.add_argument('-v', '--version', help='Endpoint model version.',
      required=False)
    parser.add_argument('-a', '--action', help='Manage action.',
      required=False)
    parser.add_argument('-c', '--command', action='store',
      choices=[
     'predict', 'build', 'manage'],
      help="Action type: 'predict' or 'build' or 'manage'",
      required=True)
    args = parser.parse_args()
    if args.command == 'predict':
        if args.endpoint is None or args.infile is None:
            print('flame predict : endpoint and input file arguments are compulsory')
            return
        version = utils.intver(args.version)
        model = {'endpoint':args.endpoint, 
         'version':version, 
         'infile':args.infile}
        success, results = context.predict_cmd(model)
        print('flame predict : ', success, results)
    else:
        if args.command == 'build':
            if args.endpoint is None or args.infile is None:
                print('flame build : endpoint and input file arguments are compulsory')
                return
            model = {'endpoint':args.endpoint,  'infile':args.infile}
            success, results = context.build_cmd(model)
            print('flame build : ', success, results)
        elif args.command == 'manage':
            manage_cmd(args)


if __name__ == '__main__':
    main()