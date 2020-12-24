# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/cost_tracking.py
# Compiled at: 2016-12-16 07:39:01
from django.utils.text import slugify
from nodeconductor.cost_tracking import CostTrackingRegister, CostTrackingStrategy, ConsumableItem
from . import models

class DeploymentStrategy(CostTrackingStrategy):
    resource_class = models.Deployment

    class Types(object):
        TYPE = 'type'
        FLAVOR = 'flavor'
        STORAGE = 'storage'

    @classmethod
    def get_consumable_items(cls):
        for flavor in models.Flavor.objects.all():
            yield ConsumableItem(item_type=cls.Types.FLAVOR, key=flavor.name, name='Flavor: %s' % flavor.name)

        for v, _ in models.Deployment.Version.CHOICES:
            for t, _ in models.Deployment.Type.CHOICES:
                d = models.Deployment(db_type=t, db_version=v)
                key = slugify(d.db_version_type)
                yield ConsumableItem(item_type=cls.Types.TYPE, key=key)

        yield ConsumableItem(item_type=cls.Types.STORAGE, key='1 GB')

    @classmethod
    def get_configuration(cls, deployment):
        return {ConsumableItem(item_type=cls.Types.TYPE, key=slugify(deployment.db_version_type)): 1, 
           ConsumableItem(item_type=cls.Types.FLAVOR, key=deployment.flavor.name): 1, 
           ConsumableItem(item_type=cls.Types.STORAGE, key='1 GB'): deployment.db_size}


CostTrackingRegister.register_strategy(DeploymentStrategy)