# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/txportal/simulator/handlers/reqinfo_handler.py
# Compiled at: 2016-03-18 12:19:39
from twisted.internet import defer
from txportal.packet import cmcc, huawei
from txportal.simulator.handlers import base_handler

class ReqInfoHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
        resp = cmcc.Portal.newMessage(cmcc.ACK_INFO, req.userIp, req.serialNo, req.reqId, secret=str(self.config.acagent.secret))
        return resp

    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(cmcc.ACK_INFO, req.userIp, req.serialNo, req.reqId, secret=str(self.config.acagent.secret))
        return resp

    def proc_huaweiv1(self, req, rundata):
        resp = huawei.Portal.newMessage(huawei.ACK_INFO, req.userIp, req.serialNo, req.reqId, str(self.config.acagent.secret))
        return defer.succeed(resp, rundata)

    def proc_huawev2(self, req, rundata):
        resp = huawei.Portal.newMessageV2(huawei.ACK_INFO, req.userIp, req.serialNo, req.reqId, str(self.config.acagent.secret), auth=req.auth)
        resp.auth_packet()
        return resp