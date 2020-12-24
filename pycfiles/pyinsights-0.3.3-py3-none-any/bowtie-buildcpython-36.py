# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/markmandel/src/pyinseq/pyinseq/third-party/bowtie-1.1.1-mac/bowtie-build
# Compiled at: 2017-02-18 15:47:24
# Size of source mod 2**32: 2807 bytes
__doc__ = '\n Copyright 2014, Ben Langmead <langmea@cs.jhu.edu>\n\n This file is part of Bowtie.\n\n Bowtie is free software: you can redistribute it and/or modify\n it under the terms of the GNU General Public License as published by\n the Free Software Foundation, either version 3 of the License, or\n (at your option) any later version.\n\n Bowtie is distributed in the hope that it will be useful,\n but WITHOUT ANY WARRANTY; without even the implied warranty of\n MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n GNU General Public License for more details.\n\n You should have received a copy of the GNU General Public License\n along with Bowtie.  If not, see <http://www.gnu.org/licenses/>.\n'
import os, sys, inspect, logging

def build_args():
    """
    Parse the wrapper arguments. Returns the options,<programm arguments> tuple.
    """
    parsed_args = {}
    to_remove = []
    argv = sys.argv[:]
    for i, arg in enumerate(argv):
        if arg == '--large-index':
            parsed_args[arg] = ''
            to_remove.append(i)
        else:
            if arg == '--debug':
                parsed_args[arg] = ''
                to_remove.append(i)
            else:
                if arg == '--verbose':
                    parsed_args[arg] = ''
                    to_remove.append(i)

    for i in reversed(to_remove):
        del argv[i]

    return (
     parsed_args, argv)


def main():
    logging.basicConfig(level=(logging.ERROR), format='%(levelname)s: %(message)s')
    delta = 200
    small_index_max_size = 4294967296 - delta
    build_bin_name = 'bowtie-build'
    build_bin_s = 'bowtie-build-s'
    build_bin_l = 'bowtie-build-l'
    curr_script = os.path.realpath(inspect.getsourcefile(main))
    ex_path = os.path.dirname(curr_script)
    build_bin_spec = os.path.join(ex_path, build_bin_s)
    options, argv = build_args()
    if '--verbose' in options:
        logging.getLogger().setLevel(logging.INFO)
    if '--debug' in options:
        build_bin_spec += '-debug'
        build_bin_l += '-debug'
    if '--large-index' in options:
        build_bin_spec = os.path.join(ex_path, build_bin_l)
    else:
        if len(argv) >= 2:
            ref_fnames = argv[(-2)]
            tot_size = 0
            for fn in ref_fnames.split(','):
                if os.path.exists(fn):
                    statinfo = os.stat(fn)
                    tot_size += statinfo.st_size

            if tot_size > small_index_max_size:
                build_bin_spec = os.path.join(ex_path, build_bin_l)
    argv[0] = build_bin_name
    argv.insert(1, 'basic-0')
    argv.insert(1, '--wrapper')
    logging.info('Command: %s %s' % (build_bin_spec, ' '.join(argv[1:])))
    os.execv(build_bin_spec, argv)


if __name__ == '__main__':
    main()