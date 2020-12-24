# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Commands/Info.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 1489 bytes
from .Command import Command
from ..TermOutput import fg, bg, attr, stylize, msg, wrapWithColor

class Info(Command):
    command = 'info'
    help = 'Print information about current repository'

    def set_args(self, subparser):
        pass

    def run(self, args):
        import os
        from ..Database import Database
        from collections import Counter
        db = Database(dataDir=(args.data_dir))
        nworks = len(db.works)
        dataPath = db.dataDir
        dirSize = 0
        for f in os.listdir(dataPath):
            f = os.path.join(dataPath, f)
            if os.path.isfile(f):
                dirSize += os.path.getsize(f)

        tagCount = Counter()
        for e in db.works:
            tagCount.update(e.tags)

        lc = fg('white') + attr('dim')
        cc = fg('white') + attr('bold')
        vc = fg('cyan')
        tc = fg('red') + attr('bold')
        tagstr = ', '.join(stylize(t, tc) + ' (' + stylize(str(c), cc) + ')' for t, c in sorted((tagCount.items()), key=(lambda x: -x[1])))
        fields = [
         (
          'Data path', stylize(dataPath, vc)),
         (
          'Database Size', stylize('{:.3f} MB'.format(dirSize / 1048576), vc)),
         (
          'Number of entries', stylize(str(nworks), vc)),
         (
          'Tags', tagstr)]
        w = max(len(x) for x, _ in fields)
        w = max(1 + w, 12)
        for l, v in fields:
            msg(wrapWithColor((stylize('{l:<{w}}'.format(l=l, w=w), lc) + v), indent=w))