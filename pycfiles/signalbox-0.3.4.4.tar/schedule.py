# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/schedule.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime, timedelta, time
import datetime as dtmod, itertools as it
from dateutil import *
from dateutil.parser import *
from dateutil.rrule import *
from dateutil_constants import *
from django.contrib.humanize.templatetags.humanize import ordinal
from django.core.exceptions import ValidationError
from django.db import models
from django.template import Context, Template
from naturaltimes import parse_natural_date
from signalbox.utilities.djangobits import render_string_with_context, safe_help
from signalbox.utilities.djangobits import supergetattr
from signalbox.utilities.linkedinline import admin_edit_url
from signalbox.utils import csv_to_list
import validators as v
NATURAL_DATE_SYNTAX_HELP = safe_help('\nEach line in this field will be read as a date on which to make an observation\nwhen the script is executed. By default each date is created relative to the\ncurrent date and time at midnight. For example, if a user signed up when this\npage loaded, these lines:\n\n<code>now</code>, <code>next week</code>, and <code>in 3 days at 5pm</code>\nwould create the following dates: <div id="exampletimes">.</div>\n\n\n<input type=hidden id="examplesyntax" value="now \n next week \n in 3 days at 5pm">\n<script type="text/javascript">\n$.post("/admin/signalbox/preview/timings/",\n    {\'syntax\': $(\'#examplesyntax\').val() },\n    function(data) { $(\'#exampletimes\').html(data);}\n);\n</script>\n\n<div class="alert">\n<i class="icon-warning-sign"></i>\nNote that specifying options here will override other\nadvanced timing options specified in other panels.</div>\n\n<a class="btn timingsdetail" href="#"\n    onclick="$(\'.timingsdetail\').toggle();return false;">Show more examples</a>\n\n<div class="hide timingsdetail">\n\nOther examples include:\n\n<pre>\n    3 days from now\n    a day ago\n    in 2 weeks\n    in 3 days at 5pm\n    now\n    10 minutes ago\n    10 minutes from now\n    in 10 minutes\n    in a minute\n    in 30 seconds\n    tomorrow at noon\n    tomorrow at 6am\n    today at 12:15 AM\n    2 days from today at 2pm\n    a week from today\n    a week from now\n    3 weeks ago\n    next Sunday at noon\n    Sunday noon\n    next Sunday at 2pm\n</pre>\n\nHOWEVER - you must check the times have been interpreted properly before using\nthe script.\n</div>\n\n')

class ScriptType(models.Model):
    """Defines what gets created by a Script."""
    name = models.CharField(max_length=255)
    observation_subclass_name = models.CharField(blank=True, max_length=255)
    require_study_ivr_number = models.BooleanField(default=False)
    sends_message_to_user = models.BooleanField(default=True, help_text='True\n        if observations created with this type of script send some form of\n        message to a user (e.g. email, sms or phone calls).')

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'signalbox'


class Reminder(models.Model):
    """Describes a reminder (c.f. ReminderInstance, ScriptReminder)"""
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=100, choices=((i, i) for i in ['sms', 'email']), default='email')
    from_address = models.EmailField(blank=True, help_text=safe_help("\nThe email address you want the reminder to appear as if it\nhas come from. Think carefully before making this something other than\nyour own email, and be sure the smpt server you are using will accept\nthis  as a from address (if you're not sure, check). If blank this will be the\nstudy email. For SMS reminders the callerid will be the SMS return number\nspecified for the Study."))
    subject = models.CharField(max_length=1024, blank=True, verbose_name='Reminder email subject', help_text='For reminder emails only')
    message = models.TextField(blank=True, help_text='The body of the message.\n        See the documentation for message_body fields on the Script model for\n        more details. You can include some variable with {{}} syntax, for\n        example {{url}} will include a link back to the observation.', verbose_name='Reminder message')

    def admin_edit_url(self):
        return admin_edit_url(self)

    class Meta:
        app_label = 'signalbox'

    def __unicode__(self):
        return self.name


class ScriptReminder(models.Model):
    """Link Model between Reminders and Scripts (c.f. ReminderInstance)"""
    hours_delay = models.PositiveIntegerField(default='48')
    script = models.ForeignKey('signalbox.Script')
    reminder = models.ForeignKey('signalbox.Reminder')

    def calculate_date(self, observation):
        return observation.due + timedelta(hours=self.hours_delay)

    def admin_edit_url(self):
        return admin_edit_url(self, indirect_pk_field='reminder')

    class Meta:
        app_label = 'signalbox'

    def __unicode__(self):
        return '%s attached to %s' % (self.reminder, self.script)


