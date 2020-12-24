# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\tools\dvstool_oracle.py
# Compiled at: 2016-01-14 15:12:15
import os, sys, re, datetime, ConfigParser, time, shutil, subprocess, glob, optparse, cStringIO, tempfile
from daversy.utils import get_uuid4
from daversy.db.oracle.connection import DEFAULT_NLS_LANG
from lxml import etree
CMDLINE = 100
TOOLERR = 101
CMDERR = 102
SQLERR = 103
MIGERR = 104
ALL_FILES = []

class DvsOracleTool(object):

    def execute(self, cmd, env=None):
        try:
            command = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE, env=env)
            self.output = ''
            output = []
            command.stdin.close()
            while 1:
                temp = command.stdout.readline()
                if not temp:
                    break
                output.append(temp.rstrip())

            result = command.wait()
            self.output = ('\n').join(output).strip()
            return result
        except KeyboardInterrupt as SystemExit:
            raise
        except:
            pass

        return

    def execute_out(self, msg, cmd, env=None):
        self.message(msg)
        command = subprocess.Popen(cmd, env=env)
        self.output = ''
        result = command.wait()
        return result

    def tempfile(self, data='', ext='.sql'):
        handle, location = tempfile.mkstemp(ext)
        os.write(handle, data)
        os.close(handle)
        location = location.replace('\\', '/')
        ALL_FILES.append(location)
        return location

    def sqlplus(self, code):
        result = False
        location = self.tempfile(code)
        try:
            env = os.environ.copy()
            env['NLS_LANG'] = DEFAULT_NLS_LANG
            status = self.execute(['sqlplus', '-S', '-L', self.connectString,
             '@' + location], env)
            result = status == 0
        except KeyboardInterrupt as SystemExit:
            raise
        except:
            pass

        return result

    def check_commands(self):
        self.execute(['sqlplus', '/?'])
        if not self.output or 'SQL*Plus' not in self.output:
            self.message('Unable to execute SQL*Plus, please check that Oracle is in the PATH.')
            self.quit(TOOLERR)
        if self.execute(['dvs']) != 0:
            self.message('Unable to execute Daversy, please ensure that it is in the PATH.')
            self.quit(TOOLERR)
        if hasattr(self, 'connectString') and not self.sqlplus(SQLPLUS_EXEC % ''):
            self.message('Unable to connect to Oracle, please check the connection string.')
            self.quit(TOOLERR)

    def message(self, msg, prefix='**'):
        if prefix:
            print prefix, msg
        else:
            print msg
        sys.stdout.flush()

    def execute_cmd(self, msg, cmd, env=None):
        self.message(msg)
        status = self.execute(cmd, env)
        if not status == 0:
            self.message('FAILED: ' + str(cmd))
            print self.output
            self.quit(CMDERR)

    def execute_ddl(self, msg, *list):
        self.message(msg)
        for ddl in list:
            if not self.sqlplus(SQLPLUS_EXEC_DDL % ddl):
                self.message('FAILED')
                print self.output
                self.quit(SQLERR)

    def execute_sql(self, msg, *list):
        self.message(msg)
        for ddl in list:
            if not self.sqlplus(SQLPLUS_EXEC % ddl):
                self.message('FAILED')
                print self.output
                self.quit(SQLERR)

    def get_version_count(self, *versions):
        sql = GETVERSIONCOUNT_SQL % ("', '").join(versions)
        if not self.sqlplus(SQLPLUS_EXEC % sql):
            self.message('Failed to get version count: %s' % (',').join(versions))
            print self.output
            self.quit(SQLERR)
        match = re.match('VERSION_COUNT\\s+\\-+\\s+(\\d+)\\s*', self.output)
        if not match:
            self.message('Failed to parse version count')
            print self.output
            self.quit(SQLERR)
        return int(match.group(1))

    def read_file(self, name):
        file = open(name, 'r')
        data = file.read()
        file.close()
        return data

    def write_file(self, name, data):
        file = open(name, 'w')
        file.write(data)
        file.close()

    def cleanup(self):
        while len(ALL_FILES):
            try:
                os.remove(ALL_FILES.pop())
            except OSError:
                pass

    def quit(self, code=0):
        self.cleanup()
        sys.exit(code)


class CleanDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog clean CONNECT-STRING')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 1:
            parser.print_help()
            self.quit(CMDLINE)
        self.connectString, = args
        self.check_commands()
        self.run()

    def run(self):
        self.execute_ddl('dropping all schema objects', DROPCODE_SQL, DROPTABLE_SQL, DROPTYPES_SQL)


class ExportDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog export SOURCE-DB DUMP-FILE')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        self.connectString, dump = args
        self.check_commands()
        self.run(dump)

    def run(self, dump):
        env = os.environ.copy()
        env['NLS_LANG'] = DEFAULT_NLS_LANG
        self.execute_ddl('recreating existing types', RECREATETYPES_SQL)
        self.execute_out('extracting source   schema', [
         'exp', self.connectString, 'file=' + dump,
         'statistics=none'], env)
        self.execute_ddl('recreating existing types', RECREATETYPES_SQL)


class ImportDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog import DUMP-FILE TARGET-DB')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        dump, self.connectString = args
        self.check_commands()
        self.run(dump)

    def run(self, dump):
        env = os.environ.copy()
        env['NLS_LANG'] = DEFAULT_NLS_LANG
        self.execute_ddl('dropping   target   schema', DROPCODE_SQL, DROPTABLE_SQL, DROPTYPES_SQL)
        self.execute_out('restoring  target   schema', [
         'imp', self.connectString, 'file=' + dump, 'full=y'], env)
        self.execute_ddl('recompiling schema', RECREATETYPES_SQL, RECOMPILE_SQL)


class CopyDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog copy SOURCE-DB TARGET-DB')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        source, target = args
        if source == target:
            parser.error('SOURCE-DB cannot be the same as TARGET-DB')
        self.check_commands()
        self.run(source, target)

    def run(self, source, target):
        self.connectString = target
        self.execute_sql('checking for connnection to target DB', 'SELECT 1 FROM dual')
        dump = self.tempfile(ext='.dmp')
        exp = ExportDb()
        exp.connectString = source
        exp.run(dump)
        imp = ImportDb()
        imp.connectString = target
        imp.run(dump)


class WrapDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog wrap SOURCE-STATE TARGET-STATE')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        source, target = args
        self.check_commands()
        self.run(source, target)

    def run(self, source, target):
        ddl = self.tempfile(ext='.sql')
        filter = self.tempfile(CODEFILTER_INI, ext='.ini')
        self.execute_cmd('generating schema DDL', [
         'dvs', 'generate', '-s', 'all',
         '-f', filter, source, ddl])
        if not self.read_file(ddl).strip():
            self.message('no objects need to be encoded, exiting.')
            shutil.copy2(source, target)
            return
        else:
            self.execute_cmd('encoding schema DDL', [
             'wrap', 'iname=' + ddl, 'oname=' + ddl + '.enc'])
            os.remove(ddl)
            os.rename(ddl + '.enc', ddl)
            data = ('\n').join(x.rstrip() for x in open(ddl).readlines()) + '\n'
            encoded_data = WRAPCODE_REGEX.findall(data)
            self.message('extracting encoded objects')
            from daversy.state import FileState
            provider = FileState()
            state = provider.load(source)
            pkg, typ = {}, {}
            for source, objtype, name in encoded_data:
                name, objtype = name.upper(), objtype.upper()
                if objtype in ('PROCEDURE', 'FUNCTION'):
                    state[(objtype.lower() + 's')][name].source = source.strip() + '\n\n/'
                if objtype == 'PACKAGE':
                    pkg[name] = source.strip() + '\n\n/\n'
                elif objtype == 'PACKAGE BODY':
                    state.packages[name].source = pkg[name] + source.strip() + '\n\n/'
                    del pkg[name]
                if objtype == 'TYPE':
                    typ[name] = source.strip() + '\n\n/\n'
                elif objtype == 'TYPE BODY':
                    state.types[name].source = typ[name] + source.strip() + '\n\n/'
                    del typ[name]

            for name in pkg:
                state.packages[name].source = pkg[name].rstrip()

            for name in typ:
                state.types[name].source = typ[name].rstrip()

            self.message('saving updated state')
            provider.save(state, target, None)
            return


class UnwrapDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog unwrap SOURCE-STATE TARGET-DB')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        state, self.connectString = args
        self.check_commands()
        self.run(state)

    def run(self, state):
        ddl = self.tempfile(ext='.sql')
        filter = self.tempfile(CODEFILTER_INI, ext='.ini')
        self.execute_cmd('generating updated objects', [
         'dvs', 'generate', '-f', filter, '-s', 'create', state, ddl])
        self.execute_ddl('dropping existing objects', DROPCODE_SQL, DROPTYPES_SQL, DROPCOMMENT_SQL)
        self.execute_ddl('creating updated objects', EXECSCRIPT_SQL % ddl)
        self.execute_cmd('generating updated comments', [
         'dvs', 'generate', '-s', 'comment', state, ddl])
        self.execute_ddl('applying updated comments', EXECSCRIPT_SQL % ddl)
        self.execute_ddl('recompiling schema', RECOMPILE_SQL)


class CreateDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog create [options] CONNECT-STRING STATE')
        parser.add_option('--wrap', action='store_true', default=False, dest='wrap', help='run the Oracle wrap utility on generated SQL')
        parser.add_option('--sql-type', dest='sql_type', metavar='TYPE', default='all', help='generated the specified SQL type (default: "all")')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        self.connectString, state = args
        self.check_commands()
        self.run(options, state)

    def run(self, options, state):
        self.execute_cmd('getting state version', ['dvs', 'name', state])
        version = self.output
        ddl = self.tempfile()
        self.execute_cmd('generating schema DDL', [
         'dvs', 'generate', '-s', options.sql_type, state, ddl])
        if options.wrap:
            self.execute_cmd('encoding schema DDL', [
             'wrap', 'iname=' + ddl, 'oname=' + ddl + '.enc'])
            os.remove(ddl)
            os.rename(ddl + '.enc', ddl)
        self.execute_ddl('dropping existing schema', DROPCODE_SQL, DROPTABLE_SQL, DROPTYPES_SQL)
        self.execute_ddl('creating new schema', SCHEMALOG_SQL % version, EXECSCRIPT_SQL % ddl)
        self.execute_ddl('recompiling schema', RECOMPILE_SQL)


class DiffDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog [options] SOURCE TARGET')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 2:
            parser.print_help()
            self.quit(CMDLINE)
        self.check_commands()
        input, output = args
        self.quit(self.run(input, output))

    def run(self, input, output):
        self.execute_cmd('comparing states', ['dvs', 'compare', input, output])
        if not self.output:
            return 0
        log = cStringIO.StringIO(self.output)
        for line in log:
            for elem in MIGRATION_NEEDED:
                if elem in line and not ('@comment' in line and line.startswith('M')):
                    return 2

        return 1


class MigrateDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog migrate [options] CONNECT-STRING STATE FILTER MIGRATION-DIR')
        parser.add_option('--wrap', action='store_true', default=False, dest='wrap', help='run the Oracle wrap utility on generated SQL')
        parser.add_option('-i', dest='include_tags', default='all', metavar='TAGS', help='include objects matching specified TAGS from filter (default: "all")')
        parser.add_option('-x', dest='exclude_tags', default='ignore', metavar='TAGS', help='exclude objects matching specified TAGS from filter (default: "ignore")')
        parser.add_option('--no-comment', action='store_true', default=False, dest='no_comment', help='do not update the comments in the target schema')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 4:
            parser.print_help()
            self.quit(CMDLINE)
        self.connectString, state, filter, migration_dir = args
        self.check_commands()
        if not os.path.isdir(migration_dir):
            parser.error('The migrations directory does not exist')
        self.quit(self.run(options, state, filter, migration_dir))

    def run(self, options, state, filter, migration_dir):
        self.execute_cmd('getting target state version', ['dvs', 'name', state])
        self.target_version = self.output
        self.execute_ddl('getting source state version', GETVERSION_SQL)
        match = re.match('SCHEMA_VERSION\\s+\\-+\\s+([\\w\\-]+)\\s*', self.output)
        if not match:
            self.message('cannot find schema version')
            print self.output
            self.quit(SQLERR)
        self.source_version = match.group(1)
        self.start_version = self.source_version
        if self.source_version == self.target_version:
            self.message('no migration needed')
            return 0
        else:
            self.message('%s => %s' % (self.source_version, self.target_version))
            self.setup_migrations(migration_dir)
            error = self.do_migrations(migration_dir)
            if error != 0:
                return error
            code_config = self.tempfile(CODEFILTER_INI, '.ini')
            ddl = self.tempfile()
            self.execute_cmd('generating updated objects', [
             'dvs', 'generate', '-f', code_config,
             '-s', 'create', state, ddl])
            if options.wrap:
                self.execute_cmd('encoding schema DDL', [
                 'wrap', 'iname=' + ddl, 'oname=' + ddl + '.enc'])
                os.remove(ddl)
                os.rename(ddl + '.enc', ddl)
            self.execute_ddl('dropping existing objects', DROPCODE_SQL, DROPTYPES_SQL, DROPCOMMENT_SQL)
            self.execute_ddl('creating updated objects', EXECSCRIPT_SQL % ddl)
            self.execute_ddl('recompiling schema', RECOMPILE_SQL)
            if not options.no_comment:
                self.execute_cmd('generating updated comments', [
                 'dvs', 'generate', '-s', 'comment', state, ddl])
                self.execute_ddl('applying updated comments', EXECSCRIPT_SQL % ddl)
            self.execute_ddl('recompiling schema', RECOMPILE_SQL)
            self.migration_check = self.tempfile(ext='.state')
            if filter:
                self.execute_cmd('extracting migrated state', [
                 'dvs', 'copy', 'oracle:' + self.connectString,
                 '-f', filter, '-i', options.include_tags,
                 '-x', options.exclude_tags, self.migration_check])
            else:
                self.execute_cmd('extracting migrated state', [
                 'dvs', 'copy', 'oracle:' + self.connectString,
                 self.migration_check])
            differ = DiffDb()
            return_val = differ.run(state, self.migration_check)
            if return_val == 2:
                self.message('migration was not successful: migrated and target schemas differ.')
                self.message(differ.output, None)
                self.execute_sql('marking unsuccessful migration', REMOVESCHEMAVERSION_SQL % self.target_version)
                return return_val
            if return_val == 1:
                self.message('warning: there were some code/comment changes!!')
                self.message(differ.output, None)
            self.execute_sql('migrated successfully to [%s]' % self.target_version, UPDATESCHEMA_SQL % (self.target_version, '** migration successful **'))
            return return_val

    def setup_migrations(self, dir):
        self.migrations = {}
        file_list = glob.glob(dir + '/*.sql')
        for file in file_list:
            data = self.read_file(file)
            match = MIGRATION_REGEX.match(data)
            if not match:
                self.message('[%s] is not a valid migration.' % os.path.basename(file))
                continue
            source, target, description = match.groups()
            if target == 'next-version':
                target = self.target_version
            entry = self.migrations.setdefault(source, {})
            entry[target] = (description, [data])

        no_migrations = ConfigParser.ConfigParser()
        no_migrations.read(os.path.join(dir, 'migration.ini'))
        for source in no_migrations.options('migrations'):
            target = no_migrations.get('migrations', source)
            entry = self.migrations.setdefault(source, {})
            entry[target] = ('** no migration needed **', [])

        self.bridge = self.get_bridge_migration(dir)
        self.migration_path = self.find_path(self.start_version)

    def do_migrations(self, dir):
        if not self.migration_path:
            self.message('unable to find a migration path')
            for i in range(len(self.broken_paths)):
                self.message('broken path #%d' % (i + 1))
                for version in self.broken_paths[i]:
                    self.message(version, '      ')

            return MIGERR
        if self.bridge:
            for guid, commands in self.bridge.items('actions'):
                if guid not in self.migration_path[1:]:
                    self.message('cannot find version [%s] in migration path' % guid)
                    self.quit(MIGERR)
                for command in commands.split('|'):
                    args = command.split()
                    meth = self.__class__.__dict__[('bridge_' + args[0].replace('-', '_'))]
                    if not meth:
                        self.message('unknown action [%s] in bridge action' % args[0])
                        self.quit(MIGERR)
                    src = self.migration_path[(self.migration_path.index(guid) - 1)]
                    meth(self, dir, src, guid, *args[1:])

        for i in range(len(self.migration_path) - 1):
            src, tgt = self.migration_path[i], self.migration_path[(i + 1)]
            desc, sql = self.migrations[src][tgt]
            if sql:
                sql.append(UPDATESCHEMA_SQL % (tgt, desc))
                self.execute_sql(('running migration: [%s]' % desc), *sql)
                time.sleep(2)

        if self.bridge:
            guid, desc = self.bridge.get('bridge', 'guid'), self.bridge.get('bridge', 'desc')
            self.execute_sql('bridge successful: [%s]' % desc, UPDATESCHEMA_SQL % (guid, desc))
        return 0

    def find_path(self, source):
        queue = [
         (
          source, [source])]
        seen = []
        leaf = []
        while queue:
            version, path = queue.pop(0)
            if version == self.target_version:
                return path
            if version not in self.migrations:
                leaf.append(path)
                continue
            if version in seen:
                self.message('Circular reference for %s' % version)
                continue
            seen.append(version)
            for migration in self.migrations[version]:
                new_path = list(path)
                new_path.append(migration)
                queue.insert(0, (migration, new_path))

        self.broken_paths = leaf
        return

    def get_bridge_migration(self, dir):
        for name in glob.glob(dir + '/*.ini'):
            if os.path.basename(name) == 'migration.ini':
                continue
            bridge = ConfigParser.ConfigParser()
            bridge.read(name)
            if 'bridge' not in bridge.sections():
                continue
            if self.source_version not in bridge.get('bridge', 'source').split():
                continue
            if self.get_version_count(bridge.get('bridge', 'guid')) != 0:
                continue
            self.message('detected bridge: [%s]' % bridge.get('bridge', 'desc'))
            self.start_version = bridge.get('bridge', 'rebase')
            self.message('%s => %s' % (self.start_version, self.target_version))
            return bridge

        return

    def bridge_skip_if_present(self, dir, src, tgt, *versions):
        count = self.get_version_count(*versions)
        if count == len(versions) and count > 0:
            desc, migr = self.migrations[src][tgt]
            self.migrations[src][tgt] = (desc, [])

    def bridge_replace_script(self, dir, src, tgt, *scripts):
        desc, migr = self.migrations[src][tgt]
        self.migrations[src][tgt] = (desc, self.get_scripts(dir, scripts))

    def bridge_run_pre_script(self, dir, src, tgt, *scripts):
        desc, migr = self.migrations[src][tgt]
        sql = self.get_scripts(dir, scripts)
        sql.extend(migr)
        self.migrations[src][tgt] = (desc, sql)

    def bridge_run_post_script(self, dir, src, tgt, *scripts):
        desc, migr = self.migrations[src][tgt]
        migr.extend(self.get_scripts(dir, scripts))
        self.migrations[src][tgt] = (desc, migr)

    def bridge_describe(self, dir, src, tgt, *new_desc):
        desc, migr = self.migrations[src][tgt]
        self.migrations[src][tgt] = ((' ').join(new_desc), migr)

    def get_scripts(self, dir, scripts):
        result = []
        for file in scripts:
            if os.path.isfile(os.path.join(dir, file)):
                result.append(open(os.path.join(dir, file), 'r').read())

        return result


