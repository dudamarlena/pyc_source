# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlflow/client.py
# Compiled at: 2020-04-10 03:26:06
# Size of source mod 2**32: 9437 bytes
import os, sys, logging, grpc, re, time, google.protobuf.wrappers_pb2 as wrapper
from google.protobuf.timestamp_pb2 import Timestamp
import sqlflow.proto.sqlflow_pb2 as pb, sqlflow.proto.sqlflow_pb2_grpc as pb_grpc
from sqlflow.env_expand import EnvExpander, EnvExpanderError
from sqlflow.rows import Rows
from sqlflow.compound_message import CompoundMessage
_LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
_LOGGER.setLevel(logging.INFO)
_LOGGER.addHandler(handler)
DEFAULT_TIMEOUT = 36000

class StreamReader(object):

    def __init__(self, stream_response):
        self._stream_response = stream_response
        self.last_response = None

    def read_one(self):
        try:
            res = next(self._stream_response)
        except StopIteration:
            return (None, None)
        else:
            return (
             res, res.WhichOneof('response'))

    def read_until_type_changed(self):
        first_rtype = None
        while True:
            try:
                response = next(self._stream_response)
            except StopIteration:
                break

            rtype = response.WhichOneof('response')
            if first_rtype == None:
                first_rtype = rtype
            if first_rtype != rtype:
                self.last_response = response
                break
            yield response


