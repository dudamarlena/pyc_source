# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/import_data.py
# Compiled at: 2018-06-04 12:38:26
# Size of source mod 2**32: 17427 bytes
import re, sys, pandokia.common as common, pandokia
exit_status = 0
line_count = 0
insert_count = 0
quiet = False
debug = False
default_record = dict()
all_test_run = dict()
all_test_runs = dict()

def read_records(filename):
    global debug
    global default_record
    global exit_status
    global line_count
    found_any = 0
    result = default_record.copy()
    parsing_name = ''
    parsing_log = False
    if filename == '-':
        data_source = sys.stdin
    else:
        data_source = open(filename, 'r')
    with data_source as (data):
        line = ''
        while 1:
            line_count += 1
            try:
                line = data.readline()
            except UnicodeDecodeError as e:
                linear_offset = data.tell()
                print('Unicode Error: {} near offset {linear_offset:d} [{linear_offset:x}h]'.format((e.reason),
                  linear_offset=linear_offset))
                continue

            if parsing_log:
                if debug:
                    print('debug: {:d}: ingesting log data: {}'.format(line_count, line.strip()))
                name = parsing_name
                if line == '\n' or line == '\r\n':
                    if debug:
                        print('debug: {:d}: End of log data'.format(line_count))
                    parsing_log = False
                    continue
                line.startswith('.') or print('Invalid input @ {:d}: Missing prefix character in multi-line: {}'.format(line_count, name, line.strip()))
                exit_status = 1
                parsing_log = False
                continue
                result[name] += line
            else:
                if not line:
                    break
                if line.startswith('#'):
                    if debug:
                        print('debug: {:d}: skipping comment'.format(line_count))
                elif not line:
                    if found_any:
                        print('Invalid input @ {:d}: Missing "END"'.format(line_count))
                        exit_status = 1
                        found_any = 0
                        yield result
                else:
                    line = line.strip()
                    if not line:
                        continue
                    if line == 'END':
                        if debug:
                            print('debug: {:d}: END found'.format(line_count))
                        if found_any:
                            yield result
                            result = default_record.copy()
                            continue
                            if line == 'SETDEFAULT':
                                if debug:
                                    print('debug: {:d}: SETDEFAULT found'.format(line_count))
                                if 'test_name' in result:
                                    s = 'Invalid input @ {:d}: test_name in SETDEFAULT {:s}'.format(line_count, name)
                                    raise Exception(s)
                                default_record = result.copy()
                                continue
                            if line == 'START':
                                if debug:
                                    print('debug: {:d}: START found'.format(line_count))
                                result = dict()
                                default_record = dict()
                                found_any = 0
                                continue
                            if line.find('=') > -1:
                                rec = line.split('=', 1)
                                elements = len(rec)
                                name = rec[0].lower()
                                if elements > 1:
                                    value = ''.join(rec[1:])
                                if debug:
                                    print('debug: {:d}: Generated key-pair from "{:s}"'.format(line_count, line))
                                result[name] = value
                                found_any = 1
                                continue
                            if not line.startswith('.'):
                                if line.endswith(':'):
                                    if debug:
                                        print('debug: {:d}: Checking for log data'.format(line_count))
                                    else:
                                        rec = [x for x in line.split(':', 1) if x]
                                        elements = len(rec)
                                        name = rec[0]
                                        if elements > 1:
                                            print('Invalid input @ {:d}: Data after colon in "{:s}"'.format(line_count, line))
                                            exit_status = 1
                                        if debug:
                                            print('debug: {:d}: Parsing log'.format(line_count))
                                    found_any += 1
                                    result[name] = ''
                                    parsing_name = name
                                    parsing_log = True
                                    continue
                            print('Invalid input @ {:d}: Unrecognized line {:s}'.format(line_count, line))
                            exit_status = 1


