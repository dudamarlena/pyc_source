# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/plugins/builtin.py
# Compiled at: 2014-09-06 21:58:19
"""
Lists builtin plugins.
"""
plugins = []
builtins = (
 ('nose.plugins.attrib', 'AttributeSelector'),
 ('nose.plugins.capture', 'Capture'),
 ('nose.plugins.logcapture', 'LogCapture'),
 ('nose.plugins.cover', 'Coverage'),
 ('nose.plugins.debug', 'Pdb'),
 ('nose.plugins.deprecated', 'Deprecated'),
 ('nose.plugins.doctests', 'Doctest'),
 ('nose.plugins.isolate', 'IsolationPlugin'),
 ('nose.plugins.failuredetail', 'FailureDetail'),
 ('nose.plugins.prof', 'Profile'),
 ('nose.plugins.skip', 'Skip'),
 ('nose.plugins.testid', 'TestId'),
 ('nose.plugins.multiprocess', 'MultiProcess'),
 ('nose.plugins.xunit', 'Xunit'),
 ('nose.plugins.allmodules', 'AllModules'),
 ('nose.plugins.collect', 'CollectOnly'))
for module, cls in builtins:
    try:
        plugmod = __import__(module, globals(), locals(), [cls])
    except KeyboardInterrupt:
        raise
    except:
        continue

    plug = getattr(plugmod, cls)
    plugins.append(plug)
    globals()[cls] = plug