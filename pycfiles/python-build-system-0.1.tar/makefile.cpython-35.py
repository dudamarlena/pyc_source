# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kiv/projects/python-build-system/python_build_system/modules/platform/tools/makefile.py
# Compiled at: 2016-10-23 20:13:57
# Size of source mod 2**32: 746 bytes


def load_deps_from_makefile(filename, target=None):
    try:
        deps_list = []
        f = open(filename, 'r')
        rule = ''
        for line in f:
            if rule and rule[(-1)] == '\\':
                rule = rule[:-1] + line.strip()
            else:
                rule = line.strip()
            if rule and rule[(-1)] != '\\' and (target is None or rule.startswith('%s:' % target)):
                if target:
                    deps = rule[len(target) + 1:]
                else:
                    deps = rule.split(':', 2)[1]
                deps = deps.strip()
                deps_list += deps.split(' ')

        f.close()
        return deps_list
    except IOError:
        pass