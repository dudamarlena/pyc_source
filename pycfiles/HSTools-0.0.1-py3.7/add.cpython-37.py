# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/funcs/add.py
# Compiled at: 2019-10-23 10:30:25
# Size of source mod 2**32: 5613 bytes
import os, sys, shutil, argparse
from hstools import hydroshare, log
logger = log.logger

def add_file(hs, resid, source, target):
    return hs.addContentToExistingResource(resid, source, target=target)


def set_usage(parser):
    optionals = []
    for option in parser._get_optional_actions():
        if len(option.option_strings) > 0:
            ostring = f"[{option.option_strings[0]}]"
            if '--' in ostring:
                optionals.append(ostring)
            else:
                optionals.insert(0, ostring)

    positionals = []
    for pos in parser._get_positional_actions():
        positionals.append(pos.dest)

    parser.usage = f"%(prog)s {' '.join(positionals)} {' '.join(optionals)}"


def add_arguments(parser):
    parser.description = long_help()
    parser.add_argument('resource_id', type=str,
      help='unique HydroShare resource identifier')
    parser.add_argument('-f', '--files', required=True, type=str,
      nargs='+',
      help='files to add to resource. By default all files will be added to the root directory of the resource. A specific directory can be specified relative to the root directory using the following syntax - <source-path>:<target-path>.')
    parser.add_argument('--overwrite', action='store_true', help='overwrite existing resource files with thesame name')
    parser.add_argument('-v', default=True, action='store_true', help='verbose output')
    parser.add_argument('-q', default=False, action='store_true', help='silent output')
    set_usage(parser)


def main(args):
    if args.v:
        log.set_verbose()
    else:
        if args.q:
            log.set_quiet()
        else:
            hs = hydroshare.hydroshare()
            if hs is None:
                raise Exception('Connection to HydroShare failed')
                sys.exit(1)
            sources = []
            targets = []
            for f in args.files:
                if ':' in f:
                    src, tar = f.split(':')
                    tar = tar.strip('/')
                else:
                    src = f
                    tar = os.path.basename(src)
                sources.append(src)
                targets.append(tar)

            for f in sources:
                if not os.path.exists(f):
                    raise Exception(f"Could not find file: {f}")
                    sys.exit(1)

            try:
                response = hs.getResourceFiles(args.resource_id)
                res_files = []
                if len(response) > 0:
                    for r in response:
                        file_path = r['url'].split('contents')[(-1)]
                        file_path = file_path[1:] if file_path[0] == '/' else file_path
                        res_files.append(file_path)

            except Exception:
                raise Exception('Error connecting to HydroShare resource')

        file_conflicts = []
        if len(res_files) > 0:
            for rf in res_files:
                if rf in targets:
                    file_conflicts.append(rf)

        if len(file_conflicts) > 0 and not args.overwrite:
            for fc in file_conflicts:
                print(f" - {fc} already exists, use --overwrite to replace")
                res_files.pop(res_files.index(fc))
                tidx = targets.index(fc)
                sources.pop(tidx)
                targets.pop(tidx)

        else:
            for fc in file_conflicts:
                logger.info(f"- removing: {fc}")
                hs.hs.deleteResourceFile(args.resource_id, fc)

    res_dirs = [os.path.dirname(p) for p in res_files]
    for i in range(0, len(targets)):
        target_path = os.path.dirname(targets[i])
        if target_path not in res_dirs:
            print(f"+ creating resource directory: {target_path}")
            try:
                hs.hs.createResourceFolder((args.resource_id), pathname=target_path)
            except Exception:
                pass

    for i in range(0, len(sources)):
        try:
            add_file(hs, args.resource_id, sources[i], targets[i])
        except Exception:
            print(f"- failed to add file {sources[i]:targets[i]}")


def short_help():
    return 'Add files to an existing HydroShare resource'


def long_help():
    return 'Add files to an existing HydroShare resource. Multiple files\n              can be added at once and folders are created as necessary.\n              By default existing files will not be replaced, use the\n              --overwrite option if this is desired.\n            '


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=(long_help()))
    add_arguments(parser)
    args = parser.parse_args()
    main(args)