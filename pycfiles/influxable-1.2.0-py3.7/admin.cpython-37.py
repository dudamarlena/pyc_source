# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/db/admin.py
# Compiled at: 2019-11-03 07:57:39
# Size of source mod 2**32: 24295 bytes
from .. import Influxable, exceptions, serializers
from .criteria import Criteria
from .query import RawQuery
from ..response import InfluxDBResponse

class Privileges:
    ALL = 'ALL'
    READ = 'READ'
    WRITE = 'WRITE'


PRIVILEGE_VALUES = [
 'ALL', 'READ', 'WRITE']

class GenericDBAdminCommand:

    @staticmethod
    def _add_database_name_to_options(options):
        database_name = GenericDBAdminCommand._get_database_name()
        full_database_name = GenericDBAdminCommand._get_full_database_name()
        database_name = GenericDBAdminCommand._format_with_double_quote(database_name)
        options.update({'database_name':database_name, 
         'full_database_name':full_database_name})
        return options

    @staticmethod
    def _execute_query(query, options={}):
        options = GenericDBAdminCommand._add_database_name_to_options(options)
        prepared_query = (query.format)(**options)
        response = RawQuery(prepared_query).execute()
        influx_response = InfluxDBResponse(response)
        influx_response.raise_if_error()
        return influx_response

    @staticmethod
    def _execute_query_with_parser(query, parser=serializers.FlatFormattedSerieSerializer, options={}):
        influx_response = GenericDBAdminCommand._execute_query(query, options)
        formatted_result = parser(influx_response).convert()
        return formatted_result

    @staticmethod
    def _get_formatted_privilege(privilege):
        privilege = str(privilege).upper()
        if privilege not in PRIVILEGE_VALUES:
            msg = 'privilege `{}` must be one of value of {}'.format(privilege, PRIVILEGE_VALUES)
            raise exceptions.InfluxDBInvalidChoiceError(msg)
        return privilege

    @staticmethod
    def _get_formatted_user_name(user_name):
        return GenericDBAdminCommand._format_with_double_quote(user_name)

    @staticmethod
    def _generate_from_clause(measurements):
        if not isinstance(measurements, list):
            msg = 'measurements type must be <list>'
            raise exceptions.InfluxDBInvalidTypeError(msg)
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        selected_measurements = ', '.join(quoted_measurements)
        from_clause = ''
        if selected_measurements:
            from_clause = 'FROM {}'.format(selected_measurements)
        return from_clause

    @staticmethod
    def _generate_where_clause(criteria):
        if not isinstance(criteria, list):
            msg = 'criteria type must be <list>'
            raise exceptions.InfluxDBInvalidTypeError(msg)
        if len(criteria):
            if not any([isinstance(c, Criteria) for c in criteria]):
                msg = 'criteria type must be <list> of <Criteria>'
                raise exceptions.InfluxDBInvalidTypeError(msg)
        where_clause = ''
        if len(criteria):
            selected_criteria = [c.evaluate() for c in criteria]
            eval_criteria = ' AND '.join(selected_criteria)
            where_clause = 'WHERE {}'.format(eval_criteria)
        return where_clause

    @staticmethod
    def _generate_limit_clause(limit):
        if limit is not None:
            if not isinstance(limit, int):
                msg = 'limit type must be <int>'
                raise exceptions.InfluxDBInvalidTypeError(msg)
        limit_clause = ''
        if limit is not None:
            limit_clause = 'LIMIT {}'.format(limit)
        return limit_clause

    @staticmethod
    def _generate_offset_clause(offset):
        if offset is not None:
            if not isinstance(offset, int):
                msg = 'offset type must be <int>'
                raise exceptions.InfluxDBInvalidTypeError(msg)
        offset_clause = ''
        if offset is not None:
            offset_clause = 'OFFSET {}'.format(offset)
        return offset_clause

    @staticmethod
    def _generate_default_clause(is_default=False):
        if is_default is True:
            return 'DEFAULT'
        return ''

    @staticmethod
    def _generate_duration_clause(duration=None):
        if duration:
            return 'DURATION {}'.format(duration)
        return ''

    @staticmethod
    def _generate_replication_clause(replication=None):
        if replication:
            return 'REPLICATION {}'.format(replication)
        return ''

    @staticmethod
    def _generate_shard_duration_clause(sh_duration=None):
        if sh_duration:
            return 'SHARD DURATION {}'.format(sh_duration)
        return ''

    @staticmethod
    def _get_database_name():
        instance = GenericDBAdminCommand._get_influxable_instance()
        database_name = instance.database_name
        return database_name

    @staticmethod
    def _get_full_database_name():
        instance = GenericDBAdminCommand._get_influxable_instance()
        full_database_name = instance.full_database_name
        return full_database_name

    @staticmethod
    def _get_influxable_instance():
        instance = Influxable.get_instance()
        return instance

    @staticmethod
    def _format_with_simple_quote(string):
        return "'{}'".format(string)

    @staticmethod
    def _format_with_double_quote(string):
        return '"{}"'.format(string)


