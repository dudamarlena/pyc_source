# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/travis/Dropbox/work/texas/tx_tecreports/tx_tecreports/fetcher/base.py
# Compiled at: 2014-01-15 13:41:53
# Size of source mod 2**32: 702 bytes
import requests
from . import models
BASE_FILER_URL_TEMPLATE = 'http://www.ethics.state.tx.us/php/filer.php?acct={filer_id}'
BASE_URL_TEMPLATE = 'http://204.65.203.5/public/{report_id}noadd.csv'

def fetch_raw_report(report_id):
    return requests.get(BASE_URL_TEMPLATE.format(report_id=report_id))


def get_report(report_id):
    raw_report = fetch_raw_report(report_id)
    return models.Report(report_id=report_id, raw_report=raw_report)


def fetch_filing_list(filer_id):
    return requests.get(BASE_FILER_URL_TEMPLATE.format(filer_id=filer_id))


def get_filings_list(filer_id):
    raw_filing_list = fetch_filing_list(filer_id)
    return models.FilingList(raw_filing_list=raw_filing_list)