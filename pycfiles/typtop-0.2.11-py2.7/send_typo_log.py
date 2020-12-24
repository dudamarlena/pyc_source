# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/typtop/send_typo_log.py
# Compiled at: 2017-03-02 10:42:21
import os, sys, random, requests, json
from typtop.dbaccess import UserTypoDB, get_time
from typtop.config import LOG_DIR, VERSION, SEC_DB_PATH, DB_NAME
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(THIS_FOLDER, 'typtopserver.crt')

def send_logs(typo_db, force=False):
    need_to_send, iter_data = typo_db.get_last_unsent_logs_iter(force)
    logger = typo_db.logger
    if not need_to_send:
        logger.info('No need to send logs now.')
        return
    list_of_logs = list(iter_data)
    install_id = str(typo_db.get_installation_id())
    dbdata = json.dumps(list_of_logs)
    url = 'https://ec2-54-209-30-18.compute-1.amazonaws.com/submit'
    r = requests.post(url, data=dict(uid=install_id.strip() + '#' + str(VERSION), data=dbdata, test=0), allow_redirects=True, verify=CERT_FILE)
    sent_successfully = r.status_code == 200
    logger.info(('Sent logs status {} ({}) (sent_successfully={})').format(r.status_code, r.text, sent_successfully))
    if sent_successfully:
        typo_db.update_last_log_sent_time(sent_time=get_time(), delete_old_logs=True)
        updatecmd = 'typtop --update' if random.randint(0, 100) <= 20 else ''
        cmd = ('\n        tail -n500 {0}/{1}.log > /tmp/t.log && mv /tmp/t.log {0}/{1}.log;\n        {2}\n        ').format(LOG_DIR, DB_NAME, updatecmd)
        os.system(cmd)


def main():
    assert len(sys.argv) > 1
    user = sys.argv[1]
    users = [user]
    force = True if len(sys.argv) > 2 and sys.argv[2] == 'force' else False
    if user == 'all':
        users = [ d for d in os.listdir(SEC_DB_PATH) if os.path.isdir(os.path.join(SEC_DB_PATH, d))
                ]
    for user in users:
        typo_db = UserTypoDB(user)
        send_logs(typo_db, force)


if __name__ == '__main__':
    main()