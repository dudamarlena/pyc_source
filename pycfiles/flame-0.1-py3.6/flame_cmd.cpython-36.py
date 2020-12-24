# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/flame_cmd.py
# Compiled at: 2018-04-06 11:01:08
# Size of source mod 2**32: 3175 bytes
import os, sys, argparse, shutil
from flame.predict import Predict
from flame.build import Build
from flame.manage import Manage

def predict_cmd(args):
    """
    Instantiates a Predict object to run a prediction
    using the given input file and model
    """
    predict = Predict(args.infile, args.endpoint, args.version)
    success, results = predict.run()
    print('flame : ', success, results)


def build_cmd(args):
    """
    Instantiates a Build object to build a model using the given input
    file (training series) and model (name of endpoint, eg. 'CACO2')
    """
    build = Build(args.infile, args.endpoint)
    success, results = build.run()
    print('flame : ', success, results)


def manage_cmd(args):
    """
    Instantiates a Build object to build a model using the given input
    file (training series) and model (name of endpoint, eg. 'CACO2')
    """
    if args.version is None:
        version = 0
    else:
        try:
            version = int(args.version)
        except:
            version = 0

    manage = Manage(args.endpoint, version, args.action, args.infile)
    success, results = manage.run()
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
        predict_cmd(args)
    else:
        if args.command == 'build':
            build_cmd(args)
        elif args.command == 'manage':
            manage_cmd(args)


if __name__ == '__main__':
    main()