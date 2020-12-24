# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_objectify.py
# Compiled at: 2015-04-13 16:10:48
"""Make sure xml_pickle and xml_objectify play nicely together --dqm
Note that xml_pickle no longer has any builtin knowledge of
xml_objectify -- used to be necessary to workaround circular refs (fpm)"""
import gnosis.xml.objectify as xo, gnosis.xml.pickle as xp
from StringIO import StringIO
import funcs
funcs.set_parser()
xml = '<?xml version="1.0"?>\n<!DOCTYPE Spam SYSTEM "spam.dtd" >\n<Spam>\n  <Eggs>Some text about eggs.</Eggs>\n  <MoreSpam>Ode to Spam</MoreSpam>\n</Spam>\n'
fh = StringIO(xml)
o = xo.make_instance(xml)
s = xp.dumps(o)
o2 = xp.loads(s)
if o.Eggs.PCDATA != o2.Eggs.PCDATA or o.MoreSpam.PCDATA != o2.MoreSpam.PCDATA:
    raise 'ERROR(1)'
print '** OK **'