class Script(models.Model):
    """Defines :class:`Observation`s to be made and a schedule to make them.

    Scripts are attached to :class:`StudyCondition`s and used when
    :class:`Observation's are being added for a :class:`Membership` to determine
    a schedule of measurements.

    Scripts specify repeating rules using the python `dateutil` library.
    dateutil syntax can either be used directly (in the `raw_date_syntax` field)
    or by  completing the `repeat_by...` fields, which are combined to generate
    a repeating rule.

    Care (and some mental effort) needs to be taken when generating repeating
    rules that the schedule is as expected --- it's actually a complicated
    problem, and dateutil is very general and abstract in what it allows, which
    means most things are possible, but at the cost of complexity. In
    particular, fields like `repeat_bymonths` can interact with other options to
    create slightly counterintuitive results. When editing a Script in the
    django admin, a preview  of dates and times to be generated is available.
    However you should consider the possibility that times between observations,
    or the latency for the first observation,  may differ based on when the user
    is randomised. A simple example: if an observation is to be repeated by hour
    at 9am, a user signing up at 8am will recieve an observation right away,
    whereas one signing up at 10am will recieve their first only the next day.

    ..note:: It may often be a good idea to split observations across multiple
    scripts to avoid having to write very complicated repeating rules. """
    name = models.CharField(max_length=200, unique=False, help_text='This is the name participants will see')
    reference = models.CharField(max_length=200, unique=True, null=True, help_text='An internal reference. Not shown to participants.')
    admin_display_name = lambda self: self.reference or self.name
    admin_display_name.short_description = 'Reference/Name'
    admin_display_name.admin_order_field = 'reference'
    is_clinical_data = models.BooleanField(default=False, help_text='\n        If checked, indicates only clinicians and superusers should\n        have access to respones made to this script.')
    breaks_blind = models.BooleanField(default=True, help_text='If checked, indicates that observations created by this\n        Script have the potential to break the blind. If so, we will exclude\n        them from views which Assessors may access.')
    show_in_tasklist = models.BooleanField(verbose_name="Show in user's list of tasks to complete", default=True, help_text="Should :class:`Observation`s generated by this script\n        appear in  a user's list of tasks to complete.")
    allow_display_of_results = models.BooleanField(default=False, help_text='If checked, then replies to these observations may be\n        visible to some users in the Admin area (e.g. for screening\n        questionnaires). If unchecked then only superusers will be able to\n        preview replies to observations made using this script.')
    show_replies_on_dashboard = models.BooleanField(default=True, help_text='If true, replies to this script are visible to the user\n        on their personal dashboard.')
    script_type = models.ForeignKey('signalbox.ScriptType', help_text='IMPORTANT: This type attribute determines the\n        interpretation of some fields below.')
    asker = models.ForeignKey('ask.Asker', blank=True, null=True, help_text='Survey which the participant will complete for the\n        Observations created by this script', verbose_name='Attached questionnaire')
    external_asker_url = models.URLField(blank=True, null=True, verbose_name='Externally hosted questionnaire url', help_text='The full url of an external questionnaire. Note that\n            you can include {{variable}} syntax to identify the Reply or\n            Observation from which the user has been redirected. For example\n            including http://monkey.com/survey1?c={{reply.observation.dyad.user.username}}\n            would pass the username of the study participant to the external system.\n            In contrast including {{reply.observation.id}} would simply pass the\n            anonymous Observation id number. Where a questionnaire will be\n            completed more than once during the study, it iss recommended to\n            include the {{reply.id}} or {{reply.token}} to allow for reconciling\n            external data with internal data at a later date.')

    def parse_external_asker_url(self, reply):
        return render_string_with_context(self.external_asker_url, {'reply': reply})

    label = models.CharField(max_length=255, blank=True, default='{{script.name}}', help_text=safe_help('This field allows individual observations to have a\n        meaningful label when listed for participants.  Either enter a simple\n        text string, for example "Main questionnaire", or have the label created\n        dynamically from information about this script object.\n\nFor example, you can enter `{{i}}` to add the index in of a particular\nobservation in a sequence  of generated observations. If you enter `{{n}}`\nthen this will be the position (\'first\', \'second\' etc.).\n\nAdvanced use: If you want to reference attributes of the Script or Membership\nobjects these are passed in as extra context, so {{script.name}}\nincludes the script name, and `{{membership.user.last_name}}` would\ninclude the user\'s surname. Mistakes when entering  these variable names\nwill not result in an error, but won\'t produce any output either. '))
    script_subject = models.CharField(max_length=1024, blank=True, verbose_name='Email subject', help_text='Subject line of an email if required. Can use django\n        template syntax to include variables: {{var}}. Currently variables\n        available are {{url}} (the link to the questionnaire), {{user}} and\n        {{userprofile}} and {{observation}}.')
    script_body = models.TextField(blank=True, help_text="Used for Email or SMS body. Can use django template syntax\n        to include variables: {{var}}. Currently variables available are {{url}}\n        (the link to the questionnaire), {{user}} and {{userprofile}} and\n        {{observation}}. Note that these are references to the django objects\n        themselves, so you can use the dot notation to access other attributed.\n        {{user.email}} or {{user.last_name}} for example, would print the user's\n        email address or last name.", verbose_name='Message')
    user_instructions = models.TextField(blank=True, null=True, help_text='Instructions shown to user on their homepage and perhaps\n        elsewhere as the link to the survey. For example, "Please fill in the\n        questionnaire above. You will need to allow N minutes to do this  in\n        full." ')
    max_number_observations = models.IntegerField(default=1, help_text='The # of observations this scipt will generate.\n            Default is 1', verbose_name='create N observations')
    RRULES = [ (i, i) for i in ('YEARLY MONTHLY WEEKLY DAILY HOURLY MINUTELY SECONDLY').split(' ') ]
    repeat = models.CharField(max_length=80, choices=RRULES, default='DAILY')
    repeat_from = models.DateTimeField(blank=True, null=True, verbose_name='Fixed start date', help_text='Leave blank for the observations to start relative to the\n        datetime they are  created (i.e. when the participant is randomised)')
    repeat_interval = models.IntegerField(blank=True, null=True, help_text='The interval between each freq iteration. For example,\n        when repeating WEEKLY, an interval of 2 means once per fortnight,\n        but with HOURLY, it means once every two hours.', verbose_name='repeat interval')
    repeat_byhours = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=20, validators=[
     v.valid_hours_list], help_text="A number or list of integers, indicating the hours of the\n       day at which observations are made. For example, '13,19' would make\n       observations happen at 1pm and 7pm.", verbose_name='repeat at these hours')

    def repeat_byhours_list(self):
        return [ int(i) for i in csv_to_list(self.repeat_byhours) if int(i) < 24 ]

    repeat_byminutes = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=20, validators=[
     v.in_minute_range], help_text='A list of numbers indicating at what minutes past the\n        hour the observations should be created. E.g. 0,30 will create\n        observations on the hour and half hour', verbose_name='repeat at these minutes past the hour')

    def repeat_byminutes_list(self):
        return [ int(i) for i in csv_to_list(self.repeat_byminutes) ]

    repeat_bydays = models.CharField(blank=True, null=True, max_length=100, help_text='One or more of MO, TU, WE, TH, FR, SA, SU separated by a\n        comma, to indicate which days observations will be created on.', verbose_name='repeat on these days of the week')

    def repeat_bydays_list(self):
        return [ WEEKDAY_MAP[i.strip()[0:2]] for i in csv_to_list(self.repeat_bydays) ]

    repeat_bymonths = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=20, help_text="A comma separated list of months as numbers (1-12),\n        indicating the months in which obervations can be made. E.g. '1,6' would\n        mean observations are only made in Jan and June.", verbose_name='repeat in these months')

    def repeat_bymonths_list(self):
        return [ int(i) for i in csv_to_list(self.repeat_bymonths) ]

    repeat_bymonthdays = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=20, help_text="An integer or comma separated list of integers; represents\n        days within a  month on observations are created. For example, '1, 24'\n        would create observations on the first and 24th of each month.", verbose_name='on these days in the month')

    def repeat_bymonthdays_list(self):
        return [ int(i) for i in csv_to_list(self.repeat_bymonthdays) ]

    delay_by_minutes = models.IntegerField(default=0, help_text='Start the\n        observations this many minutes from the time the Observations are added.')
    delay_by_hours = models.IntegerField(default=0, help_text='Start the\n        observations this many hours from the time the Observations are added.')
    delay_by_days = models.IntegerField(default=0, help_text='Start the\n        observations this many days from the time the Observations are added.')
    delay_by_weeks = models.IntegerField(default=0, null=True, help_text='Start the\n        observations this many weeks from the time the Observations are added.')
    delay_in_whole_days_only = models.BooleanField(default=True, help_text='If true, observations are delayed to the nearest number of\n        whole days, and repeat rules will start from 00:00 on the morning of\n        that day.')

    def delay(self):
        """Calculate the interval until Observations start.

        Returns a dateime.TimeDelta object"""
        return timedelta(weeks=self.delay_by_weeks, days=self.delay_by_days, hours=self.delay_by_hours, minutes=self.delay_by_minutes)

    natural_date_syntax = models.TextField(blank=True, null=True, validators=[
     v.valid_natural_datetime], help_text=NATURAL_DATE_SYNTAX_HELP)

    def eval_natural_date_synax(self):
        timesanderrors = [ parse_natural_date(t) for t in self.natural_date_syntax.splitlines()
                         ]
        times = [ i for i, e in timesanderrors if not e ]
        return times

    completion_window = models.IntegerField(blank=True, null=True, help_text='Window in minutes during which the observation can be\n        completed. If left blank, the observation will not expire.')
    jitter = models.IntegerField(blank=True, null=True, help_text='Number of minutes (plus or minus) to randomise observation\n        timing by.')
    reminders = models.ManyToManyField('signalbox.Reminder', through='signalbox.ScriptReminder')

    def calculate_start_datetime(self, start_date=None):
        """Return the date the observations should start on."""
        start_date = start_date or datetime.now()
        if type(start_date) == dtmod.date:
            start_date = datetime.combine(start_date, time())
        startfrom = start_date + self.delay()
        if self.delay_in_whole_days_only:
            return startfrom.replace(hour=0, minute=0, second=0, microsecond=0)
        return startfrom

    def datetimes_with_natural_syntax(self):
        datesyntax = self.natural_date_syntax or 'ADVANCED'
        return [ {'datetime': i, 'syntax': j} for i, j, k in it.izip_longest(self.datetimes(), datesyntax.split('\n'), '')
               ]

    def preview_of_datetimes(self):
        code = lambda x: '<code>' + str(x) + '</code>'
        return safe_help(('<br>').join(map(code, list(self.datetimes()))))

    preview_of_datetimes.allow_tags = True

    def datetimes(self, start_date=None):
        if self.natural_date_syntax:
            return self.eval_natural_date_synax()
        else:
            kwargs = {'count': self.max_number_observations, 
               'interval': self.repeat_interval, 
               'byhour': self.repeat_byhours_list(), 
               'byminute': self.repeat_byminutes_list(), 
               'byweekday': self.repeat_bydays_list(), 
               'bymonth': self.repeat_bymonths_list(), 
               'bymonthday': self.repeat_bymonthdays_list(), 
               'dtstart': self.calculate_start_datetime(start_date=start_date)}
            kwargs = dict([ (k, v) for k, v in kwargs.items() if v ])
            return rrule(FREQ_MAP[self.repeat], **kwargs)

    def make_observations(self, membership):
        from signalbox.models import Observation
        times = self.datetimes(membership.date_randomised)
        times_indexes = zip(times, xrange(1, len(list(times)) + 1))
        observations = []
        for time, index in times_indexes:
            observations.append(Observation(due_original=time, n_in_sequence=index, label=render_string_with_context(self.label, {'i': index, 'n': ordinal(index), 
               'script': self, 
               'membership': membership}), dyad=membership, created_by_script=self))

        [ i.save() for i in observations ]
        return observations

    class Meta:
        ordering = [
         'reference', 'name']
        app_label = 'signalbox'

    def clean(self):
        if self.asker and self.external_asker_url:
            raise ValidationError("You can't use both an internal\n                                    Questionnaire and one hosted on an external site.")
        if self.asker and supergetattr(self, 'script_type.require_study_ivr_number', False):
            last_q = self.asker.questions()[(-1)]
            if last_q.q_type != 'hangup':
                raise ValidationError(("The last question of a telephone call needs to be a 'hangup' type (currently {})").format(last_q.q_type))
        if self and self.script_type and self.script_type.name == 'TwilioSMS':
            if len(self.script_body) > 160:
                raise ValidationError('Messages must be < 160 characters long.')

    def __unicode__(self):
        return '(%s) %s' % (self.reference, self.name)