class SyncDb(DvsOracleTool):

    def __main__(self):
        parser = optparse.OptionParser(usage='%prog sync [options] CONNECT-STRING TEMP-CONNECT-STRING BASE-DIR')
        parser.add_option('-i', dest='include_tags', default='all', metavar='TAGS', help='include objects matching specified TAGS from filter (default: "all")')
        parser.add_option('-x', dest='exclude_tags', default='ignore', metavar='TAGS', help='exclude objects matching specified TAGS from filter (default: "ignore")')
        options, args = parser.parse_args(sys.argv[2:])
        if not len(args) == 3:
            parser.print_help()
            self.quit(CMDLINE)
        self.connectString, self.tempConnectString, self.base_dir = args
        self.check_commands()
        if not os.path.isdir(self.base_dir):
            parser.error('The base directory does not exist')
        self.quit(self.run(options, self.base_dir))

    def run(self, options, base_dir):
        self.config_dir = os.path.join(base_dir, 'config')
        self.migration_dir = os.path.join(base_dir, 'migration')
        self.filter_config = os.path.join(self.config_dir, 'schema.ini')
        self.migration_conf = os.path.join(self.migration_dir, 'migration.ini')
        self.changelog = os.path.join(base_dir, 'changes.txt')
        self.change_report = os.path.join(base_dir, 'change_report.html')
        self.change_commit = os.path.join(base_dir, 'change_report.txt')
        self.current_state = os.path.join(base_dir, 'current.state')
        self.latest_state = self.tempfile(ext='.state')
        self.execute_cmd('getting current version', ['dvs', 'name', self.current_state])
        self.current_version = self.output
        self.next_version = get_uuid4()
        self.execute_ddl('getting state version from database', GETVERSION_SQL)
        match = re.match('SCHEMA_VERSION\\s+\\-+\\s+([\\w\\-]+)\\s*', self.output)
        if not match:
            self.message('cannot find schema version')
            print self.output
            self.quit(SQLERR)
        self.db_version = match.group(1)
        if self.db_version != self.current_version:
            new_opt = optparse.Values()
            new_opt.no_comment = False
            new_opt.wrap = False
            new_opt.include_tags = options.include_tags
            new_opt.exclude_tags = options.exclude_tags
            self.migrate = MigrateDb()
            self.migrate.connectString = self.connectString
            self.migrate.target_version = self.current_version
            self.migrate.source_version = self.db_version
            self.migrate.start_version = self.db_version
            self.migrate.setup_migrations(self.migration_dir)
            if self.migrate.migration_path:
                self.message('pushing changes to the database (unsaved changes may be lost)')
                self.message('', None)
                return self.migrate.run(new_opt, self.current_state, self.filter_config, self.migration_dir)
        self.execute_cmd('extracting latest database state', [
         'dvs', 'copy', '-f', self.filter_config,
         '-n', self.next_version, '-i', options.include_tags,
         '-x', options.exclude_tags, 'oracle:' + self.connectString,
         self.latest_state])
        differ = DiffDb()
        status = differ.run(self.current_state, self.latest_state)
        if status == 0:
            self.message('no changes detected')
            return 0
        else:
            if status == 1:
                self.message('changes detected, skipping migration check')
                self.generate_diff(self.current_state, self.latest_state)
                migration_file = open(self.migration_conf, 'a')
                migration_file.write('%s = %s\n' % (self.current_version, self.next_version))
                migration_file.close()
            elif status == 2:
                self.message('changes detected, performing migration check')
                if not self.check_migration(options):
                    self.message('', None)
                    self.message('migration check failed, migrations may be incomplete or invalid.')
                    self.generate_diff(self.latest_state, self.migrate.migration_check)
                    return 1
                self.message('', None)
                self.message('migration check succeeded')
                for migration in glob.glob(self.migration_dir + '/*.sql'):
                    data = self.read_file(migration)
                    match = MIGRATION_REGEX.match(data)
                    if not match:
                        continue
                    source, target, description = match.groups()
                    if target == 'next-version':
                        self.write_file(migration, data.replace('next-version', self.next_version))

                self.generate_diff(self.current_state, self.latest_state)
                cleaner = CleanDb()
                cleaner.connectString = self.tempConnectString
                cleaner.run()
            self.execute_sql('synchronizing version numbers', UPDATESCHEMA_SQL % (self.next_version, '** migrations tested **'))
            self.message('updating the change log')
            migration_changes = []
            if hasattr(self, 'migrate') and self.migrate and self.migrate.migration_path:
                for i in range(len(self.migrate.migration_path) - 1):
                    s, t = self.migrate.migration_path[i], self.migrate.migration_path[(i + 1)]
                    migration_changes.append('- ' + self.migrate.migrations[s][t][0])

            current_date = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M] ')
            text = current_date + self.next_version + '\n%s\n\n' % ('=' * 55)
            if migration_changes:
                text += 'Migrations:\n\n' + ('\n').join(migration_changes) + '\n\n'
            text += 'Schema Changes:\n\n' + differ.output + '\n\n\n\n'
            previous_changelog = self.read_file(self.changelog)
            self.write_file(self.changelog, text + previous_changelog)
            self.write_file(self.change_commit, 'build $ver$: %s => %s\n\n%s' % (
             self.current_version, self.next_version, differ.output))
            self.message('updating the current state with latest version')
            os.remove(self.current_state)
            os.rename(self.latest_state, self.current_state)
            self.rewrite_schema()
            return 0

    def check_migration(self, orig_options):
        options = optparse.Values()
        options.sql_type = 'all'
        options.no_comment = False
        options.wrap = False
        self.message('', None)
        self.message('creating existing state on a temporary database instance')
        self.message('', None)
        self.create = CreateDb()
        self.create.connectString = self.tempConnectString
        self.create.run(options, self.current_state)
        self.message('', None)
        self.message('running migrations on the temporary database instance')
        self.message('', None)
        self.migrate = MigrateDb()
        self.migrate.connectString = self.tempConnectString
        self.migrate.migration_check = self.current_state
        result = self.migrate.run(options, self.latest_state, None, self.migration_dir)
        return result == 0

    def generate_diff(self, left, right):
        self.execute_cmd('generating schema difference report', [
         'dvs', 'compare', '--html', '--context', '10',
         left, right])
        self.write_file(self.change_report, self.output)

    def rewrite_schema(self):
        objects = {}
        document = etree.parse(self.current_state)
        for node in document.getroot():
            tag = '}' in node.tag and node.tag[node.tag.index('}') + 1:] or node.tag
            objects.setdefault(tag, [])
            objects[tag].append(node.get('name').lower())

        schema = ConfigParser.ConfigParser()
        schema.read(self.filter_config)
        config = open(self.filter_config, 'w')
        for section in schema.sections():
            names = [ o.lower() for o in schema.options(section) ]
            names.sort()
            config.write('[%s]\n' % section)
            for name in names:
                if not objects.has_key(section) or name in objects[section] or '.' in name:
                    config.write('%s=%s\n' % (name, schema.get(section, name)))

            config.write('\n')

        config.close()


