# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\__init__.py
# Compiled at: 2018-10-07 19:25:17
# Size of source mod 2**32: 1738 bytes
"""
Copyright (c) 2018 Versentiedge LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from sc2gameLobby import gameConfig
from sc2gameLobby import gameConstants
from sc2gameLobby import genericObservation as go
from sc2gameLobby import hostGame
from sc2gameLobby import joinGame
from sc2gameLobby import versions
from sc2gameLobby.__version__ import *
config = gameConfig.Config
host = hostGame.run
join = joinGame.playerJoin
clear = gameConfig.clearConfigs
active = gameConfig.activeConfigs

def updateVersion(**kwargs):
    """add/update record data using kwargs params for new keys/values"""
    versions.handle.save(kwargs)