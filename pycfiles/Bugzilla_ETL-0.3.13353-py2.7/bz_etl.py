# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\bz_etl.py
# Compiled at: 2013-12-18 19:56:33
import gc, pkg_resources
from bzETL.util.maths import Math
from bzETL.util.timer import Timer
from bzETL.util import struct
from bzETL.util.logs import Log
from bzETL.util.struct import Struct, nvl
from bzETL.util.files import File
from bzETL.util import startup
from bzETL.util.threads import Queue, Thread, AllThread, Lock, ThreadedQueue
from bzETL.util.cnv import CNV
from bzETL.util.elasticsearch import ElasticSearch
from bzETL.util.queries import Q
from bzETL.util.db import DB
from bzETL import parse_bug_history, transform_bugzilla, extract_bugzilla, alias_analysis
from extract_bugzilla import get_private_bugs, get_recent_private_attachments, get_recent_private_comments, get_comments, get_comments_by_id, get_recent_private_bugs, get_current_time, get_bugs, get_dependencies, get_flags, get_new_activities, get_bug_see_also, get_attachments, get_tracking_flags, get_keywords, get_cc, get_bug_groups, get_duplicates
from parse_bug_history import BugHistoryParser
db_cache_lock = Lock()
db_cache = []
comment_db_cache_lock = Lock()
comment_db_cache = []
get_stuff_from_bugzilla = [
 get_bugs,
 get_dependencies,
 get_flags,
 get_new_activities,
 get_bug_see_also,
 get_attachments,
 get_tracking_flags,
 get_keywords,
 get_cc,
 get_bug_groups,
 get_duplicates]

def etl_comments(db, es, param, please_stop):
    with comment_db_cache_lock:
        if not comment_db_cache:
            comment_db = DB(db)
            comment_db.begin()
            comment_db_cache.append(comment_db)
    with comment_db_cache_lock:
        Log.note('Read comments from database')
        comments = get_comments(comment_db_cache[0], param)
    with Timer('Write {{num}} comments to ElasticSearch', {'num': len(comments)}):
        es.extend({'id': c.comment_id, 'value': c} for c in comments)


def etl(db, output_queue, param, please_stop):
    """
    PROCESS RANGE, AS SPECIFIED IN param AND PUSH
    BUG VERSION RECORDS TO output_queue
    """
    with db_cache_lock:
        if not db_cache:
            for f in get_stuff_from_bugzilla:
                db = DB(db)
                db.begin()
                db_cache.append(db)

    db_results = Queue()
    with db_cache_lock:
        with AllThread() as (all):
            for i, f in enumerate(get_stuff_from_bugzilla):

                def process(target, db, param, please_stop):
                    db_results.extend(target(db, param))

                all.add(process, f, db_cache[i], param.copy())

    db_results.add(Thread.STOP)
    sorted = Q.sort(db_results, [
     'bug_id',
     '_merge_order', {'field': 'modified_ts', 'sort': -1},
     'modified_by'])
    process = BugHistoryParser(param, output_queue)
    for s in sorted:
        process.processRow(s)

    process.processRow(struct.wrap({'bug_id': parse_bug_history.STOP_BUG, '_merge_order': 1}))


def run_both_etl(db, output_queue, es_comments, param):
    comment_thread = Thread.run('etl comments', etl_comments, db, es_comments, param)
    process_thread = Thread.run('etl', etl, db, output_queue, param)
    comment_thread.join()
    process_thread.join()


def setup_es(settings, db, es, es_comments):
    """
    SETUP ES CONNECTIONS TO REFLECT IF WE ARE RESUMING, INCREMENTAL, OR STARTING OVER
    """
    current_run_time = get_current_time(db)
    if File(settings.param.first_run_time).exists and File(settings.param.last_run_time).exists:
        last_run_time = long(File(settings.param.last_run_time).read())
        if not es:
            es = ElasticSearch(settings.es)
            es_comments = ElasticSearch(settings.es_comments)
    elif File(settings.param.first_run_time).exists:
        try:
            last_run_time = 0
            current_run_time = long(File(settings.param.first_run_time).read())
            if not es:
                if not settings.es.alias:
                    settings.es.alias = settings.es.index
                    temp = ElasticSearch(settings.es).get_proto(settings.es.alias)
                    settings.es.index = temp[(-1)]
                es = ElasticSearch(settings.es)
                es.set_refresh_interval(1)
                if not settings.es_comments.alias:
                    settings.es_comments.alias = settings.es_comments.index
                    settings.es_comments.index = ElasticSearch(settings.es_comments).get_proto(settings.es_comments.alias)[(-1)]
                es_comments = ElasticSearch(settings.es_comments)
        except Exception as e:
            Log.warning('can not resume ETL, restarting', e)
            File(settings.param.first_run_time).delete()
            return setup_es(settings, db, es, es_comments)

    else:
        last_run_time = 0
        if not es:
            schema = File(settings.es.schema_file).read()
            if transform_bugzilla.USE_ATTACHMENTS_DOT:
                schema = schema.replace('attachments_', 'attachments.')
            if not settings.es.alias:
                settings.es.alias = settings.es.index
                settings.es.index = ElasticSearch.proto_name(settings.es.alias)
            es = ElasticSearch.create_index(settings.es, schema)
            if not settings.es_comments.alias:
                settings.es_comments.alias = settings.es_comments.index
                settings.es_comments.index = ElasticSearch.proto_name(settings.es_comments.alias)
            es_comments = ElasticSearch.create_index(settings.es_comments, File(settings.es_comments.schema_file).read())
        File(settings.param.first_run_time).write(unicode(CNV.datetime2milli(current_run_time)))
    return (current_run_time, es, es_comments, last_run_time)


