# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astropysics/data/ipython_config_astpys.py
# Compiled at: 2013-11-27 17:30:36
"""
The astropysics interactive IPython configuration file for ipython versions >=0.11
"""
load_subconfig('ipython_config.py')
c = get_config()
lines = '\nimport numpy\nimport numpy as np\nfrom numpy import *\nfrom numpy.random import rand,randn,randint\n\nimport scipy\nfrom scipy import stats,optimize,ndimage,integrate,interpolate,special\n\ntry:\n    import astropysics\n    from astropysics import phot,spec,coords,models,constants,objcat,obstools,plotting,utils\nexcept ImportError:\n    print "Unable to start astropysics profile, try re-running astpys-setup (or re-installing astropysics)"\n\n#silently ignore pyfits and asciitable if they are not present,as they are optional\ntry:\n\timport pyfits\nexcept ImportError:\n\tpass\ntry:\n\timport asciitable\nexcept ImportError:\n\tpass\n\n'
mpllines = "\nimport matplotlib\nmatplotlib.interactive(True)\nmatplotlib.use('{MPLBACK}')\nguiapp = %gui {GUITK}\nfrom matplotlib import pyplot as plt\nfrom matplotlib.pyplot import *\n"
c.Global.exec_lines.append(mpllines)
c.Global.exec_lines.append(lines)