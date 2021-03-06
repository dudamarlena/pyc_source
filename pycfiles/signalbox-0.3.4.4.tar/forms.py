# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/forms.py
# Compiled at: 2014-08-27 19:26:12
from ask.models import Asker
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.formtools.wizard.views import CookieWizardView
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.views.generic.edit import ProcessFormView
from localflavor.gb.forms import GBCountySelect, GBPostcodeField
from registration.forms import RegistrationForm
import selectable.forms
from signalbox.lookups import UserLookup
from signalbox.models import Membership, Reply, Study, UserProfile, UserMessage, ContactRecord, Answer
from signalbox.models.validators import date_in_past
from signalbox.models.validators import is_mobile_number, is_number_from_study_area, could_be_number
from signalbox.phone_field import PhoneNumberFormField, as_phone_number
from signalbox.utilities.djangobits import supergetattr
from django.contrib.auth import get_user_model
User = get_user_model()

def get_answers(studies):
    mems = set(Membership.objects.filter(study__in=studies))
    que = Q(observation__dyad__study__in=studies) | Q(membership__in=mems)
    replies = Reply.objects.filter(que)
    answers = Answer.objects.all().select_related('question', 'question__choiceset', 'question__scoresheet').filter(reply__in=replies).exclude(question__variable_name__isnull=True).order_by('reply')
    return answers


class DateShiftForm(forms.Form):
    """Form to allow researcher to choose a new date, used to shift observations for a Membership.
    """
    new_randomised_date = forms.DateTimeField(required=True, help_text='i.e., the date on which the participant really joined the study.\n        Observations not already complete will be shifted in time to the day/time\n        they would have been created, had the participant joined on this day.')

    def delta(self, current):
        """Return the time difference from ``current`` to new randomised date."""
        cleaned_data = super(DateShiftForm, self).clean()
        return cleaned_data.get('new_randomised_date').date() - current


class NewParticipantWizard(CookieWizardView):
    """Wizard to allow a user to be added along with a userprofile.

    Only used the in admin interface. See SignupForm below for the form used in conjunction
    with django_registration on the front end.
    """
    template_name = 'signalbox/wizard_form.html'

    def done(self, form_list, **kwargs):
        userform = form_list[0]
        passwordform = form_list[1]
        user = userform.save(commit=True)
        ps1 = passwordform.cleaned_data.get('password', None)
        if ps1:
            user.set_password(ps1)
        else:
            user.set_unusable_password()
        user.save()
        messages.add_message(self.request, messages.INFO, ('Created new user: {}').format(user.username))
        return HttpResponseRedirect(reverse('edit_participant', args=(user.id,)))


class ParticipantPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), help_text='Leave blank to set password later.', required=False)
    password_again = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)

    def clean(self):
        ps1 = self.cleaned_data.get('password', None)
        ps2 = self.cleaned_data.get('password_again', None)
        if (ps1 or ps2) and ps1 != ps2:
            raise forms.ValidationError('Passwords need to match...')
        return self.cleaned_data


class SelectExportDataForm(forms.Form):
    studies = forms.ModelMultipleChoiceField(queryset=Study.objects.all(), required=False)
    questionnaires = forms.ModelMultipleChoiceField(queryset=Asker.objects.all(), required=False)


class ContactRecordForm(forms.ModelForm):
    """Form to add ContactRecords on participants.

    Sometimes auto-specifies participant and current user"""
    participant = selectable.AutoCompleteSelectField(label='Type the name of the participant:', lookup_class=UserLookup, required=True)
    added_by = selectable.AutoCompleteSelectField(label='Who is adding this record?', lookup_class=UserLookup, required=True)

    class Meta:
        model = ContactRecord
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ContactRecordForm, self).__init__(*args, **kwargs)
        meta = getattr(self, 'Meta', None)
        exclude = getattr(meta, 'exclude', [])
        for field_name in exclude:
            if field_name in self.fields:
                del self.fields[field_name]

        return


ShortContactRecordForm = modelform_factory(ContactRecord, ContactRecordForm, exclude=('added_by',
                                                                                      'participant'))

class UserMessageForm(forms.ModelForm):
    """Form to send Emails or SMS messages to users and store a record."""
    message_to = selectable.AutoCompleteSelectField(label='To:', help_text="Type part of the participant's name, userid or email for autocompletion.", lookup_class=UserLookup, required=True)

    class Meta:
        model = UserMessage
        exclude = ['message_from', 'state']

    def clean(self):
        """SMS messages can't have subject lines and are < 130 characters"""
        cleaned_data = self.cleaned_data
        message_type = cleaned_data.get('message_type')
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')
        if message_type == 'SMS' and subject:
            raise forms.ValidationError('SMS messages cannot have a subject.')
        if message_type == 'SMS' and len(message) > 130:
            raise forms.ValidationError('SMS messages cannot be over 130 characters long.')
        return cleaned_data


class FindParticipantForm(forms.Form):
    """Quick lookup (autocompleted) form to find a participant.

    Would normally then redirect to overview."""
    participant = selectable.AutoCompleteSelectField(label='Find a participant', lookup_class=UserLookup, required=True, allow_new=True, help_text="Type part of the participant's name/userid to autocomplete.")


class CreateParticipantForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserProfileForm(forms.ModelForm):
    postcode = GBPostcodeField(required=False)
    county = GBCountySelect()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        visible_fields = settings.DEFAULT_USER_PROFILE_FIELDS
        visible_fields.extend(request.user.userprofile.get_required_fields_for_studies())
        for k in request.user.userprofile.get_required_fields_for_studies():
            setattr(self.fields[k], 'required', True)

        for k, v in self.fields.items():
            if k not in visible_fields:
                del self.fields[k]

        self.num_fields = len(filter(bool, visible_fields))
        return

    class Meta:
        model = UserProfile
        fields = settings.USER_PROFILE_FIELDS