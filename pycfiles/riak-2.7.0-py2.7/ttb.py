# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/codecs/ttb.py
# Compiled at: 2016-10-17 19:06:50
import datetime, six
from erlastic import encode, decode
from erlastic.types import Atom
from riak import RiakError
from riak.codecs import Codec, Msg
from riak.pb.messages import MSG_CODE_TS_TTB_MSG
from riak.ts_object import TsColumns
from riak.util import bytes_to_str, unix_time_millis, datetime_from_unix_time_millis
udef_a = Atom('undefined')
rpberrorresp_a = Atom('rpberrorresp')
tsgetreq_a = Atom('tsgetreq')
tsgetresp_a = Atom('tsgetresp')
tsqueryreq_a = Atom('tsqueryreq')
tsqueryresp_a = Atom('tsqueryresp')
tsinterpolation_a = Atom('tsinterpolation')
tsputreq_a = Atom('tsputreq')
tsputresp_a = Atom('tsputresp')
tsdelreq_a = Atom('tsdelreq')
timestamp_a = Atom('timestamp')

class TtbCodec(Codec):
    """
    Erlang term-to-binary Encoding and decoding methods for TcpTransport
    """

    def __init__(self, **unused_args):
        super(TtbCodec, self).__init__(**unused_args)

    def parse_msg(self, msg_code, data):
        if msg_code != MSG_CODE_TS_TTB_MSG:
            raise RiakError(("TTB can't parse code: {}").format(msg_code))
        if len(data) > 0:
            decoded = decode(data)
            self.maybe_err_ttb(decoded)
            return decoded
        else:
            return
            return

    def maybe_err_ttb(self, err_ttb):
        resp_a = err_ttb[0]
        if resp_a == rpberrorresp_a:
            errmsg = err_ttb[1]
            raise RiakError(bytes_to_str(errmsg))

    def encode_to_ts_cell(self, cell):
        if cell is None:
            return []
        else:
            if isinstance(cell, datetime.datetime):
                ts = unix_time_millis(cell)
                return ts
            if isinstance(cell, bool):
                return cell
            if isinstance(cell, six.text_type) or isinstance(cell, six.binary_type) or isinstance(cell, six.string_types):
                return cell
            if isinstance(cell, six.integer_types):
                return cell
            if isinstance(cell, float):
                return cell
            t = type(cell)
            raise RiakError(("can't serialize type '{}', value '{}'").format(t, cell))
            return

    def encode_timeseries_keyreq(self, table, key, is_delete=False):
        key_vals = None
        if isinstance(key, list):
            key_vals = key
        else:
            raise ValueError('key must be a list')
        mc = MSG_CODE_TS_TTB_MSG
        rc = MSG_CODE_TS_TTB_MSG
        req_atom = tsgetreq_a
        if is_delete:
            req_atom = tsdelreq_a
        req = (
         req_atom, table.name, [ self.encode_to_ts_cell(k) for k in key_vals ], udef_a)
        return Msg(mc, encode(req), rc)

    def validate_timeseries_put_resp(self, resp_code, resp):
        if resp is None and resp_code == MSG_CODE_TS_TTB_MSG:
            return True
        else:
            if resp is not None:
                return True
            raise RiakError('missing response object')
            return

    def encode_timeseries_put(self, tsobj):
        """
        Returns an Erlang-TTB encoded tuple with the appropriate data and
        metadata from a TsObject.

        :param tsobj: a TsObject
        :type tsobj: TsObject
        :rtype: term-to-binary encoded object
        """
        if tsobj.columns:
            raise NotImplementedError('columns are not used')
        if tsobj.rows and isinstance(tsobj.rows, list):
            req_rows = []
            for row in tsobj.rows:
                req_r = []
                for cell in row:
                    req_r.append(self.encode_to_ts_cell(cell))

                req_rows.append(tuple(req_r))

            req = (
             tsputreq_a, tsobj.table.name, [], req_rows)
            mc = MSG_CODE_TS_TTB_MSG
            rc = MSG_CODE_TS_TTB_MSG
            return Msg(mc, encode(req), rc)
        raise RiakError('TsObject requires a list of rows')

    def encode_timeseries_query(self, table, query, interpolations=None):
        q = query
        if '{table}' in q:
            q = q.format(table=table.name)
        tsi = (
         tsinterpolation_a, q, [])
        req = (tsqueryreq_a, tsi, False, udef_a)
        mc = MSG_CODE_TS_TTB_MSG
        rc = MSG_CODE_TS_TTB_MSG
        return Msg(mc, encode(req), rc)

    def decode_timeseries(self, resp_ttb, tsobj, convert_timestamp=False):
        """
        Fills an TsObject with the appropriate data and
        metadata from a TTB-encoded TsGetResp / TsQueryResp.

        :param resp_ttb: the decoded TTB data
        :type resp_ttb: TTB-encoded tsqueryrsp or tsgetresp
        :param tsobj: a TsObject
        :type tsobj: TsObject
        :param convert_timestamp: Convert timestamps to datetime objects
        :type tsobj: boolean
        """
        if resp_ttb is None:
            return tsobj
        else:
            self.maybe_err_ttb(resp_ttb)
            if resp_ttb == tsqueryresp_a:
                return tsobj
            resp_a = resp_ttb[0]
            if resp_a == tsputresp_a:
                return
            if resp_a == tsgetresp_a or resp_a == tsqueryresp_a:
                resp_data = resp_ttb[1]
                if len(resp_data) == 0:
                    return
                if len(resp_data) == 3:
                    resp_colnames = resp_data[0]
                    resp_coltypes = resp_data[1]
                    tsobj.columns = self.decode_timeseries_cols(resp_colnames, resp_coltypes)
                    resp_rows = resp_data[2]
                    tsobj.rows = []
                    for resp_row in resp_rows:
                        tsobj.rows.append(self.decode_timeseries_row(resp_row, resp_coltypes, convert_timestamp))

                else:
                    raise RiakError(('Expected 3-tuple in response, got: {}').format(resp_data))
            else:
                raise RiakError(('Unknown TTB response type: {}').format(resp_a))
            return

    def decode_timeseries_cols(self, cnames, ctypes):
        cnames = [ bytes_to_str(cname) for cname in cnames ]
        ctypes = [ str(ctype) for ctype in ctypes ]
        return TsColumns(cnames, ctypes)

    def decode_timeseries_row(self, tsrow, tsct, convert_timestamp=False):
        """
        Decodes a TTB-encoded TsRow into a list

        :param tsrow: the TTB decoded TsRow to decode.
        :type tsrow: TTB dncoded row
        :param tsct: the TTB decoded column types (atoms).
        :type tsct: list
        :param convert_timestamp: Convert timestamps to datetime objects
        :type tsobj: boolean
        :rtype list
        """
        row = []
        for i, cell in enumerate(tsrow):
            if cell is None:
                row.append(None)
            elif isinstance(cell, list) and len(cell) == 0:
                row.append(None)
            elif convert_timestamp and tsct[i] == timestamp_a:
                row.append(datetime_from_unix_time_millis(cell))
            else:
                row.append(cell)

        return row