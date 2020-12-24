#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# setup.py -- Entrails setup script
#
# July 2014, Phil Connell
#
# Copyright 2014, Ensoft Ltd.
# -----------------------------------------------------------------------------

import distutils.core

distutils.core.setup(
    name="Entrails",
    version="1.1",
    description="Python call logging framework",
    author="Phil Connell, Ensoft Ltd",
    author_email="philc@ensoft.co.uk",
    url="https://launchpad.net/entrails",
    package_dir={"": "src", },
    packages=["entrails", ],
)

