# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\exm\exm.py
# Compiled at: 2019-03-17 10:32:00
import argparse, json, os, sys, subprocess, yaml, const
from sections import env, java, maven
from utils import yaml_util
from utils import expression
parser = argparse.ArgumentParser(description='A tool for execution environment management')
parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose log')
parser.add_argument('file')
parser.add_argument('params', nargs=argparse.REMAINDER)
args = parser.parse_args()

def main():
    os.chdir(const.SCRIPT_DIR)
    if args.verbose:
        print 'Work dir: %s' % const.SCRIPT_DIR
    conf = yaml_util.load(args.file)
    run(conf)
    return 0


def run(conf):
    if args.verbose:
        print 'Execution configuration: %s' % json.dumps(conf, indent=4)
    ctx = processctx(conf)
    try:
        expression.evaluate(ctx, ctx)
        execute(ctx)
    except Exception as ex:
        print '\nFailed on execution context: %s' % json.dumps(ctx, indent=4)
        raise ex


def execute(ctx):
    execmd = '%s %s' % (ctx['exm']['command'], (' ').join(args.params))
    if args.verbose:
        print 'Run command: %s' % execmd
    forked = subprocess.Popen(execmd, shell=True)
    forked.wait()
    if forked.returncode != 0:
        if args.verbose:
            raise Exception('Exit code: ' + forked.returncode)


def processctx(conf):
    ctx = {'exm': {}}
    ctx.update(conf)
    env.process(ctx)
    java.process(ctx)
    maven.process(ctx)
    return ctx


if __name__ == '__main__':
    sys.exit(main())