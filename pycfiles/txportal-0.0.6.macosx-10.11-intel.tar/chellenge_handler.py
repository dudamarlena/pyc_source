# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/txportal/simulator/handlers/chellenge_handler.py
# Compiled at: 2016-03-18 12:19:39
from twisted.internet import defer
from txportal.packet import cmcc, huawei, pktutils
from txportal.simulator.handlers import base_handler

class ChellengeHandler(base_handler.BasicHandler):

    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(cmcc.ACK_CHALLENGE, req.userIp, req.serialNo, cmcc.CurrentSN(), secret=self.secret)
        resp.attrNum = 1
        challenge = pktutils.CreateChallenge()
        resp.attrs = [
         (
          3, challenge)]
        rundata['challenges'][resp.sid] = challenge
        return resp

    def proc_huaweiv2(self, req, rundata):
        resp = huawei.PortalV2.newMessage(huawei.ACK_CHALLENGE, req.userIp, req.serialNo, huawei.CurrentSN(), self.secret, auth=req.auth, chap=req.isChap == 0)
        resp.attrNum = 1
        challenge = pktutils.CreateChallenge()
        resp.attrs = [
         (
          3, challenge)]
        resp.auth_packet()
        rundata['challenges'][resp.sid] = challenge
        return resp