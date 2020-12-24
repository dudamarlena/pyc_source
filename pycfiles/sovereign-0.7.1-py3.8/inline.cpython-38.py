# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/sources/inline.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 883 bytes
"""
Inline Source
-------------

Example configuration (YAML):

.. code-block:: yaml

   sources:
     - type: inline
       config:
         instances:
           - instance_id: my_service
             service_clusters:
               - P2
             parameters:
               upstream_address:
                 - address: service.domain.com
                   region: us-east-1
             plan_id: 7d57270a-0348-58d3-829d-447a98fe98d5
"""
from sovereign.sources.lib import Source

class Inline(Source):

    def __init__(self, config, scope='default'):
        super(Inline, self).__init__(config, scope)
        try:
            self.instances = config['instances']
        except KeyError:
            raise KeyError('Inline source config must contain "instances"')

    def get(self):
        """ Returns the data passed via configuration """
        return self.instances