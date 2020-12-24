# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/google_sheets/google_sheets_connector.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 3008 bytes
from contextlib import suppress
from typing import Optional
import pandas as pd
from pydantic import Field, create_model
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource, strlist_to_enum

class GoogleSheetsDataSource(ToucanDataSource):
    spreadsheet_id: str = Field(...,
      title='ID of the spreadsheet',
      description='Can be found in your URL: https://docs.google.com/spreadsheets/d/<ID of the spreadsheet>/...')
    sheet = Field(None,
      title='Sheet title', description='Title of the desired sheet')
    sheet: Optional[str]
    header_row: int = Field(0,
      title='Header row', description='Row of the header of the spreadsheet')

    @classmethod
    def get_form(cls, connector: 'GoogleSheetsConnector', current_config):
        constraints = {}
        with suppress(Exception):
            data = connector.bearer_oauth_get_endpoint(current_config['spreadsheet_id'])
            available_sheets = [str(x['properties']['title']) for x in data['sheets']]
            constraints['sheet'] = strlist_to_enum('sheet', available_sheets)
        return create_model('FormSchema', **constraints, **{'__base__': cls}).schema()


class GoogleSheetsConnector(ToucanConnector):
    __doc__ = '\n    This is a connector for [GoogleSheets](https://developers.google.com/sheets/api/reference/rest)\n    using [Bearer.sh](https://app.bearer.sh/)\n    '
    data_source_model: GoogleSheetsDataSource
    bearer_integration = 'google_sheets'
    bearer_auth_id: str

    def _retrieve_data(self, data_source: GoogleSheetsDataSource) -> pd.DataFrame:
        if data_source.sheet is None:
            data = self.bearer_oauth_get_endpoint(data_source.spreadsheet_id)
            available_sheets = [str(x['properties']['title']) for x in data['sheets']]
            data_source.sheet = available_sheets[0]
        read_sheet_endpoint = f"{data_source.spreadsheet_id}/values/{data_source.sheet}"
        data = self.bearer_oauth_get_endpoint(read_sheet_endpoint)['values']
        df = pd.DataFrame(data)
        df.columns = [name or index for index, name in enumerate(df.iloc[data_source.header_row])]
        df = df[data_source.header_row + 1:]
        return df