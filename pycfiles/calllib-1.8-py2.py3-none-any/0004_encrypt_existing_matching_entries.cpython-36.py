# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0004_encrypt_existing_matching_entries.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1855 bytes
from __future__ import unicode_literals
import hashlib, json
from django.conf import settings
from django.db import migrations
from django.utils.crypto import get_random_string, pbkdf2
from .. import security
from ...reporting.report_delivery import MatchReportContent

def encrypt_match_report(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    MatchReport = apps.get_model('delivery', 'MatchReport')
    for match_report in MatchReport.objects.using(db_alias).all():
        match_report_content = MatchReportContent(identifier=(match_report.identifier),
          perp_name=(match_report.name),
          email=(match_report.contact_email),
          phone=(match_report.contact_phone),
          contact_name=(match_report.contact_name),
          voicemail=(match_report.contact_voicemail),
          notes=(match_report.contact_notes))
        match_report.salt = get_random_string()
        stretched_identifier = pbkdf2((match_report.identifier),
          (match_report.salt),
          (settings.ORIGINAL_KEY_ITERATIONS),
          digest=(hashlib.sha256))
        encrypted_match_report = security.pepper(security.encrypt_report(stretched_key=stretched_identifier,
          report_text=(json.dumps(match_report_content.__dict__))))
        match_report.encrypted = encrypted_match_report
        if match_report.seen:
            match_report.identifier = None
        match_report.save()


class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0003_allow_deletion_of_identifier')]
    operations = [
     migrations.RunPython(encrypt_match_report,
       reverse_code=(migrations.RunPython.noop))]