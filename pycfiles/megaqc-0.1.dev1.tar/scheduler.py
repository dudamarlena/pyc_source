# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewels/GitHub/MegaQC/megaqc/scheduler.py
# Compiled at: 2018-07-06 11:43:41
from __future__ import unicode_literals
from builtins import str
from flask import current_app
from flask_apscheduler import APScheduler
from megaqc.model.models import Upload
from megaqc.user.models import User
from megaqc.extensions import db
from megaqc.api.utils import handle_report_data
import datetime, gzip, json, io, os, traceback
scheduler = APScheduler()

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()


def upload_reports_job():
    with scheduler.app.app_context():
        queued_uploads = db.session.query(Upload).filter(Upload.status == b'NOT TREATED').all()
        for row in queued_uploads:
            user = db.session.query(User).filter(User.user_id == row.user_id).one()
            current_app.logger.info((b'Beginning process of upload #{} from {}').format(row.upload_id, user.email))
            row.status = b'IN TREATMENT'
            db.session.add(row)
            db.session.commit()
            gzipped = False
            with open(row.path, b'rb') as (fh):
                file_start = fh.read(3)
                if file_start == b'\x1f\x8b\x08':
                    gzipped = True
            try:
                if gzipped:
                    with io.BufferedReader(gzip.open(row.path, b'rb')) as (fh):
                        raw_data = fh.read().decode(b'utf-8')
                else:
                    with io.open(row.path, b'rb') as (fh):
                        raw_data = fh.read().decode(b'utf-8')
                data = json.loads(raw_data)
                ret = handle_report_data(user, data)
            except Exception:
                ret = (
                 False, (b'<pre><code>{}</code></pre>').format(traceback.format_exc()))
                current_app.logger.error((b'Error processing upload {}: {}').format(row.upload_id, traceback.format_exc()))

            if ret[0]:
                row.status = b'TREATED'
                row.message = b'The document has been uploaded successfully'
                os.remove(row.path)
            else:
                row.status = b'FAILED'
                row.message = (b'The document has not been uploaded : {0}').format(ret[1])
            row.modified_at = datetime.datetime.utcnow()
            current_app.logger.info((b'Finished processing upload #{} to state {}').format(row.upload_id, row.status))
            db.session.add(row)
            db.session.commit()