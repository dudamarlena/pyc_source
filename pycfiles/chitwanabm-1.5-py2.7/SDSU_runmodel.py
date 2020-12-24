# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chitwanabm\misc\SDSU_runmodel.py
# Compiled at: 2012-09-03 14:16:00
"""
Script used to simplify running the chitwanabm on SDSU lab computers. Sets up 
the python and system paths so the model can find all the required 
dependencies.
"""
import os, sys

def main():
    os.environ['PATH'] = 'Z:\\Programs\\GDAL;Z:\\Python_Local_64bit\\Scripts;' + os.environ['PATH']
    oldpaths = sys.path
    sys.path = ['Z:\\Python_Local_64bit\\site-packages', 'Z:\\Code',
     'Z:\\Python_Local_64bit\\Scripts']
    sys.path.extend(oldpaths)
    import chitwanabm.runmodel
    chitwanabm.runmodel.main()


if __name__ == '__main__':
    sys.exit(main())