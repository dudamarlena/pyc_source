# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pi/work/sysfstree/src/sysfstree/sysfstree.py
# Compiled at: 2020-04-04 02:34:56
# Size of source mod 2**32: 17561 bytes
import os, sys, fnmatch, magic, struct
from termcolor import colored

class sysfstree(object):

    def __init__(self, root, maxlevel, pinclude=[], pexclude=[], include=None, exclude=None, bold=None, ordinary=False, nobold=False, sort=True, followsyms=False):
        self.maxlevel = maxlevel
        self.include = include
        self.exclude = exclude
        self.bold = bold
        self.followsyms = followsyms
        self.ordinary = ordinary
        self.nobold = nobold
        self.root = root
        self.sort = sort
        self.pinclude = [x.split('/') for x in pinclude]
        self.pexclude = [x.split('/') for x in pexclude]
        if len(self.pinclude) > 0:
            if len(self.include):
                print('sysfstree: pinclude and include mutually exclusive')
                exit(1)
        if len(self.pexclude) > 0:
            if len(self.exclude):
                print('sysfstree: pexclude and exclude mutually exclusive')
                exit(1)

    def match_exclude(self, name, level):
        if len(self.pexclude) > 0:
            return False
        if self.exclude is None:
            return False
        try:
            matches = self.exclude[level]
        except IndexError:
            return False
        else:
            print(('match_exclude: %s in %s' % (name, matches)), file=(sys.stderr))
            if len(matches) == 0:
                return False
            if type(matches) is list:
                return any((fnmatch.fnmatch(name, pattern) for pattern in matches))
            if type(matches) is str:
                return fnmatch.fnmatch(name, matches)
            return False

    def match_include(self, name, level):
        if len(self.pinclude) > 0:
            return False
        if self.include is None:
            return True
        try:
            matches = self.include[level]
        except IndexError:
            return True
        else:
            if len(matches) == 0:
                return True
            if type(matches) is list:
                return any((fnmatch.fnmatch(name, pattern) for pattern in matches))
            if type(matches) is str:
                return fnmatch.fnmatch(name, matches)
            return True

    def match_pexclude(self, path, name, level):
        if len(self.exclude) > 0:
            return False
        if self.pexclude is None:
            return False
        for match in self.pinclude:
            try:
                if fnmatch.fnmatch(name, match[level]):
                    return False
            except IndexError:
                pass

        return False

    def match_pinclude(self, path, name, level):
        if len(self.include) > 0:
            return False
        if self.pinclude is None:
            return True
        for match in self.pinclude:
            try:
                if fnmatch.fnmatch(name, match[level]):
                    return True
            except IndexError:
                pass

        return False

    def _colored(self, text, color=None, attrs=None):
        if self.nobold:
            return text
        return colored(text, color, attrs=attrs)

    def _color(self, path, level):
        if self.bold is None:
            return path
        else:
            try:
                matches = self.bold[level]
            except IndexError:
                matches = None

            if not matches is None:
                if len(matches) == 0:
                    pass
                elif type(matches) is list:
                    if any((fnmatch.fnmatch(path, pattern) for pattern in matches)):
                        return self._colored(path, 'red', attrs=['bold'])
                elif type(matches) is str:
                    if fnmatch.fnmatch(path, matches):
                        return self._colored(path, 'red', attrs=['bold'])
        return path

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
            if self.ordinary or fstat.st_size == 4096 or fstat.st_size == 0:
                try:
                    f = open(path, 'r')
                    lines = f.readlines(1000)
                    f.close()
                    return lines
                except (PermissionError, OSError):
                    return ''
                except UnicodeDecodeError:
                    pass

                try:
                    f = open(path, 'rb')
                    bytes = f.read(4096)
                    f.close
                except (PermissionError, OSError):
                    return ''
                else:
                    return bytes
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
            yield '[%s]' % self._colored(parent_path, attrs=['bold'])
            yield from self._tree(parent_path, file_list, prefix, 0)
            return
        if (len(file_list) == 0 or self.maxlevel) != -1:
            if self.maxlevel <= level:
                return
        if self.sort:
            file_list = sorted(file_list, key=(str.casefold))
        for idx, sub_path in enumerate(file_list):
            full_path = os.path.join(parent_path, sub_path)
            if not self.match_pinclude(full_path, sub_path, level):
                if not self.match_include(sub_path, level):
                    continue
                else:
                    if self.match_exclude(sub_path, level) or self.match_pexclude(full_path, sub_path, level):
                        continue
                    idc = ('├──', '└──')[(idx == len(file_list) - 1)]
                    if os.path.islink(full_path):
                        self.followsyms or (yield '%s%s%s -> %s' % (prefix, idc, self._color(sub_path, level), os.path.realpath(full_path)))
                        continue
                if not os.path.isfile(full_path):
                    continue
                data = self.pathread(full_path)
                first = True
                if len(data) == 0:
                    yield '%s%s%s: [NULL]' % (prefix, idc, self._color(sub_path, level))
                    continue
                idc = '├──'
                if type(data) == bytes:
                    line = ''
                    count = 0
                    total = 0
                    for d in data:
                        line += ' %02x' % int(d)
                        total += 1
                        count += 1
                        if count < 16:
                            if total < len(data):
                                continue
                        yield '%s%s%s:%s' % (prefix, idc, self._color(sub_path, level), line)
                        count = 0
                        line = ''
                        if not first:
                            continue
                        sub_path = ' ' * (len(sub_path) + 1)
                        idc = '│ '
                        first = False

                    continue
                for d in data:
                    yield '%s%s%s: %s' % (prefix, idc, self._color(sub_path, level), d.rstrip())
                    if not first:
                        continue
                    sub_path = ' ' * (len(sub_path) + 1)
                    idc = '│ '
                    first = False

        for idx, sub_path in enumerate(file_list):
            full_path = os.path.join(parent_path, sub_path)
            if not self.match_pinclude(full_path, sub_path, level):
                if not self.match_include(sub_path, level):
                    continue
            if self.match_exclude(sub_path, level) or self.match_pexclude(full_path, sub_path, level):
                continue
            idc = ('├──', '└──')[(idx == len(file_list) - 1)]
            if not self.followsyms:
                if os.path.islink(full_path):
                    continue
            if not os.path.isdir(full_path):
                if os.path.islink(full_path):
                    if os.path.islink(full_path):
                        yield '%s%s[%s -> %s]' % (prefix, idc, self._color(sub_path, level), os.path.realpath(full_path))
                        full_path = os.path.realpath(full_path)
                        print('parent_path: %s' % parent_path)
                        print('full_path: %s' % full_path)
                    else:
                        yield '%s%s[%s]' % (prefix, idc, self._color(sub_path, level))
                tmp_prefix = (
                 prefix + '    ', prefix + '│   ')[(len(file_list) > 1 and idx != len(file_list) - 1)]
                paths = [d.name for d in sorted((os.scandir(full_path)), key=(lambda dirent: dirent.inode()))]
                yield from self._tree(full_path, paths, tmp_prefix, level + 1)


