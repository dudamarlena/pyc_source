# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/views/staff.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 55530 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

views/staff.py - The bulk of the application - provides most business logic and
                 renders all staff-facing views.
"""
from datetime import datetime, timedelta
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core import paginator
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.dates import MONTHS_3
import django.utils.translation as _
from django.utils.html import escape
from django import forms
from django.utils.encoding import smart_text
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

import tendenci.apps.theme.shortcuts as render_to_resp
from tendenci.apps.helpdesk.forms import TicketForm, UserSettingsForm, EmailIgnoreForm, EditTicketForm, TicketCCForm, EditFollowUpForm, TicketDependencyForm
from tendenci.apps.helpdesk.lib import send_templated_mail, query_to_dict, apply_query, safe_template_context
from tendenci.apps.helpdesk.models import Ticket, Queue, FollowUp, TicketChange, PreSetReply, Attachment, SavedSearch, IgnoreEmail, TicketCC, TicketDependency, QueueMembership
import tendenci.apps.helpdesk as helpdesk_settings
from tendenci.apps.base.http import Http403
from tendenci.apps.perms.utils import has_perm
if helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE:
    staff_member_required = user_passes_test(lambda u: u.is_authenticated and u.is_active)
else:
    staff_member_required = user_passes_test(lambda u: u.is_authenticated and u.is_active and u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_authenticated and u.is_active and u.is_superuser)

def dashboard(request):
    """
    A quick summary overview for users: A list of their own tickets, a table
    showing ticket counts by queue/status, and a list of unassigned tickets
    with options for them to 'Take' ownership of said tickets.
    """
    tickets = Ticket.objects.select_related('queue').filter(assigned_to=(request.user)).exclude(status__in=[
     Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS])
    tickets_closed_resolved = Ticket.objects.select_related('queue').filter(assigned_to=(request.user),
      status__in=[
     Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS])
    unassigned_tickets = Ticket.objects.select_related('queue').filter(assigned_to__isnull=True).exclude(status=(Ticket.CLOSED_STATUS))
    limit_queues_by_user = helpdesk_settings.HELPDESK_ENABLE_PER_QUEUE_STAFF_MEMBERSHIP and not request.user.is_superuser
    if limit_queues_by_user:
        try:
            unassigned_tickets = unassigned_tickets.filter(queue__in=(request.user.queuemembership.queues.all()))
        except QueueMembership.DoesNotExist:
            unassigned_tickets = unassigned_tickets.none()

    all_tickets_reported_by_current_user = ''
    if helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE:
        all_tickets_reported_by_current_user = Ticket.objects.select_related('queue').filter(Q(creator=(request.user)) | Q(owner=(request.user))).order_by('status')
    else:
        email_current_user = request.user.email
        if email_current_user:
            all_tickets_reported_by_current_user = Ticket.objects.select_related('queue').filter(submitter_email=email_current_user).order_by('status')
        Tickets = Ticket.objects
        if limit_queues_by_user:
            try:
                Tickets = Tickets.filter(queue__in=(request.user.queuemembership.queues.all()))
            except QueueMembership.DoesNotExist:
                Tickets = Tickets.none()

        basic_ticket_stats = calc_basic_ticket_stats(Tickets)
        from_clause = 'FROM    helpdesk_ticket t,\n                    helpdesk_queue q'
        where_clause = 'WHERE   q.id = t.queue_id'
        if limit_queues_by_user:
            from_clause = '%s,\n                    helpdesk_queuemembership qm,\n                    helpdesk_queuemembership_queues qm_queues' % from_clause
            where_clause = '%s AND\n                    qm.user_id = %d AND\n                    qm.id = qm_queues.queuemembership_id AND\n                    q.id = qm_queues.queue_id' % (where_clause, request.user.id)
        cursor = connection.cursor()
        cursor.execute("\n        SELECT      q.id as queue,\n                    q.title AS name,\n                    COUNT(CASE t.status WHEN '1' THEN t.id WHEN '2' THEN t.id END) AS open,\n                    COUNT(CASE t.status WHEN '3' THEN t.id END) AS resolved,\n                    COUNT(CASE t.status WHEN '4' THEN t.id END) AS closed\n            %s\n            %s\n            GROUP BY queue, name\n            ORDER BY q.id;\n    " % (from_clause, where_clause))
        dash_tickets = query_to_dict(cursor.fetchall(), cursor.description)
        return render_to_resp(request=request, template_name='helpdesk/dashboard.html', context={'user_tickets':tickets, 
         'user_tickets_closed_resolved':tickets_closed_resolved, 
         'unassigned_tickets':unassigned_tickets, 
         'all_tickets_reported_by_current_user':all_tickets_reported_by_current_user, 
         'dash_tickets':dash_tickets, 
         'basic_ticket_stats':basic_ticket_stats})


dashboard = staff_member_required(dashboard)

def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff:
        if not has_perm(request.user, 'helpdesk.delete_ticket', ticket):
            raise Http403
    if request.method == 'GET':
        return render_to_resp(request=request, template_name='helpdesk/delete_ticket.html', context={'ticket': ticket})
    ticket.delete()
    return HttpResponseRedirect(reverse('helpdesk_home'))


delete_ticket = staff_member_required(delete_ticket)

def followup_edit(request, ticket_id, followup_id):
    """Edit followup options with an ability to change the ticket."""
    followup = get_object_or_404(FollowUp, id=followup_id)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'GET':
        form = EditFollowUpForm(initial={'title':escape(followup.title), 
         'ticket':followup.ticket, 
         'comment':escape(followup.comment), 
         'public':followup.public, 
         'new_status':followup.new_status})
        ticketcc_string, SHOW_SUBSCRIBE = return_ticketccstring_and_show_subscribe(request.user, ticket)
        return render_to_resp(request=request, template_name='helpdesk/followup_edit.html', context={'followup':followup, 
         'ticket':ticket, 
         'form':form, 
         'ticketcc_string':ticketcc_string})
    if request.method == 'POST':
        form = EditFollowUpForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            _ticket = form.cleaned_data['ticket']
            comment = form.cleaned_data['comment']
            public = form.cleaned_data['public']
            new_status = form.cleaned_data['new_status']
            old_date = followup.date
            new_followup = FollowUp(title=title, date=old_date, ticket=_ticket, comment=comment, public=public, new_status=new_status)
            if followup.user:
                new_followup.user = followup.user
            new_followup.save()
            attachments = Attachment.objects.filter(followup=followup)
            for attachment in attachments:
                attachment.followup = new_followup
                attachment.save()

            followup.delete()
        return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket.id]))


followup_edit = staff_member_required(followup_edit)

def followup_delete(request, ticket_id, followup_id):
    """ followup delete for superuser"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket.id]))
    followup = get_object_or_404(FollowUp, id=followup_id)
    followup.delete()
    return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket.id]))


