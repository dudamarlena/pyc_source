# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/models/models.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 2809 bytes
"""
Dit bestand bevat een OE Base Model dat in alle OE toepassingen kan worden gebruikt.

Het voordeel van een generieke Base is dat we op deze werkwijze per toepassing 1 zelfde
Base kunnen gebruiken voor al de aanwezige Models.
Dit omvat zowel Models van de applicatie zelf,
als de Models uit libraries zoals oe_utils en oe_geoutils.

Hier kan eveneens de nodige generieke metadata aan ons Base Model worden meegegeven.
Hiervoor kan sqlalchemy.schema.MetaData worden gebruikt
"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
Base = declarative_base()

class Wijziging(Base):
    __doc__ = '\n    A database table configuration object.\n\n    This table contains information about the audit of a resource object.\n\n    This object will not create the db table object.\n    To create the table insert following code in the alembic migration file\n\n    `alembic revision -m "wijzigingshistoriek"`\n\n\n    from alembic import op\n    import sqlalchemy as sa\n    from sqlalchemy.dialects.postgresql import JSON\n    from sqlalchemy.sql import func\n\n\n    def upgrade():\n        op.create_table(\n            "wijzigingshistoriek",\n            sa.Column("versie", sa.String(), nullable=False),\n            sa.Column("resource_object_id", sa.Integer(), nullable=False),\n            sa.Column(\n                "updated_at",\n                sa.DateTime(timezone=True),\n                default=func.now(),\n                nullable=False,\n            ),\n            sa.Column("updated_by", sa.String(length=255), nullable=False),\n            sa.Column("updated_by_omschrijving", sa.String(length=255), nullable=False),\n            sa.Column("resource_object_json", JSON, nullable=True),\n            sa.Column("actie", sa.String(length=50), nullable=False),\n            sa.PrimaryKeyConstraint("versie", name="wijzigingshistoriek_pk"),\n        )\n\n        op.execute("GRANT ALL ON wijzigingshistoriek to <user>_dml")\n\n\n    def downgrade():\n        op.drop_table("wijzigingshistoriek")\n    '
    __tablename__ = 'wijzigingshistoriek'
    versie = Column((String(64)), primary_key=True)
    resource_object_id = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=(func.now()), nullable=False)
    updated_by = Column((String(255)),
      default='https://id.erfgoed.net/actoren/501', nullable=False)
    updated_by_omschrijving = Column((String(255)),
      default='Onroerend Erfgoed', nullable=False)
    resource_object_json = Column((MutableDict.as_mutable(JSON())), nullable=True)
    actie = Column((String(50)), nullable=False)