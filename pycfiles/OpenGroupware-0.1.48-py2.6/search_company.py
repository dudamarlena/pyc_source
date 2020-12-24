# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/address/search_company.py
# Compiled at: 2012-10-12 07:02:39
import sys
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import SearchCommand

class SearchCompany(SearchCommand):
    mode = None

    def __init__(self):
        SearchCommand.__init__(self)
        self._revolve = False

    def prepare(self, ctx, **params):
        self._cv = []
        SearchCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        SearchCommand.parse_parameters(self, **params)