followup_delete = staff_member_required(followup_delete)

def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff:
        if not has_perm(request.user, 'helpdesk.change_ticket', ticket):
            raise Http403
    if 'take' in request.GET:
        request.POST = {'owner':request.user.id, 
         'public':1, 
         'title':ticket.title, 
         'comment':''}
        return update_ticket(request, ticket_id)
    if 'subscribe' in request.GET:
        ticketcc_string, SHOW_SUBSCRIBE = return_ticketccstring_and_show_subscribe(request.user, ticket)
        if SHOW_SUBSCRIBE:
            subscribe_staff_member_to_ticket(ticket, request.user)
            return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket.id]))
    if 'close' in request.GET:
        if ticket.status == Ticket.RESOLVED_STATUS:
            if not ticket.assigned_to:
                owner = 0
            else:
                owner = ticket.assigned_to.id
            request.POST = {'new_status':Ticket.CLOSED_STATUS, 
             'public':1, 
             'owner':owner, 
             'title':ticket.title, 
             'comment':_('Accepted resolution and closed ticket')}
            return update_ticket(request, ticket_id)
    elif helpdesk_settings.HELPDESK_STAFF_ONLY_TICKET_OWNERS:
        users = User.objects.filter(is_active=True, is_staff=True).order_by(User.USERNAME_FIELD)
    else:
        users = User.objects.filter(is_active=True).order_by(User.USERNAME_FIELD)
    form = TicketForm(initial={'due_date': ticket.due_date})
    ticketcc_string, SHOW_SUBSCRIBE = return_ticketccstring_and_show_subscribe(request.user, ticket)
    return render_to_resp(request=request, template_name='helpdesk/ticket.html', context={'ticket':ticket, 
     'form':form, 
     'active_users':users, 
     'priorities':Ticket.PRIORITY_CHOICES, 
     'preset_replies':PreSetReply.objects.filter(Q(queues=(ticket.queue)) | Q(queues__isnull=True)), 
     'ticketcc_string':ticketcc_string, 
     'SHOW_SUBSCRIBE':SHOW_SUBSCRIBE})


view_ticket = staff_member_required(view_ticket)

def return_ticketccstring_and_show_subscribe(user, ticket):
    """ used in view_ticket() and followup_edit()"""
    username = user.get_username().upper()
    useremail = user.email.upper()
    strings_to_check = list()
    strings_to_check.append(username)
    strings_to_check.append(useremail)
    ticketcc_string = ''
    all_ticketcc = ticket.ticketcc_set.all()
    counter_all_ticketcc = len(all_ticketcc) - 1
    SHOW_SUBSCRIBE = True
    for i, ticketcc in enumerate(all_ticketcc):
        ticketcc_this_entry = str(ticketcc.display)
        ticketcc_string = ticketcc_string + ticketcc_this_entry
        if i < counter_all_ticketcc:
            ticketcc_string = ticketcc_string + ', '
        if strings_to_check.__contains__(ticketcc_this_entry.upper()):
            SHOW_SUBSCRIBE = False

    assignedto_username = str(ticket.assigned_to).upper()
    strings_to_check = list()
    strings_to_check.append(assignedto_username)
    if ticket.submitter_email:
        submitter_email = ticket.submitter_email.upper()
        strings_to_check.append(submitter_email)
    if strings_to_check.__contains__(username) or strings_to_check.__contains__(useremail):
        SHOW_SUBSCRIBE = False
    return (ticketcc_string, SHOW_SUBSCRIBE)


def subscribe_staff_member_to_ticket(ticket, user):
    """ used in view_ticket() and update_ticket() """
    ticketcc = TicketCC()
    ticketcc.ticket = ticket
    ticketcc.user = user
    ticketcc.can_view = True
    ticketcc.can_update = True
    ticketcc.save()


