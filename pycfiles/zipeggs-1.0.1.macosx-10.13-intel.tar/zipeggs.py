# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/zipeggs.py
# Compiled at: 2018-02-10 08:34:06
import os, shutil, zc.buildout

class ZipEggs:

    def __init__(self, buildout, name, options):
        self.source_dir = options['source']
        self.target_dir = options['target']
        if not os.path.isdir(self.source_dir):
            raise zc.buildout.UserError(('Invalid Source {s!r}').format(s=self.source_dir))
        if self.target_dir is None:
            raise zc.buildout.UserError(('Invalid Target {t!r}').format(t=self.target_dir))
        return

    def _zipit(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        for entry in os.listdir(self.source_dir):
            try:
                source = os.path.join(self.source_dir, entry)
                target = os.path.join(self.target_dir, entry)
                print ('ZipEggs: {s} > {t}').format(s=source, t=target)
                shutil.make_archive(target, 'zip', source)
                os.rename(target + '.zip', target)
                yield target
            except OSError as e:
                print ('ZipEggs: ignore {s!r}: {e!r}').format(s=entry, e=e)

    def install(self):
        return list(self._zipit())

    def update(self):
        return list(self._zipit())