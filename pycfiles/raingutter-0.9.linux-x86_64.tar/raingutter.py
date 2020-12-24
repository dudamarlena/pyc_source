# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/raingutter.py
# Compiled at: 2013-12-10 16:35:34
"""
This is the raingutter database diff and sync tool.  It can handle
general MySQL databases, but is particularly designed to handle
getting data into and out of Drupal 7 databases.
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from pprint import pprint as pp
import sys, operator, collections, socket, logging, logging.handlers, copy, time
try:
    import phpserialize
except ImportError:
    pass

sys.path.insert(0, '/home/dmalament')
import nori
T_NAME_IDX = 0
T_MULTIPLE_IDX = 1
T_S_QUERY_FUNC_IDX = 2
T_S_QUERY_ARGS_IDX = 3
T_TO_D_FUNC_IDX = 4
T_S_CHANGE_FUNC_IDX = 5
T_D_QUERY_FUNC_IDX = 6
T_D_QUERY_ARGS_IDX = 7
T_TO_S_FUNC_IDX = 8
T_D_CHANGE_FUNC_IDX = 9
T_KEY_MODE_IDX = 10
T_KEY_LIST_IDX = 11
T_IDX_COUNT = 12
nori.core.task_article = 'a'
nori.core.task_name = 'database diff/sync'
nori.core.tasks_name = 'database diffs/syncs'
nori.core.license_str = '\nExcept as otherwise noted in the source code:\n\nCopyright 2013 Daniel Malament.  All rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n\n1. Redistributions of source code must retain the above copyright notice,\n   this list of conditions and the following disclaimer.\n\n2. Redistributions in binary form must reproduce the above copyright notice,\n   this list of conditions and the following disclaimer in the documentation\n   and/or other materials provided with the distribution.\n\nTHIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY EXPRESS\nOR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES\nOF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN\nNO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,\nINCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\nLIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,\nOR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF\nLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING\nNEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,\nEVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
nori.core.exitvals['drupal'] = dict(num=40, descr='\nProblem with a Drupal database.\n')
s_drupal_readonly = None
d_drupal_readonly = None
diff_dict = collections.OrderedDict()
sourcedb = nori.MySQL('sourcedb')
destdb = nori.MySQL('destdb')
email_reporter = None
sourcedb.create_settings(heading='Source Database')
nori.core.config_settings['sourcedb_type'] = dict(descr="\nThe database's type ('generic' or 'drupal').\n", default='generic', cl_coercer=str)
destdb.create_settings(heading='Destination Database')
nori.core.config_settings['destdb_type'] = dict(descr="\nThe database's type ('generic' or 'drupal').\n", default='generic', cl_coercer=str)
nori.core.config_settings['diffsync_heading'] = dict(heading='Diff / Sync')
nori.core.config_settings['action'] = dict(descr="\nJust find differences between the databases, or actually change them?\n\nMust be either 'diff' or 'sync'.\n", default='diff', cl_coercer=str)
nori.core.config_settings['reverse'] = dict(descr='\nReverse the source and destination databases for diffs/syncs?\n\nCan be True or False.\n', default='False', cl_coercer=nori.str_to_bool)
nori.core.config_settings['bidir'] = dict(descr="\nCheck for entries which are present in the destination database but not in\nthe source database?\n\n(The other way around will always be checked.  'Source' and 'destination'\nare after taking the value of the 'reverse' setting into account.  This only\nchecks for missing entries; it does not add them to the source database.)\n\nCan be True or False.\n", default='True', cl_coercer=nori.str_to_bool)
nori.core.config_settings['pre_action_callback'] = dict(descr="\nA function to call before performing any database actions, or None.\n\nThis is intended for things like putting a web site into maintenance mode to\nprevent database changes while the script is active.\n\nThe callback function must take these keyword arguments in addition to any\nother *args and **kwargs:\n    s_db: the source-database connection object to use\n    s_cur: the source-database cursor object to use\n    d_db: the destination-database connection object to use\n    d_cur: the destination-database cursor object to use\nNote that 'source' and 'destination' here are subject to the value of the\n'reverse' setting.\n\nIf this setting is not None, the function is called once, right before the\ndiff / sync is started.\n", default=None)
nori.core.config_settings['pre_action_callback_args'] = dict(descr='\nThe arguments for the pre-action callback.\n\nMust be a tuple of (*args, **kwargs).\n\nIgnored if pre_action_callback is None.\n', default=([], {}))
nori.core.config_settings['post_action_callback'] = dict(descr="\nA function to call (once) after performing all database actions, or None.\n\nThis is separate from the change callbacks (see below), and is intended for\nthings like taking a web site out of maintenance mode (see\npre_action_callback, above)\n\nThe callback function must take these keyword arguments in addition to any\nother *args and **kwargs:\n    s_db: the source-database connection object to use\n    s_cur: the source-database cursor object to use\n    d_db: the destination-database connection object to use\n    d_cur: the destination-database cursor object to use\nNote that 'source' and 'destination' here are subject to the value of the\n'reverse' setting.\n\nIf this setting is not None, the function is called once, right after the\ndiff / sync is finished.\n", default=None)
nori.core.config_settings['post_action_callback_args'] = dict(descr='\nThe arguments for the post-action callback.\n\nMust be a tuple of (*args, **kwargs).\n\nIgnored if post_action_callback is None.\n', default=([], {}))
nori.core.config_settings['templates'] = dict(descr="\nThe templates for comparing / syncing the databases.\n\nThis must be a sequence of sequences; the inner sequences must have these\nelements:\n    * template name [string]\n    * does this template apply to multiple rows per key? [boolean]\n    * source-DB query function [function]\n    * source-DB query function arguments [tuple: (*args, **kwargs)]\n    * to-dest transform function [function]\n    * source-DB change callback function [function]\n    * dest-DB query function [function]\n    * dest-DB query function arguments [tuple: (*args, **kwargs)]\n    * to-source transform function [function]\n    * dest-DB change callback function [function]\n    * key mode [string]\n    * key list [list]\n\nIn this context, 'keys' are identifiers for use in accessing the correct\nentity in the opposite database, and 'values' are the actual content to\ndiff or sync.  Only one of the change callback functions is used (which one\ndepends on the 'reverse' setting), but both must be present regardless; use\nNone where appropriate.\n\nFunctions may be specified as None to use defaults appropriate to the given\ndatabase type.\n\nThe template name should be unique across all templates, although this is\nnot enforced (template indexes are provided for disambiguation).  It is\nrecommended not to include spaces in the names, for easier specification on\nthe command line.\n\nIf the multiple-rows-per-key flag is true, matching works differently.\nInstead of rows with the same keys matching, and their values being\ncompared, rows only match if both the keys and the values are the same.\n\nThis means that if there is no match for a row, it can either be because\nthere is no key match at all, or no key-and-value match.  If a value is\nchanged in one database, it will usually show up as the latter case; the\nscript will see this as one non-matching row on each side.  The script\nwill attempt to add the source row to the destination database, but it\nwill not delete anything from the destination database; this must be\ndone by other means.\n\nThe DB query functions must take these keyword arguments in addition to any\nother *args and **kwargs:\n    db_obj: the database connection object to use\n    db_cur: the database cursor object to use\n    mode: 'read', 'update', or 'insert'\n    key_cv: a sequence of 2- or 3-tuples indicating the names of the\n            'key' columns, the data types of the columns, and the values\n            to require for the columns (the data types are passed to the\n            appropriate transform function (see below); the values are\n            optional in 'read' mode)\n    value_cv: similar to key_cv, but for the 'value' columns; the third\n              elements of the tuples are only used in the 'update' and\n              'insert' modes\nNote that the format of the column names may differ between the two\ndatabases, and the values may also require transformation (see below).\nWhat matters is that the sets of key and value columns for each database\ncorrespond to each other and are the same length (after the transform\nfunctions have been applied).\n\nIMPORTANT: currently, key columns must be unique in each database or\nelse Bad Things will happen in the destination database.  In SQL, this\ncan be enforced with a unique index or primary key.  In Drupal, nodes\nmust have unique titles, field collections must have unique labels\nwithin nodes, and relations must have unique endpoint pairs.  For nodes,\nuse the Uniqueness and/or Unique Field modules.  For field collections,\nit is suggested to use the Automatic Entity Labels module to create\nlabels based on node titles.  For relations, there is a setting under\n'Advanced Options'.  If non-unique values are absolutely required in\nparticular nodes/relations/etc., one approach is to put those cases in a\nkey list using a key mode of 'exclude' (see below).  However, this will\nnot prevent problems if a new case is added to the source database\nwithout being added to the key list.\n\nAs described above, key_cv and value_cv contain strings referring to data\ntypes; particular data types that can/should be supported include:\n    'string'\n    'integer'\n    'decimal'\n    'term: VOCABULARY_NAME'\n    'id' [e.g., node ID or field collection item ID]\n    'ip' [IP address; stored as a number, displayed as an address]\nSome of these are Drupal-specific; in particular, the 'term' type is for\nDrupal taxonomy term references, and includes the name of the relevant\nvocabulary.  Currently, these strings are only used by (passed to) the\ntransform functions, with the exception of Drupal taxonomy term\nreferences.\n\nIn 'read' mode, the query functions must return None on failure, or a\ncomplete result set on success.  The result set must be a sequence (possibly\nempty) of row tuples, each of which contains both the 'key' and 'value'\nresults.  If the multi-row boolean is true, rows for the same keys must be\nretrieved in sequence (i.e., two rows for the same keys may not be separated\nby a row for different keys; this typically requires an ORDER BY clause in\nSQL).\n\nIn 'update' and 'insert' modes, the query functions must return a tuple of\n(number_of_full_successes, number of partial_successes, number_of_failures).\n(They will generally have to loop over the value_cv columns rather than\ndoing them all at once.)\n\nThe transform functions, if not None, must take the following parameters:\n    template: the complete template entry for this data\n    row: a single row tuple from the results returned by the query function\n         (see above)\nand must return a tuple of (number_of_key_columns, data_row).  The row must\nbe in the same format as the input, containing values suitable for\ncomparison with or insertion into the opposite database.  In many cases,\nthis will require no actual transformation, as the database connector will\nhandle data-type conversion on both ends.\n\nBoth transform functions will be called before comparing data, so be sure\nthat they both output the data in the same format.  This format must also\nmatch the keys specified in the per-template and global key lists.\n\nThe change callback functions must be either None, or else functions to call\nif this template has caused any changes in the database for a given row.\nThis is particularly important for emulating computed fields in a Drupal\ndatabase.  Change callbacks must accept the following:\n    db_obj: the database connection object to use\n    db_cur: the database cursor object to use\n    template: the complete template entry for this data\n    row: a (num_keys, data_tuple) tuple, as returned by the transform\n         functions (see above)\nand return True (success) or False (failure).\n\nThe key mode specifies which database entries to compare / sync; it may be\n'all', 'include', or 'exclude'.  For 'include' and 'exclude', the key list\nmust contain the list of keys to include / exclude; for 'all', the key list\nmust exist, but is ignored (you can use None).\n\nThe checks are made after the appropriate transform functions are applied\n(see above).\n\nIf there is a conflict between this setting and the global key mode setting\nin which one excludes an entry and the other includes it, the entry is\nexcluded.\n\nKey list entries may be tuples if there are multiple key columns in the\ndatabase queries.\n\nThe entries in the key list will be compared with the key columns of each\ndata row beginning at the first column, after applying the transform\nfunction.  It is an error for a row to have fewer key columns than are in\nthe key list, but if a row has more key columns, columns which have no\ncorresponding entry in the key list will be ignored for purposes of the\ncomparison.\n", default=[])
nori.core.config_settings['template_mode'] = dict(descr="\nWhich templates to actually apply.\n\nMay be 'all', 'include', or 'exclude'.  For 'include' and 'exclude',\ntemplate_list must contain the list of templates to include / exclude.\n", default='all', cl_coercer=str)
nori.core.config_settings['template_list'] = dict(descr="\nThe list of templates; see template_mode.\n\nIgnored if template_mode is 'all'.\n", default=[], cl_coercer=lambda x: x.split(','))
nori.core.config_settings['key_mode'] = dict(descr="\nWhich database entries to compare / sync.\n\nMay be 'all', 'include', or 'exclude'.  For 'include' and 'exclude',\nkey_list must contain the list of keys to include / exclude.\n\nThe checks are made after the appropriate transform functions are applied\n(see the templates setting, above).\n\nThis is separate from the per-template setting (see above), and is only\nuseful if all templates share a common prefix of key columns.  (That is, the\nentries in the key list (below) will be compared with the key columns of\neach data row beginning at the first column, after applying the transform\nfunction (see above).  It is an error for a row to have fewer key columns\nthan are in the key list, but if a row has more key columns, columns which\nhave no corresponding entry in the key list will be ignored for purposes of\nthe comparison.)\n\nIf there is a conflict between this setting and the per-template key mode\nsetting in which one excludes an entry and the other includes it, the entry\nis excluded.\n", default='all', cl_coercer=str)
nori.core.config_settings['key_list'] = dict(descr="\nThe list of keys; see key_mode.\n\nEntries may be tuples in the case of multi-valued keys.\n\nIgnored if key_mode is 'all'.\n", default=[], cl_coercer=lambda x: x.split(','))
nori.core.config_settings['sourcedb_change_callback'] = dict(descr='\nA function to call if the source database was changed, or None.\n\nThis is separate from the per-template functions (see above), and is\nintended for overall cleanup.  In particular, it is useful for clearing\nDrupal caches.\n\nThe callback function must take these keyword arguments in addition to any\nother *args and **kwargs:\n    db_obj: the database connection object to use\n    db_cur: the database cursor object to use\n\nCalled at most once, after the sync is complete.\n', default=None)
nori.core.config_settings['sourcedb_change_callback_args'] = dict(descr='\nThe arguments for the source-DB change callback.\n\nMust be a tuple of (*args, **kwargs).\n\nIgnored if source_db_change_callback is None.\n', default=([], {}))
nori.core.config_settings['destdb_change_callback'] = dict(descr='\nA function to call if the destination database was changed, or None.\n\nThis is separate from the per-template functions (see above), and is\nintended for overall cleanup.  In particular, it is useful for clearing\nDrupal caches.\n\nThe callback function must take these keyword arguments in addition to any\nother *args and **kwargs:\n    db_obj: the database connection object to use\n    db_cur: the database cursor object to use\n\nCalled at most once, after the sync is complete.\n', default=None)
nori.core.config_settings['destdb_change_callback_args'] = dict(descr='\nThe arguments for the destination-DB change callback.\n\nMust be a tuple of (*args, **kwargs).\n\nIgnored if source_db_change_callback is None.\n', default=([], {}))
nori.core.config_settings['reporting_heading'] = dict(heading='Reporting')
nori.core.config_settings['report_order'] = dict(descr="\nReport diff / sync results grouped by template entry ('template') or\ndatabase keys ('keys')?\n", default='template', cl_coercer=str)
nori.core.config_settings['send_report_emails'] = dict(descr='\nSend reports on diffs / syncs by email?  (True/False)\n', default=True, cl_coercer=nori.str_to_bool)
nori.core.config_settings['report_emails_from'] = dict(descr='\nAddress to send report emails from.\n\nIgnored if send_report_emails is False.\n', default=nori.core.running_as_email, default_descr='\nthe local email address of the user running the script\n(i.e., [user]@[hostname], where [user] is the current user and [hostname]\nis the local hostname)\n', cl_coercer=str)
nori.core.config_settings['report_emails_to'] = dict(descr='\nWhere to send report emails.\n\nThis must be a list of strings (even if there is only one address).\n\nIgnored if send_report_emails is False.\n', default=[
 nori.core.running_as_email], default_descr='\na list containing the local email address of the user running\nthe script (i.e., [user]@[hostname], where [user] is the current user\nand [hostname] is the local hostname)\n', cl_coercer=lambda x: x.split(','))
nori.core.config_settings['report_emails_subject'] = dict(descr='\nThe subject line of the report emails.\n\nIgnored if send_report_emails is False.\n', default=nori.core.script_shortname + ' report on ' + socket.getfqdn(), default_descr=("\n'{0} report on [hostname]', where [hostname] is the local\nhostname\n").format(nori.core.script_shortname), cl_coercer=str)
nori.core.config_settings['report_emails_host'] = dict(descr='\nThe SMTP server via which report emails will be sent.\n\nThis can be a string containing the hostname, or a tuple of the\nhostname and the port number.\n\nIgnored if send_report_emails is False.\n', default='localhost')
nori.core.config_settings['report_emails_cred'] = dict(descr='\nThe credentials to be used with the report_emails_host.\n\nThis can be None or a tuple containing the username and password.\n\nIgnored if send_report_emails is False.\n', default=None)
nori.core.config_settings['report_emails_sec'] = dict(descr='\nThe SSL/TLS options to be used with the report_emails_host.\n\nThis can be None, () for plain SSL/TLS, a tuple containing only\nthe path to a key file, or a tuple containing the paths to the key\nand certificate files.\n\nIgnored if send_report_emails is False.\n', default=None)

def validate_generic_chain(key_index, key_cv, value_index, value_cv):
    """
    Validate a generic key_cv/value_cv chain.
    Parameters:
        key_index: the index tuple of the key_cv dict in the
                   templates setting
        key_cv: the actual key_cv dict
        value_index: the index tuple of the value_cv dict in the
                     templates setting
        value_cv: the actual value_cv dict
    Dependencies:
        config settings: templates
        modules: nori
    """
    for index, cv in [(key_index, key_cv), (value_index, value_cv)]:
        nori.setting_check_not_empty(index)
        for i, col in enumerate(cv):
            nori.setting_check_type(index + (i,), nori.core.CONTAINER_TYPES)
            nori.setting_check_len(index + (i,), 2, 3)
            nori.setting_check_not_blank(index + (i, 0))
            nori.setting_check_not_blank(index + (i, 1))


def validate_drupal_cv(cv_index, cv, kv):
    """
    Validate a single Drupal key_cv/value_cv entry.

    Parameters:
        cv_index: the index tuple of the entry in the templates setting
        cv: the entry itself
        kv: 'k' if this is entry is part of a key_cv sequence, or 'v' if
            it's part of a value_cv sequence

    Dependencies:
        config settings: templates
        modules: nori

    """
    ident_index = cv_index + (0, )
    ident = cv[0]
    data_type_index = cv_index + (1, )
    data_type = cv[1]
    nori.setting_check_type(cv_index, nori.core.CONTAINER_TYPES)
    nori.setting_check_len(cv_index, 2, 3)
    nori.setting_check_not_empty(ident_index)
    nori.setting_check_list(ident_index + (0, ), [
     'node', 'fc', 'relation', 'field', 'title', 'label'])
    if ident[0] == 'node':
        nori.setting_check_len(ident_index, 3, 3)
        if kv == 'k':
            nori.setting_check_type(ident_index + (1, ), nori.core.STRING_TYPES)
        else:
            nori.setting_check_type(ident_index + (1, ), nori.core.STRING_TYPES + (nori.core.NONE_TYPE,))
        nori.setting_check_list(ident_index + (2, ), ['id', 'title'])
    elif ident[0] == 'fc':
        nori.setting_check_len(ident_index, 3, 3)
        nori.setting_check_not_blank(ident_index + (1, ))
        nori.setting_check_list(ident_index + (2, ), ['id', 'label'])
    elif ident[0] == 'relation':
        nori.setting_check_len(ident_index, 2, 2)
        nori.setting_check_not_blank(ident_index + (1, ))
    elif ident[0] == 'field':
        nori.setting_check_len(ident_index, 2, 2)
        nori.setting_check_not_blank(ident_index + (1, ))
    elif ident[0] == 'title':
        nori.setting_check_len(ident_index, 1, 1)
    elif ident[0] == 'label':
        nori.setting_check_len(ident_index, 1, 1)
    if ident[0] != 'relation':
        nori.setting_check_not_blank(data_type_index)


def get_drupal_chain_type(key_cv=None, value_cv=None, key_entities=None, value_entities=None):
    """
    Identify the type of a Drupal key/value chain.

    If the entities parameters are supplied, the cv parameters are
    ignored.  At least one set of parameters must be supplied.

    Parameters:
        key_cv: the key_cv to examine, from the template
        value_cv: the value_cv to examine, from the template
        key_entities: a list of the identifier types from the key_cv
                      (e.g. 'node')
        value_entities: a list of the identifier types from the value_cv
                        (e.g. 'field')

    """
    if key_entities is None:
        key_entities = []
        for i, cv in enumerate(key_cv):
            key_entities.append(key_cv[i][0][0])

    if value_entities is None:
        value_entities = []
        for i, cv in enumerate(value_cv):
            value_entities.append(value_cv[i][0][0])

    if len(key_entities) == 1 and key_entities[0] == 'node' and False not in [ entity == 'field' for entity in value_entities ]:
        return 'n-f'
    else:
        if len(key_entities) == 2 and key_entities[0] == 'node' and key_entities[1] == 'relation' and len(value_entities) == 1 and value_entities[0] == 'node':
            return 'n-r-n'
        if len(key_entities) == 3 and key_entities[0] == 'node' and key_entities[1] == 'relation' and key_entities[2] == 'node' and False not in [ entity == 'field' for entity in value_entities ]:
            return 'n-rn-rf'
        if len(key_entities) == 2 and key_entities[0] == 'node' and key_entities[1] == 'fc' and False not in [ entity == 'field' for entity in value_entities ]:
            return 'n-fc-f'
        return


def validate_drupal_chain(key_index, key_cv, value_index, value_cv):
    """
    Validate a Drupal key_cv/value_cv chain.

    Parameters:
        key_index: the index tuple of the key_cv dict in the
                   templates setting
        key_cv: the actual key_cv dict
        value_index: the index tuple of the value_cv dict in the
                     templates setting
        value_cv: the actual value_cv dict

    Dependencies:
        config settings: templates
        functions: validate_drupal_cv(), get_drupal_chain_type()
        modules: nori

    """
    nori.setting_check_not_empty(key_index)
    key_entities = []
    for i, cv in enumerate(key_cv):
        validate_drupal_cv(key_index + (i,), cv[i], 'k')
        key_entities.append(key_cv[i][0][0])

    nori.setting_check_not_empty(value_index)
    value_entities = []
    for i, cv in enumerate(value_cv):
        validate_drupal_cv(value_index + (i,), cv[i], 'v')
        value_entities.append(value_cv[i][0][0])

    if not get_drupal_chain_type(None, None, key_entities, value_entities):
        nori.err_exit(('Error: the key_cv / value_cv chain in {0} is not\none of the currently allowed types; exiting.').format(nori.setting_walk(key_index[0:-1])[2]), nori.core.exitvals['startup']['num'])
    return


def validate_config():
    """
    Validate diff/sync and reporting config settings.

    Dependencies:
        config settings: action, reverse, bidir, templates,
                         template_mode, template_list, key_mode,
                         key_list, sourcedb_change_callback,
                         sourcedb_change_callback_args,
                         destdb_change_callback,
                         destdb_change_callback_args, report_order,
                         send_report_emails, report_emails_from,
                         report_emails_to, report_emails_subject,
                         report_emails_host, report_emails_cred,
                         report_emails_sec
        globals: T_*
        modules: nori

    """
    nori.setting_check_list('sourcedb_type', ['generic', 'drupal'])
    nori.setting_check_list('destdb_type', ['generic', 'drupal'])
    nori.setting_check_list('action', ['diff', 'sync'])
    nori.setting_check_type('reverse', bool)
    nori.setting_check_type('bidir', bool)
    nori.setting_check_callable('pre_action_callback', may_be_none=True)
    if nori.core.cfg['pre_action_callback']:
        nori.setting_check_type('pre_action_callback_args', nori.core.CONTAINER_TYPES)
        nori.setting_check_len('pre_action_callback_args', 2, 2)
        nori.setting_check_type(('pre_action_callback_args', 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('pre_action_callback_args', 1), nori.core.MAPPING_TYPES)
    nori.setting_check_callable('post_action_callback', may_be_none=True)
    if nori.core.cfg['post_action_callback']:
        nori.setting_check_type('post_action_callback_args', nori.core.CONTAINER_TYPES)
        nori.setting_check_len('post_action_callback_args', 2, 2)
        nori.setting_check_type(('post_action_callback_args', 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('post_action_callback_args', 1), nori.core.MAPPING_TYPES)
    nori.setting_check_list('template_mode', ['all', 'include', 'exclude'])
    if nori.core.cfg['template_mode'] != 'all':
        nori.setting_check_not_empty('template_list')
        for i, t_name in enumerate(nori.core.cfg['template_list']):
            nori.check_setting_type(('template_list', i), nori.core.STRING_TYPES)

    nori.setting_check_list('key_mode', ['all', 'include', 'exclude'])
    if nori.core.cfg['key_mode'] != 'all':
        nori.setting_check_not_empty('key_list')
    nori.setting_check_callable('sourcedb_change_callback', may_be_none=True)
    if nori.core.cfg['sourcedb_change_callback']:
        nori.setting_check_type('sourcedb_change_callback_args', nori.core.CONTAINER_TYPES)
        nori.setting_check_len('sourcedb_change_callback_args', 2, 2)
        nori.setting_check_type(('sourcedb_change_callback_args', 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('sourcedb_change_callback_args', 1), nori.core.MAPPING_TYPES)
    nori.setting_check_callable('destdb_change_callback', may_be_none=True)
    if nori.core.cfg['destdb_change_callback']:
        nori.setting_check_type('destdb_change_callback_args', nori.core.CONTAINER_TYPES)
        nori.setting_check_len('destdb_change_callback_args', 2, 2)
        nori.setting_check_type(('destdb_change_callback_args', 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('destdb_change_callback_args', 1), nori.core.MAPPING_TYPES)
    nori.setting_check_not_empty('templates')
    for i, template in enumerate(nori.core.cfg['templates']):
        nori.setting_check_type(('templates', i), nori.core.CONTAINER_TYPES)
        nori.setting_check_len(('templates', i), T_IDX_COUNT, T_IDX_COUNT)
        nori.setting_check_type(('templates', i, T_NAME_IDX), nori.core.STRING_TYPES)
        nori.setting_check_type(('templates', i, T_MULTIPLE_IDX), bool)
        nori.setting_check_callable(('templates', i, T_S_QUERY_FUNC_IDX), may_be_none=True)
        nori.setting_check_type(('templates', i, T_S_QUERY_ARGS_IDX), nori.core.CONTAINER_TYPES)
        nori.setting_check_len(('templates', i, T_S_QUERY_ARGS_IDX), 2, 2)
        nori.setting_check_type(('templates', i, T_S_QUERY_ARGS_IDX, 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('templates', i, T_S_QUERY_ARGS_IDX, 1), nori.core.MAPPING_TYPES)
        nori.setting_check_callable(('templates', i, T_TO_D_FUNC_IDX), may_be_none=True)
        nori.setting_check_callable(('templates', i, T_S_CHANGE_FUNC_IDX), may_be_none=True)
        nori.setting_check_callable(('templates', i, T_D_QUERY_FUNC_IDX), may_be_none=True)
        nori.setting_check_type(('templates', i, T_D_QUERY_ARGS_IDX), nori.core.CONTAINER_TYPES)
        nori.setting_check_len(('templates', i, T_D_QUERY_ARGS_IDX), 2, 2)
        nori.setting_check_type(('templates', i, T_D_QUERY_ARGS_IDX, 0), nori.core.CONTAINER_TYPES)
        nori.setting_check_type(('templates', i, T_D_QUERY_ARGS_IDX, 1), nori.core.MAPPING_TYPES)
        nori.setting_check_callable(('templates', i, T_TO_S_FUNC_IDX), may_be_none=True)
        nori.setting_check_callable(('templates', i, T_D_CHANGE_FUNC_IDX), may_be_none=True)
        nori.setting_check_list(('templates', i, T_KEY_MODE_IDX), [
         'all', 'include', 'exclude'])
        if template[T_KEY_MODE_IDX] != 'all':
            nori.setting_check_not_empty(('templates', i, T_KEY_LIST_IDX))
        s_db_type = nori.core.cfg['sourcedb_type']
        s_key_ind = ('templates', i, T_S_QUERY_ARGS_IDX, 1, 'key_cv')
        s_key_cv = template[T_S_QUERY_ARGS_IDX][1]['key_cv']
        s_value_ind = ('templates', i, T_S_QUERY_ARGS_IDX, 1, 'value_cv')
        s_value_cv = template[T_S_QUERY_ARGS_IDX][1]['value_cv']
        if s_db_type == 'generic':
            validate_generic_chain(s_key_ind, s_key_cv, s_value_ind, s_value_cv)
        elif s_db_type == 'drupal':
            validate_drupal_chain(s_key_ind, s_key_cv, s_value_ind, s_value_cv)
        d_db_type = nori.core.cfg['destdb_type']
        d_key_ind = ('templates', i, T_D_QUERY_ARGS_IDX, 1, 'key_cv')
        d_key_cv = template[T_D_QUERY_ARGS_IDX][1]['key_cv']
        d_value_ind = ('templates', i, T_D_QUERY_ARGS_IDX, 1, 'value_cv')
        d_value_cv = template[T_D_QUERY_ARGS_IDX][1]['value_cv']
        if d_db_type == 'generic':
            validate_generic_chain(d_key_ind, d_key_cv, d_value_ind, d_value_cv)
        elif d_db_type == 'drupal':
            validate_drupal_chain(d_key_ind, d_key_cv, d_value_ind, d_value_cv)

    nori.setting_check_list('report_order', ['template', 'keys'])
    nori.setting_check_type('send_report_emails', bool)
    if nori.core.cfg['send_report_emails']:
        nori.setting_check_not_blank('report_emails_from')
        nori.setting_check_type('report_emails_to', list)
        nori.setting_check_no_blanks('report_emails_to')
        nori.setting_check_type('report_emails_subject', nori.core.STRING_TYPES)
        if nori.setting_check_type('report_emails_host', nori.core.STRING_TYPES + (tuple,)) == tuple:
            nori.setting_check_len('report_emails_host', 2, 2)
            nori.setting_check_not_blank(('report_emails_host', 0))
            nori.setting_check_num(('report_emails_host', 1), 1, 65535)
        else:
            nori.setting_check_not_blank('report_emails_host')
        if nori.setting_check_type('report_emails_cred', (nori.core.NONE_TYPE, tuple)) is not nori.core.NONE_TYPE:
            nori.setting_check_len('report_emails_cred', 2, 2)
            nori.setting_check_no_blanks('report_emails_cred')
        if nori.setting_check_type('report_emails_sec', (nori.core.NONE_TYPE, tuple)) is not nori.core.NONE_TYPE:
            nori.setting_check_len('report_emails_sec', 0, 2)
            for i, f in enumerate(nori.core.cfg['report_emails_sec']):
                nori.setting_check_file_read(('report_emails_sec', i))


class SMTPReportHandler(logging.handlers.SMTPHandler):
    """Override SMTPHandler to add diagnostics to the email."""

    def emit(self, record):
        """
        Add diagnostics to the message, and log that an email was sent.
        Dependencies:
            config settings: report_emails_to
            modules: copy, nori
        """
        r = copy.copy(record)
        if r.msg[(-1)] != '\n':
            r.msg += '\n'
        r.msg += nori.email_diagnostics()
        super(SMTPReportHandler, self).emit(r)
        nori.core.status_logger.info(('Report email sent to {0}.').format(nori.core.cfg['report_emails_to']))


def init_reporting():
    """
    Dependencies:
        config settings: send_report_emails, report_emails_host,
                         report_emails_from, report_emails_to,
                         report_emails_subject, report_emails_cred,
                         report_emails_sec
        globals: email_reporter
        classes: SMTPReportHandler
        modules: logging, nori
    """
    global email_reporter
    if nori.core.cfg['send_report_emails']:
        email_reporter = logging.getLogger(__name__ + '.reportemail')
        email_reporter.propagate = False
        email_handler = SMTPReportHandler(nori.core.cfg['report_emails_host'], nori.core.cfg['report_emails_from'], nori.core.cfg['report_emails_to'], nori.core.cfg['report_emails_subject'], nori.core.cfg['report_emails_cred'], nori.core.cfg['report_emails_sec'])
        email_reporter.addHandler(email_handler)


def generic_db_query(db_obj, db_cur, mode, tables, key_cv, value_cv, where_str=None, more_str=None, more_args=[], no_replicate=False):
    """
    Generic 'DB query function' for use in templates.

    See the description of the 'templates' config setting.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        mode: 'read', 'update', or 'insert'
        tables: either a sequence of table names, which will be joined
                with commas (INNER JOIN), or a string which will be used
                as the FROM clause of the query (don't include the FROM
                keyword)
        key_cv: a sequence of 2- or 3-tuples indicating the names of the
                'key' columns, strings representing their data types,
                and (optionally) values to require for them (in the
                WHERE clause)
                    * the data types are passed to the appropriate
                      transform function; see the description of the
                      'templates' config setting, above
                    * a value of None indicates a SQL NULL
        value_cv: same as key_cv, but for the 'value' columns; the
                  third elements of the tuples are only used in 'update'
                  mode
        where_str: if not None, a string to include in the WHERE clause
                   of the query (don't include the WHERE keyword)
        more_str: if not None, a string to add to the query; useful for
                  ORDER and GROUP BY clauses
        more_args: a list of values to supply along with the database
                   query for interpolation into the query string; only
                   needed if there are placeholders in more_str
        no_replicate: if True, attempt to turn off replication during
                      the query; failure will cause a warning, but won't
                      prevent the query from proceeding

    Dependencies:
        functions: generic_db_read(), generic_db_update(),
                   generic_db_insert()
        modules: sys, nori

    """
    if mode != 'read' and mode != 'update' and mode != 'insert':
        nori.core.email_logger.error(('Internal Error: invalid mode supplied in call to generic_db_query();\ncall was (in expanded notation):\n\ngeneric_db_query(db_obj={0},\n                 db_cur={1},\n                 mode={2},\n                 tables={3},\n                 key_cv={4},\n                 value_cv={5},\n                 where_str={6},\n                 more_str={7},\n                 more_args={8},\n                 no_replicate={9})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, mode, tables, key_cv,
         value_cv, where_str, more_str, more_args,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    if mode == 'read':
        return generic_db_read(db_obj, db_cur, tables, key_cv, value_cv, where_str, more_str, more_args)
    if mode == 'update':
        successes = 0
        failures = 0
        for i, cv in enumerate(value_cv):
            up_ret = generic_db_update(db_obj, db_cur, tables, key_cv, [
             value_cv[i]], where_str, no_replicate)
            if not up_ret:
                failures += 1
            elif db_cur.rowcount == 0:
                in_ret = generic_db_insert(db_obj, db_cur, tables, key_cv, [
                 value_cv[i]], where_str, no_replicate)
                if not in_ret:
                    failures += 1
                else:
                    successes += 1
            else:
                successes += 1

        return (
         successes, 0, failures)
    if mode == 'insert':
        successes = 0
        failures = 0
        for i, cv in enumerate(value_cv):
            in_ret = generic_db_insert(db_obj, db_cur, tables, key_cv, [
             value_cv[i]], where_str, no_replicate)
            if not in_ret:
                failures += 1
            else:
                successes += 1

        return (
         successes, 0, failures)


def generic_db_read(db_obj, db_cur, tables, key_cv, value_cv, where_str=None, more_str=None, more_args=[]):
    """
    Do the actual work for generic DB reads.

    Parameters:
        see generic_db_query()

    Dependencies:
        modules: operator, nori

    """
    query_args = []
    query_str = 'SELECT '
    query_str += (', ').join(map(operator.itemgetter(0), key_cv + value_cv))
    query_str += '\n'
    query_str += 'FROM '
    if isinstance(tables, nori.core.CONTAINER_TYPES):
        query_str += (', ').join(tables)
    else:
        query_str += tables
    query_str += '\n'
    where_parts = []
    if where_str:
        where_parts.append('(' + where_str + ')')
    for cv in key_cv:
        if len(cv) > 2:
            where_parts.append(('({0} = %s)').format(cv[0]))
            query_args.append(cv[2])

    if where_parts:
        query_str += 'WHERE ' + ('\nAND\n').join(where_parts) + '\n'
    if more_str:
        query_str += more_str
        query_args += more_args
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        return ret[1]


def generic_db_update(db_obj, db_cur, tables, key_cv, value_cv, where_str=None, no_replicate=False):
    """
    Do the actual work for generic DB updates.

    The value_cv sequence may only have one element.

    Parameters:
        see generic_db_query()

    Dependencies:
        modules: sys, nori

    """
    if len(value_cv) != 1:
        nori.core.email_logger.error(('Internal Error: multiple value_cv entries supplied in call to\ngeneric_db_update(); call was (in expanded notation):\n\ngeneric_db_update(db_obj={0},\n                 db_cur={1},\n                 tables={2},\n                 key_cv={3},\n                 value_cv={4},\n                 where_str={5},\n                 no_replicate={6})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, tables, key_cv, value_cv,
         where_str, no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    query_args = []
    query_str = 'UPDATE '
    if isinstance(tables, nori.core.CONTAINER_TYPES):
        query_str += (', ').join(tables)
    else:
        query_str += tables
    query_str += '\n'
    query_str += ('SET {0} = %s').format(value_cv[0][0]) + '\n'
    query_args.append(value_cv[0][2])
    where_parts = []
    if where_str:
        where_parts.append('(' + where_str + ')')
    for cv in key_cv:
        if len(cv) > 2:
            where_parts.append(('({0} = %s)').format(cv[0]))
            query_args.append(cv[2])

    query_str += 'WHERE ' + ('\nAND\n').join(where_parts) + '\n'
    return db_obj.execute(db_cur, query_str.split(), query_args, has_results=False)


def generic_db_insert(db_obj, db_cur, tables, key_cv, value_cv, where_str=None, no_replicate=False):
    """
    Do the actual work for generic DB inserts.

    The value_cv sequence may only have one element.

    Parameters:
        see generic_db_query()

    Dependencies:
        modules: sys, nori

    """
    if len(value_cv) != 1:
        nori.core.email_logger.error(('Internal Error: multiple value_cv entries supplied in call to\ngeneric_db_update(); call was (in expanded notation):\n\ngeneric_db_update(db_obj={0},\n                 db_cur={1},\n                 tables={2},\n                 key_cv={3},\n                 value_cv={4},\n                 where_str={5},\n                 no_replicate={6})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, tables, key_cv, value_cv,
         where_str, no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    query_args = []
    query_str = 'INSERT INTO '
    return db_obj.execute(db_cur, query_str.split(), query_args, has_results=False)


def drupal_db_query(db_obj, db_cur, mode, key_cv, value_cv, no_replicate=False):
    """
    Drupal 'DB query function' for use in templates.

    See the description of the 'templates' config setting.

    For Drupal, the key_cv and value_cv formats are far more
    complicated than for a generic DB; we need to support nodes, field
    collections, and relations, all connected in complex ways.

    Specifically, the design goal is to be able to handle the following
    cases:
        node -> field(s) (including term references)
        node -> relation -> node
        node -> relation & node -> relation_field(s) (incl. term refs)
        node -> fc -> field(s) (including term references)

    These cases aren't supported - _yet_:
        node -> fc -> fc -> field(s)
        node -> fc -> relation & node -> relation_field(s)
        node -> fc -> fc -> relation & node -> relation_field(s)
        node -> fc -> relation -> node
        node -> fc -> fc -> relation -> node
        node -> relation -> [node -> fc]
        node -> fc -> relation -> [node -> fc]
        node -> fc -> fc -> relation -> [node -> fc]
        anything with relations of arity != 2
        specifying nodes and FCs by field values
        anything with node titles or field labels as targets
        etc.

    Data identifiers (the equivalent of column names) and their
    associated values are specified as follows:
        * key_cv and value_cv are sequences ('cv' means
          'columns/values')
        * each step in the chains listed above is a tuple inside one of
          these sequences; the last step goes in value_cv, the rest in
          key_cv
        * the first identifier in key_cv must be a node
        * value_cv may not contain field collections or relations (yet)
          and may only contain nodes if the last tuple in key_cv is a
          relation
        * there may be multiple identifiers in value_cv only if they
          all refer to items which are in the same container (i.e.,
          node, field collection, or relation)
        * the tuples in key_cv and value_cv contain two or three
          elements: the identifier, a string representing the relevant
          data type, and (if present) the associated value
          (the data type is passed to the relevant transform function;
          see the description of the 'templates' config setting, above)
        * the identifiers are themselves tuples conforming to one of
          the following:
              * for nodes: ('node', content_type, ID_type)
                    * content_type is required for 'key' data, but
                      optional for 'value' data; specify None to omit it
                      in the latter case
                    * ID_type:
                          * can be:
                                * 'id' for the node ID number
                                * 'title' for the title field
                          * refers both to the node's 'value' (if
                            supplied) and to the way node 'values' are
                            retrieved from the database
                          * is required whether or not the node's
                            'value' is supplied
              * for field collections: ('fc', fc_type, ID_type)
                    * fc_type is the name of the field in the node which
                      contains the field collection itself
                    * ID_type:
                          * can be:
                                * 'id' for the FC item ID number
                                * 'label' for the label field
                          * refers both to the FC's 'value' (if
                            supplied) and to the way FC 'values' are
                            retrieved from the database
                          * is required whether or not the FC's 'value'
                            is supplied
              * for relations: ('relation', relation_type)
                    * note that supplying a value for a relation is not
                      supported
                    * therefore, the data type is optional and ignored
                    * however, remember that the overall key_cv entry
                      must be a tuple: (('relation', relation_type), )
              * for fields: ('field', field_name)
              * for title fields (in case the title of a node is also a
                'value' entry that must be changed): ('title',)
                [a 1-tuple]
              * for label fields (in case the label of a field
                collection is also a 'value' entry that must be
                changed): ('label',) [a 1-tuple]

    For example:
        key_cv = [
            (
                ('node', 'server', 'title'),
                'string',
                'host.name.com'
            ),
            (
                ('fc', 'dimm', 'label'),
                'string',
                'host.name.com-slot 1'
            ),
        ]
        value_cv = [
            (('field', 'size'), 'decimal', 4.000),
        ]

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        mode: 'read', 'update', or 'insert'
        key_cv: a sequence of 2- or 3-tuples indicating the names of the
                'key' fields, their associated data types, and
                (optionally) values to require for them (see above)
        value_cv: same as key_cv, but for the 'value' fields (see
                  above); the third elements of the tuples are only used
                  in 'update' mode
        no_replicate: if True, attempt to turn off replication during
                      the query; failure will cause a warning, but won't
                      prevent the query from proceeding

    Dependencies:
        functions: drupal_db_read(), drupal_db_update()
        modules: sys, nori

    """
    if mode != 'read' and mode != 'update' and mode != 'insert':
        nori.core.email_logger.error(('Internal Error: invalid mode supplied in call to\ndrupal_db_query(); call was (in expanded notation):\n\ndrupal_db_query(db_obj={0},\n                db_cur={1},\n                mode={2},\n                key_cv={3},\n                value_cv={4},\n                no_replicate={5})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, mode, key_cv, value_cv,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    if mode == 'read':
        return drupal_db_read(db_obj, db_cur, key_cv, value_cv)
    else:
        if mode == 'update':
            successes = 0
            failures = 0
            for i, cv in enumerate(value_cv):
                up_ret = drupal_db_update(db_obj, db_cur, key_cv, [value_cv[i]], no_replicate)
                if not up_ret:
                    failures += 1
                elif db_cur.rowcount == 0:
                    in_ret = drupal_db_insert(db_obj, db_cur, key_cv, [
                     value_cv[i]], no_replicate)
                    if not in_ret:
                        failures += 1
                    else:
                        successes += 1
                else:
                    successes += 1

            return (
             successes, 0, failures)
        if mode == 'insert':
            fulls = 0
            partials = 0
            failures = 0
            for i, cv in enumerate(value_cv):
                in_ret = drupal_db_insert(db_obj, db_cur, key_cv, [value_cv[i]], no_replicate)
                if in_ret is None:
                    failures += 1
                elif not in_ret:
                    nori.core.email_logger.error(('Warning: insert was only partially successful; manual intervention is\nprobably required.\n    key_cv: {0}\n    value_cv: {1}').format(*map(nori.pps, [key_cv, value_cv])))
                    partials += 1
                else:
                    fulls += 1

            return (
             fulls, partials, failures)
        return


def drupal_db_read(db_obj, db_cur, key_cv, value_cv):
    """
    Do the actual work for generic Drupal DB reads.

    Note: in some cases, extra columns will be returned (e.g. node type,
    if the type wasn't specified in key_cv/value_cv).  These will
    generally require post-processing in the transform function to match
    the format of the opposite query function.

    Parameters:
        see drupal_db_query()

    Dependencies:
        functions: get_drupal_chain_type()
        modules: sys, nori

    """
    chain_type = get_drupal_chain_type(key_cv, value_cv)
    if not chain_type:
        nori.core.email_logger.error(('Internal Error: invalid field list supplied in call to\ndrupal_db_read(); call was (in expanded notation):\n\ndrupal_db_read(db_obj={0},\n               db_cur={1},\n               key_cv={2},\n               value_cv={3})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, key_cv, value_cv])))
        sys.exit(nori.core.exitvals['internal']['num'])
    if chain_type == 'n-f':
        node_cv = key_cv[0]
        node_ident = node_cv[0]
        node_value_type = node_cv[1]
        if len(node_cv) > 2:
            node_value = node_cv[2]
        node_type = node_ident[1]
        node_id_type = node_ident[2]
        if node_id_type == 'id':
            key_column = 'node.nid'
        else:
            if node_id_type == 'title':
                key_column = 'node.title'
            node_value_cond = ''
            if len(node_cv) > 2:
                node_value_cond = ('AND {0} = %s').format(key_column)
            field_idents = {}
            field_value_types = {}
            field_values = []
            field_names = {}
            value_columns = []
            field_joins = []
            term_joins = []
            field_value_conds = []
            field_deleted_conds = []
            v_order_columns = []
            for i, field_cv in enumerate(value_cv):
                field_idents[i] = field_cv[0]
                field_value_types[i] = field_cv[1]
                if len(field_cv) > 2:
                    field_values.append(field_cv[2])
                field_names[i] = field_idents[i][1]
                field_joins.append(('LEFT JOIN field_data_field_{0} AS f{1}\nON f{1}.entity_id = node.nid\nAND f{1}.revision_id = node.vid').format(field_names[i], i))
                if field_value_types[i].startswith('term: '):
                    value_columns.append(('t{0}.name').format(i))
                    term_joins.append(('LEFT JOIN taxonomy_term_data AS t{0}\nON t{0}.tid = f.field_{1}_tid}').format(i, field_names[i]))
                else:
                    value_columns.append(('f{0}.field_{1}_value').format(i, field_names[i]))
                if len(field_cv) > 2:
                    field_value_conds.append(('AND {0} = %s').format(value_columns[(-1)]))
                field_deleted_conds.append(('AND (f{0}.deleted = 0 OR f{0}.deleted IS NULL)').format(i))
                v_order_columns.append(('f{0}.delta').format(i))

        query_str = ('\nSELECT {0}, {1}\nFROM node\n{2}\n{3}\nWHERE (node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node.type = %s\n{4}\n{5}\n{6}\nORDER BY node.title, node.nid, {7}\n').format(key_column, (', ').join(value_columns), ('\n').join(field_joins), ('\n').join(term_joins), node_value_cond, ('\n').join(field_value_conds), ('\n').join(field_deleted_conds), (', ').join(v_order_columns))
        query_args = [
         node_type]
        if len(node_cv) > 2:
            query_args.append(node_value)
        query_args += field_values
    elif chain_type == 'n-r-n':
        k_node_cv = key_cv[0]
        k_node_ident = k_node_cv[0]
        k_node_value_type = k_node_cv[1]
        if len(k_node_cv) > 2:
            k_node_value = k_node_cv[2]
        k_node_type = k_node_ident[1]
        k_node_id_type = k_node_ident[2]
        if k_node_id_type == 'id':
            key_column = 'k_node.nid'
        elif k_node_id_type == 'title':
            key_column = 'k_node.title'
        k_node_value_cond = ''
        if len(k_node_cv) > 2:
            k_node_value_cond = ('AND {0} = %s').format(key_column)
        rel_cv = key_cv[1]
        rel_ident = rel_cv[0]
        rel_type = rel_ident[1]
        v_node_cv = value_cv[0]
        v_node_ident = v_node_cv[0]
        v_node_value_type = v_node_cv[1]
        if len(v_node_cv) > 2:
            v_node_value = v_node_cv[2]
        v_node_type = v_node_ident[1]
        v_node_id_type = v_node_ident[2]
        if v_node_id_type == 'id':
            value_column = 'v_node.nid'
        elif v_node_id_type == 'title':
            value_column = 'v_node.title'
        extra_value_cols = ''
        v_node_type_cond = ''
        if v_node_type is None:
            extra_value_cols = ', v_node.type'
        else:
            v_node_type_cond = 'AND v_node.type = %s'
        v_node_value_cond = ''
        if len(v_node_cv) > 2:
            v_node_value_cond = ('AND {0} = %s').format(value_column)
        query_str = ("\nSELECT {0}, {1}{2}\nFROM node AS k_node\nLEFT JOIN field_data_endpoints AS e1\n          ON e1.endpoints_entity_id = k_node.nid\nLEFT JOIN field_data_endpoints AS e2\n          ON e2.entity_id = e1.entity_id\n          AND e2.revision_id = e1.revision_id\n          AND e2.endpoints_r_index > e1.endpoints_r_index\nLEFT JOIN node AS v_node\n          ON v_node.nid = e2.endpoints_entity_id\nWHERE (k_node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND k_node.type = %s\n{3}\nAND (e1.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_data_endpoints\n      GROUP BY entity_id))\nAND e1.entity_type = 'relation'\nAND e1.bundle = %s\nAND e1.endpoints_entity_type = 'node'\nAND (e1.deleted = 0 OR e1.deleted IS NULL)\nAND e2.endpoints_entity_type = 'node'\nAND (e2.deleted = 0 OR e2.deleted IS NULL)\nAND (v_node.vid IN\n     (SELECT max(vid)\n      FROM node\n      GROUP BY nid))\n{4}\n{5}\nORDER BY k_node.title, k_node.nid, e1.entity_id, v_node.title, v_node.nid\n").format(key_column, value_column, extra_value_cols, k_node_value_cond, v_node_type_cond, v_node_value_cond)
        query_args = [
         k_node_type]
        if len(k_node_cv) > 2:
            query_args.append(k_node_value)
        query_args.append(rel_type)
        if v_node_type is not None:
            query_args.append(v_node_type)
        if len(v_node_cv) > 2:
            query_args.append(v_node_value)
    elif chain_type == 'n-rn-rf':
        node1_cv = key_cv[0]
        node1_ident = node1_cv[0]
        node1_value_type = node1_cv[1]
        if len(node1_cv) > 2:
            node1_value = node1_cv[2]
        node1_type = node1_ident[1]
        node1_id_type = node1_ident[2]
        if node1_id_type == 'id':
            key_column_1 = 'node1.nid'
        elif node1_id_type == 'title':
            key_column_1 = 'node1.title'
        node1_value_cond = ''
        if len(node1_cv) > 2:
            node1_value_cond = ('AND {0} = %s').format(key_column_1)
        rel_cv = key_cv[1]
        rel_ident = rel_cv[0]
        rel_type = rel_ident[1]
        node2_cv = key_cv[2]
        node2_ident = node2_cv[0]
        node2_value_type = node2_cv[1]
        if len(node2_cv) > 2:
            node2_value = node2_cv[2]
        node2_type = node2_ident[1]
        node2_id_type = node2_ident[2]
        if node2_id_type == 'id':
            key_column_2 = 'node2.nid'
        else:
            if node2_id_type == 'title':
                key_column_2 = 'node2.title'
            node2_value_cond = ''
            if len(node2_cv) > 2:
                node2_value_cond = ('AND {0} = %s').format(key_column_2)
            field_idents = {}
            field_value_types = {}
            field_values = []
            field_names = {}
            value_columns = []
            field_joins = []
            term_joins = []
            field_entity_conds = []
            field_value_conds = []
            field_deleted_conds = []
            v_order_columns = []
            for i, field_cv in enumerate(value_cv):
                field_idents[i] = field_cv[0]
                field_value_types[i] = field_cv[1]
                if len(field_cv) > 2:
                    field_values.append(field_cv[2])
                field_names[i] = field_idents[i][1]
                field_joins.append(('LEFT JOIN field_data_field_{0} AS f{1}\nON f{1}.entity_id = e2.entity_id\nAND f{1}.revision_id = e2.revision_id').format(field_names[i], i))
                if field_value_types[i].startswith('term: '):
                    value_columns.append(('t{0}.name').format(i))
                    term_joins.append(('LEFT JOIN taxonomy_term_data AS t{0}\nON t{0}.tid = f.field_{1}_tid}').format(i, field_names[i]))
                else:
                    value_columns.append(('f{0}.field_{1}_value').format(i, field_names[i]))
                field_entity_conds.append(("AND f{0}.entity_type = 'relation'").format(i))
                if len(field_cv) > 2:
                    field_value_conds.append(('AND {0} = %s').format(value_columns[(-1)]))
                field_deleted_conds.append(('AND (f{0}.deleted = 0 OR f{0}.deleted IS NULL)').format(i))
                v_order_columns.append(('f{0}.delta').format(i))

        query_str = ("\nSELECT {0}, {1}, {2}\nFROM node AS node1\nLEFT JOIN field_data_endpoints AS e1\n          ON e1.endpoints_entity_id = node1.nid\nLEFT JOIN field_data_endpoints AS e2\n          ON e2.entity_id = e1.entity_id\n          AND e2.revision_id = e1.revision_id\n          AND e2.endpoints_r_index > e1.endpoints_r_index\nLEFT JOIN node AS node2\n          ON node2.nid = e2.endpoints_entity_id\n{3}\n{4}\nWHERE (node1.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node1.type = %s\n{5}\nAND (e1.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_data_endpoints\n      GROUP BY entity_id))\nAND e1.entity_type = 'relation'\nAND e1.bundle = %s\nAND e1.endpoints_entity_type = 'node'\nAND (e1.deleted = 0 OR e1.deleted IS NULL)\nAND e2.endpoints_entity_type = 'node'\nAND (e2.deleted = 0 OR e2.deleted IS NULL)\nAND (node2.vid IN\n     (SELECT max(vid)\n      FROM node\n      GROUP BY nid))\nAND node2.type = %s\n{6}\n{7}\n{8}\n{9}\nORDER BY k_node.title, k_node.nid, e1.entity_id, {10}\n").format(key_column_1, key_column_2, (', ').join(value_columns), ('\n').join(field_joins), ('\n').join(term_joins), node1_value_cond, node2_value_cond, ('\n').join(field_entity_conds), ('\n').join(field_value_conds), ('\n').join(field_deleted_conds), (', ').join(v_order_columns))
        query_args = [
         node1_type]
        if len(node1_cv) > 2:
            query_args.append(node1_value)
        query_args.append(rel_type)
        query_args.append(node2_type)
        if len(node2_cv) > 2:
            query_args.append(node2_value)
        query_args += field_values
    elif chain_type == 'n-fc-f':
        node_cv = key_cv[0]
        node_ident = node_cv[0]
        node_value_type = node_cv[1]
        if len(node_cv) > 2:
            node_value = node_cv[2]
        node_type = node_ident[1]
        node_id_type = node_ident[2]
        if node_id_type == 'id':
            key_column = 'node.nid'
        elif node_id_type == 'title':
            key_column = 'node.title'
        node_value_cond = ''
        if len(node_cv) > 2:
            node_value_cond = ('AND {0} = %s').format(key_column)
        fc_cv = key_cv[1]
        fc_ident = fc_cv[0]
        fc_value_type = fc_cv[1]
        if len(fc_cv) > 2:
            fc_value = fc_cv[2]
        fc_type = fc_ident[1]
        fc_id_type = fc_ident[2]
        if fc_id_type == 'id':
            extra_key_column = 'fci.item_id'
        else:
            if fc_id_type == 'label':
                extra_key_column = 'fci.label'
            fc_value_cond = ''
            if len(fc_cv) > 2:
                fc_value_cond = ('AND {0} = %s').format(extra_key_column)
            field_idents = {}
            field_value_types = {}
            field_values = []
            field_names = {}
            value_columns = []
            field_joins = []
            term_joins = []
            field_entity_conds = []
            field_value_conds = []
            field_deleted_conds = []
            v_order_columns = []
            for i, field_cv in enumerate(value_cv):
                field_idents[i] = field_cv[0]
                field_value_types[i] = field_cv[1]
                if len(field_cv) > 2:
                    field_values.append(field_cv[2])
                field_names[i] = field_idents[i][1]
                field_joins.append(('LEFT JOIN field_data_field_{0} AS f{1}\nON f{1}.entity_id = fci.item_id\nAND f{1}.revision_id = fci.revision_id').format(field_names[i], i))
                if field_value_types[i].startswith('term: '):
                    value_columns.append(('t{0}.name').format(i))
                    term_joins.append(('LEFT JOIN taxonomy_term_data AS t{0}\nON t{0}.tid = f.field_{1}_tid}').format(i, field_names[i]))
                else:
                    value_columns.append(('f{0}.field_{1}_value').format(i, field_names[i]))
                field_entity_conds.append(("AND f{0}.entity_type = 'field_collection_item'").format(i))
                if len(field_cv) > 2:
                    field_value_conds.append(('AND {0} = %s').format(value_columns[(-1)]))
                field_deleted_conds.append(('AND (f{0}.deleted = 0 OR f{0}.deleted IS NULL)').format(i))
                v_order_columns.append(('f{0}.delta').format(i))

        query_str = ("\nSELECT {0}, {1}{2}\nFROM node\nLEFT JOIN field_data_field_{3} AS fcf\n          ON fcf.entity_id = node.nid\n          AND fcf.revision_id = node.vid\nLEFT JOIN field_collection_item as fci\n          ON fci.item_id = fcf.field_{3}_value\n          AND fci.revision_id = fcf.field_{3}_revision_id\n{4}\n{5}\nWHERE (node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node.type = %s\n{6}\nAND fcf.entity_type = 'node'\nAND (fcf.deleted = 0 OR fcf.deleted IS NULL)\nAND (fci.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_collection_item\n      GROUP BY item_id))\nAND (fci.archived = 0 OR fci.archived IS NULL)\n{7}\n{8}\n{9}\n{10}\nORDER BY node.title, node.nid, fcf.delta, {11}\n").format(key_column, extra_key_column + ', ' if extra_key_column else '', (', ').join(value_columns), fc_type, ('\n').join(field_joins), ('\n').join(term_joins), node_value_cond, fc_value_cond, ('\n').join(field_entity_conds), ('\n').join(field_value_conds), ('\n').join(field_deleted_conds), (', ').join(v_order_columns))
        query_args = [
         node_type]
        if len(node_cv) > 2:
            query_args.append(node_value)
        if len(fc_cv) > 2:
            query_args.append(fc_value)
        query_args += field_values
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return
        if not ret[1]:
            return []
        return ret[1]


def drupal_db_update(db_obj, db_cur, key_cv, value_cv, no_replicate=False):
    """
    Do the actual work for generic Drupal DB updates.

    The value_cv sequence may only have one element.

    Parameters:
        see drupal_db_query()

    Dependencies:
        functions: get_drupal_chain_type()
        modules: sys, nori

    """
    if len(value_cv) != 1:
        nori.core.email_logger.error(('Internal Error: multiple value_cv entries supplied in call to\ndrupal_db_update(); call was (in expanded notation):\n\ndrupal_db_update(db_obj={0},\n                 db_cur={1},\n                 key_cv={2},\n                 value_cv={3},\n                 no_replicate={4})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, key_cv, value_cv,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    chain_type = get_drupal_chain_type(key_cv, value_cv)
    if not chain_type:
        nori.core.email_logger.error(('Internal Error: invalid field list supplied in call to\ndrupal_db_update(); call was (in expanded notation):\n\ndrupal_db_update(db_obj={0},\n                 db_cur={1},\n                 key_cv={2},\n                 value_cv={3},\n                 no_replicate={4})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, key_cv, value_cv,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    if chain_type == 'n-f':
        node_cv = key_cv[0]
        node_ident = node_cv[0]
        node_value_type = node_cv[1]
        node_value = node_cv[2]
        node_type = node_ident[1]
        node_id_type = node_ident[2]
        if node_id_type == 'id':
            key_column = 'node.nid'
        elif node_id_type == 'title':
            key_column = 'node.title'
        field_cv = value_cv[0]
        field_ident = field_cv[0]
        field_value_type = field_cv[1]
        field_value = field_cv[2]
        field_name = field_ident[1]
        if field_value_type.startswith('term: '):
            term_join = 'LEFT JOIN taxonomy_term_data AS t\nON t.name = %s'
            value_str = 't.tid'
        else:
            term_join = ''
            value_str = '%s'
        query_str = ('\nUPDATE node\nLEFT JOIN field_data_field_{0} AS f\nON f.entity_id = node.nid\nAND f.revision_id = node.vid\n{1}\nSET f.field_{0}_value = {2}\nWHERE (node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node.type = %s\nAND {3} = %s\nAND (f.deleted = 0 OR f.deleted IS NULL)\n').format(field_name, term_join, value_str, key_column)
        query_args = [
         field_value, node_type, node_value]
    elif chain_type == 'n-r-n':
        k_node_cv = key_cv[0]
        k_node_ident = k_node_cv[0]
        k_node_value_type = k_node_cv[1]
        k_node_value = k_node_cv[2]
        k_node_type = k_node_ident[1]
        k_node_id_type = k_node_ident[2]
        if k_node_id_type == 'id':
            key_column = 'k_node.nid'
        elif k_node_id_type == 'title':
            key_column = 'k_node.title'
        rel_cv = key_cv[1]
        rel_ident = rel_cv[0]
        rel_type = rel_ident[1]
        v_node_cv = value_cv[0]
        v_node_ident = v_node_cv[0]
        v_node_value_type = v_node_cv[1]
        v_node_value = v_node_cv[2]
        v_node_type = v_node_ident[1]
        v_node_id_type = v_node_ident[2]
        if v_node_id_type == 'id':
            value_column = 'v_node.nid'
        elif v_node_id_type == 'title':
            value_column = 'v_node.title'
        query_str = ("\nUPDATE node AS k_node\nLEFT JOIN field_data_endpoints AS e1\n          ON e1.endpoints_entity_id = k_node.nid\nLEFT JOIN field_data_endpoints AS e2\n          ON e2.entity_id = e1.entity_id\n          AND e2.revision_id = e1.revision_id\n          AND e2.endpoints_r_index > e1.endpoints_r_index\nLEFT JOIN node AS v_node\nSET e2.endpoints_entity_id = v_node.nid\nWHERE (k_node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND k_node.type = %s\nAND {0} = %s\nAND (e1.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_data_endpoints\n      GROUP BY entity_id))\nAND e1.entity_type = 'relation'\nAND e1.bundle = %s\nAND e1.endpoints_entity_type = 'node'\nAND (e1.deleted = 0 OR e1.deleted IS NULL)\nAND e2.endpoints_entity_type = 'node'\nAND (e2.deleted = 0 OR e2.deleted IS NULL)\nAND (v_node.vid IN\n     (SELECT max(vid)\n      FROM node\n      GROUP BY nid))\nAND v_node.type = %s\nAND {1} = %s\n").format(key_column, value_column)
        query_args = [
         k_node_type, k_node_value, rel_type, v_node_type,
         v_node_value]
    elif chain_type == 'n-rn-rf':
        node1_cv = key_cv[0]
        node1_ident = node1_cv[0]
        node1_value_type = node1_cv[1]
        node1_value = node1_cv[2]
        node1_type = node1_ident[1]
        node1_id_type = node1_ident[2]
        if node1_id_type == 'id':
            key_column_1 = 'node1.nid'
        elif node1_id_type == 'title':
            key_column_1 = 'node1.title'
        rel_cv = key_cv[1]
        rel_ident = rel_cv[0]
        rel_type = rel_ident[1]
        node2_cv = key_cv[2]
        node2_ident = node2_cv[0]
        node2_value_type = node2_cv[1]
        node2_value = node2_cv[2]
        node2_type = node2_ident[1]
        node2_id_type = node2_ident[2]
        if node2_id_type == 'id':
            key_column_2 = 'node2.nid'
        elif node2_id_type == 'title':
            key_column_2 = 'node2.title'
        field_cv = value_cv[0]
        field_ident = field_cv[0]
        field_value_type = field_cv[1]
        field_value = field_cv[2]
        field_name = field_ident[1]
        if field_value_type.startswith('term: '):
            term_join = 'LEFT JOIN taxonomy_term_data AS t\nON t.name = %s'
            value_str = 't.tid'
        else:
            term_join = ''
            value_str = '%s'
        query_str = ("\nUPDATE node AS node1\nLEFT JOIN field_data_endpoints AS e1\n          ON e1.endpoints_entity_id = node1.nid\nLEFT JOIN field_data_endpoints AS e2\n          ON e2.entity_id = e1.entity_id\n          AND e2.revision_id = e1.revision_id\n          AND e2.endpoints_r_index > e1.endpoints_r_index\nLEFT JOIN node AS node2\n          ON node2.nid = e2.endpoints_entity_id\nLEFT JOIN field_data_field_{0} AS f\nON f.entity_id = e2.entity_id\nAND f.revision_id = e2.revision_id\n{1}\nSET f.field_{0}_value = {2}\nWHERE (node1.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node1.type = %s\nAND {3} = %s\nAND (e1.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_data_endpoints\n      GROUP BY entity_id))\nAND e1.entity_type = 'relation'\nAND e1.bundle = %s\nAND e1.endpoints_entity_type = 'node'\nAND (e1.deleted = 0 OR e1.deleted IS NULL)\nAND e2.endpoints_entity_type = 'node'\nAND (e2.deleted = 0 OR e2.deleted IS NULL)\nAND (node2.vid IN\n     (SELECT max(vid)\n      FROM node\n      GROUP BY nid))\nAND node2.type = %s\nAND {4} = %s\nAND f.entity_type = 'relation'\nAND (f.deleted = 0 OR f.deleted IS NULL)\n").format(field_name, term_join, value_str, key_column_1, key_column_2)
        query_args = [
         field_value, node1_type, node1_value, rel_type,
         node2_type, node2_value]
    elif chain_type == 'n-fc-f':
        node_cv = key_cv[0]
        node_ident = node_cv[0]
        node_value_type = node_cv[1]
        node_value = node_cv[2]
        node_type = node_ident[1]
        node_id_type = node_ident[2]
        if node_id_type == 'id':
            key_column_1 = 'node.nid'
        elif node_id_type == 'title':
            key_column_1 = 'node.title'
        fc_cv = key_cv[1]
        fc_ident = fc_cv[0]
        fc_value_type = fc_cv[1]
        fc_value = fc_cv[2]
        fc_type = fc_ident[1]
        fc_id_type = fc_ident[2]
        if fc_id_type == 'id':
            key_column_2 = 'fci.item_id'
        elif fc_id_type == 'label':
            key_column_2 = 'fci.label'
        field_cv = value_cv[0]
        field_ident = field_cv[0]
        field_value_type = field_cv[1]
        field_value = field_cv[2]
        field_name = field_ident[1]
        if field_value_type.startswith('term: '):
            term_join = 'LEFT JOIN taxonomy_term_data AS t\nON t.name = %s'
            value_str = 't.tid'
        else:
            term_join = ''
            value_str = '%s'
        query_str = ("\nUPDATE node\nLEFT JOIN field_data_field_{0} AS fcf\n          ON fcf.entity_id = node.nid\n          AND fcf.revision_id = node.vid\nLEFT JOIN field_collection_item as fci\n          ON fci.item_id = fcf.field_{0}_value\n          AND fci.revision_id = fcf.field_{0}_revision_id\nLEFT JOIN field_data_field_{1} AS f\nON f.entity_id = fci.item_id\nAND f.revision_id = fci.revision_id\n{2}\nSET f.field_{1}_value = {3}\nWHERE (node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node.type = %s\nAND {4} = %s'\nAND fcf.entity_type = 'node'\nAND (fcf.deleted = 0 OR fcf.deleted IS NULL)\nAND (fci.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_collection_item\n      GROUP BY item_id))\nAND (fci.archived = 0 OR fci.archived IS NULL)\nAND {5} = %s\nAND f.entity_type = 'field_collection_item'\nAND (f.deleted = 0 OR f.deleted IS NULL)\n").format(fc_type, field_name, term_join, value_str, key_column_1, key_column_2)
        query_args = [
         field_value, node_type, node_value, fc_value]
    return db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False)


def drupal_db_insert(db_obj, db_cur, key_cv, value_cv, no_replicate=False):
    """
    Do the actual work for generic Drupal DB inserts.

    Returns True (success), False (partial success), or None (failure).

    The value_cv sequence may only have one element.

    Parameters:
        see drupal_db_query()

    Dependencies:
        functions: get_drupal_chain_type()
        modules: sys, nori

    """
    if len(value_cv) != 1:
        nori.core.email_logger.error(('Internal Error: multiple value_cv entries supplied in call to\ndrupal_db_insert(); call was (in expanded notation):\n\ndrupal_db_insert(db_obj={0},\n                 db_cur={1},\n                 key_cv={2},\n                 value_cv={3},\n                 no_replicate={4})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, key_cv, value_cv,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    chain_type = get_drupal_chain_type(key_cv, value_cv)
    if not chain_type:
        nori.core.email_logger.error(('Internal Error: invalid field list supplied in call to\ndrupal_db_insert(); call was (in expanded notation):\n\ndrupal_db_insert(db_obj={0},\n                 db_cur={1},\n                 key_cv={2},\n                 value_cv={3},\n                 no_replicate={4})\n\nExiting.').format(*map(nori.pps, [db_obj, db_cur, key_cv, value_cv,
         no_replicate])))
        sys.exit(nori.core.exitvals['internal']['num'])
    if chain_type == 'n-f':
        node_cv = key_cv[0]
        node_ident = node_cv[0]
        node_value_type = node_cv[1]
        node_value = node_cv[2]
        node_type = node_ident[1]
        node_id_type = node_ident[2]
        field_cv = value_cv[0]
        field_ident = field_cv[0]
        field_value_type = field_cv[1]
        field_value = field_cv[2]
        field_name = field_ident[1]
        ret = get_drupal_node_ids(db_obj, db_cur, node_cv)
        if ret is None:
            nori.core.email_logger.error(('Warning: could not get the IDs of the following parent node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [node_type, node_id_type,
             node_value])))
            return
        if not ret:
            return
        nid, vid = ret[0]
        return insert_drupal_field(db_obj, db_cur, 'node', node_type, nid, vid, field_cv)
    else:
        if chain_type == 'n-r-n':
            k_node_cv = key_cv[0]
            k_node_ident = k_node_cv[0]
            k_node_value_type = k_node_cv[1]
            k_node_value = k_node_cv[2]
            k_node_type = k_node_ident[1]
            k_node_id_type = k_node_ident[2]
            rel_cv = key_cv[1]
            rel_ident = rel_cv[0]
            rel_type = rel_ident[1]
            v_node_cv = value_cv[0]
            v_node_ident = v_node_cv[0]
            v_node_value_type = v_node_cv[1]
            v_node_value = v_node_cv[2]
            v_node_type = v_node_ident[1]
            v_node_id_type = v_node_ident[2]
            if k_node_id_type == 'id':
                k_nid = k_node_value
            elif k_node_id_type == 'title':
                ret = get_drupal_node_ids(db_obj, db_cur, k_node_cv)
                if ret is None:
                    nori.core.email_logger.error(('Warning: could not get the IDs of the following linked node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [k_node_type, k_node_id_type,
                     k_node_value])))
                    return
                if not ret:
                    return
                k_nid, k_vid = ret[0]
            if v_node_id_type == 'id':
                v_nid = v_node_value
            elif v_node_id_type == 'title':
                ret = get_drupal_node_ids(db_obj, db_cur, v_node_cv)
                if ret is None:
                    nori.core.email_logger.error(('Warning: could not get the IDs of the following linked node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [v_node_type, v_node_id_type,
                     v_node_value])))
                    return
                if not ret:
                    return
                v_nid, v_vid = ret[0]
            return insert_drupal_relation(db_obj, db_cur, 'node', k_nid, relation_type, 'node', v_nid)[0]
        if chain_type == 'n-rn-rf':
            partial = False
            node1_cv = key_cv[0]
            node1_ident = node1_cv[0]
            node1_value_type = node1_cv[1]
            node1_value = node1_cv[2]
            node1_type = node1_ident[1]
            node1_id_type = node1_ident[2]
            if node1_id_type == 'id':
                key_column_1 = 'node1.nid'
            elif node1_id_type == 'title':
                key_column_1 = 'node1.title'
            rel_cv = key_cv[1]
            rel_ident = rel_cv[0]
            rel_type = rel_ident[1]
            node2_cv = key_cv[2]
            node2_ident = node2_cv[0]
            node2_value_type = node2_cv[1]
            node2_value = node2_cv[2]
            node2_type = node2_ident[1]
            node2_id_type = node2_ident[2]
            if node2_id_type == 'id':
                key_column_2 = 'node2.nid'
            elif node2_id_type == 'title':
                key_column_2 = 'node2.title'
            field_cv = value_cv[0]
            field_ident = field_cv[0]
            field_value_type = field_cv[1]
            field_value = field_cv[2]
            field_name = field_ident[1]
            if node1_id_type == 'id':
                node1_nid = node1_value
            elif node1_id_type == 'title':
                ret = get_drupal_node_ids(db_obj, db_cur, node1_cv)
                if ret is None:
                    nori.core.email_logger.error(('Warning: could not get the IDs of the following linked node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [node1_type, node1_id_type,
                     node1_value])))
                    return
                if not ret:
                    return
                node1_nid, node1_vid = ret[0]
            if node2_id_type == 'id':
                node2_nid = node2_value
            else:
                if node2_id_type == 'title':
                    ret = get_drupal_node_ids(db_obj, db_cur, node2_cv)
                    if ret is None:
                        nori.core.email_logger.error(('Warning: could not get the IDs of the following linked node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [node2_type, node2_id_type,
                         node2_value])))
                        return
                    if not ret:
                        return
                    node2_nid, node2_vid = ret[0]
                ret = get_drupal_relation_ids(db_obj, db_cur, 'node', node1_nid, relation_type, 'node', node2_nid)
                if ret is None:
                    nori.core.email_logger.error(('Warning: could not get the IDs of the {0} relation with\nthe following endpoints:\n    node1_type: {1}\n    node1_id_type: {2}\n    node1_value: {3}\n    node2_type: {4}\n    node2_id_type: {5}\n    node2_value: {6}\nSkipping insert.').format(*map(nori.pps, [relation_type, node1_type,
                     node1_id_type, node1_value,
                     node2_type, node2_id_type,
                     node2_value])))
                    return
                if not ret:
                    ret = insert_drupal_relation(db_obj, db_cur, 'node', node1_nid, relation_type, 'node', node2_nid)
                    if ret[0] is None:
                        return
                    if not ret[0]:
                        partial = True
                    rid = ret[1]
                    vid = ret[2]
                else:
                    rid, vid = ret[0]
                ret = insert_drupal_field(db_obj, db_cur, 'relation', relation_type, rid, vid, field_cv)
                if ret is None:
                    return
                if not ret or partial:
                    return False
            return True
        if chain_type == 'n-fc-f':
            partial = False
            node_cv = key_cv[0]
            node_ident = node_cv[0]
            node_value_type = node_cv[1]
            node_value = node_cv[2]
            node_type = node_ident[1]
            node_id_type = node_ident[2]
            fc_cv = key_cv[1]
            fc_ident = fc_cv[0]
            fc_value_type = fc_cv[1]
            fc_value = fc_cv[2]
            fc_type = fc_ident[1]
            fc_id_type = fc_ident[2]
            field_cv = value_cv[0]
            field_ident = field_cv[0]
            field_value_type = field_cv[1]
            field_value = field_cv[2]
            field_name = field_ident[1]
            ret = get_drupal_node_ids(db_obj, db_cur, node_cv)
            if ret is None:
                nori.core.email_logger.error(('Warning: could not get the IDs of the following parent node:\n    node_type: {0}\n    node_id_type: {1}\n    node_value: {2}\nSkipping insert.').format(*map(nori.pps, [node_type, node_id_type,
                 node_value])))
                return
            if not ret:
                return
            n_id, n_vid = ret[0]
            ret = get_drupal_fc_ids(db_obj, db_cur, 'node', node_type, n_id, n_vid, fc_cv)
            if ret is None:
                nori.core.email_logger.error(('Warning: could not get the IDs of the following Drupal parent field\ncollection:\n    fc_type: {0}\n    fc_id_type: {1}\n    fc_value: {2}\n    node_type: {3}\n    node_id_type: {4}\n    node_value: {5}\nSkipping insert.').format(*map(nori.pps, [fc_type, fc_id_type, fc_value,
                 node_type, node_id_type,
                 node_value])))
                return
            if not ret:
                ret = insert_drupal_fc(db_obj, db_cur, 'node', node_type, n_id, n_vid, fc_cv)
                if ret[0] is None:
                    return
                if not ret[0]:
                    partial = True
                fc_id = ret[1]
                fc_vid = ret[2]
            else:
                fc_id, fc_vid = ret[0]
            ret = insert_drupal_field(db_obj, db_cur, 'field_collection_item', fc_type, fc_id, fc_vid, field_cv)
            if ret is None:
                return
            if not ret or partial:
                return False
            return True
        return


def get_drupal_node_ids(db_obj, db_cur, node_cv):
    """
    Get the node and revision IDs for a specified Drupal node.

    Returns None on error, an empty array if there are no results, or
    a sequence of row tuples.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        node_cv: the entry for the node in a template key_cv or
                 value_cv sequence

    """
    node_ident = node_cv[0]
    node_value_type = node_cv[1]
    node_value = node_cv[2]
    node_type = node_ident[1]
    node_id_type = node_ident[2]
    if node_id_type == 'id':
        node_ident_column = 'node.nid'
    elif node_id_type == 'title':
        node_ident_column = 'node.title'
    query_str = ('\nSELECT node.nid, node.vid\nFROM node\nWHERE (node.vid IN\n       (SELECT max(vid)\n        FROM node\n        GROUP BY nid))\nAND node.type = %s\nAND {0} = %s\n').format(node_ident_column)
    query_args = [
     node_type, node_value]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        return ret[1]


def get_drupal_relation_ids(db_obj, db_cur, e1_entity_type, e1_entity_id, relation_type, e2_entity_type, e2_entity_id):
    """
    Get the relation and revision IDs for a specified Drupal relation.

    Returns None on error, an empty array if there are no results, or
    a sequence of row tuples.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        e1_entity_type: the entity type (e.g., 'node') of the relation's
                        first endpoint
        e1_entity_id: the entity ID of the relation's first endpoint
        relation_type: the type string / bundle of the relation
        e2_entity_type: the entity type (e.g., 'node') of the relation's
                        second endpoint
        e2_entity_id: the entity ID of the relation's second endpoint

    """
    query_str = "\nSELECT e1.entity_id, e1.revision_id\nFROM field_data_endpoints AS e1\nLEFT JOIN field_data_endpoints AS e2\n          ON e2.entity_id = e1.entity_id\n          AND e2.revision_id = e1.revision_id\n          AND e2.endpoints_r_index > e1.endpoints_r_index\nWHERE (e1.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_data_endpoints\n      GROUP BY entity_id))\nAND e1.entity_type = 'relation'\nAND e1.bundle = %s\nAND e1.endpoints_entity_type = %s\nAND e1.endpoints_entity_id = %s\nAND (e1.deleted = 0 OR e1.deleted IS NULL)\nAND e2.endpoints_entity_type = %s\nAND e2.endpoints_entity_id = %s\nAND (e2.deleted = 0 OR e2.deleted IS NULL)\n"
    query_args = [
     relation_type, e1_entity_type, e1_entity_id,
     e2_entity_type, e2_entity_id]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        return ret[1]


def get_drupal_fc_ids(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, fc_cv):
    """
    Get the FC and revision IDs for a specified Drupal field collection.

    Returns None on error, an empty array if there are no results, or
    a sequence of row tuples.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        entity_type: the entity type (e.g., 'node') of the FC's parent
        bundle: the bundle (e.g., node content type) of the FC's parent
        entity_id: the ID of the FC's parent
        revision_id: the revision ID of the FC's parent
        fc_cv: the entry for the field collection in a template key_cv
               or value_cv sequence

    """
    fc_ident = fc_cv[0]
    fc_value_type = fc_cv[1]
    fc_value = fc_cv[2]
    fc_type = fc_ident[1]
    fc_id_type = fc_ident[2]
    if fc_id_type == 'id':
        fc_ident_column = 'fci.item_id'
    elif fc_id_type == 'label':
        fc_ident_column = 'fci.label'
    query_str = ('\nSELECT fci.item_id, fci.revision_id\nFROM field_data_field_{0} as fcf\nLEFT JOIN field_collection_item as fci\nON fci.item_id = fcf.field_{0}_value\nAND fci.revision_id = fcf.field_{0}_revision\nWHERE fcf.entity_type = %s\nAND fcf.bundle = %s\nAND fcf.entity_id = %s\nAND fcf.revision_id = %s\n(fcf.deleted = 0 OR fcf.deleted IS NULL)\nAND (fci.revision_id IN\n     (SELECT max(revision_id)\n      FROM field_collection_item\n      GROUP BY item_id))\nAND (fci.archived = 0 OR fci.archived IS NULL)\nAND {1} = %s\n').format(fc_type, fc_ident_column)
    query_args = [
     entity_type, bundle, entity_id, revision_id, fc_value]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        return ret[1]


def get_drupal_max_delta(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, field_name):
    """
    Get the maximum current delta for a specified Drupal field.

    Returns None on error, an empty array if there are no results, or
    a single row tuple.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        entity_type: the entity type (e.g., 'node') of the field's
                     parent
        bundle: the bundle (e.g., node content type) of the field's
                parent
        entity_id: the ID of the field's parent
        revision_id: the revision ID of the field's parent
        field_name: the name of the field

    Dependencies:
        modules: nori

    """
    query_str = ('\nSELECT max(delta)\nFROM field_data_field_{0}\nWHERE entity_type = %s\nAND bundle = %s\nAND entity_id = %s\nAND revision_id = %s\nAND deleted = 0\nGROUP BY entity_type, bundle, entity_id, revision_id\n').format(field_name)
    query_args = [
     entity_type, bundle, entity_id, revision_id]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        if len(ret[1]) != 1:
            nori.core.email_logger.error(('Warning: multiple max-delta entries for Drupal field {0}\nunder the following parent entity:\n    entity_type: {1}\n    bundle: {2}\n    entity_id: {3}\n    revision_id: {4}.').format(*map(nori.pps, [field_name, entity_type, bundle,
             entity_id, revision_id])))
            return None
        return ret[1][0]


def get_drupal_field_defaults(db_obj, db_cur, entity_type, bundle):
    """
    Get the defaults for all fields in a specified Drupal entity.

    Returns None on error, an empty array if there are no results, or
    a sequence of tuples in cv format (see drupal_db_query()).

    Only returns fields with a default.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        entity_type: the type (e.g., 'node') of the entity to check
        bundle: the bundle (e.g., node content type) of the entity to
                check

    Dependencies:
        modules: sys, nori

    """
    query_str = '\nSELECT fci.field_name, fci.data\nFROM field_config_instance as fci\nLEFT JOIN field_config as fc\nON fc.id = fci.field_id\nWHERE fci.entity_type = %s\nAND fci.bundle = %s\nAND fc.deleted = 0\n'
    query_args = [
     entity_type, bundle]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return
        if not ret[1]:
            return []
        if 'phpserialize' not in sys.modules:
            nori.core.email_logger.error(("Warning: there are defaults for Drupal fields under entity type\n{0) and bundle {1}, but the 'phpserialize' module\nis not available, so they can't be interpreted.").format(*map(nori.pps, [entity_type, bundle])))
            return
        nori.core.email_logger.error(("Warning: there are defaults for Drupal fields under entity type\n{0) and bundle {1}, but the interpretation code\nhasn't been implemented yet.").format(*map(nori.pps, [entity_type, bundle])))
        return


def get_drupal_field_cardinality(db_obj, db_cur, field_name):
    """
    Get the allowed cardinality for a specified Drupal field.

    Returns None on error, an empty array if there are no results, or
    a single row tuple.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        field_name: the name of the field

    Dependencies:
        modules: nori

    """
    query_str = '\nSELECT cardinality\nFROM field_config\nWHERE field_name = %s\nAND deleted = 0\n'
    query_args = [
     'field_' + field_name]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        if len(ret[1]) != 1:
            nori.core.email_logger.error(('Warning: multiple entries for Drupal field name {0}.').format(nori.pps(field_name)))
            return None
        return ret[1][0]


def get_drupal_term_id(db_obj, db_cur, vocab_name, term_name):
    """
    Get the term ID for a specified Drupal vocabulary term.

    Returns None on error, an empty array if there are no results, or
    a single row tuple.

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        vocab_name: the machine name of the vocabulary
        term_name: the name of the term

    Dependencies:
        modules: nori

    """
    query_str = '\nSELECT tid\nFROM taxonomy_term_data as t\nLEFT JOIN taxonomy_vocabulary as v\nON v.vid = t.vid\nWHERE v.machine_name = %s\nAND t.name = %s\n'
    query_args = [
     vocab_name, term_name]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
        return None
    else:
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return None
        if not ret[1]:
            return []
        if len(ret[1]) != 1:
            nori.core.email_logger.error(('Warning: multiple entries for term {0} in Drupal\nvocabulary {1}.').format(*map(nori.pps, [term_name,
             vocab_name])))
            return None
        return ret[1][0]


def insert_drupal_relation(db_obj, db_cur, e1_entity_type, e1_entity_id, relation_type, e2_entity_type, e2_entity_id):
    """
    Insert a Drupal relation.

    Returns a tuple: (success?, relation_id, revision_id), where success
    can be True (success), False (partial success), or None (failure).

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        e1_entity_type: the entity type (e.g., 'node') of the relation's
                        first endpoint
        e1_entity_id: the entity ID of the relation's first endpoint
        relation_type: the type string / bundle of the relation
        e2_entity_type: the entity type (e.g., 'node') of the relation's
                        second endpoint
        e2_entity_id: the entity ID of the relation's second endpoint

    Dependencies:
        modules: time, nori

    """
    db_ac = db_obj.autocommit(None)
    db_obj.autocommit(False)
    query_str = '\nINSERT INTO relation\n(relation_type, vid, uid, created, changed, arity)\nVALUES\n(%s, 0, 1, %s, %s, 2)\n'
    cur_time = int(time.time())
    query_args = [relation_type, cur_time, cur_time]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
        db_obj.rollback()
        db_obj.autocommit(db_ac)
        return (None, None, None)
    else:
        ret = db_obj.get_last_id(db_cur)
        if not ret[0]:
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        rid = ret[1]
        query_str = '\nINSERT INTO relation_revision\n(rid, relation_type, uid, created, changed, arity)\nVALUES\n(%s, %s, 1, %s, %s, 2)\n'
        cur_time = int(time.time())
        query_args = [rid, relation_type, cur_time, cur_time]
        if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        ret = db_obj.get_last_id(db_cur)
        if not ret[0]:
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        vid = ret[1]
        query_str = '\nUPDATE relation\nSET vid = %s\nWHERE rid = %s\n'
        query_args = [
         vid, rid]
        if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        endpoints = [
         (
          0, e1_entity_type, e1_entity_id),
         (
          1, e2_entity_type, e2_entity_id)]
        for i, ep_entity_type, ep_entity_id in endpoints:
            for table_infix in ['data', 'revision']:
                query_str = ("\nINSERT INTO field_{0}_endpoints\n(entity_type, bundle, deleted, entity_id, revision_id, language, delta,\n    endpoints_entity_type, endpoints_entity_id, endpoints_r_index)\nVALUES\n('relation', %s, 0, %s, %s, 'und', %s, %s, %s, %s)\n").format(table_infix)
                query_args = [
                 relation_type, rid, vid, i, ep_entity_type,
                 ep_entity_id, i]
                if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
                    db_obj.rollback()
                    db_obj.autocommit(db_ac)
                    return (None, None, None)

        ret = db_obj.commit()
        db_obj.autocommit(db_ac)
        if not ret:
            return (None, None, None)
        f_defs = get_drupal_field_defaults(db_obj, db_cur, 'relation', relation_type)
        if f_defs is None:
            return (False, rid, vid)
        for f_def in f_defs:
            if not insert_drupal_field(db_obj, db_cur, 'relation', relation_type, rid, vid, f_def):
                return (False, rid, vid)

        return (
         True, rid, vid)


def insert_drupal_fc(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, fc_cv):
    """
    Insert a Drupal field collection.

    Returns a tuple: (success?, fc_id, revision_id), where success can
    be True (success), False (partial success), or None (failure).

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        entity_type: the entity type (e.g., 'node') of the FC's parent
        bundle: the bundle (e.g., node content type) of the FC's parent
        entity_id: the ID of the FC's parent
        revision_id: the revision ID of the FC's parent
        fc_cv: the entry for the field collection in a template key_cv
               or value_cv sequence

    Dependencies:
        modules: nori

    """
    fc_ident = fc_cv[0]
    fc_value_type = fc_cv[1]
    fc_value = fc_cv[2]
    fc_type = fc_ident[1]
    fc_id_type = fc_ident[2]
    db_ac = db_obj.autocommit(None)
    db_obj.autocommit(False)
    if fc_id_type == 'id':
        query_str = "\nINSERT INTO field_collection_item\n(item_id, revision_id, field_name, archived, label)\nVALUES\n(%s, 0, %s, 0, '')\n"
        query_args = [
         fc_value, fc_type]
    elif fc_id_type == 'label':
        query_str = '\nINSERT INTO field_collection_item\n(revision_id, field_name, archived, label)\nVALUES\n(0, %s, 0, %s)\n'
        query_args = [
         'field_' + fc_type, fc_value]
    if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
        db_obj.rollback()
        db_obj.autocommit(db_ac)
        return (None, None, None)
    else:
        if fc_id_type == 'label':
            ret = db_obj.get_last_id(db_cur)
            if not ret[0]:
                db_obj.rollback()
                db_obj.autocommit(db_ac)
                return (None, None, None)
            fcid = ret[1]
        query_str = '\nINSERT INTO field_collection_item_revision\n(item_id)\nVALUES\n(%s)\n'
        query_args = [
         fcid]
        if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        ret = db_obj.get_last_id(db_cur)
        if not ret[0]:
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        vid = ret[1]
        query_str = '\nUPDATE field_collection_item\nSET revision_id = %s\nWHERE item_id = %s\n'
        query_args = [
         vid, fcid]
        if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        fcf_cv = (
         (
          'field', fc_type), 'integer', fcid)
        extra_data = [('field_' + fc_type + '_revision_id', vid)]
        if not insert_drupal_field(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, fcf_cv, extra_data, True):
            db_obj.rollback()
            db_obj.autocommit(db_ac)
            return (None, None, None)
        ret = db_obj.commit()
        db_obj.autocommit(db_ac)
        if not ret:
            return (None, None, None)
        f_defs = get_drupal_field_defaults(db_obj, db_cur, 'field_collection_item', fc_type)
        if f_defs is None:
            return (False, fcid, vid)
        for f_def in f_defs:
            if not insert_drupal_field(db_obj, db_cur, 'field_collection_item', fc_type, fcid, vid, f_def):
                return (False, fcid, vid)

        return (
         True, fcid, vid)


def insert_drupal_field(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, field_cv, extra_data=[], no_trans=False):
    """
    Insert a Drupal field entry.

    Returns True (success), False (partial success), or None (failure).

    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        entity_type: the entity type (e.g., 'node') of the field's
                     parent
        bundle: the bundle (e.g., node content type) of the field's
                parent
        entity_id: the ID of the field's parent
        revision_id: the revision ID of the field's parent
        field_cv: the entry for the field in a template key_cv or
                  value_cv sequence
        extra_data: a sequence of (column name, value) tuples to add to
                    the insert query
        no_trans: if true, don't wrap the call in a new DB transaction;
                  use this when the caller is already handling
                  transaction management

    Dependencies:
        modules: operator, nori

    """
    field_ident = field_cv[0]
    field_value_type = field_cv[1]
    field_value = field_cv[2]
    field_name = field_ident[1]
    f_card = get_drupal_field_cardinality(db_obj, db_cur, field_name)
    if not f_card:
        nori.core.email_logger.error(('Warning: could not get the cardinality of Drupal field {0};\nskipping insert.').format(nori.pps(field_name)))
        return
    else:
        f_cur_delta = get_drupal_max_delta(db_obj, db_cur, entity_type, bundle, entity_id, revision_id, field_name)
        if f_cur_delta is None:
            nori.core.email_logger.error(('Warning: could not get the maximum delta of Drupal field {0}\nunder the following parent entity:\n    entity_type: {1}\n    bundle: {2}\n    entity_id: {3}\n    revision_id: {4}\nSkipping insert.').format(*map(nori.pps, [field_name, entity_type, bundle,
             entity_id, revision_id])))
            return
        if not f_cur_delta:
            f_cur_delta = (-1, )
        if f_card[0] != -1 and f_cur_delta[0] >= f_card[0] - 1:
            nori.core.email_logger.error(('There are already the maximum number of entries {0} for Drupal field\n{1} under the following parent entity:\n    entity_type: {2}\n    bundle: {3}\n    entity_id: {4}\n    revision_id: {5}\nSkipping insert; manual intervention required.').format(*map(nori.pps, [f_card, field_name, entity_type, bundle,
             entity_id, revision_id])))
            return
        if field_value_type.startswith('term: '):
            ret = get_drupal_term_id(db_obj, db_cur, field_value_type[6:], term_name)
            if not ret:
                nori.core.email_logger.error(('Warning: could not get the ID of term {0} in Drupal\nvocabulary {1}; skipping insert.').format(*map(nori.pps, [term_name, field_value_type[6:]])))
                return
            field_value = ret[0]
            value_column = 'field_' + field_name + '_tid'
        else:
            value_column = 'field_' + field_name + '_value'
        extra_columns = ''
        extra_placeholders = ''
        extra_values = []
        if extra_data:
            extra_columns = ', ' + (', ').join(map(operator.itemgetter(0), extra_data))
            extra_placeholders = ', ' + (', ').join(map(lambda x: '%s', extra_data))
            extra_values = map(operator.itemgetter(1), extra_data)
        if not no_trans:
            db_ac = db_obj.autocommit(None)
            db_obj.autocommit(False)
        for table_infix in ['data', 'revision']:
            query_str = ("\nINSERT INTO field_{0}_field_{1}\n(entity_type, bundle, deleted, entity_id, revision_id, language, delta,\n    {2}{3})\nVALUES\n(%s, %s, 0, %s, %s, 'und', %s, %s{4})\n").format(table_infix, field_name, value_column, extra_columns, extra_placeholders)
            query_args = [
             entity_type, bundle, entity_id, revision_id,
             f_cur_delta[0] + 1, field_value]
            if extra_values:
                query_args += extra_values
            if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=False):
                if not no_trans:
                    db_obj.rollback()
                    db_obj.autocommit(db_ac)
                return

        if not no_trans:
            ret = db_obj.commit()
            db_obj.autocommit(db_ac)
            if not ret:
                return
            return True
        return True
        return


def drupal_readonly_status(db_obj, db_cur, what=None):
    """
    Get or set the read-only status of a Drupal site.
    If what is True or False, returns True on success, False on error.
    If what is None, returns True/False, or None on error.
    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
        what: if True, turn read-only mode on; if False, turn it off;
              if None, return the current status
    """
    if what is None:
        query_str = "\nSELECT value\nFROM variable\nWHERE name='site_readonly'\n"
        query_args = []
        if not db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True):
            return
        ret = db_obj.fetchall(db_cur)
        if not ret[0]:
            return
        if not ret[1]:
            return
        return ret[1][0][0] == 'i:1;'
    else:
        query_str = "\nUPDATE variable\nSET value = %s\nWHERE name='site_readonly'\n"
        query_args = [
         'i:1;' if what else 'i:0;']
        return db_obj.execute(db_cur, query_str.strip(), query_args, has_results=True)
        return


def pre_action_drupal_readonly(s_db, s_cur, d_db, d_cur):
    """
    Wrapper around drupal_readonly_status() for pre-action callbacks.
    Parameters:
        s_db: the source-database connection object to use
        s_cur: the source-database cursor object to use
        d_db: the destination-database connection object to use
        d_cur: the destination-database cursor object to use
    Dependencies:
        config settings: reverse, sourcedb_type, destdb_type
        globals: s_drupal_readonly, d_drupal_readonly
        functions: drupal_readonly_status()
        modules: sys, nori
    """
    global d_drupal_readonly
    global s_drupal_readonly
    if not nori.core.cfg['reverse']:
        s_type = nori.core.cfg['sourcedb_type']
        d_type = nori.core.cfg['destdb_type']
    else:
        s_type = nori.core.cfg['destdb_type']
        d_type = nori.core.cfg['sourcedb_type']
    if s_type == 'drupal':
        s_drupal_readonly = drupal_readonly_status(s_db, s_cur, None)
        if s_drupal_readonly is None:
            nori.core.email_logger.error("Error: can't set Drupal site read-only; exiting.")
            sys.exit(nori.core.exitvals['drupal']['num'])
        else:
            drupal_readonly_status(s_db, s_cur, True)
    if d_type == 'drupal':
        d_drupal_readonly = drupal_readonly_status(d_db, d_cur, None)
        if d_drupal_readonly is None:
            nori.core.email_logger.error("Error: can't set Drupal site read-only; exiting.")
            sys.exit(nori.core.exitvals['drupal']['num'])
        else:
            drupal_readonly_status(d_db, d_cur, True)
    return


def post_action_drupal_readonly(s_db, s_cur, d_db, d_cur):
    """
    Wrapper around drupal_readonly_status() for post-action callbacks.
    Parameters:
        s_db: the source-database connection object to use
        s_cur: the source-database cursor object to use
        d_db: the destination-database connection object to use
        d_cur: the destination-database cursor object to use
    Dependencies:
        globals: s_drupal_readonly, d_drupal_readonly
        functions: drupal_readonly_status()
        modules: nori
    """
    if s_drupal_readonly is not None:
        if not drupal_readonly_status(s_db, s_cur, s_drupal_readonly):
            nori.core.email_logger.error("Warning: can't restore Drupal site's read-only status;\nmanual intervention is probably required.")
    if d_drupal_readonly is not None:
        if not drupal_readonly_status(d_db, d_cur, d_drupal_readonly):
            nori.core.email_logger.error("Warning: can't restore Drupal site's read-only status;\nmanual intervention is probably required.")
    return


def clear_drupal_cache(db_obj, db_cur):
    """
    Clear all caches in a Drupal database.
    Parameters:
        db_obj: the database connection object to use
        db_cur: the database cursor object to use
    """
    ret = db_obj.get_table_list(db_cur)
    if not ret[0]:
        return False
    for table in ret[1]:
        if table[0].startswith('cache'):
            ret = db_obj.execute(db_cur, ('DELETE FROM {0};').format(table[0]), has_results=False)
            if not ret:
                return False

    return True


def check_key_list_match(key_mode, key_list, num_keys, row):
    """
    Search for a match between a key list and a row.
    Returns True or False.
    Parameters:
        key_mode: the per-template or global key mode ('all', 'include',
                  or 'exclude')
        key_list: the per-template or global key list to check for a
                  match
        num_keys: the number of 'key' (as opposed to 'value') elements
                  in the row
        row: a row tuple from the database results, as modified by the
             transform function
        (see the description of the templates setting, above, for more
        details)
    Dependencies:
        modules: nori
    """
    if key_mode == 'all':
        return True
    found = False
    for k_match in key_list:
        k_match = nori.scalar_to_tuple(k_match)
        if len(k_match) > num_keys:
            nori.core.email_logger.error(('\nError: key list entry has more elements than the actual row in call to\ncheck_key_list_match(); call was (in expanded notation):\n\ncheck_key_list_match(key_mode={0},\n                     key_list={1},\n                     key_cv={2},\n                     row={3})\n\nExiting.').format(*map(nori.pps, [key_mode, key_list, key_cv, row])))
            sys.exit(nori.core.exitvals['internal']['num'])
        for i, match_val in enumerate(k_match):
            if row[i] != match_val:
                break
            if i == len(k_match) - 1:
                found = True

        if found:
            break

    if key_mode == 'include':
        return found
    if key_mode == 'exclude':
        return not found


def key_filter(template_index, num_keys, row):
    """
    Determine whether to act on a key from the database.

    Returns True (act) or False (don't act).

    Parameters:
        template_index: the index of the relevant template in the
                        templates setting
        num_keys: the number of 'key' (as opposed to 'value') elements
                  in the row
        row: a row tuple from the database results, as modified by the
             transform function
        (see the description of the templates setting, above, for more
        details)

    Dependencies:
        config settings: templates, key_mode, key_list
        globals: T_KEY_MODE_IDX, T_KEY_LIST_IDX
        functions: check_key_list_match()
        modules: nori

    """
    template = nori.core.cfg['templates'][template_index]
    if nori.core.cfg['key_mode'] == 'all' and template[T_KEY_MODE_IDX] == 'all':
        return True
    if not check_key_list_match(nori.core.cfg['key_mode'], nori.core.cfg['key_list'], num_keys, row):
        return False
    if not check_key_list_match(template[T_KEY_MODE_IDX], template[T_KEY_LIST_IDX], num_keys, row):
        return False
    return True


def key_value_copy(source_data, dest_key_cv, dest_value_cv):
    """
    Transfer the values from a source DB row to the dest DB k/v seqs.
    The source_data tuple and (dest_key_cv + dest_value_cv) must be the
    same length.
    Returns a tuple of (key_cv, value_cv).
    Parameters:
        source_data: a row tuple from the source database results, as
                     modified by the transform function
        dest_key_cv: the key cv sequence from the template for the
                     destination database
        dest_value_cv: the value cv sequence from the template for the
                       destination database
    """
    new_dest_key_cv = []
    new_dest_value_cv = []
    num_keys = len(dest_key_cv)
    for i, data_val in enumerate(source_data):
        if i < num_keys:
            new_dest_key_cv.append((
             dest_key_cv[i][0], dest_key_cv[i][1], data_val))
        else:
            new_dest_value_cv.append((
             dest_value_cv[(i - num_keys)][0],
             dest_value_cv[(i - num_keys)][1], data_val))

    return (
     new_dest_key_cv, new_dest_value_cv)


def log_diff(template_index, exists_in_source, source_row, exists_in_dest, dest_row):
    """
    Record a difference between the two databases.
    Note that 'source' and 'dest' refer to the actual source and
    destination databases, after applying the value of the 'reverse'
    setting.
    Returns a tuple: (the key used in diff_dict, the index added to
                      the list).
    Parameters:
        template_index: the index of the relevant template in the
                        templates setting
        exists_in_source: True if the relevant key exists in the source
                          database, otherwise False
        source_row: a tuple of (number of key columns, transformed
                    results tuple from the source DB's query function)
        exists_in_dest: True if the relevant key exists in the
                        destination database, otherwise False
        dest_row: a tuple of (number of key columns, transformed results
                  tuple from the destination DB's query function)
    Dependencies:
        config settings: templates, report_order
        globals: diff_dict, T_NAME_IDX
        modules: nori
    """
    template = nori.core.cfg['templates'][template_index]
    if nori.core.cfg['report_order'] == 'template':
        if template_index not in diff_dict:
            diff_dict[template_index] = []
        diff_dict[template_index].append((exists_in_source, source_row,
         exists_in_dest, dest_row, None))
        diff_k = template_index
        diff_i = len(diff_dict[template_index]) - 1
    elif nori.core.cfg['report_order'] == 'keys':
        keys_str = ()
        if source_row is not None:
            num_keys = source_row[0]
            source_data = source_row[1]
            keys_tuple = source_data[0:num_keys]
        elif dest_row is not None:
            num_keys = dest_row[0]
            dest_data = dest_row[1]
            keys_tuple = dest_data[0:num_keys]
        if keys_tuple not in diff_dict:
            diff_dict[keys_tuple] = []
        diff_dict[keys_tuple].append((template_index, exists_in_source,
         source_row, exists_in_dest, dest_row,
         None))
        diff_k = keys_tuple
        diff_i = len(diff_dict[keys_tuple]) - 1
    nori.core.status_logger.info(('Diff found for template {0} ({1}):\nS: {2}\nD: {3}').format(template_index, nori.pps(template[T_NAME_IDX]), nori.pps(source_row[1]) if exists_in_source else '[no match in source database]', nori.pps(dest_row[1]) if exists_in_dest else '[no match in destination database]'))
    return (
     diff_k, diff_i)


def update_diff(diff_k, diff_i, changed):
    """
    Mark a diff as updated.
    Parameters:
        diff_k: the key used in diff_dict
        diff_i: the index in the list
        changed: can be True (fully changed), False (partly changed), or
                 None (unchanged)
    Dependencies:
        config settings: report_order
        globals: diff_dict
        modules: nori
    """
    diff_t = diff_dict[diff_k][diff_i]
    if nori.core.cfg['report_order'] == 'template':
        diff_dict[diff_k][diff_i] = (
         diff_t[0], diff_t[1], diff_t[2],
         diff_t[3], changed)
    elif nori.core.cfg['report_order'] == 'keys':
        diff_dict[diff_k][diff_i] = (
         diff_t[0], diff_t[1], diff_t[2],
         diff_t[3], diff_t[4], changed)


def render_diff_report():
    """
    Render a summary of the diffs found and/or changed.
    Returns a string.
    Dependencies:
        config settings: action, templates, report_order
        globals: diff_dict, T_NAME_IDX
        modules: nori
    """
    if nori.core.cfg['action'] == 'diff':
        diff_report = ' Diff Report '
    elif nori.core.cfg['action'] == 'sync':
        diff_report = ' Diff / Sync Report '
    diff_report = '#' * len(diff_report) + '\n' + diff_report + '\n' + '#' * len(diff_report) + '\n\n'
    if nori.core.cfg['report_order'] == 'template':
        for template_index in diff_dict:
            template = nori.core.cfg['templates'][template_index]
            section_header = ('Template {0} ({1}):').format(template_index, nori.pps(template[T_NAME_IDX]))
            section_header += '\n' + '-' * len(section_header) + '\n\n'
            diff_report += section_header
            for diff_t in diff_dict[template_index]:
                exists_in_source = diff_t[0]
                source_row = diff_t[1]
                exists_in_dest = diff_t[2]
                dest_row = diff_t[3]
                has_been_changed = diff_t[4]
                if exists_in_source:
                    source_str = nori.pps(source_row[1])
                elif exists_in_source is None:
                    source_str = '[no key match in source database]'
                else:
                    source_str = '[no match in source database]'
                if exists_in_dest:
                    dest_str = nori.pps(dest_row[1])
                elif exists_in_dest is None:
                    dest_str = '[no key match in destination database]'
                else:
                    dest_str = '[no match in destination database]'
                if has_been_changed is None:
                    changed_str = 'unchanged'
                elif not has_been_changed:
                    changed_str = 'partially changed - action may be needed!'
                else:
                    changed_str = 'changed'
                diff_report += ('Source: {0}\nDest: {1}\nStatus: {2}\n\n').format(source_str, dest_str, changed_str)

            diff_report += '\n'

    elif nori.core.cfg['report_order'] == 'keys':
        for key_str in diff_dict:
            section_header = ('Key string {0}:').format(nori.pps(key_str))
            section_header += '\n' + '-' * len(section_header) + '\n\n'
            diff_report += section_header
            for diff_t in diff_dict[key_str]:
                template_index = diff_t[0]
                exists_in_source = diff_t[1]
                source_row = diff_t[2]
                exists_in_dest = diff_t[3]
                dest_row = diff_t[4]
                has_been_changed = diff_t[5]
                template = nori.core.cfg['templates'][template_index]
                if exists_in_source:
                    num_keys = source_row[0]
                    source_data = source_row[1]
                    source_str = nori.pps(source_data[num_keys:])
                elif exists_in_source is None:
                    source_str = '[no key match in source database]'
                else:
                    source_str = '[no match in source database]'
                if exists_in_dest:
                    num_keys = dest_row[0]
                    dest_data = dest_row[1]
                    dest_str = nori.pps(dest_data[num_keys:])
                elif exists_in_dest is None:
                    dest_str = '[no key match in destination database]'
                else:
                    dest_str = '[no match in destination database]'
                if has_been_changed is None:
                    changed_str = 'unchanged'
                elif not has_been_changed:
                    changed_str = 'partially changed - action may be needed!'
                else:
                    changed_str = 'changed'
                diff_report += ('Template: {0}\nSource: {1}\nDest: {2}\nStatus: {3}\n\n').format(template[T_NAME_IDX], source_str, dest_str, changed_str)

            diff_report += '\n'

    return diff_report.strip()


def do_diff_report():
    """
    Email and log a summary of the diffs found and/or changed.
    Dependencies:
        globals: email_reporter
        functions: render_diff_report()
    """
    diff_report = render_diff_report()
    if email_reporter:
        email_reporter.error(diff_report + '\n\n\n' + '#' * 76)
    nori.core.output_logger.info('\n\n' + diff_report + '\n\n')


def do_sync(t_index, s_row, d_db, d_cur, diff_k, diff_i):
    """
    Actually sync data to the destination database.

    Returns a boolean indicating if the global destdb callback is
    needed.

    Parameters:
        t_index: the index of the relevant template in the templates
                 setting
        s_row: a tuple of (number of keys, transformed source data
               tuple)
        d_db: the connection object for the destination database
        d_cur: the cursor object for the destination database
        diff_k: the key of the diff list within diff_dict
        diff_i: the index of the diff within the list indicated by
                diff_k

    Dependencies:
        config settings: reverse, templates
        globals: (some of) T_*
        functions: generic_db_query(), drupal_db_query(),
                   key_value_copy(), update_diff()
        modules: copy, nori
        Python: 2.0/3.2, for callable()

    """
    template = nori.core.cfg['templates'][t_index]
    t_multiple = template[T_MULTIPLE_IDX]
    if not nori.core.cfg['reverse']:
        dest_type = nori.core.cfg['destdb_type']
        dest_func = template[T_D_QUERY_FUNC_IDX]
        dest_args = template[T_D_QUERY_ARGS_IDX][0]
        dest_kwargs = template[T_D_QUERY_ARGS_IDX][1]
        dest_change_func = template[T_D_CHANGE_FUNC_IDX]
    else:
        dest_type = nori.core.cfg['sourcedb_type']
        dest_func = template[T_S_QUERY_FUNC_IDX]
        dest_args = template[T_S_QUERY_ARGS_IDX][0]
        dest_kwargs = template[T_S_QUERY_ARGS_IDX][1]
        dest_change_func = template[T_S_CHANGE_FUNC_IDX]
    mode = 'insert' if t_multiple else 'update'
    if dest_func is None:
        if dest_type == 'generic':
            dest_func = generic_db_query
        elif dest_type == 'drupal':
            dest_func = drupal_db_query
    new_key_cv, new_value_cv = key_value_copy(s_row[1], dest_kwargs['key_cv'], dest_kwargs['value_cv'])
    new_dest_kwargs = copy.copy(dest_kwargs)
    new_dest_kwargs['key_cv'] = new_key_cv
    new_dest_kwargs['value_cv'] = new_value_cv
    if t_multiple:
        nori.core.status_logger.info('Inserting into destination database...')
    else:
        nori.core.status_logger.info('Updating destination database...')
    global_callback_needed = False
    fulls, partials, failures = dest_func(db_obj=d_db, db_cur=d_cur, mode=mode, *dest_args, **new_dest_kwargs)
    if failures == 0 and partials == 0:
        status = True
        nori.core.status_logger.info(mode.capitalize() + ' succeeded.')
    elif fulls == 0 and partials == 0:
        status = None
        nori.core.status_logger.info(mode.capitalize() + ' failed.')
    else:
        status = False
        nori.core.status_logger.info(mode.capitalize() + ' partially succeeded.')
    if status is not None:
        global_callback_needed = True
        update_diff(diff_k, diff_i, status)
    if not (dest_change_func and callable(dest_change_func)):
        return global_callback_needed
    else:
        if status is None:
            nori.core.status_logger.info('Skipping change callback for this template.')
            return global_callback_needed
        nori.core.status_logger.info('Calling change callback for this template...')
        ret = dest_change_func(template, s_row)
        nori.core.status_logger.info('Callback complete.' if ret else 'Callback failed.')
        return global_callback_needed


def do_diff_sync(t_index, s_rows, d_rows, d_db, d_cur):
    """
    Diff, and if necessary sync, sets of rows from the two databases.

    Returns a boolean indicating if the global destdb callback is
    needed.

    Parameters:
        t_index: the index of the relevant template in the templates
                 setting
        s_rows: a sequence of tuples, each in the format (number of
                keys, transformed row tuple from the source database's
                query results)
        d_rows: a sequence of tuples, each in the format (number of
                keys, transformed row tuple from the destination
                database's query results)
        d_db: the connection object for the destination database
        d_cur: the cursor object for the destination database

    Dependencies:
        config settings: action, bidir, templates
        globals: T_MULTIPLE_IDX
        functions: log_diff(), do_sync()
        modules: nori

    """
    template = nori.core.cfg['templates'][t_index]
    t_multiple = template[T_MULTIPLE_IDX]
    global_callback_needed = False
    for s_row in s_rows:
        s_found = False
        s_num_keys = s_row[0]
        s_data = s_row[1]
        s_keys = s_data[0:s_num_keys]
        s_vals = s_data[s_num_keys:]
        if nori.core.cfg['bidir']:
            d_found = []
        for di, d_row in enumerate(d_rows):
            d_num_keys = d_row[0]
            d_data = d_row[1]
            d_keys = d_data[0:d_num_keys]
            d_vals = d_data[d_num_keys:]
            if not t_multiple:
                if d_keys == s_keys:
                    s_found = True
                    if nori.core.cfg['bidir']:
                        d_found.append(di)
                    if d_vals != s_vals:
                        diff_k, diff_i = log_diff(t_index, True, s_row, True, d_row)
                        if nori.core.cfg['action'] == 'sync':
                            if do_sync(t_index, s_row, d_db, d_cur, diff_k, diff_i):
                                global_callback_needed = True
                    break
            elif d_keys == s_keys and d_vals == s_vals:
                s_found = True
                if nori.core.cfg['bidir']:
                    d_found.append(di)
                break

        if not s_found:
            log_diff(t_index, True, s_row, False, None)
            if t_multiple:
                if do_sync(t_index, s_row, d_db, d_cur, diff_k, diff_i):
                    global_callback_needed = True

    if nori.core.cfg['bidir']:
        for di, d_row in enumerate(d_rows):
            if di not in d_found:
                log_diff(t_index, False, None, True, d_row)

    return global_callback_needed


def run_mode_hook():
    """
    Do the actual work.

    Dependencies:
        config settings: reverse, bidir, templates, template_mode,
                         template_list, sourcedb_change_callback,
                         sourcedb_change_callback_args,
                         destdb_change_callback,
                         destdb_change_callback_args
        globals: (some of) T_*, diff_dict, sourcedb, destdb
        functions: generic_db_query(), drupal_db_query(), key_filter(),
                   log_diff(), do_diff_report(), do_diff_sync(), (functions
                   in templates), (global callback functions)
        modules: nori
        Python: 2.0/3.2, for callable()

    """
    if not nori.core.cfg['reverse']:
        s_db = sourcedb
        source_type = nori.core.cfg['sourcedb_type']
        d_db = destdb
        dest_type = nori.core.cfg['destdb_type']
    else:
        s_db = destdb
        source_type = nori.core.cfg['destdb_type']
        d_db = sourcedb
        dest_type = nori.core.cfg['sourcedb_type']
    s_db.connect()
    s_db.autocommit(True)
    s_cur = s_db.cursor(False)
    d_db.connect()
    d_db.autocommit(True)
    d_cur = d_db.cursor(False)
    pa = nori.core.cfg['pre_action_callback']
    pa_arg_t = nori.core.cfg['pre_action_callback_args']
    if pa and callable(pa):
        nori.core.status_logger.info('Calling pre-action callback...')
        ret = pa(s_db=s_db, s_cur=s_cur, d_db=d_db, d_cur=d_cur, *pa_arg_t[0], **pa_arg_t[1])
        nori.core.status_logger.info('Callback complete.' if ret else 'Callback failed.')
    for t_index, template in enumerate(nori.core.cfg['templates']):
        t_name = template[T_NAME_IDX]
        t_multiple = template[T_MULTIPLE_IDX]
        if not nori.core.cfg['reverse']:
            source_func = template[T_S_QUERY_FUNC_IDX]
            source_args = template[T_S_QUERY_ARGS_IDX][0]
            source_kwargs = template[T_S_QUERY_ARGS_IDX][1]
            to_dest_func = template[T_TO_D_FUNC_IDX]
            dest_func = template[T_D_QUERY_FUNC_IDX]
            dest_args = template[T_D_QUERY_ARGS_IDX][0]
            dest_kwargs = template[T_D_QUERY_ARGS_IDX][1]
            to_source_func = template[T_TO_S_FUNC_IDX]
        else:
            source_func = template[T_D_QUERY_FUNC_IDX]
            source_args = template[T_D_QUERY_ARGS_IDX][0]
            source_kwargs = template[T_D_QUERY_ARGS_IDX][1]
            to_dest_func = template[T_TO_S_FUNC_IDX]
            dest_func = template[T_S_QUERY_FUNC_IDX]
            dest_args = template[T_S_QUERY_ARGS_IDX][0]
            dest_kwargs = template[T_S_QUERY_ARGS_IDX][1]
            to_source_func = template[T_TO_D_FUNC_IDX]
        if nori.cfg['template_mode'] == 'include' and t_name not in nori.cfg['template_list']:
            continue
        else:
            if nori.cfg['template_mode'] == 'exclude' and t_name in nori.cfg['template_list']:
                continue
            if source_func is None:
                if source_type == 'generic':
                    source_func = generic_db_query
                elif source_type == 'drupal':
                    source_func = drupal_db_query
            if dest_func is None:
                if dest_type == 'generic':
                    dest_func = generic_db_query
                elif dest_type == 'drupal':
                    dest_func = drupal_db_query
            s_rows_raw = source_func(db_obj=s_db, db_cur=s_cur, mode='read', *source_args, **source_kwargs)
            if s_rows_raw is None:
                break
            s_rows = []
            for s_row_raw in s_rows_raw:
                if to_dest_func and callable(to_dest_func):
                    s_num_keys, s_row = to_dest_func(template, s_row_raw)
                else:
                    s_num_keys = len(source_kwargs['key_cv'])
                    s_row = s_row_raw
                if not key_filter(t_index, s_num_keys, s_row):
                    continue
                s_rows.append((s_num_keys, s_row))

            d_rows_raw = dest_func(db_obj=d_db, db_cur=d_cur, mode='read', *dest_args, **dest_kwargs)
            if d_rows_raw is None:
                break
            d_rows = []
            for d_row_raw in d_rows_raw:
                if to_source_func and callable(to_source_func):
                    d_num_keys, d_row = to_source_func(template, d_row_raw)
                else:
                    d_num_keys = len(dest_kwargs['key_cv'])
                    d_row = d_row_raw
                if not key_filter(t_index, d_num_keys, d_row):
                    continue
                d_rows.append((d_num_keys, d_row))

        global_callback_needed = False
        if not t_multiple:
            if do_diff_sync(t_index, s_rows, d_rows, d_db, d_cur):
                global_callback_needed = True
        else:
            s_row_groups = {}
            for s_row in s_rows:
                s_num_keys = s_row[0]
                s_data = s_row[1]
                if s_data[0:s_num_keys] not in s_row_groups:
                    s_row_groups[s_data[0:s_num_keys]] = []
                s_row_groups[s_data[0:s_num_keys]].append(s_row)

            d_row_groups = {}
            for d_row in d_rows:
                d_num_keys = d_row[0]
                d_data = d_row[1]
                if d_data[0:d_num_keys] not in d_row_groups:
                    d_row_groups[d_data[0:d_num_keys]] = []
                d_row_groups[d_data[0:d_num_keys]].append(d_row)

            d_keys_found = []
            for s_keys in s_row_groups:
                if s_keys in d_row_groups:
                    d_keys_found.append(s_keys)
                    if do_diff_sync(t_index, s_row_groups[s_keys], d_row_groups[s_keys], d_db, d_cur):
                        global_callback_needed = True
                else:
                    for s_row in s_row_groups[s_keys]:
                        log_diff(t_index, True, s_row, None, None)

            if nori.core.cfg['bidir']:
                for d_keys in d_row_groups:
                    if d_keys not in d_keys_found:
                        for d_row in d_row_groups[d_keys]:
                            log_diff(t_index, None, None, True, d_row)

    if global_callback_needed:
        if not nori.core.cfg['reverse']:
            cb = nori.core.cfg['destdb_change_callback']
            if cb and callable(cb):
                cb_arg_t = nori.core.cfg['destdb_change_callback_args']
        else:
            cb = nori.core.cfg['sourcedb_change_callback']
            if cb and callable(cb):
                cb_arg_t = nori.core.cfg['sourcedb_change_callback_args']
        if cb and callable(cb):
            nori.core.status_logger.info('Calling global change callback...')
            ret = cb(db_obj=d_db, db_cur=d_cur, *cb_arg_t[0], **cb_arg_t[1])
            nori.core.status_logger.info('Callback complete.' if ret else 'Callback failed.')
    pa = nori.core.cfg['post_action_callback']
    pa_arg_t = nori.core.cfg['post_action_callback_args']
    if pa and callable(pa):
        nori.core.status_logger.info('Calling post-action callback...')
        ret = pa(s_db=s_db, s_cur=s_cur, d_db=d_db, d_cur=d_cur, *pa_arg_t[0], **pa_arg_t[1])
        nori.core.status_logger.info('Callback complete.' if ret else 'Callback failed.')
    if diff_dict:
        do_diff_report()
    d_db.close_cursor(d_cur)
    d_db.close()
    s_db.close_cursor(s_cur)
    s_db.close()
    return


def main():
    nori.core.validate_config_hooks.append(validate_config)
    nori.core.process_config_hooks.append(init_reporting)
    nori.core.run_mode_hooks.append(run_mode_hook)
    nori.process_command_line()


if __name__ == '__main__':
    main()