def update_ticket(request, ticket_id, public=False):
    if (public or request.user).is_authenticated:
        if not (request.user.is_active and request.user.is_staff or helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE):
            return HttpResponseRedirect('%s?next=%s' % (reverse('login'), request.path))
        else:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            if not request.user.is_staff:
                if not has_perm(request.user, 'helpdesk.change_ticket', ticket):
                    raise Http403
            comment = request.POST.get('comment', '')
            new_status = int(request.POST.get('new_status', ticket.status))
            title = request.POST.get('title', '')
            public = request.POST.get('public', False)
            owner = int(request.POST.get('owner', -1))
            priority = int(request.POST.get('priority', ticket.priority))
            try:
                due_date_year = int(request.POST.get('due_date_year', 0))
            except ValueError:
                due_date_year = 0

            try:
                due_date_month = int(request.POST.get('due_date_month', 0))
            except ValueError:
                due_date_month = 0

            try:
                due_date_day = int(request.POST.get('due_date_day', 0))
            except ValueError:
                due_date_day = 0

            if not (due_date_year and due_date_month and due_date_day):
                due_date = ticket.due_date
            else:
                if ticket.due_date:
                    due_date = ticket.due_date
                else:
                    due_date = timezone.now()
                due_date = due_date.replace(due_date_year, due_date_month, due_date_day)
            no_changes = all([
             not request.FILES,
             not comment,
             new_status == ticket.status,
             title == ticket.title,
             priority == int(ticket.priority),
             due_date == ticket.due_date,
             owner == -1 or not owner and not ticket.assigned_to or owner and User.objects.get(id=owner) == ticket.assigned_to])
            if no_changes:
                return return_to_ticket(request.user, helpdesk_settings, ticket)
            if owner is -1:
                if ticket.assigned_to:
                    owner = ticket.assigned_to.id
            f = FollowUp(ticket=ticket, date=(timezone.now()), comment=comment)
            if request.user.is_staff or helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE:
                f.user = request.user
            f.public = public
            reassigned = False
            if owner is not -1:
                if owner != 0:
                    if ticket.assigned_to:
                        new_user = owner != ticket.assigned_to.id or ticket.assigned_to or User.objects.get(id=owner)
                        f.title = _('Assigned to %(username)s') % {'username': new_user.get_username()}
                        ticket.assigned_to = new_user
                        reassigned = True
                    else:
                        pass
                if owner == 0:
                    if ticket.assigned_to is not None:
                        f.title = _('Unassigned')
                        ticket.assigned_to = None
            if new_status != ticket.status:
                ticket.status = new_status
                ticket.save()
                f.new_status = new_status
                if f.title:
                    f.title += ' and %s' % ticket.get_status_display()
                else:
                    f.title = '%s' % ticket.get_status_display()
            if not f.title:
                if f.comment:
                    f.title = _('Comment')
                else:
                    f.title = _('Updated')
            f.save()
            files = []
            if request.FILES:
                import mimetypes
                for file in request.FILES.getlist('attachment'):
                    filename = smart_text(file.name)
                    a = Attachment(followup=f,
                      filename=filename,
                      mime_type=(mimetypes.guess_type(filename, strict=False)[0] or 'application/octet-stream'),
                      size=(file.size))
                    a.file.save(filename, file, save=False)
                    a.save()
                    if file.size < getattr(settings, 'MAX_EMAIL_ATTACHMENT_SIZE', 512000):
                        files.append([a.filename, a.file])

            if title != ticket.title:
                c = TicketChange(followup=f,
                  field=(_('Title')),
                  old_value=(ticket.title),
                  new_value=title)
                c.save()
                ticket.title = title
            if priority != ticket.priority:
                c = TicketChange(followup=f,
                  field=(_('Priority')),
                  old_value=(ticket.priority),
                  new_value=priority)
                c.save()
                ticket.priority = priority
            if due_date != ticket.due_date:
                c = TicketChange(followup=f,
                  field=(_('Due on')),
                  old_value=(ticket.due_date),
                  new_value=due_date)
                c.save()
                ticket.due_date = due_date
            if new_status in [Ticket.RESOLVED_STATUS, Ticket.CLOSED_STATUS] and not new_status == Ticket.RESOLVED_STATUS:
                if ticket.resolution is None:
                    ticket.resolution = comment
            messages_sent_to = []
            context = safe_template_context(ticket)
            context.update(resolution=(ticket.resolution),
              comment=(f.comment))
            if public and not f.comment:
                if f.new_status in (Ticket.RESOLVED_STATUS, Ticket.CLOSED_STATUS):
                    if f.new_status == Ticket.RESOLVED_STATUS:
                        template = 'resolved_'
                    else:
                        if f.new_status == Ticket.CLOSED_STATUS:
                            template = 'closed_'
                        else:
                            template = 'updated_'
                    template_suffix = 'submitter'
                    if ticket.submitter_email:
                        send_templated_mail((template + template_suffix),
                          context,
                          recipients=(ticket.submitter_email),
                          sender=(ticket.queue.from_address),
                          fail_silently=True,
                          files=files)
                        messages_sent_to.append(ticket.submitter_email)
                    template_suffix = 'cc'
                    for cc in ticket.ticketcc_set.all():
                        if cc.email_address not in messages_sent_to:
                            send_templated_mail((template + template_suffix),
                              context,
                              recipients=(cc.email_address),
                              sender=(ticket.queue.from_address),
                              fail_silently=True,
                              files=files)
                            messages_sent_to.append(cc.email_address)

                if ticket.assigned_to:
                    if request.user != ticket.assigned_to:
                        if ticket.assigned_to.email:
                            if ticket.assigned_to.email not in messages_sent_to:
                                if reassigned:
                                    template_staff = 'assigned_owner'
                                else:
                                    if f.new_status == Ticket.RESOLVED_STATUS:
                                        template_staff = 'resolved_owner'
                                    else:
                                        if f.new_status == Ticket.CLOSED_STATUS:
                                            template_staff = 'closed_owner'
                                        else:
                                            template_staff = 'updated_owner'
                                if not reassigned or reassigned and ticket.assigned_to.usersettings.settings.get('email_on_ticket_assign', False) or (reassigned or ticket.assigned_to.usersettings.settings.get)('email_on_ticket_change', False):
                                    send_templated_mail(template_staff,
                                      context,
                                      recipients=(ticket.assigned_to.email),
                                      sender=(ticket.queue.from_address),
                                      fail_silently=True,
                                      files=files)
                                    messages_sent_to.append(ticket.assigned_to.email)
                if ticket.queue.updated_ticket_cc and ticket.queue.updated_ticket_cc not in messages_sent_to:
                    if reassigned:
                        template_cc = 'assigned_cc'
                    else:
                        if f.new_status == Ticket.RESOLVED_STATUS:
                            template_cc = 'resolved_cc'
                        else:
                            if f.new_status == Ticket.CLOSED_STATUS:
                                template_cc = 'closed_cc'
                            else:
                                template_cc = 'updated_cc'
                    send_templated_mail(template_cc,
                      context,
                      recipients=(ticket.queue.updated_ticket_cc),
                      sender=(ticket.queue.from_address),
                      fail_silently=True,
                      files=files)
        if request.user.is_authenticated:
            ticket.owner = request.user
            ticket.owner_username = request.user.username
    else:
        ticket.save()
        if helpdesk_settings.HELPDESK_AUTO_SUBSCRIBE_ON_TICKET_RESPONSE:
            if request.user.is_authenticated:
                ticketcc_string, SHOW_SUBSCRIBE = return_ticketccstring_and_show_subscribe(request.user, ticket)
                if SHOW_SUBSCRIBE:
                    subscribe_staff_member_to_ticket(ticket, request.user)
    return return_to_ticket(request.user, helpdesk_settings, ticket)


