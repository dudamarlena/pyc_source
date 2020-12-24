# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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