# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/engine.py
# Compiled at: 2015-02-12 15:25:14
import time, inspect, os, json, datetime, re, operator, copy, math, ast, sys, random, threading, multiprocessing, Queue, pandas, pylab, numpy, matplotlib.cm
from collections import defaultdict
import bayesdb.settings as S
from persistence_layer import PersistenceLayer
import api_utils, data_utils, utils, pairwise, functions as funcs, select_utils, estimate_columns_utils, plotting_utils, parser as p, bayesdb.diagnostics_utils as diag_utils

class Engine(object):

    def __init__(self, crosscat_host=None, crosscat_port=8007, crosscat_engine_type='local', seed=None, testing=False, **kwargs):
        """ One optional argument that you may find yourself using frequently is seed.
        It defaults to random seed, but for testing/reproduceability purposes you may
        want a deterministic one. """
        self.persistence_layer = PersistenceLayer()
        self.parser = p.Parser()
        self.analyze_threads = dict()
        self.testing = testing
        if crosscat_host is None or crosscat_host == 'localhost':
            self.online = False
            from crosscat.CrossCatClient import get_CrossCatClient
            self.backend = get_CrossCatClient(crosscat_engine_type, seed=seed, **kwargs)
        else:
            self.online = True
            self.hostname = crosscat_host
            self.port = crosscat_port
            self.URI = 'http://' + self.hostname + ':%d' % self.port
        return

    def call_backend(self, method_name, args_dict):
        """
        Helper function used to call the CrossCat backend, whether it is remote or local.
        Accept method name and arguments for that method as input.
        """
        if self.online:
            out, id = api_utils.call(method_name, args_dict, self.URI)
        else:
            method = getattr(self.backend, method_name)
            out = method(**args_dict)
        return out

    def help(self, method=None):
        help_methods = dict()
        help_methods['create'] = '\n        CREATE BTABLE <btable> FROM <filename.csv> [WITH CODEBOOK <codebook.csv>]\n\n        CREATE COLUMN LIST <col1>[, <col2>...] FROM <btable> AS <column_list>\n        '
        help_methods['select'] = '\n        SELECT <columns|functions> FROM <btable> [WHERE <whereclause>] [ORDER BY <columns|functions>] [LIMIT <limit>]\n        '
        help_methods['infer'] = '\n        INFER <columns|functions> FROM <btable> [WHERE <whereclause>] [WITH CONFIDENCE <confidence>] [WITH <numsamples> SAMPLES] [ORDER BY <columns|functions>] [LIMIT <limit>]\n        '
        help_methods['simulate'] = '\n        SIMULATE <columns> FROM <btable> [WHERE <whereclause>] [GIVEN <column>=<value>] TIMES <times> [SAVE TO <file>]\n        '
        help_methods['estimate'] = '\n        ESTIMATE COLUMNS FROM <btable> [WHERE <whereclause>] [ORDER BY <functions>] [LIMIT <limit>] [AS <column_list>]\n\n        ESTIMATE PAIRWISE <function> FROM <btable> [FOR <columns>] [SAVE TO <file>] [SAVE CONNECTED COMPONENTS WITH THRESHOLD <threshold> AS <column_list>]\n\n        ESTIMATE PAIRWISE ROW SIMILARITY [WITH RESPECT TO <columns|column_lists>]FROM <btable> [FOR <rows>] [SAVE TO <file>] [SAVE CONNECTED COMPONENTS WITH THRESHOLD <threshold> [INTO|AS] <btable>]\n        '
        help_methods['execute'] = '\n        EXECUTE FILE <filename.bql>\n        '
        help_methods['update'] = '\n        UPDATE SCHEMA FOR <btable> SET <col1>=<type1>[,<col2>=<type2>...]\n        '
        help_methods['initialize'] = '\n        INITIALIZE <num_models> MODELS FOR <btable> [WITH CONFIG <config>]\n        '
        help_methods['analyze'] = '\n        ANALYZE <btable> [MODEL[S] <model_index>-<model_index>] FOR (<num_iterations> ITERATIONS | <seconds> SECONDS)\n        '
        help_methods['list'] = '\n        LIST BTABLES\n        '
        help_methods['show'] = '\n        SHOW SCHEMA FOR <btable>\n\n        SHOW MODELS FOR <btable>\n\n        SHOW DIAGNOSTICS FOR <btable>\n\n        SHOW COLUMN LISTS FOR <btable>\n\n        SHOW COLUMNS <column_list> FOR <btable>\n\n        SHOW ROW LISTS FOR <table>\n\n        SHOW METADATA FOR <btable> [<metadata-key1> [, <metadata-key2>...]]\n\n        SHOW LABEL FOR <btable> [<column-name-1> [, <column-name-2>...]]\n        '
        help_methods['load'] = '\n        LOAD MODELS <filename.pkl.gz> INTO <btable>\n        '
        help_methods['save'] = '\n        SAVE MODELS FROM <btable> TO <filename.pkl.gz>\n        '
        help_methods['drop'] = '\n        DROP BTABLE <btable>\n\n        DROP MODEL[S] [<model_index>-<model_index>] FROM <btable>\n        '
        help_methods['summarize'] = '\n        SUMMARIZE <SELECT|INFER|SIMULATE>\n        '
        help_methods['plot'] = '\n        PLOT <SELECT|INFER|SIMULATE>\n        '
        help_all = '\n        Welcome to BQL help.\n\n        For the BQL documentation, please visit:\n        http://probcomp.csail.mit.edu/bayesdb/docs/bql.html\n\n        Here is a list of BQL commands and their syntax:\n        '
        help_basic = "\n        Welcome to BQL help.\n\n        If you know the query you wish to use, type 'HELP <query_name>'\n\n        For all queries, type 'HELP ALL'\n\n        For the complete BQL documentation, please visit:\n        http://probcomp.csail.mit.edu/bayesdb/docs/bql.html\n        "
        if method == None:
            help_string = help_basic
        elif method == 'all':
            help_string = help_all + ('').join(help_methods.values())
        elif method in help_methods:
            help_string = help_all + help_methods[method]
        else:
            help_string = help_basic + '\n        The method you typed was not recognize. Try "HELP", "HELP ALL",\n        or one of the following:\n        \tHELP ' + ('\n\tHELP ').join(help_methods.keys()).upper()
        return dict(message=help_string)

    def is_analyzing(self, tablename):
        return tablename in self.analyze_threads and self.analyze_threads[tablename].isAlive()

    def drop_btable(self, tablename):
        """Delete table by tablename."""
        if self.is_analyzing(tablename):
            self.cancel_analyze(tablename)
            raise utils.BayesDBError('Error: cannot drop btable with ANALYZE in progress. Attempting to cancel ANALYZE; please retry drop btable once ANALYZE is successfully completed.')
        self.persistence_layer.drop_btable(tablename)
        return dict()

    def list_btables(self):
        """Return names of all btables."""
        return dict(column_labels=['btable'], data=[ [name] for name in self.persistence_layer.list_btables() ])

    def label_columns(self, tablename, mappings):
        """
        Add column labels to table in persistence layer, replacing
        labels without warning. Mappings is a dict of column names
        and their labels as given by the user.
        No length is enforced on labels - should we?
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        M_c_full = self.persistence_layer.get_metadata_full(tablename)['M_c_full']
        colnames_full = utils.get_all_column_names_in_original_order(M_c_full)
        labels_edited = {}
        for colname, label in mappings.items():
            if colname in colnames_full:
                self.persistence_layer.add_column_label(tablename, colname, label)
                labels_edited[colname] = label
            else:
                raise utils.BayesDBColumnDoesNotExistError(colname, tablename)

        labels = self.persistence_layer.get_column_labels(tablename)
        ret = {'data': [ [c, l] for c, l in labels_edited.items() ], 'column_labels': ['column', 'label']}
        ret['message'] = 'Updated column labels for %s.' % tablename
        return ret

    def update_codebook(self, tablename, codebook):
        """ Adds a codebook to a btable from a .csv

            Args:
                    tablename (str): Name of the btable
                    codebook (list of dict): The processed codebook. Should come from client because we
                            assume that .csv is stored on the client machine.
            """
        self.persistence_layer.update_codebook(tablename, codebook)
        return dict(message='Updated codebook for %s.' % tablename)

    def update_descriptions(self, tablename, mappings):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        try:
            M_c_full = self.persistence_layer.get_metadata_full(tablename)['M_c_full']
        except utils.BayesDBError:
            raise utils.BayesDBError('Error: DESCRIBE found no metadata_full file. This is most likely a result of this btable being created with an old version of BayesDB. Please try recreating the table from the original csv, and loading any models you might have.')

        if 'column_codebook' not in M_c_full.keys():
            raise utils.BayesDBError('Error: DESCRIBE found no codebook in metadata_full file. Please add a codebook.')
        descriptions_edited = dict()
        for colname, description in mappings.items():
            col_idx = M_c_full['name_to_idx'][colname]
            M_c_full['column_codebook'][col_idx]['description'] = description
            descriptions_edited[colname] = description

        self.persistence_layer.update_metadata_full(tablename, M_c_full=M_c_full)
        ret = {'data': [ [c, d] for c, d in descriptions_edited.items() ], 'column_labels': [
                           'column', 'description']}
        ret['message'] = 'Updated column descriptions for %s.' % tablename
        return ret

    def update_short_names(self, tablename, mappings):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        try:
            M_c_full = self.persistence_layer.get_metadata_full(tablename)['M_c_full']
        except utils.BayesDBError:
            raise utils.BayesDBError('Error: DESCRIBE found no metadata_full file. This is most likely a result of this btable being created with an old version of BayesDB. Please try recreating the table from the original csv, and loading any models you might have.')

        if 'column_codebook' not in M_c_full.keys():
            raise utils.BayesDBError('Error: DESCRIBE found no codebook in metadata_full file. Please add a codebook.')
        short_names_edited = dict()
        for colname, short_name in mappings.items():
            col_idx = M_c_full['name_to_idx'][colname]
            M_c_full['column_codebook'][col_idx]['short_name'] = short_name
            short_names_edited[colname] = short_name

        self.persistence_layer.update_metadata_full(tablename, M_c_full=M_c_full)
        ret = {'data': [ [c, s] for c, s in short_names_edited.items() ], 'column_labels': [
                           'column', 'short name']}
        ret['message'] = 'Updated column short names for %s.' % tablename
        return ret

    def describe(self, tablename, columnset):
        """Show column labels, human-readible name, description, and value metadat (in applicable)"""
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        labels = self.persistence_layer.get_column_labels(tablename)
        M_c = self.persistence_layer.get_metadata(tablename)['M_c']
        if columnset == None:
            colnames = M_c['name_to_idx'].keys()
        else:
            if columnset.asList()[0] == '*':
                colnames = M_c['name_to_idx'].keys()
            else:
                column_lists = self.persistence_layer.get_column_lists(tablename)
                colnames = utils.process_column_list(columnset.asList(), M_c, column_lists, dedupe=True)
                colnames = [ c.lower() for c in colnames ]
            try:
                M_c_full = self.persistence_layer.get_metadata_full(tablename)['M_c_full']
            except utils.BayesDBError:
                raise utils.BayesDBError('Error: DESCRIBE found no metadata_full file. This is most likely a result of this btable being created with an old version of BayesDB. Please try recreating the table from the original csv, and loading any models you might have.')

            ret_table = []
            for c in colnames:
                row = [
                 c]
                colname_idx_M_c = M_c_full['name_to_idx'][c]
                try:
                    colname_codebook = M_c_full['column_codebook'][colname_idx_M_c]
                    column_metadata = M_c_full['column_metadata'][colname_idx_M_c]
                except IndexError:
                    raise utils.BayesDBError('Error: DESCRIBE cannot locate codebook in metatdata. Please add a codebook to your table.')

                if colname_codebook is None:
                    raise utils.BayesDBError('Error: DESCRIBE cannot locate codebook in metatdata. Please add a codebook to your table.')
                if colname_codebook['description']:
                    short_name = colname_codebook['short_name']
                    description = colname_codebook['description']
                else:
                    short_name = c
                    description = 'No description'
                data_info_string = ''
                if column_metadata['parameters']:
                    data_info_string += str(column_metadata['parameters']) + '\n'
                if column_metadata['code_to_value']:
                    data_info_string += str(column_metadata['value_to_code'].values()) + '\n'
                ret_table.append([c, short_name, description, data_info_string])
                column_labels = [
                 'column', 'label', 'decription', 'data summary']

        ret = {'data': ret_table, 'column_labels': column_labels}
        ret['message'] = 'Describing for %s.' % tablename
        return ret

    def show_labels(self, tablename, columnset):
        """
        Show column labels for the columns in columnstring
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        labels = self.persistence_layer.get_column_labels(tablename)
        if columnset == None:
            colnames = labels.keys()
        else:
            column_lists = self.persistence_layer.get_column_lists(tablename)
            M_c = self.persistence_layer.get_metadata(tablename)['M_c']
            colnames = utils.process_column_list(columnset.asList(), M_c, column_lists, dedupe=True)
            colnames = [ c.lower() for c in colnames ]
        ret = {'data': [ [c, l] for c, l in labels.items() if c in colnames ], 'column_labels': ['column', 'label']}
        ret['message'] = 'Showing labels for %s.' % tablename
        return ret

    def update_metadata(self, tablename, mappings):
        """
        Add user metadata to table in persistence layer, replacing
        values without warning. Mappings is a dict of key names
        and their values as given by the user.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        for key, value in mappings.items():
            self.persistence_layer.add_user_metadata(tablename, key, value)

        metadata = self.persistence_layer.get_user_metadata(tablename)
        ret = {'data': [ [k, v] for k, v in metadata.items() if k in mappings.keys() ], 'column_labels': ['key', 'value']}
        ret['message'] = 'Updated user metadata for %s.' % tablename
        return ret

    def show_metadata(self, tablename, keyset):
        """
        Get user metadata from persistence layer and show the values for the keys specified
        by the user. If no keystring is given, show all metadata key-value pairs.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        metadata = self.persistence_layer.get_user_metadata(tablename)
        if keyset == None:
            metadata_keys = metadata.keys()
        else:
            metadata_keys = keyset.asList()
        ret = {'data': [ [k, metadata[k]] for k in metadata_keys if k in metadata ], 'column_labels': ['key', 'value']}
        ret['message'] = 'Showing user metadata for %s.' % tablename
        return ret

    def update_schema(self, tablename, mappings):
        """
        mappings is a dict of column name to 'numerical', 'categorical', 'cyclic', or 'ignore'
        Cannot update type for key column, or change another column to key.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if self.persistence_layer.has_models(tablename):
            raise utils.BayesDBError('Error: btable %s already has models. The schema may not be updated after models have been initialized; please either create a new btable or drop the models from this one.' % tablename)
        msg = self.persistence_layer.update_schema(tablename, mappings)
        ret = self.show_schema(tablename)
        ret['message'] = 'Updated schema.'
        return ret

    def create_btable_from_existing(self, tablename, query_colnames, cctypes_existing_full, M_c_existing_full, query_data):
        """
        Used in INTO statements to create a new btable as a portion of an existing one.
        """
        if self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBError('Btable with name %s already exists.' % tablename)
        cctypes_full, warnings = data_utils.guess_column_types(query_data, query_colnames)
        for query_idx, query_colname in enumerate(query_colnames):
            if query_colname in M_c_existing_full['name_to_idx']:
                cctypes_full[query_idx] = cctypes_existing_full[M_c_existing_full['name_to_idx'][query_colname]]

        if 'key' not in cctypes_full:
            raw_T_full, colnames_full, cctypes_full = data_utils.select_key_column(query_data, query_colnames, cctypes_full, key_column=None, testing=self.testing)
        else:
            raw_T_full = query_data
            colnames_full = query_colnames
        T_full, M_r_full, M_c_full, _ = data_utils.gen_T_and_metadata(colnames_full, raw_T_full, cctypes=cctypes_full)
        raw_T, cctypes, colnames = data_utils.remove_ignore_cols(T_full, cctypes_full, colnames_full)
        T, M_r, M_c, _ = data_utils.gen_T_and_metadata(colnames, raw_T, cctypes=cctypes)
        self.persistence_layer.create_btable(tablename, cctypes_full, cctypes, T, M_r, M_c, T_full, M_r_full, M_c_full, query_data)
        return dict(column_labels=colnames_full, data=[cctypes_full], message='Created btable %s. Schema taken from original btable:' % tablename, warnings=warnings)

    def create_btable(self, tablename, header, raw_T_full, cctypes_full=None, key_column=None, subsample=False, codebook=None):
        """
        Upload a csv table to the predictive db.
        cctypes must be a dictionary mapping column names
        to either 'ignore', 'numerical', 'categorical', or 'cyclic'. Not every
        column name must be present in the dictionary: default is numerical.

        subsample is False by default, but if it is passed an int, it will subsample using
        <subsample> rows for the initial ANALYZE, and then insert all other rows afterwards.
        """
        if self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBError('Btable with name %s already exists.' % tablename)
        warnings = []
        colnames_full = [ h.lower().strip() for h in header ]
        raw_T_full = data_utils.convert_nans(raw_T_full)
        if cctypes_full is None:
            cctypes_full, warnings = data_utils.guess_column_types(raw_T_full, colnames_full)
        raw_T_full, colnames_full, cctypes_full = data_utils.select_key_column(raw_T_full, colnames_full, cctypes_full, key_column, testing=self.testing)
        T_full, M_r_full, M_c_full, _ = data_utils.gen_T_and_metadata(colnames_full, raw_T_full, cctypes=cctypes_full, codebook=codebook)
        raw_T, cctypes, colnames = data_utils.remove_ignore_cols(raw_T_full, cctypes_full, colnames_full)
        T, M_r, M_c, _ = data_utils.gen_T_and_metadata(colnames, raw_T, cctypes=cctypes, codebook=codebook)
        T_sub = None
        if subsample:
            assert type(subsample) == int
            T_sub = T[:subsample]
        self.persistence_layer.create_btable(tablename, cctypes_full, cctypes, T, M_r, M_c, T_full, M_r_full, M_c_full, raw_T_full, T_sub)
        schema = self.show_schema(tablename)
        return dict(column_labels=schema['column_labels'], data=schema['data'], message='Created btable %s. Inferred schema:' % tablename, warnings=warnings)

    def check_btable_created_and_checked(self, tablename, client_online=False):
        """
        Checks whether a given table has been created and checked. If called from the online client,
        returns a dict with 'results' key, otherwise returns a tuple.
        """
        table_created = tablename in self.persistence_layer.btable_index
        table_checked = tablename in self.persistence_layer.btable_check_index
        if client_online:
            return {'result': {'table_created': table_created, 'table_checked': table_checked}}
        else:
            return (
             table_created, table_checked)

    def upgrade_btable(self, tablename, upgrade_key_column=None):
        """
        Btables created in early versions of BayesDB may not have attributes that are required in more
        recent versions of BayesDB (example: required key column). This function allows them to be
        upgraded simply, without having to manually recreate the btable and re-load models.
        """
        try:
            metadata = self.persistence_layer.get_metadata(tablename)
        except utils.BayesDBError:
            print 'Metadata for %s have been corrupted, and the table must be dropped.' % tablename
            print 'Press any key to confirm, and then re-create it using CREATE BTABLE'
            if not self.testing:
                user_input = raw_input()
            self.drop_btable(tablename)
            return

        try:
            metadata_full = self.persistence_layer.get_metadata_full(tablename)
        except utils.BayesDBError:
            metadata = self.persistence_layer.get_metadata(tablename)
            metadata_full = metadata
            for key in metadata.keys():
                metadata_full[key + '_full'] = metadata_full.pop(key)

            metadata_full['raw_T_full'] = data_utils.gen_raw_T_full_from_T_full(metadata_full['T_full'], metadata_full['M_c_full'])
            self.persistence_layer.write_metadata_full(tablename, metadata_full)
            print 'Upgraded %s: added metadata_full file' % tablename

        if 'key' not in metadata_full['cctypes_full']:
            print 'Table %s is from an old version of BayesDB and does not have a key column.' % tablename
            raw_T_full = metadata_full['raw_T_full']
            colnames_full = utils.get_all_column_names_in_original_order(metadata_full['M_c_full'])
            cctypes_full = metadata_full['cctypes_full']
            raw_T_full, colnames_full, cctypes_full = data_utils.select_key_column(raw_T_full, colnames_full, cctypes_full, testing=self.testing)
            T_full, M_r_full, M_c_full, _ = data_utils.gen_T_and_metadata(colnames_full, raw_T_full, cctypes=cctypes_full)
            self.persistence_layer.upgrade_btable(tablename, cctypes_full, T_full, M_r_full, M_c_full, raw_T_full)
            print 'Upgraded %s: added key column' % tablename
        cctypes_full = metadata_full['cctypes_full']
        if 'continuous' in cctypes_full or 'multinomial' in cctypes_full:
            colnames_full = utils.get_all_column_names_in_original_order(metadata_full['M_c_full'])
            mappings = dict()
            for colname, cctype in zip(colnames_full, cctypes_full):
                if cctype == 'continuous':
                    mappings[colname] = dict(cctype='numerical', parameters=None)
                elif cctype == 'multinomial':
                    mappings[colname] = dict(cctype='categorical', parameters=None)

            self.persistence_layer.update_schema(tablename, mappings)
            print "Upgraded %s: converted column types 'multinomial' to 'categorical' and 'continuous' to 'numerical'" % tablename
        self.persistence_layer.btable_check_index.append(tablename)
        if 'column_codebook' in metadata_full['M_c_full'].keys():
            if metadata_full['M_c_full']['column_codebook'] is None:
                self.persistence_layer.add_default_codebook_to_metadata(tablename)
                print 'Created empty codebook for %s.' % tablename
        elif 'column_codebook' not in metadata_full.keys():
            self.persistence_layer.add_default_codebook_to_metadata(tablename)
            print 'Createda empty codebook for %s.' % tablename
        return

    def show_schema(self, tablename):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        metadata_full = self.persistence_layer.get_metadata_full(tablename)
        M_c_full = metadata_full['M_c_full']
        colnames_full = utils.get_all_column_names_in_original_order(M_c_full)
        parameters_full = [ str(x['parameters']) for x in M_c_full['column_metadata'] ]
        cctypes_full = metadata_full['cctypes_full']
        schema_full = zip(colnames_full, cctypes_full, parameters_full)
        return dict(column_labels=['column', 'datatype', 'parameters'], data=schema_full)

    def save_models(self, tablename):
        """Opposite of load models! Returns the models, including the contents, which
        the client then saves to disk (in a pickle file)."""
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        models = self.persistence_layer.get_models(tablename)
        schema = self.persistence_layer.get_schema(tablename)
        return dict(models=models, schema=schema)

    def load_models(self, tablename, models, model_schema):
        """Load these models as if they are new models"""
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if 'X_L_list' in models:
            print 'WARNING! The models you are currently importing are stored in an old format\n                 (from version 0.1); it is deprecated and may not be supported in future releases.\n                 Please use "SAVE MODELS FROM <btable> TO <filename.pkl.gz>" to create an updated copy of your models.'
            old_models = models
            models = dict()
            for id, (X_L, X_D) in enumerate(zip(old_models['X_L_list'], old_models['X_D_list'])):
                models[id] = dict(X_L=X_L, X_D=X_D, iterations=0)

        if model_schema:
            table_schema = self.persistence_layer.get_schema(tablename)
            if table_schema != model_schema:
                if self.persistence_layer.has_models(tablename):
                    raise utils.BayesDBError('\n                        Table %s already has models under a different schema than\n                        the models you are loading. All models used must have the\n                        same schema. To load these models, first drop the existing\n                        models from the table.\n                        ' % tablename)
                else:
                    upgrade_map = dict(continuous='numerical', multinomial='categorical')
                    for colname, mapping in model_schema.items():
                        cctype = mapping['cctype']
                        if cctype in upgrade_map:
                            print 'Converting model schema column type %s to %s' % (cctype, upgrade_map[cctype])
                            model_schema[colname]['cctype'] = upgrade_map[cctype]

                    self.persistence_layer.update_schema(tablename, model_schema)
        result = self.persistence_layer.add_models(tablename, models.values())
        return self.show_models(tablename)

    def drop_models(self, tablename, model_indices=None):
        """Drop the specified models. If model_ids is None or all, drop all models."""
        if self.is_analyzing(tablename):
            raise utils.BayesDBError('Error: cannot drop models with ANALYZE in progress. Please retry once ANALYZE is successfully completed or canceled.')
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        self.persistence_layer.drop_models(tablename, model_indices)
        return self.show_models(tablename)

    def initialize_models(self, tablename, n_models=16, model_config=None):
        """
        Initialize n_models models.

        By default, model_config specifies to use the CrossCat model. You may pass 'naive bayes'
        or 'crp mixture' to use those specific models instead. Alternatively, you can pass a custom
        dictionary for model_config, as long as it contains a kernel_list, initializaiton, and
        row_initialization.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if self.is_analyzing(tablename):
            raise utils.BayesDBError('Error: cannot initialize models with ANALYZE in progress. Please retry once ANALYZE is successfully completed or canceled.')
        metadata = self.persistence_layer.get_metadata(tablename)
        M_c = metadata['M_c']
        M_r = metadata['M_r']
        if 'T_sub' in metadata and metadata['T_sub']:
            T = metadata['T_sub']
        else:
            T = metadata['T']
        if type(model_config) == str and model_config.lower() == 'naive bayes':
            model_config = dict(kernel_list=['column_hyperparameters'], initialization='together', row_initialization='together')
        else:
            if type(model_config) == str and model_config.lower() == 'crp mixture':
                model_config = dict(kernel_list=['column_hyperparameters',
                 'row_partition_hyperparameters',
                 'row_partition_assignments'], initialization='together', row_initialization='from_the_prior')
            elif type(model_config) != dict or 'kernel_list' not in model_config or 'initialization' not in model_config or 'row_initialization' not in model_config:
                model_config = dict(kernel_list=(), initialization='from_the_prior', row_initialization='from_the_prior')
            else:
                raise utils.BayesDBError('Invalid model config')
            existing_model_config = self.persistence_layer.get_model_config(tablename)
            if existing_model_config is not None and existing_model_config != model_config:
                raise utils.BayesDBError('Error: model config must match existing model config: %s' % str(existing_model_config))
            init_dict = dict(M_c=M_c, M_r=M_r, T=T, n_chains=n_models, initialization=model_config['initialization'], row_initialization=model_config['row_initialization'])
            X_L_list, X_D_list = self.call_backend('initialize', init_dict)
            if n_models == 1:
                X_L_list = [
                 X_L_list]
                X_D_list = [X_D_list]
            model_list = list()
            for X_L, X_D in zip(X_L_list, X_D_list):
                model_list.append(dict(X_L=X_L, X_D=X_D, iterations=0, time=0.0, model_config=model_config))

        self.persistence_layer.add_models(tablename, model_list)
        return self.show_models(tablename)

    def show_models(self, tablename):
        """Return the current models and their iteration counts."""
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        model_data = self.persistence_layer.get_models(tablename)
        if 'schema' in model_data.keys():
            models = model_data['models']
        else:
            models = model_data
        modelid_iteration_info = list()
        for modelid, model in sorted(models.items(), key=lambda t: t[0]):
            modelid_iteration_info.append((modelid, model['iterations']))

        if len(models) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        else:
            return dict(models=modelid_iteration_info)

    def show_diagnostics(self, tablename):
        """
        Display diagnostic information for all your models.
        TODO: generate plots of num_views, column_crp_alpha, logscore, and f_z stuff
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        models = self.persistence_layer.get_models(tablename)
        if len(models) == 0:
            raise utils.BayesDBError('No models for btable %s. Create some with the INITIALIZE MODELS command.' % tablename)
        if 'diagnostics' not in models[0].keys():
            raise utils.BayesDBError('No diagnostics found. Run ANALYZE to collect some.')
        if 'model_config' not in models[0]:
            raise utils.BayesDBError('The models in %s were created with an old version of BayesDB which does not support model diag_utils.' % tablename)
        data = list()
        diagnostic_keys = sorted(models[0]['diagnostics'].keys())
        time_key_index = diagnostic_keys.index('time')
        del diagnostic_keys[time_key_index]
        iterations_key_index = diagnostic_keys.index('iterations')
        del diagnostic_keys[iterations_key_index]
        for modelid, model in sorted(models.items(), key=lambda t: t[0]):
            data_row = [ model['diagnostics'][key][(-1)] for key in diagnostic_keys ]
            data.append(tuple([modelid, model['iterations'], model['time']] + data_row))
        else:
            return dict(column_labels=['model_id', 'iterations', 'time'] + diagnostic_keys, data=data)

    def analyze(self, tablename, model_indices=None, iterations=None, seconds=None, ct_kernel=0, background=True):
        """
        Run analyze for the selected table. model_indices may be 'all' or None to indicate all models.

        Runs for a maximum of iterations, or a maximum number of seconds.

        Previously: this command ran in the same thread as this engine.
        Now: runs each model in its own thread, and does 10 seconds of inference at a time,
        by default. Each thread also has its own crosscat engine instance!

        Args:
            tablename (type): BayesDB btable name
            iterations (int): Number of iterations to run.
            seconds (int): Number of seconds to run.
            ct_kernel (int): Specifies which crosscat column transition kernel to run. 0: Gibbs,
                1: Metropolis-Hastings
            background (bool): Run asynchronously.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if not self.persistence_layer.has_models(tablename):
            raise utils.BayesDBNoModelsError(tablename)
        metadata = self.persistence_layer.get_metadata(tablename)
        M_c = metadata['M_c']
        M_r = metadata['M_r']
        T = metadata['T']
        if 'T_sub' in metadata:
            T_sub = metadata['T_sub']
        else:
            T_sub = None
        max_model_id = self.persistence_layer.get_max_model_id(tablename)
        if max_model_id == -1:
            raise utils.BayesDBError('You must INITIALIZE MODELS before using ANALYZE.')
        models = self.persistence_layer.get_models(tablename)
        if model_indices is None or str(model_indices).upper() == 'ALL':
            modelids = sorted(models.keys())
        else:
            assert type(model_indices) == list
            modelids = model_indices
        first_model = models[modelids[0]]
        if 'model_config' in first_model and 'kernel_list' in first_model['model_config']:
            kernel_list = first_model['model_config']['kernel_list']
        else:
            kernel_list = ()
        if tablename in self.analyze_threads and self.analyze_threads[tablename].isAlive():
            raise utils.BayesDBError(("{0} is already being analyzed. Try using 'SHOW ANALYZE FOR {0}' to get more information, or 'CANCEL ANALYZE FOR {0}' to cancel the ANALYZE.").format(tablename))
        t = AnalyzeMaster(args=(tablename, modelids, kernel_list, iterations,
         seconds, M_c, T, T_sub, models, background, self))
        self.analyze_threads[tablename] = t
        t.start()
        if not background:
            t.join()
            return dict(message='Analyze complete.')
        else:
            return dict(message='Analyzing %s: models will be updated in the background.' % tablename)
            return

    def _insert_subsampled_rows(self, tablename, T, T_sub, M_c, X_L_list, X_D_list, modelids):
        """
        If the analyze in progress was using subsampling, then insert all the non-subsampled rows now.
        TODO: asserts are costly, remove before performance-critical use. They're just there for code
        correctness and readability right now.
        """
        assert T[:len(T_sub)] == T_sub
        new_rows = T[len(T_sub):]
        insert_args = dict(M_c=M_c, T=T_sub, X_L_list=X_L_list, X_D_list=X_D_list, new_rows=new_rows)
        X_L_list, X_D_list, T_new = self.call_backend('insert', insert_args)
        assert T_new == T
        for i, modelid in enumerate(modelids):
            self.persistence_layer.update_model(tablename, X_L_list[i], X_D_list[i], dict(), modelid)

    def show_analyze(self, tablename):
        if tablename in self.analyze_threads and self.analyze_threads[tablename].isAlive():
            info = self.analyze_threads[tablename].get_info()
            return dict(message=info)
        else:
            return dict(message='Table %s is not currently being analyzed.' % tablename)

    def cancel_analyze(self, tablename):
        if tablename in self.analyze_threads and self.analyze_threads[tablename].isAlive():
            self.analyze_threads[tablename].stop()
            return dict(message='Analyze for table %s is being canceled. Please wait a few moments for it to exit safely.' % tablename)
        raise utils.BayesDBError('Table %s is not being analyzed.' % tablename)

    def infer(self, tablename, functions, confidence, whereclause, limit, numsamples, order_by=False, plot=False, modelids=None, summarize=False, hist=False, freq=False, newtablename=None):
        """
        Impute missing values.
        Sample INFER: INFER columnstring FROM tablename WHERE whereclause WITH confidence LIMIT limit;
        Sample INFER INTO: INFER columnstring FROM tablename WHERE whereclause WITH confidence INTO newtablename LIMIT limit;
        Argument newtablename == null/emptystring if we don't want to do INTO

        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if not self.persistence_layer.has_models(tablename):
            raise utils.BayesDBNoModelsError(tablename)
        if numsamples is None:
            numsamples = 50
        return self.select(tablename, functions, whereclause, limit, order_by, impute_confidence=confidence, numsamples=numsamples, plot=plot, modelids=modelids, summarize=summarize, hist=hist, freq=freq, newtablename=newtablename)

    def select(self, tablename, functions, whereclause, limit, order_by, impute_confidence=None, numsamples=None, plot=False, modelids=None, summarize=False, hist=False, freq=False, newtablename=None):
        """
        BQL's version of the SQL SELECT query.

        First, reads codes from T and converts them to values.
        Then, filters the values based on the where clause.
        Then, fills in all imputed values, if applicable.
        Then, orders by the given order_by functions.
        Then, computes the queried values requested by the column string.

        query_colnames is the list of the raw columns/functions from the columnstring, with row_id prepended
        queries is a list of (query_function, query_args, aggregate) tuples, where 'query_function' is
            a function like row_id, column, similarity, or typicality, and 'query_args' are the function-specific
            arguments that that function takes (in addition to the normal arguments, like M_c, X_L_list, etc).
            aggregate specifies whether that individual function is aggregate or not

        queries: [(func, f_args, aggregate)]
        order_by: [(func, f_args, desc)]
        where_conditions: [(func, f_args, op, val)]

        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        M_c_full, M_r_full, T_full = self.persistence_layer.get_metadata_and_table_full(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        column_lists = self.persistence_layer.get_column_lists(tablename)
        key_column_name = self.persistence_layer.get_key_column_name(tablename)
        queries, query_colnames = self.parser.parse_functions(functions, M_c, T, M_c_full, T_full, column_lists, key_column_name)
        if whereclause == None:
            where_conditions = []
        else:
            where_conditions = self.parser.parse_where_clause(whereclause, M_c, T, M_c_full, T_full, column_lists)
            assert len(where_conditions) > 0 and len(where_conditions[0]) == 4
            if order_by == False:
                order_by = []
            else:
                order_by = self.parser.parse_order_by_clause(order_by, M_c, T, M_c_full, T_full, column_lists)
            if impute_confidence is not None:
                for f_list in (where_conditions, queries, order_by):
                    for i in range(len(f_list)):
                        if f_list[i][0] == funcs._column and f_list[i][1][1] is None:
                            new_f = list(f_list[i])
                            new_f_args = list(new_f[1])
                            new_f_args[1] = impute_confidence
                            new_f[1] = tuple(new_f_args)
                            f_list[i] = tuple(new_f)

            if len(X_L_list) == 0:
                select_utils.check_if_functions_need_models(queries, tablename, order_by, where_conditions)
            query_functions = [ (q[0], q[1]) for q in queries ]
            order_by_functions = [ (o[0], o[1]) for o in order_by ]
            where_functions = [ (w[0], w[1]) for w in where_conditions ]
            function_list = [ q for q in query_functions ]
            query_idxs = range(len(query_functions))
            order_by_idxs = []
            where_idxs = []
            query_size = len(query_functions)
            order_by_size = query_size

            def get_existing_f_idx(new_fun, function_list):
                for f_idx, fun in enumerate(function_list):
                    if new_fun == fun:
                        return f_idx

                return False

            for o_idx, o_fun in enumerate(order_by_functions):
                existing_f_idx = get_existing_f_idx(o_fun, function_list)
                if existing_f_idx:
                    order_by_idxs.append(existing_f_idx)
                else:
                    function_list.append(o_fun)
                    order_by_idxs.append(len(function_list) - 1)
                    order_by_size += 1

            for w_idx, w_fun in enumerate(where_functions):
                existing_f_idx = get_existing_f_idx(w_fun, function_list)
                if existing_f_idx:
                    where_idxs.append(existing_f_idx)
                else:
                    function_list.append(w_fun)
                    where_idxs.append(len(function_list) - 1)

            data_tuples = []
            for row_id, T_row in enumerate(T):
                row = [
                 None] * order_by_size
                row_values = select_utils.convert_row_from_codes_to_values(T_row, M_c)
                where_clause_eval = select_utils.evaluate_where_on_row(row_id, row_values, where_conditions, M_c, M_c_full, X_L_list, X_D_list, T, T_full, self, tablename, numsamples, impute_confidence)
                if type(where_clause_eval) == list:
                    for w_idx, val in enumerate(where_clause_eval):
                        if where_idxs[w_idx] < order_by_size:
                            row[where_idxs[w_idx]] = val

                    data_tuples.append((row_id, row))

            if len(order_by) > 0:
                scored_data_tuples = list()
                for row_id, row in data_tuples:
                    scores = []
                    for o_idx, (f, args, desc) in enumerate(order_by):
                        if row[order_by_idxs[o_idx]] is not None:
                            score = row[order_by_idxs[o_idx]]
                        else:
                            if f != funcs._column_ignore:
                                score = f(args, row_id, row, M_c, X_L_list, X_D_list, T, self, numsamples)
                            else:
                                score = f(args, row_id, row, M_c_full, T_full, self)
                            if order_by_idxs[o_idx] < query_size:
                                row[order_by_idxs[o_idx]] = score
                        if desc:
                            if data_utils.get_can_cast_to_float([score]):
                                score = float(score)
                            score *= -1
                        scores.append(score)

                    scored_data_tuples.append((tuple(scores), (row_id, row)))

                scored_data_tuples.sort(key=lambda tup: tup[0], reverse=False)
                data_tuples = [ (tup[1][0], tup[1][1][:query_size]) for tup in scored_data_tuples ]
            aggregate_cache = dict()
            for q_idx, (query_function, query_args, aggregate) in enumerate(queries):
                if aggregate:
                    aggregate_cache[q_idx] = query_function(query_args, None, None, M_c, X_L_list, X_D_list, T, self, numsamples)

            if len(aggregate_cache) == len(queries):
                limit = 1
            data = []
            row_count = 0
            for row_id, row in data_tuples:
                for q_idx, (query_function, query_args, aggregate) in enumerate(queries):
                    if aggregate:
                        row[q_idx] = aggregate_cache[q_idx]
                    elif row[q_idx] is None:
                        if query_function != funcs._column_ignore:
                            row[q_idx] = query_function(query_args, row_id, row, M_c, X_L_list, X_D_list, T, self, numsamples)
                        else:
                            row[q_idx] = query_function(query_args, row_id, row, M_c_full, T_full, self)

                data.append(tuple(row))
                row_count += 1
                if row_count >= limit:
                    break

        if newtablename is not None:
            cctypes_full = self.persistence_layer.get_cctypes_full(tablename)
            self.create_btable_from_existing(newtablename, query_colnames, cctypes_full, M_c_full, data)
        if summarize | hist | freq:
            if summarize:
                data, columns = utils.summarize_table(data, query_colnames, M_c, remove_key=True)
            elif hist:
                data, columns = utils.histogram_table(data, query_colnames, M_c, remove_key=True)
            elif freq:
                data, columns = utils.freq_table(data, query_colnames, M_c, remove_key=True)
            column_names = columns
        else:
            columns = data_utils.get_column_labels_from_M_c(M_c, query_colnames)
            column_names = query_colnames
        ret = dict(data=data, column_labels=columns, column_names=column_names)
        if plot:
            ret['M_c'] = M_c
            ret['schema_full'] = self.persistence_layer.get_schema_full(tablename)
            try:
                ret['metadata_full'] = self.persistence_layer.get_metadata_full(tablename)
            except BayesDBError:
                pass

        return ret

    def simulate(self, tablename, functions, givens, numpredictions, order_by, plot=False, modelids=None, summarize=False, hist=False, freq=False, newtablename=None):
        """Simple predictive samples. Returns one row per prediction, with all the given and predicted variables."""
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if not self.persistence_layer.has_models(tablename):
            raise utils.BayesDBNoModelsError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        if len(X_L_list) == 0:
            return {'message': 'You must INITIALIZE MODELS (and highly preferably ANALYZE) before using predictive queries.'}
        else:
            M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
            numrows = len(M_r['idx_to_name'])
            name_to_idx = M_c['name_to_idx']
            given_col_idxs_to_vals = dict()
            Y = None
            if givens is not None:
                Y = []
                for given_condition in givens.given_conditions:
                    column_value = given_condition.value
                    column_name = given_condition.column
                    column_value = utils.string_to_column_type(column_value, column_name, M_c)
                    given_col_idxs_to_vals[name_to_idx[column_name]] = column_value
                    Y.append((numrows + 1, name_to_idx[column_name], column_value))

                Y = [ (r, c, data_utils.convert_value_to_code(M_c, c, colval)) for r, c, colval in Y ]
            column_lists = self.persistence_layer.get_column_lists(tablename)
            queries, query_colnames = self.parser.parse_functions(functions, M_c, T, M_c_full=None, T_full=None, column_lists=column_lists)
            col_indices = [ query[1][0] for query in queries ]
            query_col_indices = [ idx for idx in col_indices if idx not in given_col_idxs_to_vals.keys() ]
            Q = [ (numrows + 1, col_idx) for col_idx in query_col_indices ]
            if len(Q) > 0:
                out = self.call_backend('simple_predictive_sample', dict(M_c=M_c, X_L=X_L_list, X_D=X_D_list, Y=Y, Q=Q, n=numpredictions))
            else:
                out = [ [] for x in range(numpredictions) ]
            assert type(out) == list and len(out) >= 1 and type(out[0]) == list and len(out) == numpredictions
            data = []
            for out_row in out:
                row = []
                i = 0
                for idx in col_indices:
                    if idx in given_col_idxs_to_vals:
                        row.append(given_col_idxs_to_vals[idx])
                    else:
                        row.append(data_utils.convert_code_to_value(M_c, idx, out_row[i]))
                        i += 1

                data.append(row)

            if newtablename is not None:
                cctypes = self.persistence_layer.get_cctypes(tablename)
                newtable_info = self.create_btable_from_existing(newtablename, query_colnames, cctypes, M_c, data)
                if 'key' in query_colnames:
                    query_colnames.remove('key')
            if summarize | hist | freq:
                if summarize:
                    data, columns = utils.summarize_table(data, query_colnames, M_c, remove_key=False)
                elif hist:
                    data, columns = utils.histogram_table(data, query_colnames, M_c, remove_key=False)
                elif freq:
                    data, columns = utils.freq_table(data, query_colnames, M_c, remove_key=False)
                column_names = columns
            else:
                columns = data_utils.get_column_labels_from_M_c(M_c, query_colnames)
                column_names = query_colnames
            ret = dict(data=data, column_labels=columns, column_names=column_names)
            if plot:
                ret['M_c'] = M_c
                ret['schema_full'] = self.persistence_layer.get_schema_full(tablename)
            return ret

    def show_column_lists(self, tablename):
        """
        Return a list of all column list names.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        column_lists = self.persistence_layer.get_column_lists(tablename)
        return dict(column_labels=['column list'], data=[ [k] for k in column_lists.keys() ])

    def show_row_lists(self, tablename):
        """
        Return a list of all row lists, and their row counts.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        row_lists = self.persistence_layer.get_row_lists(tablename)
        return dict(column_labels=['Row List Name', 'Row Count'], data=[ (name, len(rows)) for name, rows in row_lists.items() ])

    def show_columns(self, tablename, column_list=None):
        """
        Return the specified columnlist. If None, return all columns in original order.
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        if column_list:
            column_names = self.persistence_layer.get_column_list(tablename, column_list)
        else:
            M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
            column_names = list(M_c['name_to_idx'].keys())
        return dict(column_labels=column_names)

    def show_model(self, tablename, modelid, filename):
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        import crosscat.utils.plot_utils
        crosscat.utils.plot_utils.plot_views(numpy.array(T), X_D_list[modelid], X_L_list[modelid], M_c, filename)

    def create_column_list(self, tablename, functions, name):
        """
        Create the column list with the specified column names (functions).
        """
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        column_lists = self.persistence_layer.get_column_lists(tablename)
        queries, column_names = self.parser.parse_functions(functions, M_c, T, M_c, T, column_lists, key_column_name=None)
        if name:
            self.persistence_layer.add_column_list(tablename, name, column_names)
        return dict(column_labels=column_names)

    def estimate_columns(self, tablename, functions, whereclause, limit, order_by, name=None, modelids=None, numsamples=None):
        """
        Return all the column names from the specified table as a list.
        First, columns are filtered based on whether they match the whereclause.
        The whereclause must consist of functions of a single column only.
        Next, the columns are ordered by other functions of a single column.
        Finally, the columns are limited to the specified number.

        ## allowed functions:
        # typicality(centrality)
        # dependence probability to <col>
        # mutual information with <col>
        # correlation with <col>
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        column_indices = list(M_c['name_to_idx'].values())
        func_descriptions = []
        where_conditions = self.parser.parse_column_whereclause(whereclause, M_c, T)
        if where_conditions is not None and len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        column_indices_and_data = estimate_columns_utils.filter_column_indices(column_indices, where_conditions, M_c, T, X_L_list, X_D_list, self, numsamples)
        func_descriptions += [ estimate_columns_utils.function_description(where_item[0][0], where_item[0][1], M_c) for where_item in where_conditions ]
        if order_by and len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if order_by != False:
            order_by = self.parser.parse_column_order_by_clause(order_by, M_c)
            func_descriptions += [ estimate_columns_utils.function_description(order_item[0], order_item[1], M_c) for order_item in order_by ]
        ordered_tuples = estimate_columns_utils.order_columns(column_indices_and_data, order_by, M_c, X_L_list, X_D_list, T, self, numsamples)
        if limit != float('inf'):
            ordered_tuples = ordered_tuples[:limit]
        column_names = []
        column_data = []
        for ordered_tuple in ordered_tuples:
            if type(ordered_tuple) == int:
                ordered_tuple = ((), column_idx_tup)
            column_name_temp = M_c['idx_to_name'][str(ordered_tuple[1])]
            column_names.append(column_name_temp)
            column_data_temp = [
             data_utils.get_column_labels_from_M_c(M_c, [column_name_temp])[0]]
            column_data_temp.append(column_name_temp)
            column_data_temp.extend(ordered_tuple[0])
            column_data.append(column_data_temp)

        if name:
            self.persistence_layer.add_column_list(tablename, name, column_names)
        used_names = set()
        indices_to_pop = []
        func_descriptions.insert(0, 'column label')
        func_descriptions.insert(1, 'column name')
        for i, name in enumerate(func_descriptions):
            if name not in used_names:
                used_names.add(name)
            else:
                indices_to_pop.append(i)

        indices_to_pop.sort(reverse=True)
        for i in indices_to_pop:
            func_descriptions.pop(i)

        for column_data_list in column_data:
            for i in indices_to_pop:
                column_data_list.pop(i)

        ret = dict()
        if column_data != []:
            ret['column_labels'] = func_descriptions
            ret['data'] = column_data
        return ret

    def estimate_pairwise_row(self, tablename, function, row_list, clusters_name=None, threshold=None, modelids=None, numsamples=None):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        if len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if row_list:
            row_indices = self.persistence_layer.get_row_list(tablename, row_list)
            if len(row_indices) == 0:
                raise utils.BayesDBError('Error: Row list %s has no rows.' % row_list)
        else:
            row_indices = None
        column_lists = self.persistence_layer.get_column_lists(tablename)
        matrix, row_indices_reordered, clusters = pairwise.generate_pairwise_row_matrix(function, X_L_list, X_D_list, M_c, T, tablename, engine=self, row_indices=row_indices, cluster_threshold=threshold, column_lists=column_lists, numsamples=numsamples)
        title = 'Pairwise row %s for %s' % (function.function_id, tablename)
        ret = dict(matrix=matrix, column_names=row_indices_reordered, title=title, message='Created ' + title)
        if clusters is not None:
            cluster_name_tuples = []
            for i, cluster in enumerate(clusters):
                name = '%s_%d' % (clusters_name, i)
                num_rows = len(cluster)
                self.persistence_layer.add_row_list(tablename, name, cluster)
                cluster_name_tuples.append((name, num_rows))

            ret['clusters'] = clusters
            ret['row_lists'] = cluster_name_tuples
        return ret

    def estimate_pairwise(self, tablename, function_name, column_list=None, clusters_name=None, threshold=None, modelids=None, numsamples=None):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        if len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if column_list:
            column_names = self.persistence_layer.get_column_list(tablename, column_list)
            if len(column_names) == 0:
                raise utils.BayesDBError('Error: Column list %s has no columns.' % column_list)
            utils.check_for_duplicate_columns(column_names)
        else:
            column_names = None
        matrix, column_names_reordered, clusters = pairwise.generate_pairwise_column_matrix(function_name, X_L_list, X_D_list, M_c, T, tablename, engine=self, column_names=column_names, cluster_threshold=threshold, numsamples=numsamples)
        title = 'Pairwise column %s for %s' % (function_name, tablename)
        ret = dict(matrix=matrix, column_names=column_names_reordered, title=title, message='Created ' + title)
        if clusters is not None:
            cluster_name_tuples = []
            for i, cluster in enumerate(clusters):
                name = '%s_%d' % (clusters_name, i)
                column_names = [ M_c['idx_to_name'][str(idx)] for idx in cluster ]
                self.persistence_layer.add_column_list(tablename, name, column_names)
                cluster_name_tuples.append((name, column_names))

            ret['clusters'] = clusters
            ret['column_lists'] = cluster_name_tuples
        return ret

    def drop_column_list(self, tablename, list_name):
        """
        Remove column list from stored items for btable.
        """
        self.persistence_layer.drop_column_list(tablename, list_name)
        message = 'Column list %s removed from btable %s' % (list_name, tablename)
        return dict(message=message)

    def drop_row_list(self, tablename, list_name):
        """
        Remove row list from stored items for btable.
        """
        self.persistence_layer.drop_row_list(tablename, list_name)
        message = 'Row list %s removed from btable %s' % (list_name, tablename)
        return dict(message=message)

    def estimate_columns(self, tablename, functions, whereclause, limit, order_by, name=None, modelids=None, numsamples=None):
        """
        Return all the column names from the specified table as a list.
        First, columns are filtered based on whether they match the whereclause.
        The whereclause must consist of functions of a single column only.
        Next, the columns are ordered by other functions of a single column.
        Finally, the columns are limited to the specified number.

        ## allowed functions:
        # typicality(centrality)
        # dependence probability to <col>
        # mutual information with <col>
        # correlation with <col>
        """
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        column_indices = list(M_c['name_to_idx'].values())
        func_descriptions = []
        where_conditions = self.parser.parse_column_whereclause(whereclause, M_c, T)
        if where_conditions is not None and len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        column_indices_and_data = estimate_columns_utils.filter_column_indices(column_indices, where_conditions, M_c, T, X_L_list, X_D_list, self, numsamples)
        func_descriptions += [ estimate_columns_utils.function_description(where_item[0][0], where_item[0][1], M_c) for where_item in where_conditions ]
        if order_by and len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if order_by != False:
            order_by = self.parser.parse_column_order_by_clause(order_by, M_c)
            func_descriptions += [ estimate_columns_utils.function_description(order_item[0], order_item[1], M_c) for order_item in order_by ]
        ordered_tuples = estimate_columns_utils.order_columns(column_indices_and_data, order_by, M_c, X_L_list, X_D_list, T, self, numsamples)
        if limit != float('inf'):
            ordered_tuples = ordered_tuples[:limit]
        column_names = []
        column_data = []
        for ordered_tuple in ordered_tuples:
            if type(ordered_tuple) == int:
                ordered_tuple = ((), column_idx_tup)
            column_name_temp = M_c['idx_to_name'][str(ordered_tuple[1])]
            column_names.append(column_name_temp)
            column_data_temp = [
             data_utils.get_column_labels_from_M_c(M_c, [column_name_temp])[0]]
            column_data_temp.append(column_name_temp)
            column_data_temp.extend(ordered_tuple[0])
            column_data.append(column_data_temp)

        if name:
            if self.persistence_layer.column_list_exists(tablename, name):
                print 'WARNING: Column list name %s already exists for btable %s and will not be overwritten.' % (name, tablename)
                print '    Use "DROP COLUMN LIST %s FROM %s" first.' % (name, tablename)
            else:
                self.persistence_layer.add_column_list(tablename, name, column_names)
        used_names = set()
        indices_to_pop = []
        func_descriptions.insert(0, 'column label')
        func_descriptions.insert(1, 'column name')
        for i, name in enumerate(func_descriptions):
            if name not in used_names:
                used_names.add(name)
            else:
                indices_to_pop.append(i)

        indices_to_pop.sort(reverse=True)
        for i in indices_to_pop:
            func_descriptions.pop(i)

        for column_data_list in column_data:
            for i in indices_to_pop:
                column_data_list.pop(i)

        ret = dict()
        if column_data != []:
            ret['column_labels'] = func_descriptions
            ret['data'] = column_data
        return ret

    def estimate_pairwise_row(self, tablename, function, row_list, clusters_name=None, threshold=None, modelids=None, numsamples=None):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        if len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if row_list:
            row_indices = self.persistence_layer.get_row_list(tablename, row_list)
            if len(row_indices) == 0:
                raise utils.BayesDBError('Error: Row list %s has no rows.' % row_list)
        else:
            row_indices = None
        column_lists = self.persistence_layer.get_column_lists(tablename)
        matrix, row_indices_reordered, clusters = pairwise.generate_pairwise_row_matrix(function, X_L_list, X_D_list, M_c, T, tablename, engine=self, row_indices=row_indices, cluster_threshold=threshold, column_lists=column_lists, numsamples=numsamples)
        title = 'Pairwise row %s for %s' % (function.function_id, tablename)
        ret = dict(matrix=matrix, column_names=row_indices_reordered, title=title, message='Created ' + title)
        if clusters is not None:
            if self.persistence_layer.row_list_exists(tablename, clusters_name):
                print 'WARNING: Column lists with prefix %s already exist for btable %s' % (clusters_name, tablename)
                print '    Use "DROP ROW LIST %s FROM %s" first.' % (clusters_name, tablename)
            else:
                cluster_name_tuples = []
                for i, cluster in enumerate(clusters):
                    name = '%s_%d' % (clusters_name, i)
                    num_rows = len(cluster)
                    self.persistence_layer.add_row_list(tablename, name, cluster)
                    cluster_name_tuples.append((name, num_rows))

                ret['clusters'] = clusters
                ret['row_lists'] = cluster_name_tuples
        return ret

    def estimate_pairwise(self, tablename, function_name, column_list=None, clusters_name=None, threshold=None, modelids=None, numsamples=None):
        if not self.persistence_layer.check_if_table_exists(tablename):
            raise utils.BayesDBInvalidBtableError(tablename)
        X_L_list, X_D_list, M_c = self.persistence_layer.get_latent_states(tablename, modelids)
        M_c, M_r, T = self.persistence_layer.get_metadata_and_table(tablename)
        if len(X_L_list) == 0:
            raise utils.BayesDBNoModelsError(tablename)
        if column_list:
            column_names = self.persistence_layer.get_column_list(tablename, column_list)
            if len(column_names) == 0:
                raise utils.BayesDBError('Error: Column list %s has no columns.' % column_list)
            utils.check_for_duplicate_columns(column_names)
        else:
            column_names = None
        matrix, column_names_reordered, clusters = pairwise.generate_pairwise_column_matrix(function_name, X_L_list, X_D_list, M_c, T, tablename, engine=self, column_names=column_names, cluster_threshold=threshold, numsamples=numsamples)
        title = 'Pairwise column %s for %s' % (function_name, tablename)
        ret = dict(matrix=matrix, column_names=column_names_reordered, title=title, message='Created ' + title)
        if clusters is not None:
            if self.persistence_layer.column_list_exists(tablename, clusters_name):
                print 'WARNING: Column lists with prefix %s already exist for btable %s' % (clusters_name, tablename)
                print '    Use "DROP COLUMN LIST %s FROM %s" first.' % (clusters_name, tablename)
            else:
                cluster_name_tuples = []
                for i, cluster in enumerate(clusters):
                    name = '%s_%d' % (clusters_name, i)
                    column_names = [ M_c['idx_to_name'][str(idx)] for idx in cluster ]
                    self.persistence_layer.add_column_list(tablename, name, column_names)
                    cluster_name_tuples.append((name, column_names))

                ret['clusters'] = clusters
                ret['column_lists'] = cluster_name_tuples
        return ret


get_name = lambda x: getattr(x, '__name__')
get_Engine_attr = lambda x: getattr(Engine, x)
is_Engine_method_name = lambda x: inspect.ismethod(get_Engine_attr(x))

def get_method_names():
    return filter(is_Engine_method_name, dir(Engine))


def get_method_name_to_args():
    method_names = get_method_names()
    method_name_to_args = dict()
    for method_name in method_names:
        method = Engine.__dict__[method_name]
        arg_str_list = inspect.getargspec(method).args[1:]
        method_name_to_args[method_name] = arg_str_list

    return method_name_to_args


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

    def __init__(self, target, args):
        super(StoppableThread, self).__init__(target=target, args=args)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class AnalyzeMaster(StoppableThread):

    def __init__(self, args):
        self.target = self.analyze_master
        super(AnalyzeMaster, self).__init__(target=self.target, args=args)

    def get_info(self):
        if not hasattr(self, 'start_time'):
            return "Analyze hasn't started"
        else:
            elapsed_seconds = time.time() - self.start_time
            if self.requested_iterations is None:
                remaining_seconds = self.total_seconds - elapsed_seconds
                if remaining_seconds > 0:
                    return 'Iterations completed: %d\nElapsed minutes: %0.2f\nRemaining minutes: %0.2f' % (self.iters_done, elapsed_seconds / 60.0, remaining_seconds / 60.0)
                return 'Iterations completed: %d\nTime complete: waiting for final iteration to finish.' % self.iters_done
            else:
                return 'Iterations completed: %d\nRemaining iterations: %d\nElapsed minutes: %02.f\nEstimated remaining minutes:%0.2f' % (self.iters_done, self.requested_iterations - self.iters_done, elapsed_seconds / 60.0, self.time_remaining_estimate / 60.0)
            return timing_str

    def analyze_master(self, tablename, modelids, kernel_list, iterations, seconds, M_c, T, T_sub, models, background, engine):
        """
        Helper function for analyze. This is the thread that runs in the background as the previous analyze
        command returns before analyze is complete.
        """
        self.iters_done = 0
        self.time_remaining_estimate = -1
        if iterations is None:
            self.requested_iterations = None
            iterations = 1000
        else:
            self.requested_iterations = iterations
        self.start_time = time.time()
        self.total_seconds = seconds
        X_L_list = [ models[i]['X_L'] for i in models.keys() ]
        X_D_list = [ models[i]['X_D'] for i in models.keys() ]
        threads = []
        for i, modelid in enumerate(modelids):
            if T_sub is None:
                p = AnalyzeWorker(args=(modelid, tablename, kernel_list, iterations, seconds, M_c, T, X_L_list[i], X_D_list[i], background, engine))
            else:
                p = AnalyzeWorker(args=(modelid, tablename, kernel_list, iterations, seconds, M_c, T_sub, X_L_list[i], X_D_list[i], background, engine))
            p.daemon = True
            p.start()
            threads.append(p)

        workers_done = False
        while not workers_done:
            time.sleep(0.25)
            workers_done = True
            for p in threads:
                if not p.isAlive():
                    p.join()
                else:
                    workers_done = False

            info = zip(*[ p.get_progress() for p in threads ])
            iter_list = info[0]
            self.iters_done = min(iter_list)
            time_estimates = info[1]
            self.time_remaining_estimate = max(time_estimates)
            if self.stopped():
                for p in threads:
                    if p.isAlive():
                        p.stop()

        if T_sub is not None:
            engine._insert_subsampled_rows(tablename, T, T_sub, M_c, X_L_list, X_D_list, modelids)
        if background:
            print "\nAnalyze for table %s complete. Use 'SHOW MODELS FOR %s' to view models." % (tablename, tablename)
        return


class AnalyzeWorker(StoppableThread):
    """ Controls ANALYZE for a single model.

    Attributes:
        target (function): analyze method
        iterations_done (int): Number of iterations performed by this worker
        time_per_model (float): Average time per iteration. Includes analyze and IO.
        collect_diagnostics_steps (int): Maximum number of steps between diagnostic data
            collections.
        collect_diagnostics_time (float): Maximum time (seconds) between diagnostic data
            collections.
        collection_ticker (int): Keeps track of the number of iterations since the last diagnostics
            collection.
        collection_timer (float): Keeps track for the time (seconds) since the last diagnostics
            collection.

    """

    def __init__(self, args):
        self.target = self.do_analyze_for_model
        super(AnalyzeWorker, self).__init__(target=self.target, args=args)
        self.iterations_done = 0
        self.time_per_model = 0
        self.collect_diagnostics_steps = 5
        self.collect_diagnostics_time = 300.0
        self.collection_ticker = 0
        self.collection_timer = 0

    def get_diagnostics(self, X_L, X_D):
        """Computes each single-state diagnostic available
        """
        diagnostics = dict()
        for item in diag_utils.single_state_diagnostics:
            item_method = getattr(diag_utils, 'get_' + item)
            diagnostics[item] = item_method(X_L, X_D)

        return diagnostics

    def get_progress(self):
        time_left = (self.iterations - self.iterations_done) * self.time_per_model
        return (self.iterations_done, time_left)

    def do_analyze_for_model(self, modelid, tablename, kernel_list, iterations, seconds, M_c, T, X_L, X_D, background, engine):
        analyze_args = dict(M_c=M_c, T=T, do_diagnostics=True, kernel_list=kernel_list, X_L=X_L, X_D=X_D, n_steps=1)
        start_time = time.time()
        last_write_time = start_time
        models_per_call = 1
        self.total_analyze_time = 0
        self.total_write_time = 0
        self.iterations = iterations
        self.iterations_done = 0
        self.collection_timer = 0.0
        self.collection_ticker = 0
        diagnostics_data = self.get_diagnostics(X_L, X_D)
        for i in range(iterations):
            cur_time = time.time()
            X_L, X_D, diagnostics_dict = engine.call_backend('analyze', analyze_args)
            this_iter_analyze_time = time.time() - cur_time
            self.collection_timer += this_iter_analyze_time
            self.collection_ticker += 1
            if self.collection_ticker == self.collect_diagnostics_steps or self.collection_timer > self.collect_diagnostics_time:
                diagnostics_data = self.get_diagnostics(X_L, X_D)
                diagnostics_data['logscore'] = diagnostics_dict['logscore'][(-1)]
                self.collection_timer = 0.0
                self.collection_ticker = 0
            analyze_args['X_L'] = X_L
            analyze_args['X_D'] = X_D
            cur_time = time.time()
            elapsed = cur_time - start_time
            engine.persistence_layer.update_model(tablename, X_L, X_D, diagnostics_data, modelid, increment_iterations=1, increment_time=this_iter_analyze_time)
            self.total_write_time += time.time() - cur_time
            self.iterations_done += 1
            if self.stopped() or elapsed >= seconds and seconds is not None:
                return
            self.time_per_model = float(elapsed) / self.iterations_done
            if self.time_per_model > 5:
                models_per_call = 1
            else:
                models_per_call = int(5.0 / self.time_per_model)
            if iterations - self.iterations_done < models_per_call:
                models_per_call = iterations - self.iterations_done
            analyze_args['n_steps'] = models_per_call

        return