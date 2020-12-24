# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/salesforce_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 12414 bytes
__doc__ = '\nThis module contains a Salesforce Hook\nwhich allows you to connect to your Salesforce instance,\nretrieve data from it, and write that data to a file\nfor other uses.\n\nNOTE:   this hook also relies on the simple_salesforce package:\n        https://github.com/simple-salesforce/simple-salesforce\n'
from simple_salesforce import Salesforce
from airflow.hooks.base_hook import BaseHook
import json, pandas as pd, time
from airflow.utils.log.logging_mixin import LoggingMixin

class SalesforceHook(BaseHook):

    def __init__(self, conn_id, *args, **kwargs):
        """
        Create new connection to Salesforce
        and allows you to pull data out of SFDC and save it to a file.

        You can then use that file with other
        Airflow operators to move the data into another data source

        :param conn_id:     the name of the connection that has the parameters
                            we need to connect to Salesforce.
                            The connection should be type `http` and include a
                            user's security token in the `Extras` field.
        .. note::
            For the HTTP connection type, you can include a
            JSON structure in the `Extras` field.
            We need a user's security token to connect to Salesforce.
            So we define it in the `Extras` field as:
                `{"security_token":"YOUR_SECURITY_TOKEN"}`
        """
        self.conn_id = conn_id
        self._args = args
        self._kwargs = kwargs
        self.connection = self.get_connection(conn_id)
        self.extras = self.connection.extra_dejson

    def sign_in(self):
        """
        Sign into Salesforce.

        If we have already signed it, this will just return the original object
        """
        if hasattr(self, 'sf'):
            return self.sf
        else:
            sf = Salesforce(username=(self.connection.login),
              password=(self.connection.password),
              security_token=(self.extras['security_token']),
              instance_url=(self.connection.host),
              sandbox=(self.extras.get('sandbox', False)))
            self.sf = sf
            return sf

    def make_query(self, query):
        """
        Make a query to Salesforce.  Returns result in dictionary

        :param query:    The query to make to Salesforce
        """
        self.sign_in()
        self.log.info('Querying for all objects')
        query = self.sf.query_all(query)
        self.log.info('Received results: Total size: %s; Done: %s', query['totalSize'], query['done'])
        query = json.loads(json.dumps(query))
        return query

    def describe_object(self, obj):
        """
        Get the description of an object from Salesforce.

        This description is the object's schema
        and some extra metadata that Salesforce stores for each object

        :param obj:     Name of the Salesforce object
                        that we are getting a description of.
        """
        self.sign_in()
        return json.loads(json.dumps(self.sf.__getattr__(obj).describe()))

    def get_available_fields(self, obj):
        """
        Get a list of all available fields for an object.

        This only returns the names of the fields.
        """
        self.sign_in()
        desc = self.describe_object(obj)
        return [f['name'] for f in desc['fields']]

    @staticmethod
    def _build_field_list(fields):
        return ','.join(fields)

    def get_object_from_salesforce(self, obj, fields):
        """
        Get all instances of the `object` from Salesforce.
        For each model, only get the fields specified in fields.

        All we really do underneath the hood is run:
            SELECT <fields> FROM <obj>;
        """
        field_string = self._build_field_list(fields)
        query = 'SELECT {0} FROM {1}'.format(field_string, obj)
        self.log.info('Making query to Salesforce: %s', query if len(query) < 30 else ' ... '.join([query[:15], query[-15:]]))
        return self.make_query(query)

    @classmethod
    def _to_timestamp(cls, col):
        """
        Convert a column of a dataframe to UNIX timestamps if applicable

        :param col:     A Series object representing a column of a dataframe.
        """
        try:
            col = pd.to_datetime(col)
        except ValueError:
            log = LoggingMixin().log
            log.warning('Could not convert field to timestamps: %s', col.name)
            return col
        else:
            converted = []
            for i in col:
                try:
                    converted.append(i.timestamp())
                except ValueError:
                    converted.append(pd.np.NaN)
                except AttributeError:
                    converted.append(pd.np.NaN)

            return pd.Series(converted, index=(col.index))

    def write_object_to_file(self, query_results, filename, fmt='csv', coerce_to_timestamp=False, record_time_added=False):
        """
        Write query results to file.

        Acceptable formats are:
            - csv:
                comma-separated-values file.  This is the default format.
            - json:
                JSON array.  Each element in the array is a different row.
            - ndjson:
                JSON array but each element is new-line delimited
                instead of comma delimited like in `json`

        This requires a significant amount of cleanup.
        Pandas doesn't handle output to CSV and json in a uniform way.
        This is especially painful for datetime types.
        Pandas wants to write them as strings in CSV,
        but as millisecond Unix timestamps.

        By default, this function will try and leave all values as
        they are represented in Salesforce.
        You use the `coerce_to_timestamp` flag to force all datetimes
        to become Unix timestamps (UTC).
        This is can be greatly beneficial as it will make all of your
        datetime fields look the same,
        and makes it easier to work with in other database environments

        :param query_results:       the results from a SQL query
        :param filename:            the name of the file where the data
                                    should be dumped to
        :param fmt:                 the format you want the output in.
                                    *Default:* csv.
        :param coerce_to_timestamp: True if you want all datetime fields to be
                                    converted into Unix timestamps.
                                    False if you want them to be left in the
                                    same format as they were in Salesforce.
                                    Leaving the value as False will result
                                    in datetimes being strings.
                                    *Defaults to False*
        :param record_time_added:   *(optional)* True if you want to add a
                                    Unix timestamp field to the resulting data
                                    that marks when the data
                                    was fetched from Salesforce.
                                    *Default: False*.
        """
        fmt = fmt.lower()
        if fmt not in ('csv', 'json', 'ndjson'):
            raise ValueError('Format value is not recognized: {0}'.format(fmt))
        df = pd.DataFrame.from_records(query_results, exclude=['attributes'])
        df.columns = [c.lower() for c in df.columns]
        if coerce_to_timestamp:
            if df.shape[0] > 0:
                object_name = query_results[0]['attributes']['type']
                self.log.info('Coercing timestamps for: %s', object_name)
                schema = self.describe_object(object_name)
                possible_timestamp_cols = [i['name'].lower() for i in schema['fields'] if i['type'] in ('date',
                                                                                                        'datetime') if i['name'].lower() in df.columns]
                df[possible_timestamp_cols] = df[possible_timestamp_cols].apply(lambda x: self._to_timestamp(x))
        if record_time_added:
            fetched_time = time.time()
            df['time_fetched_from_salesforce'] = fetched_time
        if fmt == 'csv':
            self.log.info('Cleaning data and writing to CSV')
            possible_strings = df.columns[(df.dtypes == 'object')]
            df[possible_strings] = df[possible_strings].apply(lambda x: x.str.replace('\r\n', ''))
            df[possible_strings] = df[possible_strings].apply(lambda x: x.str.replace('\n', ''))
            df.to_csv(filename, index=False)
        else:
            if fmt == 'json':
                df.to_json(filename, 'records', date_unit='s')
            else:
                if fmt == 'ndjson':
                    df.to_json(filename, 'records', lines=True, date_unit='s')
        return df