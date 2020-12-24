# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/models/meta.py
# Compiled at: 2019-06-18 07:34:37
# Size of source mod 2**32: 563 bytes
"""
Dit bestand bevat een OE Base Model dat in alle OE toepassingen kan worden gebruikt. Het voordeel van een generieke
Base is dat we op deze werkwijze per toepassing 1 zelfde Base kunnen gebruiken voor al de aanwezige Models.
Dit omvat zowel Models van de applicatie zelf, als de Models uit libraries zoals oe_utils en oe_geoutils.

Hier kan eveneens de nodige generieke metadata aan ons Base Model worden meegegeven.
Hiervoor kan sqlalchemy.schema.MetaData worden gebruikt
"""
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()