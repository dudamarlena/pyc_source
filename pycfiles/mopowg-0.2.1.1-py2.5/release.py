# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/mopowg/release.py
# Compiled at: 2007-08-02 04:59:49
version = '0.2.1.1'
author = 'Fred Lin'
email = 'gasolin@gmail.com'
copyright = 'Copyright 2007 Fred Lin and contributors'
license = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
description = 'Doc generator with styles, and syntax highlighting blocks'
long_description = "mopowg is an easy to install, cross-platform doc generator which is based on docutils.\n\nmopowg could generate full documents with figures, styles, and syntax highlighting blocks.\n\nIt includes a command line tool and will provide the web front-end.\n\nInstall mopowg\n--------------\n\nYou could use easy_install command to install mopowg::\n\n\n    $ easy_install mopowg\n\nor you could install mopowg from sourse\n\nFirst download the source::\n\n    $ hg clone http://hg.python.org.tw/mopowg\n\nthen::\n\n    $ python setup.py install\n\nUsage\n-----\n\nRun as a command\n----------------\n\n::\n\n  $ mopowg -i docs\n\nRun as a single file\n--------------------\n\nYou could embeded mopowg into your project with a single file.\n\nput mopowg.py to a document folder. run mopowg.py::\n\n\n    $ python mopowg.py -i docs\n    \nRun as a module\n---------------\n\nYou could import mopowg module in your program::\n\n    import os\n    from mopowg import mopowg\n\n    path = os.path.join(os.getcwd(), 'docs')\n    ld = mopowg.scanner(path)\n    mopowg.generator(input=ld)\n\nChangeLog\n----------\n\n  * Add license information (MIT)\n  * Add '--preview' option\n  * customable wiki pattern for convertor\n  * customable file extension for saver\n  * Web front end example: Turbogears 2 toolbox plugin: wikidoki http://trac.turbogears.org/browser/projects/ToolBox2/trunk/toolbox/controllers/wikidoki.py\n  * wikipattern cause command not work fixed\n\n"