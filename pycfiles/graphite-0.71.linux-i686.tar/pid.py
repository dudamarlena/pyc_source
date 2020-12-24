# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/graphite/pid.py
# Compiled at: 2009-01-26 15:41:45
"""This is a compatibility module so that graphite
can use either sping (http://sping.sourceforge.net)
or piddle (http://piddle.sourceforge.net).
"""
try:
    import sping
    _s = True
except ImportError:
    _s = False

if not _s:
    try:
        import piddle
    except ImportError:
        raise ImportError, 'Cannot import either sping or piddle.'

if _s:
    from sping import *
    try:
        import sping.PS as piddlePS
    except ImportError:
        pass
    else:
        try:
            import sping.PDF as piddlePDF
        except ImportError:
            pass
        else:
            try:
                import sping.PIL as piddlePIL
            except ImportError:
                pass
            else:
                try:
                    import sping.SVG as piddleSVG
                except ImportError:
                    pass
                else:
                    try:
                        import sping.TK as piddleTK
                    except ImportError:
                        pass
                    else:
                        try:
                            import sping.WX as piddleWX
                        except ImportError:
                            pass
                        else:
                            Font = sping.pid.Font
                            try:
                                import sping.stringformat as stringformat
                            except ImportError:
                                pass

else:
    colors = piddle
    Font = piddle.Font
    import piddlePS, piddlePDF
    try:
        import piddleVCR
    except ImportError:
        pass

    try:
        import piddleTK
    except ImportError:
        pass

    try:
        import piddleQD
    except ImportError:
        pass

    try:
        import piddlePIL
    except ImportError:
        pass

    try:
        import piddleGL
    except ImportError:
        pass

    try:
        import piddleSVG
    except ImportError:
        pass

    try:
        import piddleSVG
    except ImportError:
        pass

    import piddleFIG, piddleAI, stringformat
del _s