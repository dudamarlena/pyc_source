# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/erd.py
# Compiled at: 2016-02-12 12:18:44
from eralchemy import render_er
from sqlalchemy import MetaData
from dmsa.utility import get_model_json
from dmsa.makers import make_model

def write(model, model_version, output, service):
    """Generate entity relationship diagram for the data model specified.

    Arguments:
      model          Model to generate DDL for.
      model_version  Model version to generate DDL for.
      output         Output file for ERD.
      service        Base URL of the data models service to use.
    """
    metadata = MetaData()
    model_json = get_model_json(model, model_version, service)
    make_model(model_json, metadata)
    render_er(metadata, output)


if __name__ == '__main__':
    main()