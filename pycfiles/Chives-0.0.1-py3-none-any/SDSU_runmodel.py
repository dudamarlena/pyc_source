# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chitwanabm\misc\SDSU_runmodel.py
# Compiled at: 2012-09-03 14:16:00
__doc__ = '\nScript used to simplify running the chitwanabm on SDSU lab computers. Sets up \nthe python and system paths so the model can find all the required \ndependencies.\n'
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