def return_to_ticket(user, helpdesk_settings, ticket):
    """ Helpder function for update_ticket """
    if user.is_staff or helpdesk_settings.HELPDESK_ALLOW_NON_STAFF_TICKET_UPDATE:
        return HttpResponseRedirect(ticket.get_absolute_url())
    return HttpResponseRedirect(ticket.ticket_url)


def mass_update(request):
    tickets = request.POST.getlist('ticket_id')
    action = request.POST.get('action', None)
    if tickets:
        return action or HttpResponseRedirect(reverse('helpdesk_list'))
    elif action.startswith('assign_'):
        parts = action.split('_')
        user = User.objects.get(id=(parts[1]))
        action = 'assign'
    else:
        if action == 'take':
            user = request.user
            action = 'assign'
    for t in Ticket.objects.filter(id__in=tickets):
        if action == 'assign' and t.assigned_to != user:
            t.assigned_to = user
            t.save()
            f = FollowUp(ticket=t, date=(timezone.now()), title=(_('Assigned to %(username)s in bulk update' % {'username': user.get_username()})), public=True, user=(request.user))
            f.save()
        elif action == 'unassign' and t.assigned_to is not None:
            t.assigned_to = None
            t.save()
            f = FollowUp(ticket=t, date=(timezone.now()), title=(_('Unassigned in bulk update')), public=True, user=(request.user))
            f.save()
        elif action == 'close' and t.status != Ticket.CLOSED_STATUS:
            t.status = Ticket.CLOSED_STATUS
            t.save()
            f = FollowUp(ticket=t, date=(timezone.now()), title=(_('Closed in bulk update')), public=False, user=(request.user), new_status=(Ticket.CLOSED_STATUS))
            f.save()
        elif action == 'close_public' and t.status != Ticket.CLOSED_STATUS:
            t.status = Ticket.CLOSED_STATUS
            t.save()
            f = FollowUp(ticket=t, date=(timezone.now()), title=(_('Closed in bulk update')), public=True, user=(request.user), new_status=(Ticket.CLOSED_STATUS))
            f.save()
            context = safe_template_context(t)
            context.update(resolution=(t.resolution),
              queue=(t.queue))
            messages_sent_to = []
            if t.submitter_email:
                send_templated_mail('closed_submitter',
                  context,
                  recipients=(t.submitter_email),
                  sender=(t.queue.from_address),
                  fail_silently=True)
                messages_sent_to.append(t.submitter_email)
            for cc in t.ticketcc_set.all():
                if cc.email_address not in messages_sent_to:
                    send_templated_mail('closed_submitter',
                      context,
                      recipients=(cc.email_address),
                      sender=(t.queue.from_address),
                      fail_silently=True)
                    messages_sent_to.append(cc.email_address)

            if t.assigned_to:
                if request.user != t.assigned_to:
                    if t.assigned_to.email:
                        if t.assigned_to.email not in messages_sent_to:
                            send_templated_mail('closed_owner',
                              context,
                              recipients=(t.assigned_to.email),
                              sender=(t.queue.from_address),
                              fail_silently=True)
                            messages_sent_to.append(t.assigned_to.email)
            if t.queue.updated_ticket_cc and t.queue.updated_ticket_cc not in messages_sent_to:
                send_templated_mail('closed_cc',
                  context,
                  recipients=(t.queue.updated_ticket_cc),
                  sender=(t.queue.from_address),
                  fail_silently=True)
        elif action == 'delete':
            t.delete()

    return HttpResponseRedirect(reverse('helpdesk_list'))


mass_update = staff_member_required(mass_update)

