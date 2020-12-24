# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/imex/csv_.py
# Compiled at: 2016-10-03 09:39:22
import os, csv, traceback, logging
logger = logging.getLogger(__name__)
import gtk
from sqlalchemy import ColumnDefault, Boolean
import bauble, bauble.db as db
from bauble.i18n import _
from bauble.error import BaubleError
import bauble.utils as utils, bauble.pluginmgr as pluginmgr, bauble.task
from bauble import pb_set_fraction
QUOTE_STYLE = csv.QUOTE_MINIMAL
QUOTE_CHAR = '"'

class UnicodeReader(object):

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.reader = csv.DictReader(f, dialect=dialect, **kwds)
        self.encoding = encoding

    def next(self):
        row = self.reader.next()
        t = {}
        for k, v in row.iteritems():
            if v == '':
                t[k] = None
            else:
                t[k] = utils.to_unicode(v, self.encoding)

        return t

    def __iter__(self):
        return self


class UnicodeWriter(object):

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.writer = csv.writer(f, dialect=dialect, **kwds)
        self.encoding = encoding

    def writerow(self, row):
        """
        Write a row.  If row is a dict then row.values() is written
        and therefore care should be taken to ensure that row.values()
        returns a consisten order.
        """
        if isinstance(row, dict):
            row = row.values()
        t = []
        for s in row:
            if s is None:
                t.append(None)
            else:
                t.append(utils.to_unicode(s, self.encoding))

        self.writer.writerow(t)
        return

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Importer(object):

    def start(self, **kwargs):
        """
        start the import process, this is a non blocking method, queue the
        process as a bauble task
        """
        return bauble.task.queue(self.run, **kwargs)

    def run(self, **kwargs):
        """
        where all the action happens
        """
        raise NotImplementedError


