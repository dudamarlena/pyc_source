# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\extract_bugzilla.py
# Compiled at: 2013-12-18 14:05:11
from bzETL.parse_bug_history import MAX_TIME
from bzETL.util.cnv import CNV
from bzETL.util.db import SQL
from bzETL.util.logs import Log
from bzETL.util.queries import Q
from bzETL.util.struct import Struct, Null
SCREENED_FIELDDEFS = [
 19,
 24,
 42,
 45,
 56,
 64,
 74,
 83]
MIXED_CASE = [
 19,
 24]
PRIVATE_ATTACHMENT_FIELD_ID = 65
PRIVATE_COMMENTS_FIELD_ID = 82
PRIVATE_BUG_GROUP_FIELD_ID = 66
bugs_columns = Null

def get_current_time(db):
    """
    RETURN GMT TIME
    """
    output = db.query('\n        SELECT\n            UNIX_TIMESTAMP(now()) `value`\n        ')[0].value
    return CNV.unix2datetime(output)


def milli2string(db, value):
    """
    CONVERT GMT MILLI TO BUGZILLA DATETIME STRING
    """
    value = max(value, 0)
    output = db.query("\n        SELECT\n            CAST(CONVERT_TZ(FROM_UNIXTIME({{start_time}}/1000), 'UTC', 'US/Pacific') AS CHAR) `value`\n        ", {'start_time': value})[0].value
    return output


def get_bugs_table_columns(db, schema_name):
    return db.query("\n        SELECT\n            column_name,\n            column_type\n        FROM\n            information_schema.columns\n        WHERE\n            table_schema={{schema}} AND\n            table_name='bugs' AND\n            column_name NOT IN (\n                'bug_id',       #EXPLICIT\n                'delta_ts',     #NOT NEEDED\n                'lastdiffed',   #NOT NEEDED\n                'creation_ts',  #EXPLICIT\n                'reporter',     #EXPLICIT\n                'assigned_to',  #EXPLICIT\n                'qa_contact',   #EXPLICIT\n                'product_id',   #EXPLICIT\n                'component_id', #EXPLICIT\n                'cclist_accessible',    #NOT NEEDED\n                'reporter_accessible',  #NOT NEEDED\n                'short_desc',           #NOT ALLOWED\n                'bug_file_loc',         #NOT ALLOWED\n                'deadline',             #NOT NEEDED\n                'estimated_time'       #NOT NEEDED\n\n            )\n    ", {'schema': schema_name})


def get_private_bugs(db, param):
    if param.allow_private_bugs:
        return {0}
    try:
        private_bugs = db.query('SELECT DISTINCT bug_id FROM bug_group_map')
        return set(Q.select(private_bugs, 'bug_id')) | {0}
    except Exception as e:
        Log.error('problem getting private bugs', e)


def get_recent_private_bugs(db, param):
    """
    GET ONLY BUGS THAT HAVE SWITCHED PRIVACY INDICATOR
    THIS LIST IS USED TO SIGNAL BUGS THAT NEED TOTAL RE-ETL
    """
    if param.allow_private_bugs:
        return []
    param.field_id = PRIVATE_BUG_GROUP_FIELD_ID
    try:
        return db.query('\n        SELECT\n            a.bug_id\n        FROM\n            bugs_activity a\n        WHERE\n            bug_when >= {{start_time_str}} AND\n            fieldid={{field_id}}\n        ', param)
    except Exception as e:
        Log.error('problem getting recent private attachments', e)


def get_recent_private_attachments(db, param):
    """
    GET ONLY RECENT ATTACHMENTS THAT HAVE SWITCHED PRIVACY INDICATOR
    THIS LIST IS USED TO SIGNAL BUGS THAT NEED TOTAL RE-ETL
    """
    if param.allow_private_bugs:
        return []
    param.field_id = PRIVATE_ATTACHMENT_FIELD_ID
    try:
        return db.query('\n        SELECT\n            a.attach_id,\n            a.bug_id\n        FROM\n            bugs_activity a\n        WHERE\n            bug_when >= {{start_time_str}} AND\n            fieldid={{field_id}}\n        ', param)
    except Exception as e:
        Log.error('problem getting recent private attachments', e)


