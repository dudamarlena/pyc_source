# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/MarshallComponent.py
# Compiled at: 2008-10-19 12:19:52
"""======================================
Legacy stub for BasicMarshallComponent
======================================

The functionality of this component has been superceeded by the Marshaller and
DeMarshaller components in Kamaelia.Util.Marshalling. Please use these in
preference.

This component contains both marshalling and demarshalling facilities. It is
a thin wrapper combining a Marshalling and DeMarshalling component.

Example Usage
-------------

None at present.

How does it work?
-----------------

Behaviour is consistent with that of Kamaelia.Util.Marshalling, except that the
"inbox" inbox and "outbox" outbox are not used.

Marshall data by sending it to the "marshall" inbox. The marshalled data is
sent to the "marshalled" outbox.

Demarshall data by sending it to the "demarshall" inbox. The marshalled data is
sent to the "demarshalled" outbox.

"""
from Kamaelia.Chassis.Graphline import Graphline
from Kamaelia.Util.Marshalling import Marshaller, DeMarshaller

def BasicMarshallComponent(klass):
    return Graphline(marsh=Marshaller(klass), demarsh=DeMarshaller(klass), linkages={('self', 'marshall'): ('marsh', 'inbox'), 
       ('marsh', 'outbox'): ('self', 'marshalled'), 
       ('self', 'demarshall'): ('demarsh', 'inbox'), 
       ('demarsh', 'outbox'): ('self', 'demarshalled'), 
       ('self', 'control'): ('marsh', 'control'), 
       ('marsh', 'signal'): ('demarsh', 'control'), 
       ('demarsh', 'signal'): ('self', 'signal')})


__kamaelia_prefabs__ = (
 BasicMarshallComponent,)
if __name__ == '__main__':
    print 'no test harness (NASTY)'
    print 'Sample Test Harness could probably make us of MimeDict as an example'
    print '\nProbable usage:\n\nfrom Kamaelia.Support.Data.MimeDict import MimeDict\n\nclass MimeDictMarshaller(Kamaelia.Util.MarshallComponent.MarshallComponent):\n    def __init__(self,*argv,**argd):\n        super(MimeDictMarshaller, self).__init__(MimeDict, *argv,**argd)\n\nCreate components after that thus:\n\nmds = MimeDictMarshaller()\n\nOr:\ndef MarshallerFactory(klass):\n   class newclass(Kamaelia.Util.MarshallComponent.MarshallComponent):\n      def __init__(self,*argv,**argd):\n         super(newclass, self).__init__(klass, *argv,**argd)\n   return newclass\n\nMimeDictMarshaller=MarshallerFactory(MimeDict)\n\nmds = MimeDictMarshaller()\n\n'