MIGRATION_NEEDED = [
 'foreign-key', 'table', 'index', 'sequence', 'materialized-view']
SQLPLUS_EXEC = '\nWHENEVER SQLERROR EXIT FAILURE ROLLBACK;\nSET DEFINE off;\nSET SQLBLANKLINES ON;\n%s\nexit\n/\n'
SQLPLUS_EXEC_DDL = '\nWHENEVER SQLERROR CONTINUE;\nSET DEFINE off;\nSET SQLBLANKLINES ON;\n%s\nexit\n/\n'
DROPCODE_SQL = '\nDECLARE CURSOR object_list IS\n      SELECT   object_name, object_type\n      FROM     user_objects\n      WHERE    object_type IN (\'PACKAGE\', \'FUNCTION\', \'PROCEDURE\', \'TRIGGER\', \'VIEW\')\n      AND      object_name NOT LIKE \'BIN$%\';\nBEGIN\n   FOR rec IN object_list LOOP\n      EXECUTE IMMEDIATE \' DROP \' || rec.object_type || \' "\' || rec.object_name || \'"\';\n   END LOOP;\nEND;\n/\n'
DROPTYPES_SQL = '\nDECLARE CURSOR object_list IS\n      SELECT   type_name\n      FROM     user_types\n      ORDER BY typecode ASC;\nBEGIN\n   FOR rec IN object_list LOOP\n      EXECUTE IMMEDIATE \' DROP TYPE "\' || rec.type_name || \'" FORCE \';\n   END LOOP;\nEND;\n/\n'
DROPTABLE_SQL = '\nDECLARE CURSOR object_list IS\n      SELECT object_name FROM user_objects WHERE object_type = \'MATERIALIZED VIEW\' AND object_name NOT LIKE \'BIN$%\';\nBEGIN\n   FOR rec IN object_list LOOP\n      EXECUTE IMMEDIATE \' DROP MATERIALIZED VIEW "\' || rec.object_name || \'"\';\n   END LOOP;\nEND;\n/\nDECLARE CURSOR object_list IS\n      SELECT object_name FROM user_objects WHERE object_type = \'TABLE\' AND object_name NOT LIKE \'BIN$%\';\nBEGIN\n   FOR rec IN object_list LOOP\n      EXECUTE IMMEDIATE \' DROP TABLE "\' || rec.object_name || \'" CASCADE CONSTRAINTS PURGE\';\n   END LOOP;\nEND;\n/\nDECLARE CURSOR object_list IS\n      SELECT object_name FROM user_objects WHERE object_type = \'SEQUENCE\';\nBEGIN\n   FOR rec IN object_list LOOP\n      EXECUTE IMMEDIATE \' DROP SEQUENCE "\' || rec.object_name || \'"\';\n   END LOOP;\nEND;\n/\n'
DROPCOMMENT_SQL = "\nBEGIN\n    FOR rec IN (SELECT table_name, column_name FROM user_col_comments WHERE comments IS NOT NULL) LOOP\n        EXECUTE IMMEDIATE 'COMMENT ON COLUMN '||rec.table_name||'.'||rec.column_name||' IS ''''';\n    END LOOP;\nEND;\n/\n"
RECOMPILE_SQL = "\nDECLARE\n  ncount INTEGER;\nBEGIN\n    SELECT count(*)    INTO ncount\n    FROM  user_objects WHERE status <> 'VALID';\n    IF ncount > 0 THEN\n       dbms_utility.compile_schema(USER);\n    END IF;\nEND;\n/\n"
SCHEMALOG_SQL = "\nCREATE TABLE schema_log (\n    schema_version     CHAR(36),\n    schema_timestamp   TIMESTAMP DEFAULT sysdate,\n    schema_description VARCHAR2(255),\n    CONSTRAINT schema_log_req CHECK (schema_version IS NOT NULL)\n)\n/\nINSERT INTO schema_log(schema_version, schema_description) VALUES ('%s', '*** fresh creation ***')\n/\n"
UPDATESCHEMA_SQL = "\nINSERT INTO schema_log(schema_version, schema_description) VALUES ('%s', '%s')\n/\n"
REMOVESCHEMAVERSION_SQL = "\nDELETE FROM schema_log WHERE schema_version = '%s'\n/\n"
EXECSCRIPT_SQL = '\n@"%s"\n/\n'
RECREATETYPES_SQL = '\nDECLARE\n    sql_query clob;\n    sql_tbl   dbms_sql.clob_table;\n    i         binary_integer;\n    n         binary_integer;\nBEGIN\n    DECLARE CURSOR type_sql IS\n        SELECT ltrim(rtrim(\n                 replace(dbms_metadata.get_ddl(\'TYPE\', type_name), \'"\' || user || \'".\'),\n                 \' \'||chr(10)||chr(13)), \' \'||chr(10)||chr(13)) AS source\n        FROM   sys.user_types WHERE  type_name NOT LIKE \'%$%\' ORDER BY typecode DESC, type_name;\n    BEGIN\n        n := 1;\n        FOR rec in type_sql LOOP\n            sql_tbl(n) := rec.source;\n            n := n + 1;\n        END LOOP;\n    END;\n\n    DECLARE CURSOR drop_types IS\n        SELECT type_name FROM user_types ORDER BY typecode ASC;\n    BEGIN\n       FOR rec IN drop_types LOOP\n          EXECUTE IMMEDIATE \' DROP TYPE "\' || rec.type_name || \'" FORCE \';\n       END LOOP;\n    END;\n\n    i := 1;\n    LOOP\n       EXIT WHEN i = n;\n       sql_query := sql_tbl(i);\n       EXECUTE IMMEDIATE to_char(sql_query);\n       i := i + 1;\n    END LOOP;\n\n    dbms_utility.compile_schema(user);\nEND;\n/\n'
GETVERSION_SQL = '\nSELECT schema_version\nFROM   schema_log\nWHERE  schema_timestamp = ( SELECT MAX(schema_timestamp) FROM schema_log );\n'
GETVERSIONCOUNT_SQL = "\nSELECT COUNT(DISTINCT schema_version) AS version_count\nFROM   schema_log\nWHERE  schema_version IN ('%s');\n"
CODEFILTER_INI = '\n[table]\n[external-table]\n[materialized-view]\n[sequence]\n[index]\n[foreign-key]\n[view]\n.*=all\n[stored-procedure]\n.*=all\n[function]\n.*=all\n[package]\n.*=all\n[trigger]\n.*=all\n[type]\n.*=all\n'
MIGRATION_REGEX = re.compile('/\\*\\*\\*\\s+Source-Version:\\s+([\\w\\-]+)\\s+Target-Version:\\s+([\\w\\-]+)\\s+Description:\\s+(.+?)\\s+\\*\\*\\*\\/')
WRAPCODE_REGEX = re.compile('(CREATE\\s+OR\\s+REPLACE\\s+(TYPE|TYPE\\s+BODY|FUNCTION|PROCEDURE|PACKAGE|PACKAGE\\s+BODY)\\s+\\"?(\\w+?)\\"? wrapped.+?)(?=\\s+\\/\\s+)', re.S | re.I)
TOOLS = {'sync': SyncDb, 'migrate': MigrateDb, 'create': CreateDb, 'diff': DiffDb, 'clean': CleanDb, 'wrap': WrapDb, 
   'import': ImportDb, 'export': ExportDb, 'copy': CopyDb, 'unwrap': UnwrapDb}

def main():
    if len(sys.argv) == 1 or sys.argv[1] not in TOOLS.keys():
        print 'Please specify a valid command (%s)' % (', ').join(TOOLS.keys())
        sys.exit(1)
    tool = TOOLS[sys.argv[1]]()
    try:
        tool.__main__()
        tool.cleanup()
    except:
        tool.cleanup()
        raise


if __name__ == '__main__':
    main()