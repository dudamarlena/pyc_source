# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/multinode.py
# Compiled at: 2019-05-16 13:41:33
from insights import combiner
from insights.combiners.hostname import hostname
from insights.core.context import create_product
from insights.parsers.metadata import MetadataJson
from insights.specs import Specs

@combiner(MetadataJson, [hostname, Specs.machine_id])
def multinode_product(md, hn, machine_id):
    hn = hn.fqdn if hn else machine_id.content[0].rstrip()
    return create_product(md.data, hn)


@combiner(multinode_product)
def docker(product):
    if product and product.name == 'docker':
        return product


@combiner(multinode_product)
def OSP(product):
    if product and product.name == 'osp':
        return product


@combiner(multinode_product)
def RHEV(product):
    if product and product.name == 'rhev':
        return product


@combiner(multinode_product)
def RHEL(product):
    if product and product.name == 'rhel':
        return product