class CSVImporter(Importer):
    """imports comma separated value files into a Ghini database.

    It imports multiple files, each of them equally named as the bauble
    database tables. The bauble tables dependency graph defines the correct
    import order, each file being imported will completely replace any
    existing data in the corresponding table.

    The CSVImporter imports the rows of the CSV file in chunks rather than
    one row at a time.  The non-server side column defaults are determined
    before the INSERT statement is generated instead of getting new defaults
    for each row.  This shouldn't be a problem but it also means that your
    column default should change depending on the value of previously
    inserted rows.

    """

    def __init__(self):
        super(CSVImporter, self).__init__()
        self.__error = False
        self.__cancel = False
        self.__pause = False
        self.__error_exc = False

    def start(self, filenames=None, metadata=None, force=False):
        """start the import process. this is a non blocking method: we queue
        the process as a bauble task. there is no callback informing whether
        it is successfully completed or not.

        """
        if metadata is None:
            metadata = db.metadata
        if filenames is None:
            filenames = self._get_filenames()
        if filenames is None:
            return
        else:
            bauble.task.queue(self.run(filenames, metadata, force))
            return

    @staticmethod
    def _toposort_file(filename, key_pairs):
        """
        filename: the csv file to sort

        key_pairs: tuples of the form (parent, child) where for each
        line in the file the line[parent] needs to be sorted before
        any of the line[child].  parent is usually the name of the
        foreign_key column and child is usually the column that the
        foreign key points to, e.g ('parent_id', 'id')
        """
        f = open(filename, 'rb')
        reader = UnicodeReader(f, quotechar=QUOTE_CHAR, quoting=QUOTE_STYLE)
        bychild = {}
        for line in reader:
            for parent, child in key_pairs:
                bychild[line[child]] = line

        f.close()
        fields = reader.reader.fieldnames
        del reader
        pairs = []
        for line in bychild.values():
            for parent, child in key_pairs:
                if line[parent] and line[child]:
                    pairs.append((line[parent], line[child]))

        sorted_keys = utils.topological_sort(bychild.keys(), pairs)
        sorted_lines = []
        for key in sorted_keys:
            sorted_lines.append(bychild[key])

        import tempfile
        tmppath = tempfile.mkdtemp()
        head, tail = os.path.split(filename)
        filename = os.path.join(tmppath, tail)
        tmpfile = open(filename, 'wb')
        tmpfile.write('%s\n' % (',').join(fields))
        writer = csv.DictWriter(tmpfile, fields, quotechar=QUOTE_CHAR, quoting=QUOTE_STYLE)
        writer.writerows(sorted_lines)
        tmpfile.flush()
        tmpfile.close()
        del writer
        return filename

    def run(self, filenames, metadata, force=False):
        """
        A generator method for importing filenames into the database.
        This method periodically yields control so that the GUI can
        update.

        :param filenames:
        :param metadata:
        :param force: default=False
        """
        transaction = None
        connection = None
        self.__error_exc = BaubleError(_('Unknown Error.'))
        try:
            connection = metadata.bind.connect()
            transaction = connection.begin()
        except Exception as e:
            msg = _('Error connecting to database.\n\n%s') % utils.xml_safe(e)
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            return

        filename_dict = {}
        for f in filenames:
            path, base = os.path.split(f)
            table_name, ext = os.path.splitext(base)
            if table_name in filename_dict:
                safe = utils.xml_safe
                values = dict(table_name=safe(table_name), file_name=safe(filename_dict[table_name]), file_name2=safe(f))
                msg = _('More than one file given to import into table <b>%(table_name)s</b>: %(file_name)s, (file_name2)s') % values
                utils.message_dialog(msg, gtk.MESSAGE_ERROR)
                return
            filename_dict[table_name] = f

        sorted_tables = []
        for table in metadata.sorted_tables:
            try:
                sorted_tables.insert(0, (table, filename_dict.pop(table.name)))
            except KeyError as e:
                pass

        if len(filename_dict) > 0:
            msg = _('Could not match all filenames to table names.\n\n%s') % filename_dict
            utils.message_dialog(msg, gtk.MESSAGE_ERROR)
            return
        else:
            total_lines = 0
            filesizes = {}
            for filename in filenames:
                nlines = len(open(filename).readlines())
                filesizes[filename] = nlines
                total_lines += nlines

            created_tables = []

            def create_table(table):
                table.create(bind=connection)
                if table.name not in created_tables:
                    created_tables.append(table.name)

            steps_so_far = 0
            cleaned = None
            insert = None
            depends = set()
            try:
                for table, filename in sorted_tables:
                    logger.debug(table.name)
                    d = utils.find_dependent_tables(table)
                    depends.update(list(d))
                    del d

                if len(depends) > 0:
                    if not force:
                        msg = _('In order to import the files the following tables will need to be dropped:\n\n<b>%s</b>\n\nWould you like to continue?') % (', ').join(sorted([ d.name for d in depends ]))
                        response = utils.yes_no_dialog(msg)
                    else:
                        response = True
                    if response and len(depends) > 0:
                        logger.debug('dropping: %s' % (', ').join([ d.name for d in depends ]))
                        metadata.drop_all(bind=connection, tables=depends)
                    else:
                        return
                transaction.commit()
                transaction = connection.begin()
                update_every = 127
                for table, filename in reversed(sorted_tables):
                    if self.__cancel or self.__error:
                        break
                    msg = _('importing %(table)s table from %(filename)s') % {'table': table.name, 'filename': filename}
                    bauble.task.set_message(msg)
                    yield
                    if filesizes[filename] <= 1:
                        if not table.exists():
                            create_table(table)
                        continue
                    if table in depends or not table.exists():
                        logger.info('%s does not exist. creating.' % table.name)
                        logger.debug('%s does not exist. creating.' % table.name)
                        create_table(table)
                    else:
                        if table.name not in created_tables and table not in depends:
                            if not force:
                                msg = _('The <b>%s</b> table already exists in the database and may contain some data. If a row the import file has the same id as a row in the database then the file will not import correctly.\n\n<i>Would you like to drop the table in the database first. You will lose the data in your database if you do this?</i>') % table.name
                                response = utils.yes_no_dialog(msg)
                            else:
                                response = True
                            if response:
                                table.drop(bind=connection)
                                create_table(table)
                        if self.__cancel or self.__error:
                            break
                        transaction.commit()
                        transaction = connection.begin()
                        f = open(filename, 'rb')
                        tmp = UnicodeReader(f, quotechar=QUOTE_CHAR, quoting=QUOTE_STYLE)
                        tmp.next()
                        csv_columns = set(tmp.reader.fieldnames)
                        del tmp
                        f.close()
                        defaults = {}
                        for column in table.c:
                            if isinstance(column.default, ColumnDefault):
                                defaults[column.name] = column.default.execute()

                        column_names = table.c.keys()
                        self_keys = filter(lambda f: f.column.table == table, table.foreign_keys)
                        if self_keys:
                            key_pairs = map(lambda x: (x.parent.name, x.column.name), self_keys)
                            filename = self._toposort_file(filename, key_pairs)
                        column_keys = list(csv_columns.union(defaults.keys()))
                        insert = table.insert(bind=connection).compile(column_keys=column_keys)
                        values = []

                        def do_insert():
                            if values:
                                connection.execute(insert, *values)
                            del values[:]
                            percent = float(steps_so_far) / float(total_lines)
                            if 0 < percent < 1.0:
                                pb_set_fraction(percent)

                        isempty = lambda v: v in ('', None)
                        f = open(filename, 'rb')
                        reader = UnicodeReader(f, quotechar=QUOTE_CHAR, quoting=QUOTE_STYLE)
                        for line in reader:
                            while self.__pause:
                                yield

                            if self.__cancel or self.__error:
                                break
                            for column in table.c.keys():
                                if column in defaults and (column not in line or isempty(line[column])):
                                    line[column] = defaults[column]
                                elif column in line and isempty(line[column]):
                                    line[column] = None
                                elif column in line and line[column] == 'False' and isinstance(table.c[column].type, Boolean):
                                    line[column] = False
                                elif column in line and line[column] == 'True' and isinstance(table.c[column].type, Boolean):
                                    line[column] = True

                            values.append(line)
                            steps_so_far += 1
                            if steps_so_far % update_every == 0:
                                do_insert()
                                yield

                    if self.__error or self.__cancel:
                        break
                    do_insert()
                    transaction.commit()
                    logger.debug('%s: %s' % (
                     table.name,
                     table.select().alias().count().execute().fetchone()[0]))
                    transaction = connection.begin()

                logger.debug('creating: %s' % (', ').join([ d.name for d in depends ]))
                metadata.create_all(connection, depends, checkfirst=True)
            except GeneratorExit as e:
                transaction.rollback()
                raise
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                transaction.rollback()
                self.__error = True
                self.__error_exc = e
                raise
            else:
                transaction.commit()

            col = None
            try:
                for table, filename in sorted_tables:
                    for col in table.c:
                        utils.reset_sequence(col)

            except Exception as e:
                col_name = None
                try:
                    col_name = col.name
                except Exception:
                    pass

                msg = _('Error: Could not set the sequence for column: %s') % col_name
                utils.message_details_dialog(utils.xml_safe(msg), traceback.format_exc(), type=gtk.MESSAGE_ERROR)

            return

    def _get_filenames(self):

        def on_selection_changed(filechooser, data=None):
            """
            only make the ok button sensitive if the selection is a file
            """
            f = filechooser.get_preview_filename()
            if f is None:
                return
            else:
                ok = filechooser.action_area.get_children()[1]
                ok.set_sensitive(os.path.isfile(f))
                return

        fc = gtk.FileChooserDialog(_('Choose file(s) to import...'), None, gtk.FILE_CHOOSER_ACTION_OPEN, (
         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
         gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        fc.set_select_multiple(True)
        fc.connect('selection-changed', on_selection_changed)
        r = fc.run()
        if r != gtk.RESPONSE_ACCEPT:
            fc.destroy()
            return
        else:
            filenames = fc.get_filenames()
            fc.destroy()
            return filenames

    def on_response(self, widget, response, data=None):
        logger.debug('on_response')
        logger.debug(response)


class CSVExporter(object):

    def start(self, path=None):
        if path is None:
            d = gtk.FileChooserDialog(_('Select a directory'), None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (
             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
            response = d.run()
            path = d.get_filename()
            d.destroy()
            if response != gtk.RESPONSE_ACCEPT:
                return
        if not os.path.exists(path):
            raise ValueError(_('CSVExporter: path does not exist.\n%s') % path)
        try:
            bauble.task.queue(self.__export_task(path))
        except Exception as e:
            logger.debug(e)

        return

    def __export_task(self, path):
        filename_template = os.path.join(path, '%s.txt')
        steps_so_far = 0
        ntables = 0
        for table in db.metadata.sorted_tables:
            ntables += 1
            filename = filename_template % table.name
            if os.path.exists(filename):
                msg = _('Export file <b>%(filename)s</b> for <b>%(table)s</b> table already exists.\n\n<i>Would you like to continue?</i>') % {'filename': filename, 'table': table.name}
                if utils.yes_no_dialog(msg):
                    return

        def replace(s):
            if isinstance(s, (str, unicode)):
                s.replace('\n', '\\n')
            return s

        def write_csv(filename, rows):
            f = open(filename, 'wb')
            writer = UnicodeWriter(f, quotechar=QUOTE_CHAR, quoting=QUOTE_STYLE)
            writer.writerows(rows)
            f.close()

        update_every = 30
        for table in db.metadata.sorted_tables:
            filename = filename_template % table.name
            steps_so_far += 1
            fraction = float(steps_so_far) / float(ntables)
            pb_set_fraction(fraction)
            msg = _('exporting %(table)s table to %(filename)s') % {'table': table.name, 'filename': filename}
            bauble.task.set_message(msg)
            logger.info('exporting %s' % table.name)
            results = table.select().execute().fetchall()
            if len(results) == 0:
                write_csv(filename, [table.c.keys()])
                yield
                continue
            rows = []
            rows.append(table.c.keys())
            ctr = 0
            for row in results:
                values = map(replace, row.values())
                rows.append(values)
                if ctr == update_every:
                    yield
                    ctr = 0
                ctr += 1

            write_csv(filename, rows)


class CSVImportCommandHandler(pluginmgr.CommandHandler):
    command = 'imcsv'

    def __call__(self, cmd, arg):
        importer = CSVImporter()
        importer.start(arg)


class CSVExportCommandHandler(pluginmgr.CommandHandler):
    command = 'excsv'

    def __call__(self, cmd, arg):
        exporter = CSVExporter()
        exporter.start(arg)


class CSVImportTool(pluginmgr.Tool):
    category = _('Import')
    label = _('Comma Separated Value')

    @classmethod
    def start(cls):
        """
        Start the CSV importer.  This tool will also reinitialize the
        plugins after importing.
        """
        msg = _('It is possible that importing data into this database could destroy or corrupt your existing data.\n\n<i>Would you like to continue?</i>')
        if utils.yes_no_dialog(msg):
            c = CSVImporter()
            c.start()


class CSVExportTool(pluginmgr.Tool):
    category = _('Export')
    label = _('Comma Separated Value')

    @classmethod
    def start(cls):
        c = CSVExporter()
        c.start()