def incremental_etl(settings, param, db, es, es_comments, output_queue):
    private_bugs = get_private_bugs(db, param)
    es.delete_record({'terms': {'bug_id': private_bugs}})
    possible_public_bugs = get_recent_private_bugs(db, param)
    possible_public_bugs = set(Q.select(possible_public_bugs, 'bug_id'))
    private_attachments = get_recent_private_attachments(db, param)
    bugs_to_refresh = set(Q.select(private_attachments, 'bug_id'))
    es.delete_record({'terms': {'bug_id': bugs_to_refresh}})
    bug_list = (possible_public_bugs | bugs_to_refresh) - private_bugs
    if bug_list:
        refresh_param = param.copy()
        refresh_param.bug_list = bug_list
        refresh_param.start_time = 0
        refresh_param.start_time_str = extract_bugzilla.milli2string(db, 0)
        try:
            etl(db, output_queue, refresh_param, please_stop=None)
        except Exception as e:
            Log.error('Problem with etl using parameters {{parameters}}', {'parameters': refresh_param}, e)

    private_comments = get_recent_private_comments(db, param)
    comment_list = set(Q.select(private_comments, 'comment_id')) | {0}
    es_comments.delete_record({'terms': {'comment_id': comment_list}})
    changed_comments = get_comments_by_id(db, comment_list, param)
    es_comments.extend({'id': c.comment_id, 'value': c} for c in changed_comments)
    with Timer('time to get bug list'):
        if param.allow_private_bugs:
            bug_list = Q.select(db.query('\n                SELECT\n                    b.bug_id\n                FROM\n                    bugs b\n                WHERE\n                    delta_ts >= {{start_time_str}}\n            ', {'start_time_str': param.start_time_str}), 'bug_id')
        else:
            bug_list = Q.select(db.query('\n                SELECT\n                    b.bug_id\n                FROM\n                    bugs b\n                LEFT JOIN\n                    bug_group_map m ON m.bug_id=b.bug_id\n                WHERE\n                    delta_ts >= {{start_time_str}} AND\n                    m.bug_id IS NULL\n            ', {'start_time_str': param.start_time_str}), 'bug_id')
    if not bug_list:
        return
    else:
        with Thread.run('alias analysis', alias_analysis.main, settings=settings, bug_list=bug_list):
            param.bug_list = bug_list
            run_both_etl(**{'db': db, 
               'output_queue': output_queue, 
               'es_comments': es_comments, 
               'param': param.copy()})
        return


def full_etl(resume_from_last_run, settings, param, db, es, es_comments, output_queue):
    with Thread.run('alias_analysis', alias_analysis.main, settings=settings):
        end = nvl(settings.param.end, db.query('SELECT max(bug_id)+1 bug_id FROM bugs')[0].bug_id)
        start = nvl(settings.param.start, 0)
        if resume_from_last_run:
            start = nvl(settings.param.start, Math.floor(get_max_bug_id(es), settings.param.increment))
        for b in range(start, end, settings.param.increment):
            if settings.args.quick and b < end - settings.param.increment and b != 0:
                continue
            gc.collect()
            min, max = b, b + settings.param.increment
            try:
                with Timer('time to get bug list'):
                    if param.allow_private_bugs:
                        bug_list = Q.select(db.query('\n                            SELECT\n                                b.bug_id\n                            FROM\n                                bugs b\n                            WHERE\n                                delta_ts >= {{start_time_str}} AND\n                                ({{min}} <= b.bug_id AND b.bug_id < {{max}})\n                        ', {'min': min, 
                           'max': max, 
                           'start_time_str': param.start_time_str}), 'bug_id')
                    else:
                        bug_list = Q.select(db.query('\n                            SELECT\n                                b.bug_id\n                            FROM\n                                bugs b\n                            LEFT JOIN\n                                bug_group_map m ON m.bug_id=b.bug_id\n                            WHERE\n                                delta_ts >= {{start_time_str}} AND\n                                ({{min}} <= b.bug_id AND b.bug_id < {{max}}) AND\n                                m.bug_id IS NULL\n                        ', {'min': min, 
                           'max': max, 
                           'start_time_str': param.start_time_str}), 'bug_id')
                if not bug_list:
                    continue
                param.bug_list = bug_list
                run_both_etl(**{'db': db, 
                   'output_queue': output_queue, 
                   'es_comments': es_comments, 
                   'param': param.copy()})
            except Exception as e:
                Log.warning('Problem with dispatch loop in range [{{min}}, {{max}})', {'min': min, 
                   'max': max}, e)


