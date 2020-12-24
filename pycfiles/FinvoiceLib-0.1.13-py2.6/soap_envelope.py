# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/soap_envelope.py
# Compiled at: 2010-03-24 05:43:08
from lxml import etree

class SoapEnvelope(object):
    seller_id = None
    seller_intermediator_id = None
    buyer_id = None
    buyer_intermediator_id = None

    def __init__(self, tree):
        ns = tree.nsmap.get('eb')

        def build_xpath(elem, role):
            return '//{%(N)s}%(elem)s/{%(N)s}PartyId[../{%(N)s}Role = "%(role)s"]/text()' % {'N': ns, 'elem': elem, 'role': role}

        get_seller_id = etree.ETXPath(build_xpath('From', 'Sender'))
        get_seller_intermed_id = etree.ETXPath(build_xpath('From', 'Intermediator'))
        get_buyer_id = etree.ETXPath(build_xpath('To', 'Receiver'))
        get_buyer_intermed_id = etree.ETXPath(build_xpath('To', 'Intermediator'))
        seller_id = get_seller_id(tree)
        if len(seller_id) > 0:
            self.seller_id = str(seller_id[0])
        seller_intermediator_id = get_seller_intermed_id(tree)
        if len(seller_intermediator_id) > 0:
            self.seller_intermediator_id = seller_intermediator_id[0]
        buyer_id = get_buyer_id(tree)
        if len(buyer_id) > 0:
            self.buyer_id = str(buyer_id[0])
        buyer_intermediator_id = get_buyer_intermed_id(tree)
        if len(buyer_intermediator_id) > 0:
            self.buyer_intermediator_id = buyer_intermediator_id[0]