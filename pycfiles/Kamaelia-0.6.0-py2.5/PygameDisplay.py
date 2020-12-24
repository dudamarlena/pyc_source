# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/PygameDisplay.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.UI.Pygame.Display import _PygameEventSource as ___PygameEventSource
from Kamaelia.UI.Pygame.Display import PygameDisplay as __PygameDisplay
Deprecate.deprecationWarning('Use Kamaelia.UI.Pygame.Display instead of Kamaelia.UI.PygameDisplay')
_PygameEventSource = Deprecate.makeClassStub(___PygameEventSource, 'Use Kamaelia.UI.Pygame.Display:_PygameEventSource instead of Kamaelia.UI.PygameDisplay:_PygameEventSource', 'WARN')
PygameDisplay = Deprecate.makeClassStub(__PygameDisplay, 'Use Kamaelia.UI.Pygame.Display:PygameDisplay instead of Kamaelia.UI.PygameDisplay:PygameDisplay', 'WARN')