def ticket_list(request):
    context = {}
    query_params = {'filtering':{},  'sorting':None, 
     'sortreverse':False, 
     'keyword':None, 
     'other_filter':None}
    from_saved_query = False
    if request.GET.get('search_type', None) == 'header':
        query = request.GET.get('q')
        filter = None
        if query.find('-') > 0:
            try:
                queue, id = query.split('-')
                id = int(id)
            except ValueError:
                id = None

            if id:
                filter = {'queue__slug':queue, 
                 'id':id}
        else:
            try:
                query = int(query)
            except ValueError:
                query = None

            if query:
                filter = {'id': int(query)}
        if filter:
            try:
                ticket = (Ticket.objects.get)(**filter)
                return HttpResponseRedirect(ticket.staff_url)
            except Ticket.DoesNotExist:
                pass

            saved_query = None
            if request.GET.get('saved_query', None):
                from_saved_query = True
                try:
                    saved_query = SavedSearch.objects.get(pk=(request.GET.get('saved_query')))
                except SavedSearch.DoesNotExist:
                    return HttpResponseRedirect(reverse('helpdesk_list'))
                else:
                    if not saved_query.shared:
                        if not saved_query.user == request.user:
                            return HttpResponseRedirect(reverse('helpdesk_list'))
                import pickle
                from base64 import b64decode
                query_params = pickle.loads(b64decode(str(saved_query.query).encode()))
        else:
            query_params = 'queue' in request.GET or 'assigned_to' in request.GET or 'status' in request.GET or 'q' in request.GET or 'sort' in request.GET or 'sortreverse' in request.GET or {'filtering':{'status__in': [1, 2, 3]}, 
             'sorting':'created'}
    else:
        queues = request.GET.getlist('queue')
        if queues:
            try:
                queues = [int(q) for q in queues]
                query_params['filtering']['queue__id__in'] = queues
            except ValueError:
                pass

        owners = request.GET.getlist('assigned_to')
        if owners:
            try:
                owners = [int(u) for u in owners]
                query_params['filtering']['assigned_to__id__in'] = owners
            except ValueError:
                pass

        statuses = request.GET.getlist('status')
        if statuses:
            try:
                statuses = [int(s) for s in statuses]
                query_params['filtering']['status__in'] = statuses
            except ValueError:
                pass

            date_from = request.GET.get('date_from')
            if date_from:
                query_params['filtering']['created__gte'] = date_from
            date_to = request.GET.get('date_to')
            if date_to:
                query_params['filtering']['created__lte'] = date_to
            q = request.GET.get('q', None)
            if q:
                qset = Q(title__icontains=q) | Q(description__icontains=q) | Q(resolution__icontains=q) | Q(submitter_email__icontains=q)
                context = dict(context, query=q)
                query_params['other_filter'] = qset
            sort = request.GET.get('sort', None)
            if sort not in ('status', 'assigned_to', 'created', 'title', 'queue', 'priority'):
                sort = 'created'
            query_params['sorting'] = sort
            sortreverse = request.GET.get('sortreverse', None)
            query_params['sortreverse'] = sortreverse
        else:
            tickets = Ticket.objects.select_related()
            queue_choices = Queue.objects.all()
            if helpdesk_settings.HELPDESK_ENABLE_PER_QUEUE_STAFF_MEMBERSHIP:
                user_queues = request.user.is_superuser or request.user.queuemembership.queues.all()
                tickets = tickets.filter(queue__in=user_queues)
                queue_choices = user_queues
        if not request.user.is_staff:
            tickets = tickets.filter(Q(creator=(request.user)) | Q(owner=(request.user)))
        try:
            ticket_qs = apply_query(tickets, query_params)
        except ValidationError:
            query_params = {'filtering':{'status__in': [1, 2, 3]},  'sorting':'created'}
            ticket_qs = apply_query(tickets, query_params)

        ticket_paginator = paginator.Paginator(ticket_qs, request.user.usersettings.settings.get('tickets_per_page') or 20)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            tickets = ticket_paginator.page(page)
        except (paginator.EmptyPage, paginator.InvalidPage):
            tickets = ticket_paginator.page(ticket_paginator.num_pages)

        search_message = ''
        if 'query' in context:
            if settings.DATABASES['default']['ENGINE'].endswith('sqlite'):
                search_message = _('<p><strong>Note:</strong> Your keyword search is case sensitive because of your database. This means the search will <strong>not</strong> be accurate. By switching to a different database system you will gain better searching! For more information, read the <a href="http://docs.djangoproject.com/en/dev/ref/databases/#sqlite-string-matching">Django Documentation on string matching in SQLite</a>.')
        import pickle
        from base64 import b64encode
        urlsafe_query = b64encode(pickle.dumps(query_params)).decode()
        user_saved_queries = SavedSearch.objects.filter(Q(user=(request.user)) | Q(shared__exact=True))
        querydict = request.GET.copy()
        querydict.pop('page', 1)
        return render_to_resp(request=request, template_name='helpdesk/ticket_list.html', context=dict(context,
          query_string=(querydict.urlencode()),
          tickets=tickets,
          user_choices=User.objects.filter(is_active=True, is_staff=True),
          queue_choices=queue_choices,
          status_choices=(Ticket.STATUS_CHOICES),
          urlsafe_query=urlsafe_query,
          user_saved_queries=user_saved_queries,
          query_params=query_params,
          from_saved_query=from_saved_query,
          saved_query=saved_query,
          search_message=search_message))


ticket_list = staff_member_required(ticket_list)

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff:
        if not has_perm(request.user, 'helpdesk.change_ticket', ticket):
            raise Http403
    elif request.method == 'POST':
        form = EditTicketForm((request.POST), instance=ticket)
        if form.is_valid():
            ticket = form.save()
            if ticket.owner:
                ticket.owner_username = ticket.owner.username
            else:
                ticket.owner = request.user
                ticket.owner_username = request.user.username
            ticket.save()
            return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        form = EditTicketForm(instance=ticket)
    return render_to_resp(request=request, template_name='helpdesk/edit_ticket.html', context={'form': form})


edit_ticket = staff_member_required(edit_ticket)

def create_ticket(request):
    if helpdesk_settings.HELPDESK_STAFF_ONLY_TICKET_OWNERS:
        assignable_users = User.objects.filter(is_active=True, is_staff=True).order_by(User.USERNAME_FIELD)
    else:
        assignable_users = User.objects.filter(is_active=True).order_by(User.USERNAME_FIELD)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        form.fields['queue'].choices = [('', '--------')] + [[q.id, q.title] for q in Queue.objects.all()]
        form.fields['assigned_to'].choices = [('', '--------')] + [[u.id, u.get_username()] for u in assignable_users]
        if form.is_valid():
            ticket = form.save(user=(request.user))
            ticket.creator = request.user
            ticket.creator_username = request.user.username
            ticket.owner = request.user
            ticket.owner_username = request.user.username
            ticket.save()
            return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        initial_data = {}
        if request.user.usersettings.settings.get('use_email_as_submitter', False):
            if request.user.email:
                initial_data['submitter_email'] = request.user.email
        if 'queue' in request.GET:
            initial_data['queue'] = request.GET['queue']
        form = TicketForm(initial=initial_data)
        form.fields['queue'].choices = [('', '--------')] + [[q.id, q.title] for q in Queue.objects.all()]
        form.fields['assigned_to'].choices = [('', '--------')] + [[u.id, u.get_username()] for u in assignable_users]
        if helpdesk_settings.HELPDESK_CREATE_TICKET_HIDE_ASSIGNED_TO:
            form.fields['assigned_to'].widget = forms.HiddenInput()
        return render_to_resp(request=request, template_name='helpdesk/create_ticket.html', context={'form': form})