class AlterAdminCommand:

    @staticmethod
    def alter_retention_policy(policy_name, duration=None, replication=None, shard_duration=None, is_default=False):
        if not duration:
            if not replication:
                if not shard_duration:
                    if not is_default:
                        msg = '`duration` or `replication` or `shard_duration`  or `is_default` must be not null'
                        raise exceptions.InfluxDBError(msg)
        policy_name = GenericDBAdminCommand._format_with_double_quote(policy_name)
        default_clause = GenericDBAdminCommand._generate_default_clause(is_default)
        duration_clause = GenericDBAdminCommand._generate_duration_clause(duration)
        replication_clause = GenericDBAdminCommand._generate_replication_clause(replication)
        shard_duration_clause = GenericDBAdminCommand._generate_shard_duration_clause(shard_duration)
        options = {'default_clause':default_clause, 
         'duration_clause':duration_clause, 
         'policy_name':policy_name, 
         'replication_clause':replication_clause, 
         'shard_duration_clause':shard_duration_clause}
        query = 'ALTER RETENTION POLICY {policy_name} ON {database_name} {duration_clause} {replication_clause} {shard_duration_clause} {default_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class CreateAdminCommand:

    @staticmethod
    def create_continuous_query():
        raise NotImplementedError

    @staticmethod
    def create_database--- This code section failed: ---

 L. 221         0  LOAD_GLOBAL              GenericDBAdminCommand
                2  LOAD_METHOD              _format_with_double_quote

 L. 222         4  LOAD_FAST                'new_database_name'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'new_database_name'

 L. 224        10  LOAD_STR                 'new_database_name'
               12  LOAD_FAST                'new_database_name'
               14  BUILD_MAP_1           1 
               16  STORE_FAST               'options'

 L. 226        18  LOAD_STR                 ''
               20  STORE_FAST               'with_clause'

 L. 227        22  LOAD_FAST                'duration'
               24  POP_JUMP_IF_TRUE     38  'to 38'
               26  LOAD_FAST                'replication'
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  LOAD_FAST                'shard_duration'
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  LOAD_FAST                'policy_name'
               36  POP_JUMP_IF_FALSE   110  'to 110'
             38_0  COME_FROM            32  '32'
             38_1  COME_FROM            28  '28'
             38_2  COME_FROM            24  '24'

 L. 228        38  LOAD_STR                 ''
               40  STORE_FAST               'policy_clause'

 L. 229        42  LOAD_FAST                'policy_name'
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 230        46  LOAD_STR                 'NAME "{}"'
               48  LOAD_METHOD              format
               50  LOAD_FAST                'policy_name'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  STORE_FAST               'policy_clause'
             56_0  COME_FROM            44  '44'

 L. 232        56  LOAD_GLOBAL              GenericDBAdminCommand
               58  LOAD_METHOD              _generate_duration_clause

 L. 233        60  LOAD_FAST                'duration'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  STORE_FAST               'duration_clause'

 L. 235        66  LOAD_GLOBAL              GenericDBAdminCommand
               68  LOAD_METHOD              _generate_replication_clause

 L. 236        70  LOAD_FAST                'replication'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  STORE_FAST               'replication_clause'

 L. 238        76  LOAD_GLOBAL              GenericDBAdminCommand
               78  LOAD_METHOD              _generate_shard_duration_clause

 L. 239        80  LOAD_FAST                'shard_duration'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'shard_duration_clause'

 L. 245        86  LOAD_STR                 'WITH {duration_clause} {replication_clause} {shard_duration_clause} {policy_clause}'
               88  STORE_FAST               'with_clause'

 L. 247        90  LOAD_FAST                'options'
               92  LOAD_METHOD              update

 L. 248        94  LOAD_FAST                'duration_clause'

 L. 249        96  LOAD_FAST                'replication_clause'

 L. 250        98  LOAD_FAST                'policy_clause'

 L. 251       100  LOAD_FAST                'shard_duration_clause'
              102  LOAD_CONST               ('duration_clause', 'replication_clause', 'policy_clause', 'shard_duration_clause')
              104  BUILD_CONST_KEY_MAP_4     4 
              106  CALL_METHOD_1         1  '1 positional argument'
              108  POP_TOP          
            110_0  COME_FROM            36  '36'

 L. 253       110  LOAD_STR                 'CREATE DATABASE {new_database_name}'
              112  LOAD_FAST                'with_clause'
              114  BINARY_ADD       
              116  STORE_FAST               'query'

 L. 254       118  LOAD_GLOBAL              InfluxDBAdmin
              120  LOAD_METHOD              _execute_query
              122  LOAD_FAST                'query'
              124  LOAD_FAST                'options'
              126  CALL_METHOD_2         2  '2 positional arguments'
              128  POP_TOP          

 L. 255       130  LOAD_CONST               True
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_STR' instruction at offset 110

    @staticmethod
    def create_retention_policy--- This code section failed: ---

 L. 265         0  LOAD_FAST                'duration'
                2  POP_JUMP_IF_TRUE     30  'to 30'
                4  LOAD_FAST                'replication'
                6  POP_JUMP_IF_TRUE     30  'to 30'
                8  LOAD_FAST                'shard_duration'
               10  POP_JUMP_IF_TRUE     30  'to 30'

 L. 266        12  LOAD_FAST                'is_default'
               14  POP_JUMP_IF_TRUE     30  'to 30'

 L. 267        16  LOAD_STR                 '`duration` or `replication` or `shard_duration`  or `is_default` must be not null'
               18  STORE_FAST               'msg'

 L. 269        20  LOAD_GLOBAL              exceptions
               22  LOAD_METHOD              InfluxDBError
               24  LOAD_FAST                'msg'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            14  '14'
             30_1  COME_FROM            10  '10'
             30_2  COME_FROM             6  '6'
             30_3  COME_FROM             2  '2'

 L. 271        30  LOAD_FAST                'duration'
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  LOAD_FAST                'replication'
               36  POP_JUMP_IF_TRUE     46  'to 46'
             38_0  COME_FROM            32  '32'
               38  LOAD_FAST                'duration'
               40  POP_JUMP_IF_FALSE    60  'to 60'
               42  LOAD_FAST                'replication'
               44  POP_JUMP_IF_TRUE     60  'to 60'
             46_0  COME_FROM            36  '36'

 L. 272        46  LOAD_STR                 '`duration` or `replication` must be not null'
               48  STORE_FAST               'msg'

 L. 273        50  LOAD_GLOBAL              exceptions
               52  LOAD_METHOD              InfluxDBError
               54  LOAD_FAST                'msg'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            44  '44'
             60_1  COME_FROM            40  '40'

 L. 275        60  LOAD_GLOBAL              GenericDBAdminCommand
               62  LOAD_METHOD              _format_with_double_quote

 L. 276        64  LOAD_FAST                'policy_name'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  STORE_FAST               'policy_name'

 L. 279        70  LOAD_GLOBAL              GenericDBAdminCommand
               72  LOAD_METHOD              _generate_default_clause

 L. 280        74  LOAD_FAST                'is_default'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  STORE_FAST               'default_clause'

 L. 282        80  LOAD_GLOBAL              GenericDBAdminCommand
               82  LOAD_METHOD              _generate_duration_clause

 L. 283        84  LOAD_FAST                'duration'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'duration_clause'

 L. 285        90  LOAD_GLOBAL              GenericDBAdminCommand
               92  LOAD_METHOD              _generate_replication_clause

 L. 286        94  LOAD_FAST                'replication'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'replication_clause'

 L. 288       100  LOAD_GLOBAL              GenericDBAdminCommand
              102  LOAD_METHOD              _generate_shard_duration_clause

 L. 289       104  LOAD_FAST                'shard_duration'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               'shard_duration_clause'

 L. 293       110  LOAD_FAST                'default_clause'

 L. 294       112  LOAD_FAST                'duration_clause'

 L. 295       114  LOAD_FAST                'replication_clause'

 L. 296       116  LOAD_FAST                'policy_name'

 L. 297       118  LOAD_FAST                'shard_duration_clause'
              120  LOAD_CONST               ('default_clause', 'duration_clause', 'replication_clause', 'policy_name', 'shard_duration_clause')
              122  BUILD_CONST_KEY_MAP_5     5 
              124  STORE_FAST               'options'

 L. 302       126  LOAD_STR                 'CREATE RETENTION POLICY {policy_name} ON {database_name} {duration_clause} {replication_clause} {shard_duration_clause} {default_clause}'
              128  STORE_FAST               'query'

 L. 304       130  LOAD_GLOBAL              InfluxDBAdmin
              132  LOAD_METHOD              _execute_query
              134  LOAD_FAST                'query'
              136  LOAD_FAST                'options'
              138  CALL_METHOD_2         2  '2 positional arguments'
              140  POP_TOP          

 L. 305       142  LOAD_CONST               True
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 144

    @staticmethod
    def create_subscription(subscription_name, hosts, any=False):
        subscription_name = GenericDBAdminCommand._format_with_double_quote(subscription_name)
        destination_type = 'ANY' if any else 'ALL'
        formatted_hosts = ', '.join(["'{}'".format(h) for h in hosts])
        options = {'hosts':formatted_hosts, 
         'destination_type':destination_type, 
         'subscription_name':subscription_name}
        query = 'CREATE SUBSCRIPTION {subscription_name} ON {full_database_name} DESTINATIONS {destination_type} {hosts}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def create_user(user_name, password, with_privileges=False):
        user_name = GenericDBAdminCommand._get_formatted_user_name(user_name)
        password = GenericDBAdminCommand._format_with_simple_quote(password)
        privilege_clause = 'WITH ALL PRIVILEGES' if with_privileges else ''
        options = {'user_name':user_name, 
         'password':password, 
         'privilege_clause':privilege_clause}
        query = 'CREATE USER {user_name} WITH PASSWORD {password} {privilege_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class DeleteAdminCommand:

    @staticmethod
    def delete(measurements=[], criteria=[]):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        where_clause = GenericDBAdminCommand._generate_where_clause(criteria)
        if not from_clause:
            if not where_clause:
                msg = '`measurements` or `criteria` must be not null'
                raise exceptions.InfluxDBError(msg)
        options = {'from_clause':from_clause,  'where_clause':where_clause}
        query = 'DELETE {from_clause} {where_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class DropAdminCommand:

    @staticmethod
    def drop_continuous_query(query_name):
        query_name = GenericDBAdminCommand._format_with_double_quote(query_name)
        options = {'query_name': query_name}
        query = 'DROP CONTINUOUS QUERY {query_name} ON {database_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_database(database_name_to_delete):
        _database_name = GenericDBAdminCommand._format_with_double_quote(database_name_to_delete)
        options = {'_database_name': _database_name}
        query = 'DROP DATABASE {_database_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_measurement(measurement_name):
        measurement_name = GenericDBAdminCommand._format_with_double_quote(measurement_name)
        options = {'measurement_name': measurement_name}
        query = 'DROP MEASUREMENT {measurement_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_retention_policy(policy_name):
        policy_name = GenericDBAdminCommand._format_with_double_quote(policy_name)
        options = {'policy_name': policy_name}
        query = 'DROP RETENTION POLICY {policy_name} ON {database_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_series(measurements=[], criteria=[]):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        where_clause = GenericDBAdminCommand._generate_where_clause(criteria)
        if not from_clause:
            if not where_clause:
                msg = '`measurements` or `criteria` must be not null'
                raise exceptions.InfluxDBError(msg)
        options = {'from_clause':from_clause,  'where_clause':where_clause}
        query = 'DROP SERIES {from_clause} {where_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_shard(shard_id):
        options = {'shard_id': shard_id}
        query = 'DROP SHARD {shard_id}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_subscription(subscription_name):
        subscription_name = GenericDBAdminCommand._format_with_double_quote(subscription_name)
        options = {'subscription_name': subscription_name}
        query = 'DROP SUBSCRIPTION {subscription_name} ON {full_database_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def drop_user(user_name):
        user_name = GenericDBAdminCommand._get_formatted_user_name(user_name)
        options = {'user_name': user_name}
        query = 'DROP USER {user_name}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class ExplainAdminCommand:

    @staticmethod
    def explain(query, analyze=False):
        analyze = 'ANALYZE' if analyze else ''
        options = {'analyze':analyze, 
         'query':query}
        query = 'EXPLAIN {analyze} {query}'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)


