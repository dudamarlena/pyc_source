# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ctstore/model.py
# Compiled at: 2016-07-08 01:04:39
from cantools import db

class Product(db.ModelBase):
    name = db.String()
    description = db.Text()
    image = db.Binary()
    price = db.Float()