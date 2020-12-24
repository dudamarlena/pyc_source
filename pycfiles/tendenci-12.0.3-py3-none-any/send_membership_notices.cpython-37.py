# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/management/commands/send_membership_notices.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 14677 bytes
from datetime import datetime, timedelta
import time, traceback
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.template.loader import render_to_string
from django.template import engines, TemplateDoesNotExist

class Command(BaseCommand):
    __doc__ = '\n    Get a list of membership notices from the notice table,\n    and send each notice to members who meet the criteria.\n\n    Usage: python manage.py send_membership_notices --verbosity 1\n    '

    def handle(self, *args, **options):
        verbosity = 1
        if 'verbosity' in options:
            verbosity = options['verbosity']
        else:
            from django.conf import settings
            from tendenci.apps.memberships.models import Notice, MembershipDefault, NoticeLog, NoticeDefaultLogRecord
            from tendenci.apps.base.utils import fieldify
            import tendenci.apps.notifications as notification
            from tendenci.apps.site_settings.utils import get_setting
            site_display_name = get_setting('site', 'global', 'sitedisplayname')
            site_contact_name = get_setting('site', 'global', 'sitecontactname')
            site_contact_email = get_setting('site', 'global', 'sitecontactemail')
            site_url = get_setting('site', 'global', 'siteurl')
            corp_replace_str = '\n                            <br /><br />\n                            <font color="#FF0000">\n                            Organizational Members, please contact your company\n                            Membership coordinator\n                            to ensure that your membership is being renewed.\n                            </font>\n                            '
            email_context = {'sender':get_setting('site', 'global', 'siteemailnoreplyaddress'), 
             'sender_display':site_display_name, 
             'reply_to':site_contact_email}
            now = datetime.now()
            nowstr = time.strftime('%d-%b-%y %I:%M %p', now.timetuple())

            def email_admins_recap(notices, total_sent):
                recap_recipient = get_admin_emails()
                if recap_recipient:
                    template_name = 'memberships/notices/email_recap.html'
                    try:
                        recap_email_content = render_to_string(template_name=template_name,
                          context={'notices':notices, 
                         'total_sent':total_sent, 
                         'site_url':site_url, 
                         'site_display_name':site_display_name, 
                         'site_contact_name':site_contact_name, 
                         'site_contact_email':site_contact_email})
                        recap_subject = '%s Membership Notices Distributed' % site_display_name
                        email_context.update({'subject':recap_subject, 
                         'content':recap_email_content, 
                         'content_type':'html'})
                        notification.send_emails(recap_recipient, 'membership_notice_email', email_context)
                    except (TemplateDoesNotExist, IOError):
                        pass

            def email_script_errors(err_msg):
                script_recipient = get_script_support_emails()
                if script_recipient:
                    email_context.update({'subject':'Error Processing Membership Notices on %s' % site_url, 
                     'content':'%s \n\nTime Submitted: %s\n' % (err_msg, nowstr), 
                     'content_type':'text'})
                    notification.send_emails(script_recipient, 'membership_notice_email', email_context)

            def get_script_support_emails():
                admins = getattr(settings, 'ADMINS', None)
                if admins:
                    recipients_list = [admin[1] for admin in admins]
                    return recipients_list

            def get_admin_emails():
                admin_emails = get_setting('module', 'memberships', 'membershiprecipients').strip()
                if admin_emails:
                    admin_emails = admin_emails.split(',')
                if not admin_emails:
                    admin_emails = get_setting('site', 'global', 'admincontactemail').strip().split(',')
                return admin_emails

            def process_notice(notice):
                notice.members_sent = []
                num_sent = 0
                if notice.notice_time == 'before':
                    start_dt = now + timedelta(days=(notice.num_days))
                else:
                    start_dt = now - timedelta(days=(notice.num_days))
                if notice.notice_type == 'disapprove' or notice.notice_type == 'disapprove_renewal':
                    status_detail_list = [
                     'disapproved']
                else:
                    status_detail_list = [
                     'active', 'expired']
                memberships = MembershipDefault.objects.filter(status=True,
                  status_detail__in=status_detail_list)
                if notice.notice_type == 'join':
                    memberships = memberships.filter(join_dt__year=(start_dt.year),
                      join_dt__month=(start_dt.month),
                      join_dt__day=(start_dt.day),
                      renewal=False)
                else:
                    if notice.notice_type == 'renewal':
                        memberships = memberships.filter(renew_dt__year=(start_dt.year),
                          renew_dt__month=(start_dt.month),
                          renew_dt__day=(start_dt.day),
                          renewal=True)
                    else:
                        if notice.notice_type == 'approve' or notice.notice_type == 'approve_renewal':
                            memberships = memberships.filter(application_approved_denied_dt__year=(start_dt.year),
                              application_approved_denied_dt__month=(start_dt.month),
                              application_approved_denied_dt__day=(start_dt.day),
                              application_approved=True)
                        else:
                            if notice.notice_type == 'disapprove' or notice.notice_type == 'disapprove_renewal':
                                memberships = memberships.filter(application_approved_denied_dt__year=(start_dt.year),
                                  application_approved_denied_dt__month=(start_dt.month),
                                  application_approved_denied_dt__day=(start_dt.day),
                                  application_approved=False)
                            else:
                                memberships = memberships.filter(expire_dt__year=(start_dt.year),
                                  expire_dt__month=(start_dt.month),
                                  expire_dt__day=(start_dt.day))
                                if get_setting('module', 'memberships', 'renewalreminderexcludecorpmembers'):
                                    memberships = memberships.exclude(corporate_membership_id__gt=0)
                                if notice.membership_type:
                                    memberships = memberships.filter(membership_type=(notice.membership_type))
                                memberships_count = memberships.count()
                                if memberships_count > 0:
                                    email_context.update({'content_type': notice.content_type})
                                    passwd_str = '\n                        If you\'ve forgotten your password or need to reset\n                        the auto-generated one, click <a href="%s%s">here</a>\n                        and follow the instructions on the page to\n                        reset your password.\n                        ' % (site_url, reverse('auth_password_reset'))
                                    global_context = {'site_display_name':site_display_name, 
                                     'site_contact_name':site_contact_name, 
                                     'site_contact_email':site_contact_email, 
                                     'time_submitted':nowstr, 
                                     'sitedisplayname':site_display_name, 
                                     'sitecontactname':site_contact_name, 
                                     'sitecontactemail':site_contact_email, 
                                     'timesubmitted':nowstr, 
                                     'password':passwd_str}
                                    notice_log = NoticeLog(notice=notice, num_sent=0)
                                    notice_log.save()
                                    notice.log = notice_log
                                    notice.err = ''
                                    for membership in memberships:
                                        if notice.notice_type == 'expiration':
                                            if membership.auto_renew:
                                                if membership.has_rp():
                                                    continue
                                        try:
                                            email_member(notice, membership, global_context)
                                            if memberships_count <= 50:
                                                notice.members_sent.append(membership)
                                            num_sent += 1
                                            notice_log_record = NoticeDefaultLogRecord(notice_log=notice_log,
                                              membership=membership)
                                            notice_log_record.save()
                                        except:
                                            notice.err += traceback.format_exc()
                                            print(traceback.format_exc())

                                    if num_sent > 0:
                                        notice_log.num_sent = num_sent
                                        notice_log.save()
                                return num_sent

            def email_member(notice, membership, global_context):
                user = membership.user
                body = notice.email_content
                context = membership.get_field_items()
                context['membership'] = membership
                context.update(global_context)
                if membership.corporate_membership_id:
                    context['corporate_membership_notice'] = corp_replace_str
                else:
                    if membership.expire_dt:
                        context.update({'expire_dt': time.strftime('%d-%b-%y %I:%M %p', membership.expire_dt.timetuple())})
                    if membership.payment_method:
                        payment_method_name = membership.payment_method.human_name
                    else:
                        payment_method_name = ''
                context.update({'member_number':membership.member_number, 
                 'payment_method':payment_method_name, 
                 'referer_url':'%s%s?next=%s' % (site_url, reverse('auth_login'), membership.referer_url), 
                 'membership_link':'%s%s' % (site_url, membership.get_absolute_url()), 
                 'view_link':'%s%s' % (site_url, membership.get_absolute_url()), 
                 'renew_link':'%s%s' % (site_url, membership.get_absolute_url()), 
                 'mymembershipslink':'%s%s' % (site_url, membership.get_absolute_url()), 
                 'membershiplink':'%s%s' % (site_url, membership.get_absolute_url()), 
                 'renewlink':'%s%s' % (site_url, membership.get_absolute_url())})
                body = fieldify(body)
                body = body + ' <br /><br />{% include "email_footer.html" %}'
                template = engines['django'].from_string(body)
                body = template.render(context=context)
                email_recipient = user.email
                subject = notice.subject.replace('(name)', user.get_full_name())
                template = engines['django'].from_string(subject)
                subject = template.render(context=context)
                email_context.update({'subject':subject, 
                 'content':body})
                if notice.sender:
                    email_context.update({'reply_to': notice.sender})
                if notice.sender_display:
                    email_context.update({'sender_display': notice.sender_display})
                notification.send_emails([email_recipient], 'membership_notice_email', email_context)
                if verbosity > 1:
                    print('To ', email_recipient, subject)

            exception_str = ''
            notices = Notice.objects.filter(status=True, status_detail='active').exclude(notice_time='attimeof')
            if notices:
                if verbosity > 1:
                    print('Start sending out notices to members:')
                total_notices = 0
                total_sent = 0
                for notice in notices:
                    total_notices += 1
                    total_sent += process_notice(notice)
                    if hasattr(notice, 'err'):
                        exception_str += notice.err

                if total_sent > 0:
                    processed_notices = [notice for notice in notices if hasattr(notice, 'log') if notice.log.num_sent > 0]
                    email_admins_recap(processed_notices, total_sent)
                if exception_str:
                    email_script_errors(exception_str)
                if verbosity > 1:
                    print('Total notice processed: %d' % total_notices)
                    print('Total email sent: %d' % total_sent)
                    print('Done')
            elif verbosity > 1:
                print('No notices on the site.')