class GrantAdminCommand:

    @staticmethod
    def grant(privilege, user_name):
        privilege = GenericDBAdminCommand._get_formatted_privilege(privilege)
        user_name = GenericDBAdminCommand._get_formatted_user_name(user_name)
        options = {'privilege':privilege, 
         'user_name':user_name}
        query = 'GRANT {privilege} ON {database_name} TO {user_name}'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)


class KillAdminCommand:

    @staticmethod
    def kill(query_id):
        options = {'query_id': query_id}
        query = 'KILL QUERY {query_id}'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)


class RevokeAdminCommand:

    @staticmethod
    def revoke(privilege, user_name):
        privilege = GenericDBAdminCommand._get_formatted_privilege(privilege)
        user_name = GenericDBAdminCommand._get_formatted_user_name(user_name)
        options = {'privilege':privilege, 
         'user_name':user_name}
        query = 'REVOKE {privilege} ON {database_name} FROM {user_name}'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)


class ShowAdminCommand:

    @staticmethod
    def show_field_key_cardinality(exact=False):
        exact = 'EXACT' if exact else ''
        options = {'exact': exact}
        query = 'SHOW FIELD KEY {exact} CARDINALITY'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_measurement_cardinality(exact=False):
        exact = 'EXACT' if exact else ''
        options = {'exact': exact}
        query = 'SHOW MEASUREMENT {exact} CARDINALITY'
        parser = serializers.FlatSingleValueSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_series_cardinality(exact=False):
        exact = 'EXACT' if exact else ''
        options = {'exact': exact}
        query = 'SHOW SERIES {exact} CARDINALITY'
        parser = serializers.FlatSingleValueSerializer
        if exact:
            parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_tag_key_cardinality(exact=False):
        exact = 'EXACT' if exact else ''
        options = {'exact': exact}
        query = 'SHOW TAG KEY {exact} CARDINALITY'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_tag_values_cardinality(key, exact=False):
        key_clause = 'KEY = "{key}"'.format(key=key)
        exact = 'EXACT' if exact else ''
        options = {'exact':exact, 
         'key_clause':key_clause}
        query = 'SHOW TAG VALUES {exact} CARDINALITY WITH {key_clause}'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_continuous_queries():
        query = 'SHOW CONTINUOUS QUERIES'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_diagnostics():
        query = 'SHOW DIAGNOSTICS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_field_keys(measurements=[]):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        options = {'from_clause': from_clause}
        query = 'SHOW FIELD KEYS {from_clause}'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_grants(user_name):
        options = {'user_name': user_name}
        query = 'SHOW GRANTS FOR {user_name}'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_databases():
        query = 'SHOW DATABASES'
        parser = serializers.FlatSimpleResultSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_measurements(criteria=[]):
        where_clause = GenericDBAdminCommand._generate_where_clause(criteria)
        options = {'where_clause': where_clause}
        query = 'SHOW MEASUREMENTS {where_clause}'
        parser = serializers.FlatSimpleResultSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_queries():
        query = 'SHOW QUERIES'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_retention_policies():
        query = 'SHOW RETENTION POLICIES'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_series(measurements=[], criteria=[], limit=None, offset=None):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        where_clause = GenericDBAdminCommand._generate_where_clause(criteria)
        limit_clause = GenericDBAdminCommand._generate_limit_clause(limit)
        offset_clause = GenericDBAdminCommand._generate_offset_clause(offset)
        options = {'from_clause':from_clause, 
         'where_clause':where_clause, 
         'limit_clause':limit_clause, 
         'offset_clause':offset_clause}
        query = 'SHOW SERIES ON {database_name} {from_clause} {where_clause} {limit_clause} {offset_clause}'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_stats():
        query = 'SHOW STATS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_shards():
        query = 'SHOW SHARDS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_shard_groups():
        query = 'SHOW SHARD GROUPS'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_subscriptions():
        query = 'SHOW SUBSCRIPTIONS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)

    @staticmethod
    def show_tag_keys(measurements=[]):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        options = {'from_clause': from_clause}
        query = 'SHOW TAG KEYS {from_clause}'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_tag_values(key, measurements=[]):
        key_clause = 'KEY = "{key}"'.format(key=key)
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        options = {'key_clause':key_clause, 
         'from_clause':from_clause}
        query = 'SHOW TAG VALUES {from_clause} WITH {key_clause}'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser, options)

    @staticmethod
    def show_users():
        query = 'SHOW USERS'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query_with_parser(query, parser)


class InfluxDBAdmin(GenericDBAdminCommand, AlterAdminCommand, CreateAdminCommand, DeleteAdminCommand, DropAdminCommand, ExplainAdminCommand, GrantAdminCommand, KillAdminCommand, RevokeAdminCommand, ShowAdminCommand):
    pass