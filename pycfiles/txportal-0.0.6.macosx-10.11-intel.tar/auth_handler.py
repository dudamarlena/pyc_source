# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/txportal/simulator/handlers/auth_handler.py
# Compiled at: 2016-03-18 12:19:39
import struct
from twisted.internet import defer
from txportal.packet import cmcc, huawei
from txportal.simulator.handlers import base_handler
import functools

class AuthHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
        resp = cmcc.Portal.newMessage(cmcc.ACK_AUTH, req.userIp, req.serialNo, req.reqId, secret=self.secret)
        resp.attrNum = 1
        resp.attrs = [
         (5, 'success')]
        return resp

    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(cmcc.ACK_AUTH, req.userIp, req.serialNo, req.reqId, secret=self.secret)
        resp.attrNum = 1
        resp.attrs = [
         (5, 'success')]
        return resp

    def proc_huaweiv1(self, req, rundata):
        resp = huawei.Portal.newMessage(huawei.ACK_AUTH, req.userIp, req.serialNo, req.reqId, secret=self.secret)
        resp.attrNum = 1
        resp.attrs = [
         (5, 'success')]
        return resp

    @defer.inlineCallbacks
    def proc_huaweiv2(self, req, rundata):
        resp = huawei.PortalV2.newMessage(huawei.ACK_AUTH, req.userIp, req.serialNo, req.reqId, self.secret, auth=req.auth, chap=req.isChap == 0)
        resp.attrNum = 1
        resp.attrs = [
         (5, 'success')]
        resp.auth_packet()
        return resp