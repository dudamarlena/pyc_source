# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/utils.py
# Compiled at: 2019-08-21 04:17:01
# Size of source mod 2**32: 4855 bytes
import argparse, json, traceback, sys
from .job import Job
_global_args = {}

def makeOptions(sc, py_obj):
    if isinstance(py_obj, dict):
        json_string = json.dumps(py_obj)
    else:
        if isinstance(py_obj, basestring):
            json_string = py_obj
        else:
            raise TypeError('Unexpected type ' + str(type(py_obj)) + ' in makeOptions')
    return sc._jvm.JsonOptions(json_string)


def _call_site(sc, call_site, info):
    return sc._jvm.CallSite(call_site, info)


def _as_java_list(sc, scala_seq_obj):
    return sc._jvm.GluePythonUtils.seqAsJava(scala_seq_obj)


def _as_scala_option(sc, some_val):
    return sc._jvm.GluePythonUtils.constructOption(some_val)


def _as_resolve_choiceOption(sc, choice_option_str):
    return sc._jvm.GluePythonUtils.constructChoiceOption(choice_option_str)


def callsite():
    return ''.join(traceback.format_list(traceback.extract_stack()[:-2]))


class GlueArgumentError(Exception):
    pass


class GlueArgumentParser(argparse.ArgumentParser):

    def error(self, msg):
        raise GlueArgumentError(msg)


def getResolvedOptions(args, options):
    parser = GlueArgumentParser()
    if Job.continuation_options()[0][2:] in options:
        raise RuntimeError('Using reserved arguments ' + Job.continuation_options()[0][2:])
    if Job.job_bookmark_options()[0][2:] in options:
        raise RuntimeError('Using reserved arguments ' + Job.job_bookmark_options()[0][2:])
    parser.add_argument((Job.job_bookmark_options()[0]), choices=(Job.job_bookmark_options()[1:]), required=False)
    parser.add_argument((Job.continuation_options()[0]), choices=(Job.continuation_options()[1:]), required=False)
    for option in Job.id_params()[1:]:
        if option in options:
            raise RuntimeError('Using reserved arguments ' + option)
        parser.add_argument(option, required=False)

    if Job.encryption_type_options()[0] in options:
        raise RuntimeError('Using reserved arguments ' + Job.encryption_type_options()[0])
    parser.add_argument((Job.encryption_type_options()[0]), choices=(Job.encryption_type_options()[1:]))
    options = [opt for opt in options if opt not in {'TempDir', 'RedshiftTempDir'}]
    parser.add_argument('--RedshiftTempDir', required=False)
    parser.add_argument('--TempDir', required=False)
    for option in options:
        parser.add_argument(('--' + option), required=True)

    parsed, extra = parser.parse_known_args(args[1:])
    parsed_dict = vars(parsed)
    if 'TempDir' in parsed_dict and parsed_dict['TempDir'] is not None:
        parsed_dict['RedshiftTempDir'] = parsed_dict['TempDir']
    else:
        if 'RedshiftTempDir' in parsed:
            if parsed_dict['RedshiftTempDir'] is not None:
                parsed_dict['TempDir'] = parsed_dict['RedshiftTempDir']
        bookmark_value = parsed_dict.pop('continuation_option', None)
        if 'job_bookmark_option' not in parsed_dict or parsed_dict['job_bookmark_option'] is None:
            if bookmark_value is None:
                bookmark_value = Job.job_bookmark_options()[3]
            else:
                option_index = Job.continuation_options().index(bookmark_value)
                bookmark_value = Job.job_bookmark_options()[option_index]
            parsed_dict['job_bookmark_option'] = bookmark_value
        _global_args.update(parsed_dict)
        return parsed_dict