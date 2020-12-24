# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/capture0_data/company_info.py
# Compiled at: 2016-09-25 17:48:19
# Size of source mod 2**32: 305 bytes
import random
from typing import List
from capture0_data.online_handles import get_companies, IndexCompany

def get_random_company_names() -> List[IndexCompany]:
    raw_companies = get_companies()
    random.shuffle(raw_companies)
    random_companies = raw_companies[:20]
    return random_companies