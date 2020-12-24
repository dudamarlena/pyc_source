# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/controllers/getprebeliever.py
# Compiled at: 2008-02-28 15:45:46
import logging, xmlrpclib, pylons
from pylons import request
from pylons.controllers import XMLRPCController
from salvationfocus.lib.base import *
from salvationfocus.model import Session
from salvationfocus.model.Prebeliever import Prebeliever
from datetime import datetime
log = logging.getLogger(__name__)

class GetprebelieverController(XMLRPCController):

    def get_prebeliever(self):
        session = Session()
        pre = session.query(Prebeliever).filter_by(last_viewed=None).order_by(Prebeliever.date_entered.asc()).first()
        if pre == None:
            pre = session.query(Prebeliever).order_by(Prebeliever.last_viewed.asc()).first()
            if pre == None:
                result = {}
                result['error'] = 'No prebelievers'
                session.close()
                return result
        pre.last_viewed = datetime.now()
        if pre.times_viewed:
            pre.times_viewed = pre.times_viewed + 1
        else:
            pre.times_viewed = 1
        session.commit()
        session.close()
        return pre.toDictionary()