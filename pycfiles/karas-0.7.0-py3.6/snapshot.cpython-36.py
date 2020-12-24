# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/training/extensions/snapshot.py
# Compiled at: 2019-01-08 04:39:39
# Size of source mod 2**32: 890 bytes
import os, shutil, torch
from karas.training import extension
from karas.training import utils

class Snapshot(extension.Extension):
    __doc__ = '\n    if target == None, save the trainer\n    '

    def __init__(self, target=None, filename='snapshot_iter_{.iteration}.pth'):
        self._tmpl = filename
        self._tget = target

    def __call__(self, trainer):
        device = trainer.updater.device
        fn = self._tmpl.format(trainer)
        prefix = 'tmp' + fn
        with utils.tempdir(prefix=prefix, dir=(trainer.out)) as (tmpdir):
            tmppath = os.path.join(tmpdir, fn)
            if self._tget is None:
                trainer.serialize(tmppath)
            else:
                torch.save(self._tget.cpu(), tmppath)
            shutil.move(tmppath, os.path.join(trainer.out, fn))
        if self._tget is not None:
            self._tget.to(device)