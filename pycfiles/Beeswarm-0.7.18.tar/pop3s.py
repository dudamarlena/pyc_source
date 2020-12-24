# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/pop3s.py
# Compiled at: 2016-11-12 07:38:04
import logging
from beeswarm.drones.honeypot.capabilities.pop3 import Pop3
from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase
logger = logging.getLogger(__name__)

class Pop3S(Pop3, HandlerBase):
    """
    This class will get wrapped in SSL. This is possible because we by convention  wrap
    all capabilities that ends with the letter 's' in SSL."""
    pass