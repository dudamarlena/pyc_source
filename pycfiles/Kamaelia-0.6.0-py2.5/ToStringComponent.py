# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/ToStringComponent.py
# Compiled at: 2008-10-19 12:19:52
"""This is a deprecation stub, due for later removal.
"""
import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.Util.Stringify import Stringify as __Stringify
Deprecate.deprecationWarning('Use Kamaelia.Util.Stringify instead of Kamaelia.Util.ToStringComponent')
ToStringComponent = Deprecate.makeClassStub(__Stringify, 'Use Kamaelia.Util.Stringify:Stringify instead of Kamaelia.Util.ToStringComponent:ToStringComponent', 'WARN')