def main(settings, es=None, es_comments=None):
    if not settings.param.allow_private_bugs and es and not es_comments:
        Log.error('Must have ES for comments')
    resume_from_last_run = File(settings.param.first_run_time).exists and not File(settings.param.last_run_time).exists
    try:
        try:
            with DB(settings.bugzilla) as (db):
                current_run_time, es, es_comments, last_run_time = setup_es(settings, db, es, es_comments)
                with ThreadedQueue(es, size=1000) as (output_queue):
                    param = Struct()
                    param.end_time = CNV.datetime2milli(get_current_time(db))
                    param.start_time = last_run_time - 60000
                    param.start_time_str = extract_bugzilla.milli2string(db, param.start_time)
                    param.alias_file = settings.param.alias_file
                    param.allow_private_bugs = settings.param.allow_private_bugs
                    if last_run_time > 0:
                        incremental_etl(settings, param, db, es, es_comments, output_queue)
                    else:
                        full_etl(resume_from_last_run, settings, param, db, es, es_comments, output_queue)
                    output_queue.add(Thread.STOP)
            if settings.es.alias:
                es.delete_all_but(settings.es.alias, settings.es.index)
                es.add_alias(settings.es.alias)
            if settings.es_comments.alias:
                es.delete_all_but(settings.es_comments.alias, settings.es_comments.index)
                es_comments.add_alias(settings.es_comments.alias)
            File(settings.param.last_run_time).write(unicode(CNV.datetime2milli(current_run_time)))
        except Exception as e:
            Log.error('Problem with main ETL loop', e)

    finally:
        try:
            close_db_connections()
        except Exception as e:
            pass

        try:
            es.set_refresh_interval(1)
        except Exception as e:
            pass


def get_max_bug_id(es):
    try:
        results = es.search({'query': {'filtered': {'query': {'match_all': {}}, 'filter': {'script': {'script': 'true'}}}}, 'from': 0, 
           'size': 0, 
           'sort': [], 'facets': {'0': {'statistical': {'field': 'bug_id'}}}})
        if results.facets['0'].count == 0:
            return 0
        return results.facets['0'].max
    except Exception as e:
        Log.error('Can not get_max_bug from {{host}}/{{index}}', {'host': es.settings.host, 
           'index': es.settings.index}, e)


def close_db_connections():
    globals()['db_cache'], temp = [], db_cache
    for db in temp:
        db.commit()
        db.close()

    globals()['comment_db_cache'], temp = [], comment_db_cache
    for db in temp:
        db.commit()
        db.close()


def start():
    with startup.SingleInstance():
        try:
            try:
                settings = startup.read_settings(defs=[
                 {'name': [
                           '--quick', '--fast'], 
                    'help': 'use this to process the first and last block, useful for testing the config settings before doing a full run', 
                    'action': 'store_true', 
                    'dest': 'quick'},
                 {'name': [
                           '--restart', '--reset', '--redo'], 
                    'help': 'use this to force a reprocessing of all data', 
                    'action': 'store_true', 
                    'dest': 'restart'}])
                if settings.args.restart:
                    for l in struct.listwrap(settings.debug.log):
                        if l.filename:
                            File(l.filename).parent.delete()

                    File(settings.param.first_run_time).delete()
                    File(settings.param.last_run_time).delete()
                Log.start(settings.debug)
                d = pkg_resources.Distribution(project_name='Bugzilla-ETL', version='0.3.13353')
                filename = pkg_resources.resource_filename(__name__, 'resources/json/bugzilla_aliases.json')
                Log.note('alias file at:{{filename}}', {'filename': filename})
                main(settings)
            except Exception as e:
                Log.note('Done ETL')
                Log.error('Can not start', e)

        finally:
            Log.stop()


if __name__ == '__main__':
    start()