def _main2(paths, maxlevel=-1, pinclude=[], pexclude=[], include=[], exclude=[], bold=[], ordinary=False, nobold=False, sort=True, followsyms=False):
    print(('paths: %s' % paths), file=(sys.stderr))
    for p in paths:
        sysfs = sysfstree(p, maxlevel=maxlevel, pinclude=pinclude,
          pexclude=pexclude,
          include=include,
          exclude=exclude,
          bold=bold,
          ordinary=ordinary,
          nobold=nobold,
          sort=sort,
          followsyms=followsyms)
        try:
            for l in sysfs._tree(p, os.listdir(p), '', -1):
                print(('%s' % l), file=(sys.stdout))

        except PermissionError:
            print('[%s] [PermissionError]' % p)


def _test(args):
    import doctest
    doctest.testmod()
    _main2(['/sys/kernel/config/usb_gadget'], bold=[[], ['UDC']], sort=False)


def main():
    import argparse, json
    parser = argparse.ArgumentParser(description='Display information about Gadget USB from SysFS and ConfigFS',
      formatter_class=(lambda prog: argparse.RawTextHelpFormatter(prog, width=999)))
    parser.add_argument('-T', '--test', help='run tests', action='store_true')
    parser.add_argument('-O', '--ordinary', help='not in /sys', action='store_true')
    parser.add_argument('-P', '--path', nargs='*', help='include (shell pattern match)', default=[])
    parser.add_argument('-I', '--include', nargs='*', help='include (shell pattern match)', default=[])
    parser.add_argument('-E', '--exclude', nargs='*', help='exclude (shell pattern match)', default=[])
    parser.add_argument('--pinclude', nargs='*', help='path include (shell pattern match)', default=[])
    parser.add_argument('--pexclude', nargs='*', help='path exclude (shell pattern match)', default=[])
    parser.add_argument('-B', '--bold', nargs='*', help='bold (shell pattern match)', default=[])
    parser.add_argument('-N', '--nobold', nargs='*', help='bold (shell pattern match)', default=[])
    parser.add_argument('--include_list', type=(json.loads), help='json list version of include', default=[])
    parser.add_argument('--exclude_list', type=(json.loads), help='json list version of exclude', default=[])
    parser.add_argument('--bold_list', type=(json.loads), help='json list version of bold')
    parser.add_argument('--udc', help='/sys/class/udc', action='store_true')
    parser.add_argument('--usb-gadget', '--gadget', help='/sys/kernel/config/usb_gadget', action='store_true')
    parser.add_argument('--usb-gadget-udc', '--gadget-udc', help='/sys/kernel/config/usb_gadget/*/udc', action='store_true')
    parser.add_argument('-m', '--maxlevel', help='max level', type=int, default=(-1))
    parser.add_argument('paths', metavar='Path', type=str, nargs=(argparse.REMAINDER), help='pathname', default=[])
    args = parser.parse_args()
    print(('args: %s' % args), file=(sys.stderr))
    if args.bold:
        if args.bold_list:
            print('--bold and --bold_list are mutually incompatible, use only one', file=(sys.stderr))
            exit(1)
    if args.include:
        if args.include_list:
            print('--include and --include_list are mutually incompatible, use only one', file=(sys.stderr))
            exit(1)
    if args.exclude:
        if args.exclude_list:
            print('--exclude and --exclude_list are mutually incompatible, use only one', file=(sys.stderr))
            exit(1)
    if args.bold:
        args.bold_list = [
         args.bold]
    if args.include:
        args.include_list = [
         args.include]
    if args.exclude:
        args.exclude_list = [
         args.exclude]
    if args.test:
        _test(args)
    if args.udc:
        print('udc')
        for s in os.listdir('/sys/class/udc'):
            _main2([os.path.realpath('/sys/class/udc/%s' % s)], maxlevel=(args.maxlevel))

        return
    if args.usb_gadget:
        print('usb_gadget')
        _main2(['/sys/kernel/config/usb_gadget'], maxlevel=(args.maxlevel))
        return
    if args.usb_gadget_udc:
        print('usb_gadget_udc')
        _main2(['/sys/kernel/config/usb_gadget/'], maxlevel=(args.maxlevel), include=[[], ['UDC']], bold=[[], ['UDC']])
        return
    for path in args.path + args.paths:
        _main2([path], maxlevel=(args.maxlevel), include=(args.include_list),
          exclude=(args.exclude_list),
          pinclude=(args.pinclude),
          pexclude=(args.pexclude),
          bold=(args.bold_list),
          ordinary=(args.ordinary),
          nobold=(args.nobold))


if __name__ == '__main__':
    main()