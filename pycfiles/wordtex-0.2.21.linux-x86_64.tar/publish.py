# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/publish.py
# Compiled at: 2013-11-13 15:05:10
import pdb
from cloudtb import publish
VERSION = '0.2.21'
publish.YOUR_LICENSE = ("  \n#     LICENSE: The GNU Public License v3 or Greater\n#\n#     WordTeX (wordtex) v{version}\n#     Copyright 2013 Garrett Berg\n#     \n#     Loosly based on LaTeX2WP version 0.6.2, Luca Trevisan Copyright 2009\n#    \n#     This file is part of wordtex, a program that converts\n#     a LaTeX document into a format that is ready to be\n#     copied and pasted into WordPress.\n#    \n#     You are free to redistribute and/or modify wordtex under the\n#     terms of the GNU General Public License (GPL), version 3\n#     or (at your option) any later version.\n#    \n#     You should have received a copy of the GNU General Public\n#     License along with wordtex.  If you can't find it,\n").format(version=VERSION)
publish.LAST_LINE = '#     see <http://www.gnu.org/licenses/>'
publish.CLOUDTB_VERSION_URL = '/home/user/Projects/CloudformDesign/PythonCloudform/cloudtb'
if __name__ == '__main__':
    from cloudtb import dbe
    publish.main()