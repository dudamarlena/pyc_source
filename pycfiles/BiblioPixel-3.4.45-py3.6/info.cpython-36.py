# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/info.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2071 bytes
"""
Print information about BiblioPixel
"""
DESCRIPTION = "\nPrints the versions of BiblioPixel's dependencies, and the platform\nthat the program is running on.\n"
import datetime, os, platform, sys, bibliopixel, BiblioPixelAnimations, loady
from bibliopixel.util import log
from bibliopixel.util.platform import Platform
NONE = '(none)'
MODULES = (bibliopixel, BiblioPixelAnimations, loady)

def run(args):
    platform = Platform()
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    bp_path = sys.argv[0]
    library_path = os.path.dirname(bibliopixel.__file__)
    dependencies = '\n'.join(_dependency(m) for m in MODULES)
    if platform.cpuinfo:
        cpuinfo = CPUINFO % '\n'.join(platform.cpuinfo)
    else:
        cpuinfo = ''
    log.printer((MESSAGE.format)(**locals()))


def add_arguments(parser):
    parser.set_defaults(run=run)


def _dependency(module):
    path = os.path.dirname(module.__file__)
    parent = os.path.dirname(path)
    try:
        fp = open(os.path.join(path, 'VERSION'))
    except:
        try:
            fp = open(os.path.join(parent, 'VERSION'))
        except:
            fp = None

    version = fp.read().strip() if fp else NONE
    try:
        import git
        repo = git.Repo(os.path.dirname(path))
    except:
        commit_id = tag = NONE
    else:
        commit_id = repo.commit('HEAD').hexsha[:7]
        tag = repo.tags[(-1)].name if repo.tags else '(none)'
    return '    %s: version %s, git commit: %s, git tag %s' % (
     module.__name__, version, commit_id, tag)


MESSAGE = 'Timestamp:        {now}\nPython version:   {platform.python_version}\n`bp` path:        {bp_path}\nLibrary path:     {library_path}\n\nPlatform:         {platform.platform}\nPlatform version: {platform.platform_version}\nPlatform release: {platform.release}\n\nDependencies:\n{dependencies}\n{cpuinfo}'
CPUINFO = '\ncpuinfo\n--------------------------------------------------------------------------------\n%s\n--------------------------------------------------------------------------------\n'