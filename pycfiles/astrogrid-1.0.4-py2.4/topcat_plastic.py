# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/topcat_plastic.py
# Compiled at: 2008-06-05 09:27:47
"""
This example shows how to send a message to TOPCAT without running the Astrogrid AR.
When launching TOPCAT go to:

     Interop -> Start External Plastic Hub 

before running this script. Then call it using:

  python topcat_plastic.py 33.5 -3.5 0.1

where first two numbers are RA, DEC in degrees and third is radius in degrees.

"""
import os, sys
try:
    import xmlrpclib
except:
    print 'Need Python version 2.4 or larger.'
    sys.exit()

_PLASTIC_STARTFILE = os.path.expanduser('~/.plastic')
try:
    plastic_file = file(_PLASTIC_STARTFILE)
except:
    print 'Plastic Hub not found.\nPlease start the external plastic hub: TOPCAT -> Interop -> Start External Plastic Hub'
    sys.exit()

props = plastic_file.readlines()
props = [ s.split('=') for s in props if s.startswith('plastic.xmlrpc.url') ]
xmlrpcurl = props[0][1].rstrip().replace('\\', '')
hub = xmlrpclib.Server(xmlrpcurl)
myId = hub.plastic.hub.registerNoCallBack('Python Script')
(ra, dec, rad) = sys.argv[1:]
tables = ['swire_xmm', 'swire_lockman']
for t in tables:
    print 'Querying %s (%s, %s, %s)' % (t, ra, dec, rad)
    u = 'http://bohr.pact.cpes.susx.ac.uk:8080/swire/SubmitCone?DSACATTAB=SWIRE.%s&RA=%s&DEC=%s&SR=%s' % (t, ra, dec, rad)
    hub.plastic.hub.request(myId, 'ivo://votech.org/votable/loadFromURL', [u, u])

hub.plastic.hub.unregister(myId)