def get_recent_private_comments(db, param):
    """
    GET COMMENTS THAT HAVE HAD THEIR PRIVACY INDICATOR CHANGED
    """
    if param.allow_private_bugs:
        return []
    param.field_id = PRIVATE_COMMENTS_FIELD_ID
    try:
        comments = db.query('\n            SELECT\n                a.comment_id,\n                a.bug_id\n            FROM\n                bugs_activity a\n            WHERE\n                bug_when >= {{start_time_str}} AND\n                fieldid={{field_id}}\n            ', param)
        return comments
    except Exception as e:
        Log.error('problem getting recent private attachments', e)


def get_bugs(db, param):
    try:
        if not bugs_columns:
            columns = get_bugs_table_columns(db, db.settings.schema)
            globals()['bugs_columns'] = columns

        def lower(col):
            if col.column_type.startswith('varchar'):
                return 'lower(' + db.quote_column(col.column_name) + ') ' + db.quote_column(col.column_name)
            else:
                return db.quote_column(col.column_name)

        param.bugs_columns = Q.select(bugs_columns, 'column_name')
        param.bugs_columns_SQL = SQL((',\n').join([ lower(c) for c in bugs_columns ]))
        param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
        if param.allow_private_bugs:
            param.sensitive_columns = SQL("\n                '<screened>' short_desc,\n                '<screened>' bug_file_loc\n            ")
        else:
            param.sensitive_columns = SQL('\n                short_desc,\n                bug_file_loc\n            ')
        bugs = db.query("\n            SELECT\n                bug_id,\n                UNIX_TIMESTAMP(CONVERT_TZ(b.creation_ts, 'US/Pacific','UTC'))*1000 AS modified_ts,\n                lower(pr.login_name) AS modified_by,\n                UNIX_TIMESTAMP(CONVERT_TZ(b.creation_ts, 'US/Pacific','UTC'))*1000 AS created_ts,\n                lower(pr.login_name) AS created_by,\n                lower(pa.login_name) AS assigned_to,\n                lower(pq.login_name) AS qa_contact,\n                lower(prod.`name`) AS product,\n                lower(comp.`name`) AS component,\n                {{sensitive_columns}},\n                {{bugs_columns_SQL}}\n            FROM bugs b\n                LEFT JOIN profiles pr ON b.reporter = pr.userid\n                LEFT JOIN profiles pa ON b.assigned_to = pa.userid\n                LEFT JOIN profiles pq ON b.qa_contact = pq.userid\n                LEFT JOIN products prod ON prod.id = product_id\n                LEFT JOIN components comp ON comp.id = component_id\n            WHERE\n                {{bug_filter}}\n            ", param)
        output = []
        for r in bugs:
            flatten_bugs_record(r, output)

        return output
    except Exception as e:
        Log.error('can not get basic bug data', e)


def flatten_bugs_record(r, output):
    for field_name, value in r.items():
        if value != '---':
            newRow = Struct()
            newRow.bug_id = r.bug_id
            newRow.modified_ts = r.modified_ts
            newRow.modified_by = r.modified_by
            newRow.field_name = field_name
            newRow.new_value = value
            newRow._merge_order = 1
            output.append(newRow)


