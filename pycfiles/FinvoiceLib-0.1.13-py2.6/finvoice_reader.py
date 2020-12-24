# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/reader/finvoice_reader.py
# Compiled at: 2010-03-24 05:47:13
from lxml import etree
from lxml import objectify
from pkg_resources import resource_stream
from finvoicelib.error import LxmlErrorWrapper
from finvoicelib.reader.message import Message
from finvoicelib.reader.xml_reader import FinvoiceXmlReader

class Reader(object):
    """

    Finvoice file may contain more than one message.

    Message consists of:
     * SOAP-Envelop (ebxml) (optional)
     * Finvoice-xml

    """
    errors = None
    messages = None
    dtd_resource = '../resources/Finvoice.dtd'

    def __init__(self, xml):
        if isinstance(xml, basestring):
            f = open(xml)
        else:
            f = xml
        self.errors = []
        self.messages = []
        r = FinvoiceXmlReader(f)
        for block in r:
            if block.soap:
                env = etree.XML(block.soap)
            else:
                env = None
            if block.payload:
                print '========NEW PAYLOAD ============='
                print block.payload
                xml_tree = objectify.XML(block.payload)
                msg = Message(xml_tree, env)
                if not self.validate(xml_tree):
                    print 'Invalid XML!'
                    msg.errors += self.errors
                self.messages.append(msg)

        return

    def validate(self, xml_tree):
        f = resource_stream(__name__, self.dtd_resource)
        dtd = etree.DTD(f)
        if dtd.validate(xml_tree):
            return True
        for error in dtd.error_log.filter_from_errors():
            self.errors.append(LxmlErrorWrapper(error))

        return False