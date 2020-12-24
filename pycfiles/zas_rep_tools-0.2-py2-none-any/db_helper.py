# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/db_helper.py
# Compiled at: 2018-10-25 10:50:26
from __future__ import generators
import os, sys, regex, inspect, itertools, logging, json
from pysqlcipher import dbapi2 as sqlite
import functools
from pyhashxx import hashxx
from datetime import datetime as dt
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.utils.zaslogger import ZASLogger
sql_supported_data_type = [
 'NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB']
sql_supported_data_functions = ['date', 'time', 'datetime', 'julianday', 'strftime']

def dict_to_list(inp_dict, order_list):
    out_list = []
    for col in order_list:
        try:
            out_list.append(inp_dict[col])
        except:
            out_list.append(None)

    return out_list


def log_and_execute(cursor, sql, *args):
    s = sql
    if len(args) > 0:
        cursor.execute('SELECT ' + (', ').join([ 'quote(?)' for i in args ]), args)
        quoted_values = cursor.fetchone()
        for quoted_value in quoted_values:
            s = s.replace('?', quoted_value, 1)

    print 'SQL command: ' + s
    cursor.execute(sql, args)


class DBErrorCatcher(type):

    def __new__(cls, name, bases, dct):
        if 'DBErrorCatcher' in dct:
            if dct['DBErrorCatcher']:
                self.L = ZASLogger('DBErrorCatcher', level=logging.ERROR, logger_usage=True)
                self.logger = self.L.getLogger()
                for m in dct:
                    if hasattr(dct[m], '__call__'):
                        dct[m] = catch_exception(dct[m], logger)

        return type.__new__(cls, name, bases, dct)