create_ticket = staff_member_required(create_ticket)

def raw_details(request, type):
    if type not in ('preset', ):
        raise Http404
    if type == 'preset':
        if request.GET.get('id', False):
            try:
                preset = PreSetReply.objects.get(id=(request.GET.get('id')))
                return HttpResponse(preset.body)
            except PreSetReply.DoesNotExist:
                raise Http404

    raise Http404


raw_details = staff_member_required(raw_details)

def hold_ticket(request, ticket_id, unhold=False):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if unhold:
        ticket.on_hold = False
        title = _('Ticket taken off hold')
    else:
        ticket.on_hold = True
        title = _('Ticket placed on hold')
    f = FollowUp(ticket=ticket,
      user=(request.user),
      title=title,
      date=(timezone.now()),
      public=True)
    f.save()
    ticket.save()
    return HttpResponseRedirect(ticket.get_absolute_url())


hold_ticket = staff_member_required(hold_ticket)

def unhold_ticket(request, ticket_id):
    return hold_ticket(request, ticket_id, unhold=True)


unhold_ticket = staff_member_required(unhold_ticket)

def rss_list(request):
    return render_to_resp(request=request, template_name='helpdesk/rss_list.html', context={'queues': Queue.objects.all()})


rss_list = staff_member_required(rss_list)

def report_index(request):
    if not request.user.is_staff:
        raise Http403
    number_tickets = Ticket.objects.all().count()
    saved_query = request.GET.get('saved_query', None)
    return render_to_resp(request=request, template_name='helpdesk/report_index.html', context={'number_tickets':number_tickets, 
     'saved_query':saved_query})


report_index = staff_member_required(report_index)

def run_report(request, report):
    if not request.user.is_staff:
        raise Http403
    else:
        if Ticket.objects.all().count() == 0 or report not in ('queuemonth', 'usermonth',
                                                               'queuestatus', 'queuepriority',
                                                               'userstatus', 'userpriority',
                                                               'userqueue', 'daysuntilticketclosedbymonth'):
            return HttpResponseRedirect(reverse('helpdesk_report_index'))
        report_queryset = Ticket.objects.all().select_related()
        limit_queues_by_user = helpdesk_settings.HELPDESK_ENABLE_PER_QUEUE_STAFF_MEMBERSHIP and not request.user.is_superuser
        if limit_queues_by_user:
            try:
                report_queryset = report_queryset.filter(queue__in=(request.user.queuemembership.queues.all()))
            except QueueMembership.DoesNotExist:
                report_queryset = report_queryset.none()

    from_saved_query = False
    saved_query = None
    if request.GET.get('saved_query', None):
        from_saved_query = True
        try:
            saved_query = SavedSearch.objects.get(pk=(request.GET.get('saved_query')))
        except SavedSearch.DoesNotExist:
            return HttpResponseRedirect(reverse('helpdesk_report_index'))
        else:
            if not saved_query.shared:
                if not saved_query.user == request.user:
                    return HttpResponseRedirect(reverse('helpdesk_report_index'))
        import pickle
        from base64 import b64decode
        query_params = pickle.loads(b64decode(str(saved_query.query).encode()))
        report_queryset = apply_query(report_queryset, query_params)
    from collections import defaultdict
    summarytable = defaultdict(int)
    summarytable2 = defaultdict(int)

    def month_name(m):
        return MONTHS_3[m].title()

    first_ticket = Ticket.objects.all().order_by('created')[0]
    first_month = first_ticket.created.month
    first_year = first_ticket.created.year
    last_ticket = Ticket.objects.all().order_by('-created')[0]
    last_month = last_ticket.created.month
    last_year = last_ticket.created.year
    periods = []
    year, month = first_year, first_month
    working = True
    periods.append('%s %s' % (month_name(month), year))
    while working:
        month += 1
        if month > 12:
            year += 1
            month = 1
        if not year > last_year:
            if month > last_month:
                if year >= last_year:
                    working = False
        periods.append('%s %s' % (month_name(month), year))

    if report == 'userpriority':
        title = _('User by Priority')
        col1heading = _('User')
        possible_options = [t[1].title() for t in Ticket.PRIORITY_CHOICES]
        charttype = 'bar'
    else:
        if report == 'userqueue':
            title = _('User by Queue')
            col1heading = _('User')
            queue_options = Queue.objects.all()
            if limit_queues_by_user:
                try:
                    queue_options = queue_options.filter(pk__in=(request.user.queuemembership.queues.all()))
                except QueueMembership.DoesNotExist:
                    queue_options = queue_options.none()

            possible_options = [q.title for q in queue_options]
            charttype = 'bar'
        else:
            if report == 'userstatus':
                title = _('User by Status')
                col1heading = _('User')
                possible_options = [s[1].title() for s in Ticket.STATUS_CHOICES]
                charttype = 'bar'
            else:
                if report == 'usermonth':
                    title = _('User by Month')
                    col1heading = _('User')
                    possible_options = periods
                    charttype = 'date'
                else:
                    if report == 'queuepriority':
                        title = _('Queue by Priority')
                        col1heading = _('Queue')
                        possible_options = [t[1].title() for t in Ticket.PRIORITY_CHOICES]
                        charttype = 'bar'
                    else:
                        if report == 'queuestatus':
                            title = _('Queue by Status')
                            col1heading = _('Queue')
                            possible_options = [s[1].title() for s in Ticket.STATUS_CHOICES]
                            charttype = 'bar'
                        else:
                            if report == 'queuemonth':
                                title = _('Queue by Month')
                                col1heading = _('Queue')
                                possible_options = periods
                                charttype = 'date'
                            else:
                                if report == 'daysuntilticketclosedbymonth':
                                    title = _('Days until ticket closed by Month')
                                    col1heading = _('Queue')
                                    possible_options = periods
                                    charttype = 'date'
                                metric3 = False
                                for ticket in report_queryset:
                                    if report == 'userpriority':
                                        metric1 = '%s' % ticket.get_assigned_to
                                        metric2 = '%s' % ticket.get_priority_display()
                                    else:
                                        if report == 'userqueue':
                                            metric1 = '%s' % ticket.get_assigned_to
                                            metric2 = '%s' % ticket.queue.title
                                        else:
                                            if report == 'userstatus':
                                                metric1 = '%s' % ticket.get_assigned_to
                                                metric2 = '%s' % ticket.get_status_display()
                                            else:
                                                if report == 'usermonth':
                                                    metric1 = '%s' % ticket.get_assigned_to
                                                    metric2 = '%s %s' % (month_name(ticket.created.month), ticket.created.year)
                                                else:
                                                    if report == 'queuepriority':
                                                        metric1 = '%s' % ticket.queue.title
                                                        metric2 = '%s' % ticket.get_priority_display()
                                                    else:
                                                        if report == 'queuestatus':
                                                            metric1 = '%s' % ticket.queue.title
                                                            metric2 = '%s' % ticket.get_status_display()
                                                        else:
                                                            if report == 'queuemonth':
                                                                metric1 = '%s' % ticket.queue.title
                                                                metric2 = '%s %s' % (month_name(ticket.created.month), ticket.created.year)
                                                            else:
                                                                if report == 'daysuntilticketclosedbymonth':
                                                                    metric1 = '%s' % ticket.queue.title
                                                                    metric2 = '%s %s' % (month_name(ticket.created.month), ticket.created.year)
                                                                    metric3 = ticket.modified - ticket.created
                                                                    metric3 = metric3.days
                                                                summarytable[(metric1, metric2)] += 1
                                    if metric3 and report == 'daysuntilticketclosedbymonth':
                                        summarytable2[(metric1, metric2)] += metric3

                                table = []
                                if report == 'daysuntilticketclosedbymonth':
                                    for key in summarytable2:
                                        summarytable[key] = summarytable2[key] / summarytable[key]

                                header1 = sorted(set(list((i for i, _ in summarytable))))
                                column_headings = [
                                 col1heading] + possible_options
                                for item in header1:
                                    data = []
                                    for hdr in possible_options:
                                        data.append(summarytable[(item, hdr)])

                                    table.append([item] + data)

                                return render_to_resp(request=request, template_name='helpdesk/report_output.html', context={'title':title, 
                                 'charttype':charttype, 
                                 'data':table, 
                                 'headings':column_headings, 
                                 'from_saved_query':from_saved_query, 
                                 'saved_query':saved_query})


