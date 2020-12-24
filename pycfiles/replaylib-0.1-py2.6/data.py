# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/replaylib/data.py
# Compiled at: 2010-06-15 22:19:18
from collections import defaultdict

class ReplayDataResponse(object):

    def __init__(self):
        self.body_chunks = []

    def rec_start(self, version, status, reason, headers):
        self.version = version
        self.status = status
        self.reason = reason
        self.headers = headers

    def rec_body(self, s):
        self.body_chunks.append(s)

    @property
    def body(self):
        return ('').join(self.body_chunks)


class ReplayData(object):

    def __init__(self):
        self.map = defaultdict(list)
        self.playback_pos = defaultdict(int)

    def start_response(self, hash):
        resp = ReplayDataResponse()
        self.map[hash].append(resp)
        return resp

    def get_next_response(self, hash):
        pos = self.playback_pos[hash]
        response = self.map[hash][pos]
        self.playback_pos[hash] += 1
        return response