def catch_exception(f, logger):

    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except sqlite.DataError as e:
            msg = ("sqlite.DataError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except sqlite.InternalError as e:
            msg = ("sqlite.InternalError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except sqlite.IntegrityError as e:
            msg = ("sqlite.IntegrityError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except sqlite.OperationalError as e:
            msg = ("sqlite.OperationalError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except sqlite.NotSupportedError as e:
            msg = ("sqlite.NotSupportedError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except sqlite.ProgrammingError as e:
            msg = ("sqlite.ProgrammingError: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()
        except KeyboardInterrupt:
            self.logger.warning('KeyboardInterrupt: Process was stopped from User. Some inconsistence in the current DB may situated.')
            sys.exit()
        except Exception as e:
            msg = ("OtherExceptions: '{}'-Function returned following Error: '{}'. ").format(f.__name__, e)
            self.logger.error(msg)
            sys.exit()

    return func


attributs_names_corpus = [
 ('id', 'INTEGER NOT NULL'),
 ('name', 'TEXT NOT NULL'),
 ('platform_name', 'TEXT NOT NULL'),
 ('template_name', 'TEXT'),
 ('version', 'TEXT'),
 ('language', 'TEXT NOT NULL'),
 ('created_at', 'TEXT NOT NULL'),
 ('source', 'TEXT'),
 ('license', 'TEXT'),
 ('visibility', 'TEXT NOT NULL'),
 ('typ', 'TEXT NOT NULL'),
 ('tokenizer', 'TEXT'),
 ('sent_splitter', 'TEXT'),
 ('pos_tagger', 'TEXT'),
 ('sentiment_analyzer', 'TEXT'),
 ('preprocession', 'INTEGER'),
 ('del_url', 'INTEGER'),
 ('del_punkt', 'INTEGER'),
 ('del_num', 'INTEGER'),
 ('del_mention', 'INTEGER'),
 ('del_hashtag', 'INTEGER'),
 ('del_html', 'INTEGER'),
 ('case_sensitiv', 'INTEGER'),
 ('lang_classification', 'INTEGER'),
 ('emojis_normalization', 'INTEGER'),
 ('sent_num', 'INTEGER'),
 ('token_num', 'INTEGER'),
 ('doc_num', 'INTEGER'),
 ('text_field_name', 'TEXT'),
 ('id_field_name', 'TEXT'),
 ('locked', 'INTEGER')]
doc_id_tag = 'id'
default_columns_and_types_for_corpus_documents = [
 ('rowid', 'INTEGER PRIMARY KEY'),
 (
  doc_id_tag, 'INTEGER'),
 ('text', 'JSON NOT NULL')]
default_constraints_for_corpus_documents = [
 'CONSTRAINT "Uniq_ID" UNIQUE ("id")']
default_index_for_corpus_documents = [
 'CREATE UNIQUE INDEX IF NOT EXISTS ix_id ON documents (id);']
extended_columns_and_types_for_corpus_documents_twitter = [
 ('t_created_at', 'TEXT'),
 ('t_language', 'TEXT'),
 ('t_used_client', 'TEXT'),
 ('u_created_at', 'TEXT'),
 ('u_description', 'TEXT'),
 ('u_favourites', 'INTEGER'),
 ('u_followers', 'INTEGER'),
 ('u_friends', 'TEXT'),
 ('u_id', 'INTEGER NOT NULL'),
 ('u_lang', 'TEXT'),
 ('u_given_name', 'TEXT'),
 ('u_username', 'TEXT NOT NULL'),
 ('u_verified', 'TEXT'),
 ('u_location', 'TEXT'),
 ('is_extended', 'INTEGER'),
 ('is_retweet', 'INTEGER'),
 ('is_answer', 'INTEGER')]
extended_columns_and_types_for_corpus_documents_blogger = [
 ('gender', 'TEXT NOT NULL'),
 ('age', 'INTEGER NOT NULL'),
 ('working_area', 'TEXT NOT NULL'),
 ('star_constellation', 'TEXT NOT NULL')]
attributs_names_stats = [
 ('id', 'INTEGER NOT NULL'),
 ('corpus_id', 'INTEGER'),
 ('name', 'TEXT NOT NULL'),
 ('version', 'TEXT'),
 ('created_at', 'TEXT NOT NULL'),
 ('visibility', 'TEXT NOT NULL'),
 ('typ', 'TEXT NOT NULL'),
 ('db_frozen', 'INTEGER'),
 ('context_lenght', 'INTEGER'),
 ('language', 'TEXT'),
 ('repl_up', 'INTEGER'),
 ('ignore_hashtag', 'INTEGER'),
 ('ignore_url', 'INTEGER'),
 ('ignore_mention', 'INTEGER'),
 ('ignore_punkt', 'INTEGER'),
 ('ignore_num', 'INTEGER'),
 ('force_cleaning', 'INTEGER'),
 ('case_sensitiv', 'INTEGER'),
 ('full_repetativ_syntagma', 'INTEGER'),
 ('min_scope_for_indexes', 'INTEGER'),
 ('locked', 'INTEGER'),
 ('pos_tagger', 'TEXT'),
 ('sentiment_analyzer', 'TEXT'),
 ('baseline_delimiter', 'TEXT')]
default_col_baseline_main = (
 ('syntagma', 'TEXT PRIMARY KEY NOT NULL'),
 ('stemmed', 'TEXT NOT NULL'),
 ('scope', 'INTEGER NOT NULL'),
 ('occur_syntagma_all', 'INTEGER NOT NULL'))
default_col_baseline_repls_core = (
 ('occur_repl_uniq', 'TEXT'),
 ('occur_repl_exhausted', 'TEXT'))
default_col_baseline_redus_core = (
 ('occur_redu_uniq', 'TEXT'),
 ('occur_redu_exhausted', 'TEXT'))
default_col_baseline_repls_addit = (('occur_full_syn_repl', 'TEXT'), )
default_col_baseline_redus_addit = (('occur_full_syn_redu', 'TEXT'), )
default_columns_and_types_for_stats_baseline = list(default_col_baseline_main + default_col_baseline_repls_core + default_col_baseline_redus_core + default_col_baseline_repls_addit + default_col_baseline_redus_addit)
default_constraints_for_stats_baseline = [
 'CONSTRAINT "Uniq_Syntagma" UNIQUE ("syntagma")',
 'CONSTRAINT "Uniq_Syntagma" UNIQUE ("stemmed")']
default_indexes_for_stats_baseline = [
 'CREATE UNIQUE INDEX IF NOT EXISTS "ix_syntagma" ON "baseline" ("syntagma");']
tag_normalized_word = 'normalized_word'
default_col_for_rep_core = (('id', 'INTEGER PRIMARY KEY'), )
default_col_for_rep_doc_info = (
 ('doc_id', 'INTEGER NOT NULL'),
 ('redufree_len', 'JSON NOT NULL'))
default_col_for_rep_indexes = (
 ('index_in_corpus', 'JSON NOT NULL'),
 ('index_in_redufree', 'JSON NOT NULL'))
default_col_for_repl_word_info = (
 (
  tag_normalized_word, ' TEXT NOT NULL'),
 ('rle_word', 'TEXT NOT NULL'),
 ('stemmed', 'TEXT NOT NULL'))
default_col_for_rep_repl_data = (
 ('repl_letter', 'TEXT NOT NULL'),
 ('repl_length', 'INTEGER NOT NULL'),
 ('index_of_repl', 'INTEGER NOT NULL'),
 ('in_redu', 'JSON'))
default_col_for_rep_addit_info_word = (
 ('pos', ' TEXT NOT NULL'),
 ('polarity', 'JSON NOT NULL'))
default_columns_and_types_for_stats_replications = list(default_col_for_rep_core + default_col_for_rep_doc_info + default_col_for_rep_indexes + default_col_for_repl_word_info + default_col_for_rep_repl_data + default_col_for_rep_addit_info_word)
default_constraints_for_stats_replications = [
 'CONSTRAINT "Uniq_Repl_ID" UNIQUE ("id")']
default_indexes_for_stats_replications = []
default_col_for_rep_redu_data = (
 ('orig_words', 'JSON NOT NULL'),
 ('redu_length', 'INTEGER NOT NULL'))
default_col_for_redu_word_info = (
 (
  tag_normalized_word, ' TEXT NOT NULL'),
 ('stemmed', 'TEXT NOT NULL'))
default_columns_and_types_for_stats_reduplications = list(default_col_for_rep_core + default_col_for_rep_doc_info + default_col_for_rep_indexes + default_col_for_redu_word_info + default_col_for_rep_redu_data + default_col_for_rep_addit_info_word)
default_constraints_for_stats_reduplications = [
 'CONSTRAINT "Uniq_Redu-ID" UNIQUE ("id")']
default_indexes_for_stats_reduplications = []
default_indexes = {'corpus': {'documents': default_index_for_corpus_documents}, 
   'stats': {'replications': default_indexes_for_stats_replications, 
             'reduplications': default_indexes_for_stats_reduplications, 
             'baseline': default_indexes_for_stats_baseline}}
default_tables = {'corpus': {'info': attributs_names_corpus, 
              'documents': {'basic': default_columns_and_types_for_corpus_documents, 
                            'twitter': extended_columns_and_types_for_corpus_documents_twitter, 
                            'blogger': extended_columns_and_types_for_corpus_documents_blogger}}, 
   'stats': {'info': attributs_names_stats, 
             'replications': default_columns_and_types_for_stats_replications, 
             'reduplications': default_columns_and_types_for_stats_reduplications, 
             'baseline': default_columns_and_types_for_stats_baseline}}
default_constraints = {'corpus': {'documents': default_constraints_for_corpus_documents}, 
   'stats': {'replications': default_constraints_for_stats_replications, 
             'reduplications': default_constraints_for_stats_reduplications, 
             'repl_baseline': default_constraints_for_stats_baseline, 
             'redu_baseline': default_constraints_for_stats_baseline}}

def columns_and_values_to_str(columns_names, values):
    """
    without Datatypes
    """
    if isinstance(columns_names, list) and isinstance(values, list):
        str_columns_and_values = ''
        i = 1
        for column, value in zip(columns_names, values):
            if value is None:
                value = 'NULL'
            if value == 'NULL':
                if len(columns_names) > 1:
                    if i < len(columns_names):
                        str_columns_and_values += ('\n{}={}, ').format(column, value)
                    else:
                        str_columns_and_values += ('\n{}={} ').format(column, value)
                    i += 1
                elif len(columns_names) == 1:
                    str_columns_and_values += ('{}={}').format(column, value)
                else:
                    return False
            elif len(columns_names) > 1:
                if i < len(columns_names):
                    str_columns_and_values += ("\n{}='{}', ").format(column, value)
                else:
                    str_columns_and_values += ("\n{}='{}' ").format(column, value)
                i += 1
            elif len(columns_names) == 1:
                str_columns_and_values += ("{}='{}'").format(column, value)
            else:
                return False

    else:
        return False
    return str_columns_and_values


def values_to_placeholder(number):
    output = ''
    for i in range(number):
        if i < number - 1:
            output += '?,'
        elif i == number - 1:
            output += '?'

    return output


def columns_and_types_in_tuples_to_str(attributs_names):
    """
    use by table initialisation (with Datatypes)
    """
    if isinstance(attributs_names, list):
        str_attributs_names = ''
        i = 1
        for attribut in attributs_names:
            if not isinstance(attribut, tuple):
                return False
            if len(attributs_names) > 1:
                if i < len(attributs_names):
                    str_attributs_names += ('\n{} {}, ').format(attribut[0], attribut[1])
                else:
                    str_attributs_names += ('\n{} {} ').format(attribut[0], attribut[1])
                i += 1
            elif len(attributs_names) == 1:
                str_attributs_names += ('\n{} {}\n').format(attribut[0], attribut[1])
            else:
                return False

    else:
        return False
    return str_attributs_names


def list_of_select_objects_to_str(inputobj):
    """
    without Datatypes
    """
    try:
        inputobj + ''
        outputstr += (' {}').format(inputobj)
    except TypeError:
        outputstr = ''
        i = 1
        for obj in inputobj:
            if isinstance(obj, unicode):
                obj = obj.encode('utf8')
            if len(inputobj) > 1:
                if i < len(inputobj):
                    outputstr += ('\n{}, ').format(obj)
                else:
                    outputstr += ('\n{} ').format(obj)
                i += 1
            elif len(inputobj) == 1:
                outputstr += ('{}').format(obj)
            else:
                return False

    return outputstr


def constraints_list_to_str(constraints):
    """
    without Datatypes
    """
    if isinstance(constraints, list):
        str_constraints = ''
        i = 0
        for constrain in constraints:
            if len(constraints) > 1:
                if i == 0:
                    str_constraints += (',\n{} ').format(constrain)
                elif i < 0 and i < len(constraints):
                    str_constraints += ('\n{}, ').format(constrain)
                else:
                    str_constraints += ('\n{} ').format(constrain)
                i += 1
            elif len(constraints) == 1:
                str_constraints += (',\n{}').format(constrain)
            else:
                return False

    else:
        return False
    return str_constraints


def clean_value(value):
    if isinstance(value, (str, unicode)):
        newval = value.replace('\n', '\\n"')
        newval = newval.replace('"', "'")
        newval = newval.replace('\r', '\\r"')
        return newval
    else:
        return False


def values_to_tuple(values, mode):
    values_as_list = list()
    if mode == 'one':
        try:
            for value in values:
                if isinstance(value, (list, dict, tuple)):
                    values_as_list.append(json.dumps(value))
                else:
                    values_as_list.append(value)

        except:
            return False

    else:
        try:
            for row in values:
                temp_row = []
                for item in row:
                    if isinstance(item, (list, dict, tuple)):
                        temp_row.append(unicode(json.dumps(item)))
                    else:
                        temp_row.append(item)

                values_as_list.append(tuple(temp_row))

        except:
            return False

    return tuple(values_as_list)


def values_to_list(values, mode):
    values_as_list = list()
    if mode == 'one':
        try:
            for value in values:
                if isinstance(value, (tuple, list, dict)):
                    values_as_list.append(json.dumps(value))
                else:
                    values_as_list.append(value)

        except:
            return False

    else:
        try:
            for row in values:
                temp_row = []
                for item in row:
                    if isinstance(item, (tuple, list, dict)):
                        temp_row.append(unicode(json.dumps(item)))
                    else:
                        temp_row.append(item)

                values_as_list.append(temp_row)

        except:
            return False

    return values_as_list


def where_condition_to_str(inputobj, connector='AND'):
    try:
        inputobj.decode
        return (' {}').format(inputobj)
    except:
        return (' {} ').format(connector).join(inputobj)


def get_file_name(prjFolder, first_id, DBname, language, visibility, typ, fileName=False, platform_name=False, second_id=False, encrypted=False, rewrite=False, stop_if_db_already_exist=False):
    status = True
    i = 0
    while status:
        if not fileName:
            if platform_name:
                if encrypted:
                    if i == 1:
                        if second_id:
                            fileName = ('{}_{}_{}_{}_{}_{}_{}_encrypted_{}').format(first_id, second_id, typ, platform_name, DBname, language, visibility, i)
                        else:
                            fileName = ('{}_{}_{}_{}_{}_{}_encrypted_{}').format(first_id, typ, platform_name, DBname, language, visibility, i)
                    elif second_id:
                        fileName = ('{}_{}_{}_{}_{}_{}_{}_encrypted').format(first_id, second_id, typ, platform_name, DBname, language, visibility)
                    else:
                        fileName = ('{}_{}_{}_{}_{}_{}_encrypted').format(first_id, typ, platform_name, DBname, language, visibility)
                elif i == 1:
                    if second_id:
                        fileName = ('{}_{}_{}_{}_{}_{}_{}_plaintext_{}').format(first_id, second_id, typ, platform_name, DBname, language, visibility, i)
                    else:
                        fileName = ('{}_{}_{}_{}_{}_{}_plaintext_{}').format(first_id, typ, platform_name, DBname, language, visibility, i)
                elif second_id:
                    fileName = ('{}_{}_{}_{}_{}_{}_{}_plaintext').format(first_id, second_id, ttyp, platform_name, DBname, language, visibility)
                else:
                    fileName = ('{}_{}_{}_{}_{}_{}_plaintext').format(first_id, typ, platform_name, DBname, language, visibility)
            elif encrypted:
                if i == 1:
                    if second_id:
                        fileName = ('{}_{}_{}_{}_{}_{}_encrypted_{}').format(first_id, second_id, typ, DBname, language, visibility, i)
                    else:
                        fileName = ('{}_{}_{}_{}_{}_encrypted_{}').format(first_id, typ, DBname, language, visibility, i)
                elif second_id:
                    fileName = ('{}_{}_{}_{}_{}_{}_encrypted').format(first_id, second_id, typ, DBname, language, visibility)
                else:
                    fileName = ('{}_{}_{}_{}_{}_encrypted').format(first_id, typ, DBname, language, visibility)
            elif i == 1:
                if second_id:
                    fileName = ('{}_{}_{}_{}_{}_{}_plaintext_{}').format(first_id, second_id, typ, DBname, language, visibility, i)
                else:
                    fileName = ('{}_{}_{}_{}_{}_plaintext_{}').format(first_id, typ, DBname, language, visibility, i)
            elif second_id:
                fileName = ('{}_{}_{}_{}_{}_{}_plaintext').format(first_id, second_id, typ, DBname, language, visibility)
            else:
                fileName = ('{}_{}_{}_{}_{}_plaintext').format(first_id, typ, DBname, language, visibility)
        else:
            if i > 0:
                fileName_without_extension = os.path.splitext(fileName)[0]
                pattern = '^(.*?)(_[0-9]*)$'
                matched = regex.findall(pattern, fileName_without_extension)
                if matched:
                    fileName_without_extension = matched[0][0]
                fileName = fileName_without_extension + '_' + str(i)
            if i > 10000:
                print 'db_helpers.get_file_name(): Script was Aborting!!! To avoid never-ending loop'
                return (False, False)
                sys.exit()
            i += 1
            if '.db' not in fileName:
                fileName = fileName + '.db'
            path_to_db = os.path.join(prjFolder, fileName)
            if stop_if_db_already_exist:
                if os.path.isfile(path_to_db):
                    status = False
                    return (
                     fileName, None)
            if rewrite:
                if os.path.isfile(path_to_db):
                    status = False
                return (
                 fileName, path_to_db)
            if not os.path.isfile(path_to_db):
                status = False
                return (
                 fileName, path_to_db)

    return


def get_file_name_for_empty_DB(prjFolder, DBname, fileName=False, encrypted=False, rewrite=False, stop_if_db_already_exist=False):
    status = True
    i = 0
    while status:
        if not fileName:
            if encrypted:
                if i == 1:
                    fileName = ('{}_encrypted_{}').format(DBname, i)
                else:
                    fileName = ('{}_encrypted').format(DBname)
            elif i == 1:
                fileName = ('{}_plaintext_{}').format(DBname, i)
            else:
                fileName = ('{}_plaintext').format(DBname)
        else:
            if i > 0:
                fileName_without_extension = os.path.splitext(fileName)[0]
                pattern = '^(.*?)(_[0-9]*)$'
                matched = regex.findall(pattern, fileName_without_extension)
                if matched:
                    fileName_without_extension = matched[0][0]
                fileName = fileName_without_extension + '_' + str(i)
            if i > 10000:
                print 'db_helpers.get_file_name_for_empty_DB(): Aborting!!! To avoid never-ending loop'
                sys.exit()
            i += 1
            if '.db' not in fileName:
                fileName = fileName + '.db'
            path_to_db = os.path.join(prjFolder, fileName)
            if stop_if_db_already_exist:
                if os.path.isfile(path_to_db):
                    status = False
                    return (
                     fileName, None)
            if rewrite:
                if os.path.isfile(path_to_db):
                    status = False
                return (
                 fileName, path_to_db)
            if not os.path.isfile(path_to_db):
                status = False
                return (
                 fileName, path_to_db)

    return


def create_id(name, lang, typ, visibility):
    time_now = dt.now().strftime('%H:%M:%S')
    return str(hashxx(('{}{}{}{}{}').format(name[0], lang[0], typ[0], visibility[0], time_now)))[2:6]