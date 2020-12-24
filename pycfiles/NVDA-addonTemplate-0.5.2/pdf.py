# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\pdf.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.pdf

Common PDF Builder definition for various other Tool modules that use it.
Add an explicit action to run epstopdf to convert .eps files to .pdf

"""
__revision__ = 'src/engine/SCons/Tool/pdf.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Builder, SCons.Tool
PDFBuilder = None
EpsPdfAction = SCons.Action.Action('$EPSTOPDFCOM', '$EPSTOPDFCOMSTR')

def generate(env):
    global PDFBuilder
    try:
        env['BUILDERS']['PDF']
    except KeyError:
        if PDFBuilder is None:
            PDFBuilder = SCons.Builder.Builder(action={}, source_scanner=SCons.Tool.PDFLaTeXScanner, prefix='$PDFPREFIX', suffix='$PDFSUFFIX', emitter={}, source_ext_match=None, single_source=True)
        env['BUILDERS']['PDF'] = PDFBuilder

    env['PDFPREFIX'] = ''
    env['PDFSUFFIX'] = '.pdf'
    return


def generate2(env):
    bld = env['BUILDERS']['PDF']
    bld.add_action('.eps', EpsPdfAction)
    env['EPSTOPDF'] = 'epstopdf'
    env['EPSTOPDFFLAGS'] = SCons.Util.CLVar('')
    env['EPSTOPDFCOM'] = '$EPSTOPDF $EPSTOPDFFLAGS ${SOURCE} --outfile=${TARGET}'


def exists(env):
    return 1