class test_result(object):

    def _lookup(self, name, default=None):
        if name in self.dict:
            return self.dict[name]
        if default is not None:
            return default
        self.missing.append(name)

    def __init__(self, dict):
        global all_test_run
        self.dict = dict
        self.missing = []
        self.test_run = self._lookup('test_run')
        all_test_run[self.test_run] = 1
        self.project = self._lookup('project')
        self.test_name = self._lookup('test_name')
        self.context = self._lookup('context', 'default')
        self.host = self._lookup('host', 'unknown')
        self.location = self._lookup('location', '')
        self.test_runner = self._lookup('test_runner')
        self.status = self._lookup('status')
        self.log = self._lookup('log', '')
        self.start_time = self._lookup('start_time', '')
        self.end_time = self._lookup('end_time', '')
        self.has_okfile = 'tda__okfile' in dict
        if '\n' in self.test_name:
            self.test_name = self.test_name.replace('\n', '_')
        if ' ' in self.test_name:
            self.test_name = self.test_name.replace(' ', '_')
        if '\t' in self.test_name:
            self.test_name = self.test_name.replace('\t', '_')
        while self.test_name.startswith('/') or self.test_name.startswith('.'):
            self.test_name = self.test_name[1:]

        try:
            if self.start_time != '':
                self.start_time = common.parse_time(self.start_time)
                self.start_time = common.sql_time(self.start_time)
        except ValueError:
            print('')
            print('INVALID START TIME, line %d' % line_count)

        try:
            if self.end_time != '':
                self.end_time = common.parse_time(self.end_time)
                self.end_time = common.sql_time(self.end_time)
        except ValueError:
            print('')
            print('INVALID END TIME, line %d' % line_count)

        self.tda = {}
        self.tra = {}
        for x in dict:
            if x.startswith('tda_'):
                self.tda[x[4:]] = self._lookup(x)
            if x.startswith('tra_'):
                self.tra[x[4:]] = self._lookup(x)

        if len(self.missing) > 0:
            print('FIELDS MISSING %s %d' % (self.missing, line_count))
            exit_status = 1

    def try_insert(self, db, key_id):
        if self.has_okfile:
            okf = 'T'
        else:
            okf = 'F'
        if key_id:
            ss = 'key_id, '
            ss1 = ', :13'
            parm = [key_id]
        else:
            parm = []
            ss = ''
            ss1 = ''
        parm += [self.test_run,
         self.host,
         self.project,
         self.test_name,
         self.context,
         self.status,
         self.start_time,
         self.end_time,
         self.location,
         self.attn,
         self.test_runner,
         okf]
        return db.execute('INSERT INTO result_scalar ( %s test_run, host, project, test_name, context, status, start_time, end_time, location, attn, test_runner, has_okfile ) values  ( :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12 %s )' % (
         ss, ss1), parm)

    def insert(self, db):
        global insert_count
        if len(self.missing) > 0:
            print('NOT INSERTED DUE TO MISSING FIELDS %s %s %d' % (
             self.missing, self.test_name, line_count))
            exit_status = 1
            return
        else:
            if self.test_name.endswith('nose.failure.Failure.runTest'):
                print('NOT INSERTING %s, (not an error)' % self.test_name)
                print('Can we have the nose plugin stop reporting these?')
                return
            else:
                self.test_name = self.test_name.replace('//', '/')
                if self.status == 'P':
                    self.attn = 'N'
                else:
                    self.attn = 'Y'
                self.attn = self._lookup('attn', self.attn)
                if db.next:
                    key_id = db.next('sequence_key_id')
                else:
                    key_id = None
            try:
                res = self.try_insert(db, key_id)
                if not db.next:
                    key_id = res.lastrowid
                insert_count += 1
            except db.IntegrityError as e:
                db.rollback()
                c = db.execute("select status from result_scalar where test_run = :1 and host = :2 and context = :3 and project = :4 and test_name = :5 and status = 'M'", (
                 self.test_run,
                 self.host,
                 self.context,
                 self.project,
                 self.test_name))
                x = c.fetchone()
                if x is not None:
                    db.execute("delete from result_scalar where test_run = :1 and host = :2 and context = :3 and project = :4 and test_name = :5 and status = 'M'", (
                     self.test_run,
                     self.host,
                     self.context,
                     self.project,
                     self.test_name))
                    res = self.try_insert(db, key_id)
                    insert_count += 1
                else:
                    raise e

            for x in self.tda:
                db.execute('INSERT INTO result_tda ( key_id, name, value ) values ( :1, :2, :3 )', (
                 key_id,
                 x,
                 self.tda[x]))

            for x in self.tra:
                db.execute('INSERT INTO result_tra ( key_id, name, value ) values ( :1, :2, :3 )', (
                 key_id,
                 x,
                 self.tra[x]))

            if len(self.log) > 990000:
                self.log = self.log[0:990000] + '\n\n\nLOG TRUNCATED BECAUSE MYSQL CANNOT HANDLE RECORDS > 1 MB\n'
                print('LOG TRUNCATED: key_id=%d' % key_id)
            db.execute('INSERT INTO result_log ( key_id, log ) values ( :1, :2 )', (
             key_id, self.log))
            db.commit()
            if self.test_run not in all_test_runs:
                try:
                    db.execute('INSERT INTO distinct_test_run ( test_run, valuable ) VALUES ( :1, 0 )', (
                     self.test_run,))
                    db.commit()
                except db.IntegrityError:
                    db.rollback()

                all_test_runs[self.test_run] = 1