class Client:

    def __init__(self, server_url=None, ca_crt=None):
        """A minimum client that issues queries to and fetch results/logs from sqlflowserver.

        :param server_url: sqlflowserver url. If None, read value from
                           environment variable SQLFLOW_SERVER.
        :type server_url: str.

        :param ca_crt: Path to CA certificates of SQLFlow client, if None,
                       try to find the file from the environment variable:
                       SQLFLOW_CA_CRT, otherwise using insecure client.
        :type ca_crt: str.

        :raises: ValueError

        Example:
        >>> client = sqlflow.Client(server_url="localhost:50051")

        """
        if server_url is None:
            if 'SQLFLOW_SERVER' not in os.environ:
                raise ValueError("Can't find environment variable SQLFLOW_SERVER")
            server_url = os.environ['SQLFLOW_SERVER']
        self._stub = pb_grpc.SQLFlowStub(self.new_rpc_channel(server_url, ca_crt))
        self._expander = EnvExpander(os.environ)

    def new_rpc_channel(self, server_url, ca_crt):
        if ca_crt is None:
            if 'SQLFLOW_CA_CRT' not in os.environ:
                channel = grpc.insecure_channel(server_url)
        else:
            if ca_crt is None:
                ca_crt = os.environ['SQLFLOW_CA_CRT']
            with open(ca_crt, 'rb') as (f):
                creds = grpc.ssl_channel_credentials(f.read())
            channel = grpc.secure_channel(server_url, creds)
        return channel

    def sql_request(self, sql):
        token = os.getenv('SQLFLOW_USER_TOKEN', '')
        db_conn_str = os.getenv('SQLFLOW_DATASOURCE', '')
        exit_on_submit_env = os.getenv('SQLFLOW_EXIT_ON_SUBMIT', 'True')
        user_id = os.getenv('SQLFLOW_USER_ID', '')
        hive_location = os.getenv('SQLFLOW_HIVE_LOCATION', '')
        hdfs_namenode_addr = os.getenv('SQLFLOW_HDFS_NAMENODE_ADDR', '')
        hdfs_user = os.getenv('JUPYTER_HADOOP_USER', '')
        hdfs_pass = os.getenv('JUPYTER_HADOOP_PASS', '')
        if exit_on_submit_env.isdigit():
            exit_on_submit = bool(int(exit_on_submit_env))
        else:
            exit_on_submit = exit_on_submit_env.lower() == 'true'
        se = pb.Session(token=token, db_conn_str=db_conn_str,
          exit_on_submit=exit_on_submit,
          user_id=user_id,
          hive_location=hive_location,
          hdfs_namenode_addr=hdfs_namenode_addr,
          hdfs_user=hdfs_user,
          hdfs_pass=hdfs_pass)
        try:
            sql = self._expander.expand(sql)
        except Exception as e:
            _LOGGER.error('%s', e)
            raise e

        return pb.Request(sql=sql, session=se)

    def execute(self, operation):
        """Run a SQL statement

        :param operation: SQL statement to be executed.
        :type operation: str.

        :returns: sqlflow.client.Rows

        Example:

        >>> client.execute("select * from iris limit 1")

        """
        try:
            stream_response = self._stub.Run((self.sql_request(operation)), timeout=DEFAULT_TIMEOUT)
            return self.display(stream_response)
        except grpc.RpcError as e:
            raise e
        except EnvExpanderError as e:
            raise e

    def read_fetch_response(self, job_id):
        req = pb.FetchRequest()
        pb_job = pb.Job(id=job_id)
        pb_job.id = job_id
        req.job.CopyFrom(pb_job)
        compound_message = CompoundMessage()
        column_names = None
        rows = []
        while True:
            fetch_response = self._stub.Fetch(req)
            for response in fetch_response.responses.response:
                rtype = response.WhichOneof('response')
                if rtype == 'message':
                    msg = response.message.message
                    if re.match('<[a-z][\\s\\S]*>.*', msg):
                        from IPython.core.display import display, HTML
                        display(HTML(msg))
                    else:
                        _LOGGER.info(msg)
                else:
                    if rtype == 'eoe':

                        def _rows_gen():
                            for row in rows:
                                yield [self._decode_any(d) for d in row.data]

                        compound_message.add_rows(Rows(column_names, _rows_gen), None)
                        rows = []
                        break
                    else:
                        if rtype == 'head':
                            column_names = [column_name for column_name in response.head.column_names]
                        else:
                            rows.append(response.row)

            if fetch_response.eof:
                break
            req = fetch_response.updated_fetch_since
            time.sleep(2)

        return compound_message

    def display_html(self, first_line, stream_reader):
        resp_list = [
         first_line]
        for res in stream_reader.read_until_type_changed():
            resp_list.append(res.message.message)

        from IPython.core.display import display, HTML
        display(HTML('\n'.join(resp_list)))

    def display(self, stream_response):
        """Display stream response like log or table.row"""
        reader = StreamReader(stream_response)
        response, rtype = reader.read_one()
        compound_message = CompoundMessage()
        while 1:
            if response == None:
                break
            if rtype == 'message':
                if re.match('<[a-z][\\s\\S]*>.*', response.message.message):
                    self.display_html(response.message.message, reader)
                else:
                    _LOGGER.info(response.message.message)
                    for response in reader.read_until_type_changed():
                        _LOGGER.info(response.message.message)

                    response = reader.last_response
                    if response is not None:
                        rtype = response.WhichOneof('response')
                        continue
                    else:
                        if rtype == 'job':
                            job = response.job
                            return self.read_fetch_response(job.id)
                        column_names = [column_name for column_name in response.head.column_names]

                        def rows_gen():
                            for res in reader.read_until_type_changed():
                                yield [self._decode_any(a) for a in res.row.data]

                        compound_message.add_rows(Rows(column_names, rows_gen), None)
                    response, rtype = reader.read_one()

        return compound_message

    @classmethod
    def _decode_any(cls, any_message):
        """Decode a google.protobuf.any_pb2
        """
        try:
            message = next(getattr(wrapper, type_name)() for type_name, desc in wrapper.DESCRIPTOR.message_types_by_name.items() if any_message.Is(desc))
            any_message.Unpack(message)
            return message.value
        except StopIteration:
            if any_message.Is(pb.Row.Null.DESCRIPTOR):
                return
            if any_message.Is(Timestamp.DESCRIPTOR):
                timestamp_message = Timestamp()
                any_message.Unpack(timestamp_message)
                return timestamp_message.ToDatetime()
            raise TypeError('Unsupported type {}'.format(any_message))