def get_dependencies(db, param):
    param.blocks_filter = db.esfilter2sqlwhere({'terms': {'blocked': param.bug_list}})
    param.dependson_filter = db.esfilter2sqlwhere({'terms': {'dependson': param.bug_list}})
    return db.query("\n        SELECT blocked AS bug_id\n            , CAST(null AS signed) AS modified_ts\n            , CAST(null AS char(255)) AS modified_by\n            , 'dependson' AS field_name\n            , CAST(dependson AS SIGNED) AS new_value\n            , CAST(null AS SIGNED) AS old_value\n            , CAST(null AS signed) AS attach_id\n            , 2 AS _merge_order\n        FROM dependencies d\n        WHERE\n           {{blocks_filter}}\n        UNION\n        SELECT dependson dependson\n            , null\n            , null\n            , 'blocked'\n            , CAST(blocked AS SIGNED)\n            , null\n            , null\n            , 2\n        FROM dependencies d\n        WHERE\n            {{dependson_filter}}\n        ORDER BY bug_id\n    ", param)


def get_duplicates(db, param):
    param.dupe_filter = db.esfilter2sqlwhere({'terms': {'dupe': param.bug_list}})
    param.dupe_of_filter = db.esfilter2sqlwhere({'terms': {'dupe_of': param.bug_list}})
    return db.query("\n        SELECT dupe AS bug_id\n            , CAST(null AS signed) AS modified_ts\n            , CAST(null AS char(255)) AS modified_by\n            , 'dupe_of' AS field_name\n            , CAST(dupe_of AS SIGNED) AS new_value\n            , CAST(null AS SIGNED) AS old_value\n            , CAST(null AS signed) AS attach_id\n            , 2 AS _merge_order\n        FROM duplicates d\n        WHERE\n            {{dupe_filter}}\n        UNION\n        SELECT dupe_of\n            , null\n            , null\n            , 'dupe_by'\n            , CAST(dupe AS SIGNED)\n            , null\n            , null\n            , 2\n        FROM duplicates d\n        WHERE\n            {{dupe_of_filter}}\n        ORDER BY bug_id\n    ", param)


