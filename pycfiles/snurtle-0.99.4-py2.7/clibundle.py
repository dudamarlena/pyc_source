# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/clibundle.py
# Compiled at: 2012-08-03 08:35:35
from snurtle.cmd2 import options, make_option

class CLIBundle(object):

    def _get_entity(self, objectid, expected_type=None, detail_level=0):
        callid = self.server.get_object_by_id(fetchid=objectid, detail=detail_level, callback=self.callback, feedback=self.pfeedback)
        response = self.get_response(callid)
        if not response:
            self.set_result('No response from server before timeout', error=True)
            return False
        if isinstance(response.payload, dict):
            if expected_type:
                if response.payload['entityname'] != expected_type:
                    self.set_result(('Specified object is not a "{0}", is a "{1}"').format(expected_type, response.payload['entityname']), error=True)
                    return False
            return response
        self.set_result(response)
        return False