# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/tukey/tukey-middleware/auth_proxy/auth_db.py
# Compiled at: 2012-11-07 15:40:35
import psycopg2, logging, sys
sys.path.append('../local')
import local_settings

def connect():
    conn_template = "dbname='%s' user='%s' host='%s' password='%s'"
    db_name = 'federated_auth'
    db_username = 'cloudgui'
    db_password = local_settings.AUTH_DB_PASSWORD
    host = 'localhost'
    conn_str = conn_template % (db_name, db_username, host, db_password)
    return psycopg2.connect(conn_str)


def connect_and_query(query):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        raise

    return results


def userInfo(method, id, cloud_name):
    logger = logging.getLogger('tukey-auth')
    pre_query = "\n        select username, password from \n        login join login_enabled on login.id = login_enabled.login_id \n        join login_identifier on login.userid = login_identifier.userid\n        join login_identifier_enabled on login_identifier.id = \n            login_identifier_enabled.login_identifier_id\n        join login_method on login_method.method_id = login_identifier.method_id\n        join cloud on cloud.cloud_id = login.cloud_id\n        where cloud_name='%(cloud)s' and login_method.method_name='%(meth)s' \n            and login_identifier.identifier='%(id)s';\n    "
    query = pre_query % {'meth': method, 'id': id, 'cloud': cloud_name}
    creds = connect_and_query(query)
    if creds is None:
        logger.debug('creds is none')
        creds = ('', '')
    logger.debug(creds)
    return creds


def get_key_from_db(cloud, username):
    query = "\n        select password from login, cloud where \n        login.cloud_id = cloud.cloud_id and cloud_name='%(cloud)s'\n        and username='%(username)s'\n    " % locals()
    result = connect_and_query(query)
    if result is not None:
        return result[0]
    else:
        return


def enable_identifier(username, identifier, method):
    insert_and_query = "\n        insert into login_identifier_enabled (login_identifier_id) \n        select login_identifier.id from login_identifier \n        join login on login_identifier.userid=login.userid \n        join login_method on login_identifier.method_id = login_method.method_id\n        where username='%(username)s' and identifier='%(identifier)s'\n            and method_name='%(method)s';\n        select login_identifier_id from login_identifier_enabled \n        join login_identifier on login_identifier_enabled.login_identifier_id = \n            login_identifier.id\n        join login_method on login_identifier.method_id = login_method.method_id\n        join login on login_identifier.userid=login.userid \n        where username='%(username)s' and identifier='%(identifier)s'\n            and method_name='%(method)s';\n\n    " % locals()
    return connect_and_query(insert_and_query)


def insert_sshkey(cloud, username, pubkey, fingerprint, keyname):
    logger = logging.getLogger('tukey-auth')
    insert_and_query = "\n        insert into keypair (pubkey, fingerprint, name, userid, cloud_id)\n        select '%(pubkey)s', '%(fingerprint)s', '%(keyname)s', userid, cloud.cloud_id\n        from cloud, login where username='%(username)s' and\n            cloud_name='%(cloud)s' and login.cloud_id=cloud.cloud_id;\n        select id from keypair where fingerprint='%(fingerprint)s';\n    " % locals()
    return connect_and_query(insert_and_query)


def delete_sshkey(cloud, username, keyname):
    logger = logging.getLogger('tukey-auth')
    delete_keypair = "\n        delete from keypair using cloud, login\n        where name='%(keyname)s' and keypair.userid=login.userid and \n        cloud.cloud_name='%(cloud)s' and cloud.cloud_id=login.cloud_id \n        and login.username='%(username)s';\n    " % locals()
    logger.debug(delete_keypair)
    result = True
    try:
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(delete_keypair)
            conn.commit()
        except:
            result = False

    finally:
        cur.close()
        conn.close()

    return result


def get_keypairs(cloud, username):
    query = "\n        select name, fingerprint, pubkey from keypair, login, cloud \n        where cloud_name='%(cloud)s' and cloud.cloud_id = login.cloud_id\n        and login.username='%(username)s' and login.userid=keypair.userid;\n    " % locals()
    results = []
    try:
        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute(query)
            results = cur.fetchall()
        except:
            pass

    finally:
        cur.close()
        conn.close()

    attributes = ['name', 'fingerprint', 'public_key']
    return [ {'keypair': {attributes[i]:row[i] for i in range(0, len(row))}}
     for row in results ]


def get_keypair(cloud, username, keyname):
    logger = logging.getLogger('tukey-auth')
    select_keypair = "\n        select pubkey, fingerprint from keypair, cloud, login\n        where name='%(keyname)s' and username='%(username)s' and \n        cloud_name='%(cloud)s' and cloud.cloud_id = login.cloud_id\n        and login.userid = keypair.userid;\n    " % locals()
    logger.debug(select_keypair)
    return connect_and_query(select_keypair)