run_report = staff_member_required(run_report)

def save_query(request):
    title = request.POST.get('title', None)
    shared = request.POST.get('shared', False) in ('on', 'True', True, 'TRUE')
    query_encoded = request.POST.get('query_encoded', None)
    return title and query_encoded or HttpResponseRedirect(reverse('helpdesk_list'))
    query = SavedSearch(title=title, shared=shared, query=query_encoded, user=(request.user))
    query.save()
    return HttpResponseRedirect('%s?saved_query=%s' % (reverse('helpdesk_list'), query.id))


save_query = staff_member_required(save_query)

def delete_saved_query(request, id):
    query = get_object_or_404(SavedSearch, id=id, user=(request.user))
    if request.method == 'POST':
        query.delete()
        return HttpResponseRedirect(reverse('helpdesk_list'))
    return render_to_resp(request=request, template_name='helpdesk/confirm_delete_saved_query.html', context={'query': query})


delete_saved_query = staff_member_required(delete_saved_query)

def user_settings(request):
    s = request.user.usersettings
    if request.POST:
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            s.settings = form.cleaned_data
            s.save()
    else:
        form = UserSettingsForm(s.settings)
    return render_to_resp(request=request, template_name='helpdesk/user_settings.html', context={'form': form})


user_settings = staff_member_required(user_settings)

def email_ignore(request):
    return render_to_resp(request=request, template_name='helpdesk/email_ignore_list.html', context={'ignore_list': IgnoreEmail.objects.all()})


email_ignore = superuser_required(email_ignore)

def email_ignore_add(request):
    if request.method == 'POST':
        form = EmailIgnoreForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('helpdesk_email_ignore'))
    else:
        form = EmailIgnoreForm(request.GET)
    return render_to_resp(request=request, template_name='helpdesk/email_ignore_add.html', context={'form': form})


email_ignore_add = superuser_required(email_ignore_add)

def email_ignore_del(request, id):
    ignore = get_object_or_404(IgnoreEmail, id=id)
    if request.method == 'POST':
        ignore.delete()
        return HttpResponseRedirect(reverse('helpdesk_email_ignore'))
    return render_to_resp(request=request, template_name='helpdesk/email_ignore_del.html', context={'ignore': ignore})


email_ignore_del = superuser_required(email_ignore_del)