def get_bug_groups(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query("\n        SELECT bug_id\n            , CAST(null AS signed) AS modified_ts\n            , CAST(null AS char(255)) AS modified_by\n            , 'bug_group' AS field_name\n            , lower(CAST(g.`name` AS char(255))) AS new_value\n            , CAST(null AS char(255)) AS old_value\n            , CAST(null AS signed) AS attach_id\n            , 2 AS _merge_order\n        FROM bug_group_map bg\n        JOIN groups g ON bg.group_id = g.id\n        WHERE\n            {{bug_filter}}\n    ", param)


def get_cc(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query("\n        SELECT bug_id\n            , CAST(null AS signed) AS modified_ts\n            , CAST(null AS char(255)) AS modified_by\n            , 'cc' AS field_name\n            , lower(CAST(p.login_name AS char(255))) AS new_value\n            , CAST(null AS char(255)) AS old_value\n            , CAST(null AS signed) AS attach_id\n            , 2 AS _merge_order\n        FROM\n            cc\n        JOIN\n            profiles p ON cc.who = p.userid\n        WHERE\n            {{bug_filter}}\n    ", param)


def get_all_cc_changes(db, bug_list):
    CC_FIELD_ID = 37
    if not bug_list:
        return []
    return db.query("\n            SELECT\n                bug_id,\n                CAST({{max_time}} AS signed) AS modified_ts,\n                CAST(null AS char(255)) AS new_value,\n                lower(CAST(p.login_name AS CHAR(255) CHARACTER SET utf8)) AS old_value\n            FROM\n                cc\n            LEFT JOIN\n                profiles p ON cc.who = p.userid\n            WHERE\n                {{bug_filter}}\n        UNION ALL\n            SELECT\n                a.bug_id,\n                UNIX_TIMESTAMP(CONVERT_TZ(bug_when, 'US/Pacific','UTC'))*1000 AS modified_ts,\n                lower(CAST(trim(added) AS CHAR CHARACTER SET utf8)) AS new_value,\n                lower(CAST(trim(removed) AS CHAR CHARACTER SET utf8)) AS old_value\n            FROM\n                bugs_activity a\n            WHERE\n                a.fieldid = {{cc_field_id}} AND\n                {{bug_filter}}\n    ", {'max_time': MAX_TIME, 
       'cc_field_id': CC_FIELD_ID, 
       'bug_filter': db.esfilter2sqlwhere({'terms': {'bug_id': bug_list}})})


def get_tracking_flags(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query('\n        SELECT\n            bug_id,\n            CAST({{start_time}} AS signed) AS modified_ts,\n            lower(f.name) AS field_name,\n            lower(t.value) AS new_value,\n            1 AS _merge_order\n        FROM\n            tracking_flags_bugs t\n        JOIN\n            tracking_flags f on f.id=t.tracking_flag_id\n        WHERE\n            {{bug_filter}}\n        ORDER BY\n            bug_id\n    ', param)


def get_keywords(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query("\n        SELECT bug_id\n            , NULL AS modified_ts\n            , NULL AS modified_by\n            , 'keywords' AS field_name\n            , lower(kd.name) AS new_value\n            , NULL AS old_value\n            , NULL AS attach_id\n            , 2 AS _merge_order\n        FROM keywords k\n        JOIN keyworddefs kd ON k.keywordid = kd.id\n        WHERE\n            {{bug_filter}}\n        ORDER BY bug_id\n    ", param)


def get_attachments(db, param):
    """
    GET ALL CURRENT ATTACHMENTS
    """
    if param.allow_private_bugs:
        param.attachments_filter = SQL('1=1')
    else:
        param.attachments_filter = SQL('isprivate=0')
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    output = db.query("\n        SELECT bug_id\n            , UNIX_TIMESTAMP(CONVERT_TZ(a.creation_ts, 'US/Pacific','UTC'))*1000 AS modified_ts\n            , lower(login_name) AS modified_by\n            , UNIX_TIMESTAMP(CONVERT_TZ(a.creation_ts, 'US/Pacific','UTC'))*1000 AS created_ts\n            , login_name AS created_by\n            , ispatch AS 'attachments_ispatch'\n            , isobsolete AS 'attachments_isobsolete'\n            , isprivate AS 'attachments_isprivate'\n            , attach_id\n        FROM\n            attachments a\n            JOIN profiles p ON a.submitter_id = p.userid\n        WHERE\n            {{bug_filter}} AND\n            {{attachments_filter}}\n        ORDER BY\n            bug_id,\n            attach_id,\n            a.creation_ts\n    ", param)
    return flatten_attachments(output)


attachments_fields = [
 'created_ts', 'created_by', 'attachments_ispatch', 'attachments_isobsolete', 'attachments_isprivate']

def flatten_attachments(data):
    output = []
    for r in data:
        for a in attachments_fields:
            output.append(Struct(bug_id=r.bug_id, modified_ts=r.modified_ts, modified_by=r.modified_by, field_name=a, new_value=r[a], attach_id=r.attach_id, _merge_order=7))

    return output


def get_bug_see_also(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query("\n        SELECT bug_id\n            , CAST(null AS signed) AS modified_ts\n            , CAST(null AS char(255)) AS modified_by\n            , 'see_also' AS field_name\n            , CAST(`value` AS char(255)) AS new_value\n            , CAST(null AS char(255)) AS old_value\n            , CAST(null AS signed) AS attach_id\n            , 2 AS _merge_order\n        FROM bug_see_also\n        WHERE\n            {{bug_filter}}\n        ORDER BY bug_id\n    ", param)


def get_new_activities(db, param):
    if param.allow_private_bugs:
        param.screened_fields = SQL(SCREENED_FIELDDEFS)
    else:
        param.screened_fields = SQL([-1])
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'a.bug_id': param.bug_list}})
    param.mixed_case_fields = SQL(MIXED_CASE)
    if param.start_time > 0:
        Log.debug()
    output = db.query("\n        SELECT\n            a.bug_id,\n            UNIX_TIMESTAMP(CONVERT_TZ(bug_when, 'US/Pacific','UTC'))*1000 AS modified_ts,\n            lower(login_name) AS modified_by,\n            replace(field.`name`, '.', '_') AS field_name,\n            CAST(\n                CASE\n                WHEN a.fieldid IN {{screened_fields}} THEN '<screened>'\n                WHEN a.fieldid IN {{mixed_case_fields}} THEN trim(added)\n                WHEN trim(added)='' THEN NULL\n                ELSE lower(trim(added))\n                END\n            AS CHAR CHARACTER SET utf8) AS new_value,\n            CAST(\n                CASE\n                WHEN a.fieldid IN {{screened_fields}} THEN '<screened>'\n                WHEN a.fieldid IN {{mixed_case_fields}} THEN trim(removed)\n                WHEN trim(removed)='' THEN NULL\n                ELSE lower(trim(removed))\n                END\n            AS CHAR CHARACTER SET utf8) AS old_value,\n            attach_id,\n            9 AS _merge_order\n        FROM\n            bugs_activity a\n        JOIN\n            profiles p ON a.who = p.userid\n        JOIN\n            fielddefs field ON a.fieldid = field.`id`\n        WHERE\n            {{bug_filter}} AND\n            bug_when >= {{start_time_str}}\n        ORDER BY\n            bug_id,\n            bug_when DESC,\n            attach_id\n    ", param)
    return output


def get_flags(db, param):
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    return db.query("\n        SELECT bug_id\n            , UNIX_TIMESTAMP(CONVERT_TZ(f.creation_date, 'US/Pacific','UTC'))*1000 AS modified_ts\n            , ps.login_name AS modified_by\n            , 'flagtypes_name' AS field_name\n            , CONCAT(ft.`name`,status,IF(requestee_id IS NULL,'',CONCAT('(',pr.login_name,')'))) AS new_value\n            , CAST(null AS char(255)) AS old_value\n            , attach_id\n            , 8 AS _merge_order\n        FROM\n            flags f\n        JOIN `flagtypes` ft ON f.type_id = ft.id\n        JOIN profiles ps ON f.setter_id = ps.userid\n        LEFT JOIN profiles pr ON f.requestee_id = pr.userid\n        WHERE\n            {{bug_filter}}\n        ORDER BY\n            bug_id\n    ", param)


def get_comments(db, param):
    if param.allow_private_bugs:
        return []
    if not param.bug_list:
        return []
    param.comments_filter = SQL('isprivate=0')
    param.bug_filter = db.esfilter2sqlwhere({'terms': {'bug_id': param.bug_list}})
    try:
        comments = db.query("\n            SELECT\n                c.comment_id,\n                c.bug_id,\n                p.login_name modified_by,\n                UNIX_TIMESTAMP(CONVERT_TZ(bug_when, 'US/Pacific','UTC'))*1000 AS modified_ts,\n                c.thetext comment,\n                c.isprivate\n            FROM\n                longdescs c\n            LEFT JOIN\n                profiles p ON c.who = p.userid\n            WHERE\n                {{bug_filter}} AND\n                bug_when >= {{start_time_str}} AND\n                {{comments_filter}}\n            ", param)
        return comments
    except Exception as e:
        Log.error('can not get comment data', e)


def get_comments_by_id(db, comments, param):
    """
    GET SPECIFIC COMMENTS
    """
    if param.allow_private_bugs:
        return []
    param.comments_filter = db.esfilter2sqlwhere({'and': [{'term': {'isprivate': 0}}, {'terms': {'c.comment_id': comments}}]})
    try:
        comments = db.query("\n            SELECT\n                c.comment_id,\n                c.bug_id,\n                p.login_name modified_by,\n                UNIX_TIMESTAMP(CONVERT_TZ(bug_when, 'US/Pacific','UTC'))*1000 AS modified_ts,\n                c.thetext comment,\n                c.isprivate\n            FROM\n                longdescs c\n            LEFT JOIN\n                profiles p ON c.who = p.userid\n            WHERE\n                {{comments_filter}}\n            ", param)
        return comments
    except Exception as e:
        Log.error('can not get comment data', e)