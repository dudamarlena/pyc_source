# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/instrument_api.py
# Compiled at: 2019-11-15 04:27:31
# Size of source mod 2**32: 1325 bytes
"""InstrumentApi module class"""
import json
from common.base import Base

class InstrumentApi(Base):

    def get_instrument_by_id_api(self, instrument_id):
        api_url = self._InstrumentApi__get_api_url(instrument_id)
        return self.api_get(api_url, params={})

    def get_all_instruments_api(self):
        api_url = self._InstrumentApi__get_api_url()
        return self.api_get(api_url, params={})

    def get_all_instruments_by_identifier_api(self, identifier):
        api_url = self._InstrumentApi__get_api_url()
        return self.api_get(api_url, params={'identifier': identifier})

    def get_all_instruments_by_facility_id_api(self, facility_id):
        api_url = self._InstrumentApi__get_api_url()
        return self.api_get(api_url, params={'facility_id': facility_id})

    def get_all_instruments_by_topic_id_api(self, topic_id):
        api_url = self._InstrumentApi__get_api_url()
        return self.api_get(api_url, params={'topic_id': topic_id})

    def get_instrument_active_proposal_api(self, instrument_id):
        api_specific = '{0}/active_proposal'.format(instrument_id)
        api_url = self._InstrumentApi__get_api_url(api_specific)
        return self.api_get(api_url, params={})

    def __get_api_url(self, api_specifics=''):
        model_name = 'instruments/'
        return self.get_api_url(model_name, api_specifics)