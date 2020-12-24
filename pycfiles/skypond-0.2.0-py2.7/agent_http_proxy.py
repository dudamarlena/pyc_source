# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/base/agent_http_proxy.py
# Compiled at: 2019-05-07 01:07:29
from __future__ import absolute_import
from .base_agent import Agent
import requests, json
REASONABLE_REACT_RESPONSE_LENGTH = 8
REASONABLE_INFO_RESPONSE_LENGTH = 1028

class AgentHTTPProxy(Agent):

    def __init__(self, agent_base_address):
        super().__init__()
        self.agent_base_address = agent_base_address

    def post(self, endpoint, payload):
        headers = {'content-type': 'application/json'}
        target = self.agent_base_address + '/' + endpoint
        r = requests.post(target, json=list(payload), timeout=0.5)
        response_length = len(r.content)
        if response_length <= REASONABLE_REACT_RESPONSE_LENGTH:
            return r.json()

    def get(self, endpoint):
        headers = {'content-type': 'application/json'}
        target = self.agent_base_address + '/' + endpoint
        r = requests.get(target, timeout=5)
        response_length = len(r.content)
        if response_length <= REASONABLE_INFO_RESPONSE_LENGTH:
            return r.json()

    def react(self, observation):
        return self.post('react', observation)

    def describe(self):
        return self.get('information')