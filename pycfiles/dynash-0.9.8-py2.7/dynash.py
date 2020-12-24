# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/dynash/dynash.py
# Compiled at: 2014-11-12 14:21:39
from __future__ import unicode_literals
from version import __version__
from cmd2 import Cmd
import boto
from boto.dynamodb.exceptions import DynamoDBResponseError, DynamoDBConditionalCheckFailedError, BotoClientError
from boto.dynamodb.condition import *
from boto.dynamodb.types import Binary
import ast, json, csv, logging, os, os.path, pprint, re, shlex, sys, traceback
try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        readline = None

else:
    import rlcompleter
    readline.parse_and_bind(b'tab: complete')

HISTORY_FILE = b'.dynash_history'
VALID_TYPES = set([b'S', b'N', b'B', b'SS', b'NS'])

class DynamoEncoder(json.JSONEncoder):
    """
    This is mainly used to transform sets to lists
    """

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        return JSONEncoder.default(self, o)


class DynamoDBShell(Cmd):
    prompt = b'dynash> '
    consistent = False
    consumed = False
    pretty = True
    verbose = False
    settable = Cmd.settable + b'\n        consistent consistent reads vs. eventual consistency\n        consumed print consumed units\n        prompt command prompt\n        pretty pretty-print results\n        verbose verbose logging of boto requests\n        '

    def _onchange_verbose(self, old, new):
        if new:
            boto.set_stream_logger(b'boto', level=logging.DEBUG)
        else:
            boto.set_stream_logger(b'boto', level=logging.WARNING)

    def __init__(self, verbose=False):
        Cmd.__init__(self)
        self.pp = pprint.PrettyPrinter(indent=4)
        try:
            self.conn = boto.connect_dynamodb()
        except Exception as e:
            self.conn = None
            print e
            print b"Cannot connect to dynamodb - Check your credentials in ~/.boto or use the 'login' command"

        if readline:
            readline.set_completer_delims(re.sub(b'[-~]', b'', readline.get_completer_delims()))
            path = os.path.join(os.environ.get(b'HOME', b''), HISTORY_FILE)
            self.history_file = os.path.abspath(path)
        else:
            self.history_file = None
        self.tables = []
        self.table = None
        self.consistent = False
        self.consumed = False
        self.verbose = verbose
        self.next_key = None
        self.schema = {}
        if verbose:
            self._onchange_verbose(None, verbose)
        return

    def pprint(self, object, prefix=b''):
        print b'%s%s' % (prefix, self.pp.pformat(object) if self.pretty else str(object))

    def print_iterator(self, gen):
        encoder = DynamoEncoder()
        prev_item = None
        print b'['
        for next_item in gen:
            if prev_item:
                print b'  %s,' % encoder.encode(prev_item)
            prev_item = next_item

        if prev_item:
            print b'  %s' % encoder.encode(prev_item)
        print b']'
        return

    def print_iterator_array(self, gen, keys):
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL, doublequote=False, escapechar=str(b'\\'))

        def to_array(item):
            return [ item.get(k) for k in keys ]

        def value(v):
            if isinstance(v, basestring):
                return v.encode(b'utf-8')
            return v

        for item in gen:
            writer.writerow([ value(v) for v in to_array(item) ])

    def getargs(self, line):
        return shlex.split(str(line.decode(b'unicode-escape')))

    def get_type(self, stype):
        if stype == b'S':
            return b'S'
        else:
            if stype == b'N':
                return 1
            if stype == b'B':
                return Binary(b'B')
            if stype == b'SS':
                return set([b'S'])
            if stype == b'NS':
                return set([1])
            return

    def get_first_rest(self, line):
        param, _, rest = line.partition(b' ')
        return (param, rest.strip())

    def get_table_params(self, line):
        if line and (line[0] == b':' or not self.table):
            table_name, line = self.get_first_rest(line)
            return (
             self.conn.get_table(table_name.lstrip(b':')), line)
        else:
            return (
             self.table, line)

    def get_table(self, line):
        if line:
            return self.conn.get_table(line)
        else:
            return self.table

    def get_typed_key_value(self, table, value, is_hash=True):
        schema = table.schema
        keytype = schema.hash_key_type if is_hash else schema.range_key_type
        if not keytype:
            return value
        try:
            if keytype == b'S':
                return str(value)
            if keytype == b'N':
                if b'.' in value:
                    return float(value)
                return int(value)
        except:
            pass

        return value

    def get_typed_value(self, field, value):
        ftype = self.schema.get(field)
        if not ftype:
            return value
        try:
            if ftype == b'S':
                return str(value)
            if ftype == b'N':
                if b'.' in value:
                    return float(value)
                return int(value)
            print b'type %s is not supported yet' % ftype
        except:
            pass

        return value

    def get_list(self, line):
        try:
            return json.loads(line)
        except:
            return ast.literal_eval(line)

    def get_expected(self, line):
        expected = {}
        while line.startswith(b'!'):
            param, line = self.get_first_rest(line[1:])
            name, value = param.split(b':', 1)
            expected[name] = value or False

        return (expected or None, line)

    def do_env(self, line):
        """
        env {environment-name}
        """
        if not line:
            print b'use: env {environment-name}'
        elif not set_environment(line):
            print b'no configuration for environment %s' % line
        else:
            self.do_login(b'')

    def do_schema(self, line):
        """
        schema

        schema --clear

        schema filed_name field_type
        """
        args = self.getargs(line)
        if not args:
            for k in sorted(self.schema):
                print b'%s\t%s' % (k, self.schema[k])

        elif args[0] == b'--clear':
            self.schema.clear()
        else:
            fname = args[0]
            ftype = args[1]
            if ftype not in VALID_TYPES:
                print b'invalid type: use %s' % list(VALID_TYPES)
            else:
                self.schema[fname] = ftype

    def do_login(self, line):
        """login aws-acces-key aws-secret"""
        if line:
            args = self.getargs(line)
            self.conn = boto.connect_dynamodb(aws_access_key_id=args[0], aws_secret_access_key=args[1])
        else:
            self.conn = boto.connect_dynamodb()
        self.do_tables(b'')

    def do_tables(self, line):
        """List tables"""
        self.tables = self.conn.list_tables()
        print b'\nAvailable tables:'
        self.pprint(self.tables)

    def do_describe(self, line):
        """describe [-c] {tablename}..."""
        args = self.getargs(line)
        if b'-c' in args:
            create_info = True
            args.remove(b'-c')
        else:
            create_info = False
        if not args:
            if self.table:
                args = [
                 self.table.name]
            else:
                args = self.tables
        for table in args:
            desc = self.conn.describe_table(table)
            if create_info:
                info = desc[b'Table']
                schema = info[b'KeySchema']
                name = info[b'TableName']
                hkey = schema[b'HashKeyElement']
                hkey = b'%s:%s' % (hkey[b'AttributeName'], hkey[b'AttributeType'])
                if b'RangeKeyElement' in schema:
                    rkey = schema[b'RangeKeyElement']
                    rkey = b' %s:%s' % (rkey[b'AttributeName'], rkey[b'AttributeType'])
                else:
                    rkey = b''
                prov = info[b'ProvisionedThroughput']
                prov = b'-c %d,%d' % (prov[b'ReadCapacityUnits'], prov[b'WriteCapacityUnits'])
                print b'create %s %s %s%s' % (name, prov, hkey, rkey)
            else:
                self.pprint(desc, b'%s: ' % table)

    def do_use(self, line):
        """use {tablename}"""
        self.table = self.conn.get_table(line)
        self.pprint(self.conn.describe_table(self.table.name))
        self.prompt = b'%s> ' % self.table.name

    def do_create(self, line):
        """create {tablename} [-c rc,wc] {hkey}[:{type} {rkey}:{type}]"""
        args = self.getargs(line)
        rc = wc = 5
        name = args.pop(0)
        if args[0] == b'-c':
            args.pop(0)
            capacity = args.pop(0).strip()
            rc, _, wc = capacity.partition(b',')
            rc = int(rc)
            wc = int(wc) if wc != b'' else rc
        hkey, _, hkey_type = args.pop(0).partition(b':')
        hkey_type = self.get_type(hkey_type or b'S')
        if args:
            rkey, _, rkey_type = args.pop(0).partition(b':')
            rkey_type = self.get_type(rkey_type or b'S')
        else:
            rkey = rkey_type = None
        t = self.conn.create_table(name, self.conn.create_schema(hkey, hkey_type, rkey, rkey_type), rc, wc)
        self.pprint(self.conn.describe_table(t.name))
        return

    def do_drop(self, line):
        """drop {tablename}"""
        self.conn.delete_table(self.conn.get_table(line))

    def do_refresh(self, line):
        """refresh {table_name}"""
        table = self.get_table(line)
        table.refresh(True)
        self.pprint(self.conn.describe_table(table.name))

    def do_capacity(self, line):
        """capacity {tablename} {read_units} {write_units}"""
        args = self.getargs(line)
        table = self.get_table(args[0])
        read_units = int(args[1])
        write_units = int(args[2])
        desc = self.conn.describe_table(table.name)
        prov = desc[b'Table'][b'ProvisionedThroughput']
        current_read, current_write = prov[b'ReadCapacityUnits'], prov[b'WriteCapacityUnits']
        if read_units < current_read or write_units < current_write:
            table.update_throughput(read_units, write_units)
            print b'%s: updating capacity to %d read units, %d write units' % (table.name, read_units, write_units)
            print b''
            self.do_refresh(table.name)
        else:
            print b'%s: current capacity is %d read units, %d write units' % (table.name, current_read, current_write)
            while current_read < read_units or current_write < write_units:
                if read_units - current_read > current_read:
                    current_read *= 2
                else:
                    current_read = read_units
                if write_units - current_write > current_write:
                    current_write *= 2
                else:
                    current_write = write_units
                print b'%s: updating capacity to %d read units, %d write units' % (table.name, current_read, current_write)
                table.update_throughput(current_read, current_write)
                print b''
                self.do_refresh(table.name)
                print b''

    def do_put(self, line):
        """put [:tablename] [!fieldname:expectedvalue] {json-body} [{json-body}, {json-body}...]"""
        table, line = self.get_table_params(line)
        expected, line = self.get_expected(line)
        if line.startswith(b'(') or line.startswith(b'['):
            list = self.get_list(line)
            wlist = self.conn.new_batch_write_list()
            wlist.add_batch(table, [ table.new_item(None, None, item) for item in list ])
            response = self.conn.batch_write_item(wlist)
            consumed = response[b'Responses'][table.name][b'ConsumedCapacityUnits']
            if b'UnprocessedItems' in response and response[b'UnprocessedItems']:
                print b''
                print b'unprocessed: ', response[b'UnprocessedItems']
                print b''
        else:
            item = json.loads(line)
            table.new_item(None, None, item).put(expected_value=expected)
            consumed = None
        if self.consumed and consumed:
            print b'consumed units:', consumed
        return

    def do_import(self, line):
        """import [:tablename] filename|list"""
        table, line = self.get_table_params(line)
        if line[0] == b'[':
            list = self.get_list(line)
        else:
            with open(line) as (f):
                list = self.get_list(f.read())
        items = 0
        consumed = 0
        for item in list:
            table.new_item(None, None, item).put()
            items += 1
            print item[b'id']

        print b'imported %s items, consumed units:%s' % (items, consumed)
        return

    def do_update(self, line):
        """update [:tablename] {hashkey[,rangekey]} [!fieldname:expectedvalue] [-add|-delete] [+ALL_OLD|ALL_NEW|UPDATED_OLD|UPDATED_NEW] {attributes}"""
        table, line = self.get_table_params(line)
        hkey, line = line.split(b' ', 1)
        expected, attr = self.get_expected(line)
        if attr[0] == b'-':
            op, attr = attr.split(b' ', 1)
            op = op[1]
        else:
            op = b'u'
        if attr[0] == b'+':
            ret, attr = attr.split(b' ', 1)
            ret = ret[1:]
        else:
            ret = b'ALL_NEW'
        if b',' in hkey:
            hkey, rkey = hkey.split(b',', 1)
        else:
            rkey = None
        item = table.new_item(hash_key=self.get_typed_key_value(table, hkey), range_key=self.get_typed_key_value(table, rkey, False))
        attr = json.loads(attr.strip())
        for name in attr.keys():
            value = attr[name]
            if isinstance(value, list):
                value = set(value)
            if op == b'a':
                item.add_attribute(name, value)
            elif op == b'd':
                item.delete_attribute(name, value)
            else:
                item.put_attribute(name, value)

        self.pprint(item)
        updated = item.save(expected_value=expected or None, return_values=ret)
        self.pprint(updated)
        if self.consumed:
            print b'consumed units:', item.consumed_units
        return

    def do_get(self, line):
        """
        get [:tablename] {haskkey} [rangekey]
        or
        get [:tablename] ((hkey,rkey), (hkey,rkey)...)

        """
        table, line = self.get_table_params(line)
        if line.startswith(b'(') or line.startswith(b'[') or b',' in line:
            list = self.get_list(line)
            from collections import OrderedDict
            ordered = OrderedDict()
            for id in list:
                if not isinstance(id, tuple):
                    hkey = self.get_typed_key_value(table, unicode(id))
                    rkey = None
                else:
                    hkey = self.get_typed_key_value(table, unicode(id[0]), True)
                    rkey = self.get_typed_key_value(table, unicode(id[1]), False)
                ordered[(hkey, rkey)] = None

            batch = self.conn.new_batch_list()
            batch.add_batch(table, ordered.keys())
            response = batch.submit()
            hkey = table.schema.hash_key_name
            rkey = table.schema.range_key_name
            for item in response[b'Responses'][table.name][b'Items']:
                ordered[(item.get(hkey), item.get(rkey))] = item

            self.pprint(filter(None, ordered.values()))
        else:
            args = self.getargs(line)
            hkey = self.get_typed_key_value(table, args[0], True)
            rkey = self.get_typed_key_value(table, args[1], False) if len(args) > 1 else None
            item = table.get_item(hkey, rkey, consistent_read=self.consistent)
            self.pprint(item)
            if self.consumed:
                print b'consumed units:', item.consumed_units
        return

    def do_rm(self, line):
        """rm [:tablename] [!fieldname:expectedvalue] [-v] {haskkey [rangekey]}"""
        table, line = self.get_table_params(line)
        expected, line = self.get_expected(line)
        args = self.getargs(line)
        if b'-v' in args:
            ret = b'ALL_OLD'
            args.remove(b'-v')
        else:
            ret = None
        hkey = self.get_typed_key_value(table, args[0], True)
        rkey = self.get_typed_key_value(table, args[1], False) if len(args) > 1 else None
        item = table.new_item(hash_key=hkey, range_key=rkey)
        item = item.delete(expected_value=expected, return_values=ret)
        self.pprint(item)
        if self.consumed:
            print b'consumed units:', item.consumed_units
        return

    def do_rmattr(self, line):
        """rmattr [:tablename] [!fieldname:expectedvalue] [-v] {haskkey,[rangekey]} attr [attr...]"""
        table, line = self.get_table_params(line)
        expected, line = self.get_expected(line)
        args = self.getargs(line)
        if b'-v' in args:
            ret = b'ALL_OLD'
            args.remove(b'-v')
        else:
            ret = None
        hkey = self.get_typed_key_value(table, args[0], True)
        rkey = self.get_typed_key_value(table, args[1], False) if len(args) > 1 else None
        item = table.new_item(hash_key=hkey, range_key=rkey)
        for arg in args:
            item.delete_attribute(arg)

        item = item.save(expected_value=expected, return_values=ret)
        self.pprint(item)
        if self.consumed:
            print b'consumed units:', item.consumed_units
        return

    def do_scan(self, line):
        """
        scan [:tablename] [--batch=#] [-{max}] [--count|-c] [--array|-a] [+filter_attribute:filter_value] [attributes,...]

        if filter_value contains '=' it's interpreted as {conditional}={value} where condtional is:

            eq (equal value)
            ne {value} (not equal value)
            le (less or equal then value)
            lt (less then value)
            ge (greater or equal then value)
            gt (greater then value)
            :exists (value exists)
            :nexists (value does not exists)
            contains (contains value)
            ncontains (does not contains value)
            begin (attribute begins with value)
            between (between value1 and value2 - use: between=value1,value2)

        otherwise the value must fully match (equal attribute)
        """
        table, line = self.get_table_params(line)
        args = self.getargs(line)
        scan_filter = {}
        count = False
        as_array = False
        max_size = None
        batch_size = None
        start = None
        while args:
            arg = args[0]
            if arg.startswith(b'+'):
                args.pop(0)
                filter_name, filter_value = arg[1:].split(b':', 1)
                if filter_value.startswith(b'begin='):
                    filter_cond = BEGINS_WITH(self.get_typed_value(filter_name, filter_value[6:]))
                elif filter_value.startswith(b'eq='):
                    filter_cond = EQ(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value.startswith(b'ne='):
                    filter_cond = NE(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value.startswith(b'le='):
                    filter_cond = LE(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value.startswith(b'lt='):
                    filter_cond = LT(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value.startswith(b'ge='):
                    filter_cond = GE(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value.startswith(b'gt='):
                    filter_cond = GT(self.get_typed_value(filter_name, filter_value[3:]))
                elif filter_value == b':exists':
                    filter_cond = NOT_NULL()
                elif filter_value == b':nexists':
                    filter_cond = NULL()
                elif filter_value.startswith(b'contains='):
                    filter_cond = CONTAINS(self.get_typed_value(filter_name, filter_value[9:]))
                elif filter_value.startswith(b'between='):
                    parts = filter_value[8:].split(b',', 1)
                    filter_cond = BETWEEN(self.get_typed_value(parts[0]), self.get_typed_value(filter_name, parts[1]))
                else:
                    filter_cond = EQ(self.get_typed_value(filter_name, filter_value))
                scan_filter[filter_name] = filter_cond
            elif arg.startswith(b'--batch='):
                args.pop(0)
                batch_size = int(arg[8:])
            elif arg.startswith(b'--max='):
                args.pop(0)
                max_size = int(arg[6:])
            elif arg.startswith(b'--start='):
                args.pop(0)
                start = (arg[8:],)
            elif arg == b'--next':
                args.pop(0)
                if self.next_key:
                    start = self.next_key
                else:
                    print b'no next'
                    return
            elif arg in ('--array', '-a'):
                args.pop(0)
                as_array = True
            elif arg in ('--count', '-c'):
                args.pop(0)
                count = True
            elif arg[0] == b'-' and arg[1:].isdigit():
                args.pop(0)
                max_size = int(arg[1:])
            elif arg == b'--':
                args.pop(0)
                break
            elif arg.startswith(b'-'):
                args.pop(0)
                print b'invalid argument: %s' % arg
                break
            else:
                break

        attr_keys = args[0].split(b',') if args else None
        attrs = list(set(attr_keys)) if attr_keys else None
        result = table.scan(scan_filter=scan_filter, attributes_to_get=attrs, request_limit=batch_size, max_results=max_size, count=count, exclusive_start_key=start)
        if count:
            print b'count: %s/%s' % (result.scanned_count, result.count)
            self.next_key = None
        else:
            if as_array and attr_keys:
                self.print_iterator_array(result, attr_keys)
            else:
                self.print_iterator(result)
            self.next_key = result.last_evaluated_key
        if self.consumed:
            print b'consumed units:', result.consumed_units
        return

    def do_query(self, line):
        """
        query [:tablename] [-r] [--count|-c] [--array|-a] [-{max}] [{rkey-condition}] hkey [attributes,...]

        where rkey-condition:
            --eq={key} (equal key)
            --ne={key} (not equal key)
            --le={key} (less or equal than key)
            --lt={key} (less than key)
            --ge={key} (greater or equal than key)
            --gt={key} (greater than key)
            --exists   (key exists)
            --nexists  (key does not exists)
            --contains={key} (contains key)
            --ncontains={key} (does not contains key)
            --begin={startkey} (rkey begins with startkey)
            --between={firstkey},{lastkey} (between firstkey and lastkey)
        """
        table, line = self.get_table_params(line)
        args = self.getargs(line)
        condition = None
        count = False
        as_array = False
        max_size = None
        batch_size = None
        start = None
        if b'-r' in args:
            asc = False
            args.remove(b'-r')
        else:
            asc = True
        while args:
            arg = args[0]
            if arg[0] == b'-' and arg[1:].isdigit():
                max_size = int(arg[1:])
                args.pop(0)
            elif args[0].startswith(b'--max='):
                arg = args.pop(0)
                max_size = int(arg[6:])
            elif arg in ('--count', '-c'):
                count = True
                args.pop(0)
            elif arg in ('--array', '-a'):
                as_array = True
                args.pop(0)
            elif args[0].startswith(b'--batch='):
                arg = args.pop(0)
                batch_size = int(arg[8:])
            elif args[0].startswith(b'--start='):
                arg = args.pop(0)
                start = (arg[8:],)
            elif args[0] == b'--next':
                arg = args.pop(0)
                if self.next_key:
                    start = self.next_key
                else:
                    print b'no next'
                    return
            elif arg.startswith(b'--begin='):
                condition = BEGINS_WITH(self.get_typed_key_value(table, arg[8:], False))
                args.pop(0)
            elif arg.startswith(b'--eq='):
                condition = EQ(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg.startswith(b'--ne='):
                condition = NE(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg.startswith(b'--le='):
                condition = LE(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg.startswith(b'--lt='):
                condition = LT(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg.startswith(b'--ge='):
                condition = GE(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg.startswith(b'--gt='):
                condition = GT(self.get_typed_key_value(table, arg[5:], False))
                args.pop(0)
            elif arg == b'--exists':
                condition = NOT_NULL()
                args.pop(0)
            elif arg == b'--nexists':
                condition = NULL()
                args.pop(0)
            elif arg.startswith(b'--contains='):
                condition = CONTAINS(self.get_typed_key_value(table, arg[11:], False))
                args.pop(0)
            elif arg.startswith(b'--between='):
                parts = arg[10:].split(b',', 1)
                condition = BETWEEN(self.get_typed_key_value(table, parts[0], True), self.get_typed_key_value(table, parts[1], False))
                args.pop(0)
            else:
                break

        hkey = self.get_typed_key_value(table, args.pop(0))
        attr_keys = args[0].split(b',') if args else None
        attrs = list(set(attr_keys)) if attr_keys else None
        result = table.query(hkey, range_key_condition=condition, attributes_to_get=attrs, scan_index_forward=asc, request_limit=batch_size, max_results=max_size, count=count, exclusive_start_key=start)
        if count:
            print b'count: %s/%s' % (result.scanned_count, result.count)
            self.next_key = None
        else:
            if as_array and attr_keys:
                self.print_iterator_array(result, attr_keys)
            else:
                self.print_iterator(result)
            self.next_key = result.last_evaluated_key
        if self.consumed:
            print b'consumed units:', result.consumed_units
        return

    def do_rmall(self, line):
        """remove [tablename...] yes"""
        args = self.getargs(line)
        if args and args[(-1)] == b'yes':
            args.pop()
            if not args:
                args = [
                 self.table.name]
            while args:
                table = self.conn.get_table(args.pop(0))
                print b'from table ' + table.name
                for item in table.scan(attributes_to_get=[], request_limit=10):
                    print b'  removing %s' % item
                    item.delete()

        else:
            print b'ok, never mind...'

    def do_EOF(self, line):
        """Exit shell"""
        return True

    do_ls = do_tables
    do_mkdir = do_create
    do_rmdir = do_drop
    do_delete = do_drop
    do_cd = do_use
    do_q = do_query
    do_l = do_scan
    do_exit = do_quit = do_EOF

    def emptyline(self):
        pass

    def onecmd(self, s):
        try:
            return Cmd.onecmd(self, s)
        except IndexError:
            print b'invalid number of arguments'
            return False
        except NotImplementedError as e:
            print e.message
        except DynamoDBConditionalCheckFailedError as e:
            print e.error_message
        except (DynamoDBResponseError, BotoClientError) as dberror:
            print self.pp.pformat(dberror)
        except:
            traceback.print_exc()

        return False

    def default(self, line):
        line = line.strip()
        if line and line[0] in ('#', ';'):
            return False
        else:
            return Cmd.default(self, line)

    def completedefault(self, test, line, beginidx, endidx):
        list = []
        for t in self.tables:
            if t.startswith(test):
                list.append(t)

        return list

    def preloop(self):
        print b'\ndynash %s: A simple shell to interact with DynamoDB' % __version__
        if self.history_file and os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)
        if self.conn:
            try:
                self.do_tables(b'')
            except:
                traceback.print_exc()

    def postloop(self):
        if self.history_file:
            readline.set_history_length(100)
            readline.write_history_file(self.history_file)
        print b'Goodbye!'


def set_environment(env):
    found = False
    for section in [b'Credentials', b'DynamoDB']:
        env_section = b'%s.%s' % (env, section)
        if boto.config.has_section(env_section):
            found = True
            if not boto.config.has_section(section):
                boto.config.add_section(section)
            for o in boto.config.options(env_section):
                boto.config.set(section, o, boto.config.get(env_section, o))

    return found


def run_command():
    import sys
    args = sys.argv
    args.pop(0)
    verbose = False
    while args and args[0].startswith(b'-'):
        arg = args.pop(0)
        if arg.startswith(b'--env='):
            set_environment(arg[6:])
        elif arg.startswith(b'--verbose'):
            verbose = True
        elif arg == b'--':
            break
        else:
            print b'invalid option or parameter: %s' % arg
            sys.exit(1)

    DynamoDBShell(verbose).cmdloop()


if __name__ == b'__main__':
    run_command()