# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhn_entitlement_cert_xml.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.rhn_entitlement_cert_xml import RHNCertConf
xml_content = '\n<?xml version="1.0" encoding="UTF-8"?>\n<rhn-cert version="0.1">\n  <rhn-cert-field name="product">RHN-SATELLITE-001</rhn-cert-field>\n  <rhn-cert-field name="owner">Clay\'s Precious Satellite</rhn-cert-field>\n  <rhn-cert-field name="issued">2005-01-11 00:00:00</rhn-cert-field>\n  <rhn-cert-field name="expires">2005-03-11 00:00:00</rhn-cert-field>\n  <rhn-cert-field name="slots">30</rhn-cert-field>\n  <rhn-cert-field name="provisioning-slots">30</rhn-cert-field>\n  <rhn-cert-field name="nonlinux-slots">30</rhn-cert-field>\n  <rhn-cert-field name="channel-families" quantity="10" family="rhel-cluster"/>\n  <rhn-cert-field name="channel-families" quantity="30" family="rhel-ws-extras"/>\n  <rhn-cert-field name="channel-families" quantity="10" family="rhel-gfs"/>\n  <rhn-cert-field name="channel-families" quantity="10" family="rhel-es-extras"/>\n  <rhn-cert-field name="channel-families" quantity="40" family="rhel-as"/>\n  <rhn-cert-field name="channel-families" quantity="30" family="rhn-tools"/>\n  <rhn-cert-field name="channel-families" quantity="102" flex="0" family="sam-rhel-server-6"/>\n  <rhn-cert-field name="channel-families" quantity="102" flex="51" family="cf-tools-5-beta"/>\n  <rhn-cert-field name="satellite-version">5.2</rhn-cert-field>\n  <rhn-cert-field name="generation">2</rhn-cert-field>\n  <rhn-cert-signature>\n-----BEGIN PGP SIGNATURE-----\nVersion: Crypt::OpenPGP 1.03\n\niQBGBAARAwAGBQJCAG7yAAoJEJ5yna8GlHkysOkAn07qmlUrkGKs7/5yb8H/nboG\nmhHkAJ9wdmqOeKfcBa3IUDL53oNMEBP/dg==\n=0Kv7\n-----END PGP SIGNATURE-----\n</rhn-cert-signature>\n</rhn-cert>\n'

def test_match():
    result = RHNCertConf(context_wrap(xml_content, path='/etc/sysconfig/rhn/rhn_entitlement_cert_xml'))
    assert result.get('product') == 'RHN-SATELLITE-001'
    assert result.get('channel-families').get('rhel-cluster') == {'quantity': '10'}
    assert result.file_name == 'rhn_entitlement_cert_xml'