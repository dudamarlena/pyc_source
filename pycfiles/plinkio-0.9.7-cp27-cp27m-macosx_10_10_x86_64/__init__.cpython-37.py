# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /build/plink/build/lib/plink/__init__.py
# Compiled at: 2019-07-15 20:56:41
# Size of source mod 2**32: 930 bytes
from .version import version as __version__
from .manager import LinkManager
from .viewer import LinkViewer
from .editor import LinkDisplay, LinkEditor
__all__ = [
 'LinkManager', 'LinkViewer', 'LinkDisplay', 'LinkEditor']
if __name__ == '__main__':
    LE = LinkEditor()
    LE.window.mainloop()