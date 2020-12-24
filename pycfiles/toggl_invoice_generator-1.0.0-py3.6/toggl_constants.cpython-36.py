# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/toggl_invoice_generator/toggl_constants.py
# Compiled at: 2018-11-02 14:55:22
# Size of source mod 2**32: 1051 bytes
ENVFileTemplate = "\n#!/usr/bin/env bash\n\n# https://github.com/toggl/toggl_api_docs\nexport TOGGL_API_TOKEN=''\n\n# Sometimes you have a billable rate and a non-billable rate.\nexport BILLABLE_RATE='10.0'\nexport NON_BILLABLE_RATE='5.0'\nexport FULFILLMENT_DELAY='30'\n\n# Make sure to iterate the invoice number with each use\nexport INVOICE_NUMBER=space-needle-0\nexport OUTPUT_DIR=$PWD\nexport INVOICE_FILENAME='Invoice.pdf'\n\nexport SERVICE_PROVIDER='The Freemont Troll'\nexport SERVICE_PROVIDER_EMAIL='freemont-troll@jbcurtin.io'\nexport SERVICE_PROVIDER_PHONE=''\nexport SERVICE_PROVIDER_ADDRESS='Troll Ave N'\nexport SERVICE_PROVIDER_ADDRESS_TWO='#office'\nexport SERVICE_PROVIDER_CITY='Seattle'\nexport SERVICE_PROVIDER_STATE='WA'\nexport SERVICE_PROVIDER_POSTAL='98103'\n\nexport RECIPIENT='Seattle Space Needle'\nexport RECIPIENT_EMAIL='space-needle@jbcurtin.io'\nexport RECIPIENT_PHONE=''\nexport RECIPIENT_ADDRESS='400 Broad St'\nexport RECIPIENT_ADDRESS_TWO='#office'\nexport RECIPIENT_CITY='Seattle'\nexport RECIPIENT_STATE='WA'\nexport RECIPIENT_POSTAL='98109'\n"