# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/rfc3411.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto import rfc1157, rfc1905
readClassPDUs = {rfc1157.GetRequestPDU.tagSet: 1, rfc1157.GetNextRequestPDU.tagSet: 1, rfc1905.GetRequestPDU.tagSet: 1, rfc1905.GetNextRequestPDU.tagSet: 1, rfc1905.GetBulkRequestPDU.tagSet: 1}
writeClassPDUs = {rfc1157.SetRequestPDU.tagSet: 1, rfc1905.SetRequestPDU.tagSet: 1}
responseClassPDUs = {rfc1157.GetResponsePDU.tagSet: 1, rfc1905.ResponsePDU.tagSet: 1, rfc1905.ReportPDU.tagSet: 1}
notificationClassPDUs = {rfc1157.TrapPDU.tagSet: 1, rfc1905.SNMPv2TrapPDU.tagSet: 1, rfc1905.InformRequestPDU.tagSet: 1}
internalClassPDUs = {rfc1905.ReportPDU.tagSet: 1}
confirmedClassPDUs = {rfc1157.GetRequestPDU.tagSet: 1, rfc1157.GetNextRequestPDU.tagSet: 1, rfc1157.SetRequestPDU.tagSet: 1, rfc1905.GetRequestPDU.tagSet: 1, rfc1905.GetNextRequestPDU.tagSet: 1, rfc1905.GetBulkRequestPDU.tagSet: 1, rfc1905.SetRequestPDU.tagSet: 1, rfc1905.InformRequestPDU.tagSet: 1}
unconfirmedClassPDUs = {rfc1157.GetResponsePDU.tagSet: 1, rfc1905.ResponsePDU.tagSet: 1, rfc1157.TrapPDU.tagSet: 1, rfc1905.ReportPDU.tagSet: 1, rfc1905.SNMPv2TrapPDU.tagSet: 1}