def run(argv, hack_callback=None):
    global debug
    global insert_count
    global line_count
    global quiet
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-H', '--host')
    parser.add_argument('-c', '--context', default='unk')
    parser.add_argument('-p', '--project')
    parser.add_argument('--test-runner')
    parser.add_argument('--test-run')
    parser.add_argument('filename', nargs='*', default=[sys.stdin])
    args = parser.parse_args(argv)
    pdk_db = pandokia.cfg.pdk_db
    default_test_runner = ''
    insert_count = 0
    line_count = 0
    duplicate_count = 0
    failure_count = 0
    quiet = args.quiet
    debug = args.debug
    for handle in args.filename:
        if not quiet:
            print('FILE: %s' % handle)
        for x in read_records(handle):
            if x is None:
                print('Failed: Invalid test record @ {}'.format(line_count))
                failure_count += 1
            else:
                if 'test_run' not in x:
                    x['test_run'] = args.test_run
                else:
                    if 'context' not in x:
                        x['context'] = args.context
                    else:
                        if 'host' not in x:
                            x['host'] = args.host
                        if 'project' not in x:
                            x['project'] = args.project
                        if 'test_runner' not in x:
                            x['test_runner'] = args.test_runner
                    if 'name' in x:
                        x['test_name'] = x['name']
                        del x['name']
                if 'test_name' not in x:
                    print('warning: no test name on line: %4d' % line_count)
                    print('   %s' % [zz for zz in x])
                else:
                    if x['test_name'].endswith('.xml') or x['test_name'].endswith('.log'):
                        x['test_name'] = x['test_name'][:-4]
                    else:
                        rx = test_result(x)
                        if hack_callback:
                            if not hack_callback(rx):
                                continue
                        try:
                            rx.insert(pdk_db)
                            if not quiet:
                                print('Imported: {}'.format(rx.test_name))
                        except pdk_db.IntegrityError as e:
                            if debug:
                                print('IntegrityError: Cannot insert {} due to "{}"'.format(rx.test_name, e))
                            if not quiet:
                                print('Skipped: {}'.format(rx.test_name))
                            duplicate_count += 1

                    pdk_db.commit()

    result_str = '{:d} records inserted'.format(insert_count)
    if duplicate_count:
        result_str += ' ({:d} skipped)'.format(duplicate_count)
    if failure_count:
        result_str += ' ({:d} failed)'.format(failure_count)
    if not quiet:
        print(result_str)
    sys.exit(exit_status)


def hack_import(args):
    run(args, hack_callback=pyetchack)


def pyetchack(arg):
    n = arg.test_name
    if not n.endswith('.all'):
        return False
    else:
        arg.test_name = arg.test_name.replace('.peng.all', '')
        return True