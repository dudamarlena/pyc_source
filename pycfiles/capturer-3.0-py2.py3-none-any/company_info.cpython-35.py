# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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