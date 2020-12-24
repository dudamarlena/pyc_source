# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/amq_broker.py
# Compiled at: 2019-05-16 13:41:33
"""
AMQBroker - file ``/var/opt/amq-broker/*/etc/broker.xml``
=========================================================

Configuration of Active MQ Artemis brokers.
"""
from .. import XMLParser, parser
from insights.specs import Specs

@parser(Specs.amq_broker)
class AMQBroker(XMLParser):
    """
    Provides access to broker.xml files that are stored in the conventional
    location for Active MQ Artemis.

    Examples:
        >>> doc.get_elements(".//journal-pool-files", "urn:activemq:core")[0].text
        "10"
        >>> doc.get_elements(".//journal-type", "urn:activemq:core")[0].text
        "NIO"
    """
    pass