def ticket_cc(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    copies_to = ticket.ticketcc_set.all()
    return render_to_resp(request=request, template_name='helpdesk/ticket_cc_list.html', context={'copies_to':copies_to, 
     'ticket':ticket})


ticket_cc = staff_member_required(ticket_cc)

def ticket_cc_add(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketCCForm(request.POST)
        if form.is_valid():
            ticketcc = form.save(commit=False)
            ticketcc.ticket = ticket
            ticketcc.save()
            return HttpResponseRedirect(reverse('helpdesk_ticket_cc', kwargs={'ticket_id': ticket.id}))
    else:
        form = TicketCCForm()
    return render_to_resp(request=request, template_name='helpdesk/ticket_cc_add.html', context={'ticket':ticket, 
     'form':form})


ticket_cc_add = staff_member_required(ticket_cc_add)

def ticket_cc_del(request, ticket_id, cc_id):
    cc = get_object_or_404(TicketCC, ticket__id=ticket_id, id=cc_id)
    if request.method == 'POST':
        cc.delete()
        return HttpResponseRedirect(reverse('helpdesk_ticket_cc', kwargs={'ticket_id': cc.ticket.id}))
    return render_to_resp(request=request, template_name='helpdesk/ticket_cc_del.html', context={'cc': cc})


ticket_cc_del = staff_member_required(ticket_cc_del)

def ticket_dependency_add(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketDependencyForm(request.POST)
        if form.is_valid():
            ticketdependency = form.save(commit=False)
            ticketdependency.ticket = ticket
            if ticketdependency.ticket != ticketdependency.depends_on:
                ticketdependency.save()
            return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket.id]))
    else:
        form = TicketDependencyForm()
    return render_to_resp(request=request, template_name='helpdesk/ticket_dependency_add.html', context={'ticket':ticket, 
     'form':form})


ticket_dependency_add = staff_member_required(ticket_dependency_add)

def ticket_dependency_del(request, ticket_id, dependency_id):
    dependency = get_object_or_404(TicketDependency, ticket__id=ticket_id, id=dependency_id)
    if request.method == 'POST':
        dependency.delete()
        return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket_id]))
    return render_to_resp(request=request, template_name='helpdesk/ticket_dependency_del.html', context={'dependency': dependency})


ticket_dependency_del = staff_member_required(ticket_dependency_del)

def attachment_del(request, ticket_id, attachment_id):
    get_object_or_404(Ticket, id=ticket_id)
    attachment = get_object_or_404(Attachment, id=attachment_id)
    attachment.delete()
    return HttpResponseRedirect(reverse('helpdesk_view', args=[ticket_id]))


attachment_del = staff_member_required(attachment_del)

def calc_average_nbr_days_until_ticket_resolved(Tickets):
    nbr_closed_tickets = len(Tickets)
    days_per_ticket = 0
    days_each_ticket = list()
    for ticket in Tickets:
        time_ticket_open = ticket.modified - ticket.created
        days_this_ticket = time_ticket_open.days
        days_per_ticket += days_this_ticket
        days_each_ticket.append(days_this_ticket)

    if nbr_closed_tickets > 0:
        mean_per_ticket = days_per_ticket / nbr_closed_tickets
    else:
        mean_per_ticket = 0
    return mean_per_ticket


def calc_basic_ticket_stats(Tickets):
    all_open_tickets = Tickets.exclude(status=(Ticket.CLOSED_STATUS))
    today = datetime.today()
    date_30 = date_rel_to_today(today, 30)
    date_60 = date_rel_to_today(today, 60)
    date_30_str = date_30.strftime('%Y-%m-%d')
    date_60_str = date_60.strftime('%Y-%m-%d')
    ota_le_30 = all_open_tickets.filter(created__gte=date_30_str)
    N_ota_le_30 = len(ota_le_30)
    ota_le_60_ge_30 = all_open_tickets.filter(created__gte=date_60_str, created__lte=date_30_str)
    N_ota_le_60_ge_30 = len(ota_le_60_ge_30)
    ota_ge_60 = all_open_tickets.filter(created__lte=date_60_str)
    N_ota_ge_60 = len(ota_ge_60)
    ots = list()
    ots.append(['< 30 days', N_ota_le_30, get_color_for_nbr_days(N_ota_le_30), sort_string(date_30_str, '')])
    ots.append(['30 - 60 days', N_ota_le_60_ge_30, get_color_for_nbr_days(N_ota_le_60_ge_30), sort_string(date_60_str, date_30_str)])
    ots.append(['> 60 days', N_ota_ge_60, get_color_for_nbr_days(N_ota_ge_60), sort_string('', date_60_str)])
    all_closed_tickets = Tickets.filter(status=(Ticket.CLOSED_STATUS))
    average_nbr_days_until_ticket_closed = calc_average_nbr_days_until_ticket_resolved(all_closed_tickets)
    all_closed_last_60_days = all_closed_tickets.filter(created__gte=date_60_str)
    average_nbr_days_until_ticket_closed_last_60_days = calc_average_nbr_days_until_ticket_resolved(all_closed_last_60_days)
    basic_ticket_stats = {'average_nbr_days_until_ticket_closed':average_nbr_days_until_ticket_closed, 
     'average_nbr_days_until_ticket_closed_last_60_days':average_nbr_days_until_ticket_closed_last_60_days, 
     'open_ticket_stats':ots}
    return basic_ticket_stats


def get_color_for_nbr_days(nbr_days):
    """ """
    if nbr_days < 5:
        color_string = 'green'
    else:
        if nbr_days >= 5 and nbr_days < 10:
            color_string = 'orange'
        else:
            color_string = 'red'
    return color_string


def days_since_created(today, ticket):
    return (today - ticket.created).days


def date_rel_to_today(today, offset):
    return today - timedelta(days=offset)


def sort_string(begin, end):
    return 'sort=created&date_from=%s&date_to=%s&status=%s&status=%s&status=%s' % (begin, end, Ticket.OPEN_STATUS, Ticket.REOPENED_STATUS, Ticket.RESOLVED_STATUS)