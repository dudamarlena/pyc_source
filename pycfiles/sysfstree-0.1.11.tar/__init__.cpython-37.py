# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/sysfstree/__init__.py
# Compiled at: 2020-02-14 02:39:45
# Size of source mod 2**32: 8492 bytes
import os, sys, fnmatch, magic, struct

class sysfstree(object):

    def __init__(self, root, maxlevel, include=None, exclude=None):
        self.maxlevel = maxlevel
        self.include = include
        self.exclude = exclude
        self.root = root

    def match_exclude(self, name, matches):
        if len(matches) == 0:
            return False
        if type(matches) is list:
            return any((fnmatch.fnmatch(name, pattern) for pattern in matches))
        if type(matches) is str:
            return fnmatch.fnmatch(name, matches)
        return False

    def match_include(self, name, matches):
        if len(matches) == 0:
            return True
        if type(matches) is list:
            return any((fnmatch.fnmatch(name, pattern) for pattern in matches))
        if type(matches) is str:
            return fnmatch.fnmatch(name, matches)
        return True

    def pathdescriptors(self, path):
        try:
            bdata = []
            with open(path, 'rb') as (f):
                byte = f.read(1)
                while byte:
                    bdata.append(struct.unpack('B', byte)[0])
                    byte = f.read(1)

            length = 0
            descriptors = []
            hexstr = ''
            for x in bdata:
                t = '%02x' % x
                if length == 0:
                    hexstr = t
                    length = x - 1
                else:
                    length -= 1
                    hexstr += ' ' + t
                if length == 0:
                    length = 0
                    descriptors.append(hexstr)
                    hexstr = ''

            return descriptors
        except Exception:
            return ''

    def pathread(self, path):
        try:
            fstat = os.stat(path)
        except PermissionError:
            return ''
        else:
            if fstat.st_size == 4096 or fstat.st_size == 0:
                try:
                    f = open(path, 'r')
                    lines = f.readlines(1000)
                    f.close()
                    return lines
                except (PermissionError, OSError):
                    return ''
                except UnicodeDecodeError:
                    return '[UnicodeDecodeError]'

            if fstat.st_size == 65553:
                return self.pathdescriptors(path)
            try:
                filetype = magic.from_file(path)
                if 'ELF' in filetype:
                    return [
                     'ELF file']
            except (magic.MagicException, PermissionError):
                return ''
            else:
                return '<UNKNOWN>'

    def _tree(self, parent_path, file_list, prefix, level):
        if level == -1:
            yield '[%s]' % parent_path
            yield from self._tree(parent_path, file_list, prefix, 0)
            return
        if (len(file_list) == 0 or self.maxlevel) != -1:
            if self.maxlevel <= level:
                return
        file_list.sort(key=(lambda f: os.path.isfile(os.path.join(parent_path, f))))
        for idx, sub_path in enumerate(file_list):
            full_path = os.path.join(parent_path, sub_path)
            try:
                if not self.match_include(sub_path, self.include[level]):
                    continue
            except IndexError:
                pass

            try:
                if self.match_exclude(sub_path, self.exclude[level]):
                    continue
            except IndexError:
                pass

            idc = ('┣━', '┗━')[(idx == len(file_list) - 1)]
            if os.path.isdir(full_path):
                if not os.path.islink(full_path):
                    yield '%s%s[%s]' % (prefix, idc, sub_path)
                    tmp_prefix = (
                     prefix + '    ', prefix + '┃   ')[(len(file_list) > 1 and idx != len(file_list) - 1)]
                    yield from self._tree(full_path, os.listdir(full_path), tmp_prefix, level + 1)
            else:
                if os.path.islink(full_path):
                    yield '%s%s%s -> %s' % (prefix, idc, sub_path, os.path.realpath(full_path))
            if os.path.isfile(full_path):
                l = self.pathread(full_path)
                first = True
                for d in l:
                    yield '%s%s%s: %s' % (prefix, idc, sub_path, d.rstrip())
                    if not first:
                        continue
                    sub_path = ' ' * (len(sub_path) + 1)
                    idc = '┃'
                    first = False


def _main(paths, maxlevel=-1, include=[], exclude=[]):
    for p in paths:
        sysfs = sysfstree(p, maxlevel=maxlevel, include=include, exclude=exclude)
        for l in sysfs._tree(p, os.listdir(p), '', -1):
            print(('%s' % l), file=(sys.stdout))


def _test(args):
    import doctest
    doctest.testmod()
    _main(['/sys'], include=[['power'], ['pm_freeze_timeout', 'state']])
    _main(['/sys/devices/platform/soc'], include=[['*.usb'], ['usb3'], ['descriptors', 'ep_00', 'driver']])
    _main(['/sys/kernel/debug/tracing/events/workqueue/workqueue_execute_end'])
    sysname, nodename, release, version, machine = os.uname()
    path = '/lib/modules/' + release + '/kernel/drivers/usb/gadget/function/'
    _main([path], maxlevel=(args.maxlevel), include=['usb_f_*'])


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Display information about Gadget USB from SysFS and ConfigFS',
      formatter_class=(lambda prog: argparse.RawTextHelpFormatter(prog, width=999)))
    parser.add_argument('-T', '--test', help='/sys/devices/platform/soc/*.usb/udc', action='store_true')
    parser.add_argument('-P', '--path', nargs='*', help='include (shell pattern match)', default=[])
    parser.add_argument('-I', '--include', nargs='*', help='include (shell pattern match)', default=[])
    parser.add_argument('-E', '--exclude', nargs='*', help='exclude (shell pattern match)', default=[])
    parser.add_argument('-m', '--maxlevel', help='max level', type=int, default=(-1))
    parser.add_argument('paths', metavar='Path', type=str, nargs=(argparse.REMAINDER), help='pathname', default=[])
    args = parser.parse_args()
    print('args: %s' % args)
    if args.test:
        _test(args)
    for path in args.path + args.paths:
        _main([path], maxlevel=(args.maxlevel), include=[args.include], exclude=[args.exclude])


if __name__ == '__main__':
    main()