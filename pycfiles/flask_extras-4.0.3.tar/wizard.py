# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_extras/flask_extras/forms/wizard.py
# Compiled at: 2016-12-06 13:26:11
"""A simple multi-step wizard that uses the flask application session.

Creating multi-step forms of arbitrary length is simple and intuitive.

Example usage:

```
from flask.ext.wtf import FlaskForm

class MultiStepTest1(FlaskForm):
    field1 = StringField(validators=[validators.DataRequired()],)
    field2 = StringField(validators=[validators.DataRequired()],)

class MultiStepTest2(FlaskForm):
    field3 = StringField(validators=[validators.DataRequired()],)
    field4 = StringField(validators=[validators.DataRequired()],)

class MyCoolForm(MultiStepWizard):
    __forms__ = [
        MultiStepTest1,
        MultiStepTest2,
    ]
```
"""
from flask import session
from flask_wtf import FlaskForm

class MultiStepWizard(FlaskForm):
    """Generates a multi-step wizard.

    The wizard uses the app specified session backend to store both
    form data and current step.

    TODO: make sure all the expected features of the typical form
    are exposed here, but automatically determining the active form
    and deferring to it. See __iter__ and data for examples.
    """
    __forms__ = []

    def __iter__(self):
        """Get the specific forms' fields for standard WTForm iteration."""
        _, form = self.get_active()
        return form.__iter__()

    def __len__(self):
        """Override the len method to emulate standard wtforms."""
        return len(self.__forms)

    def __getitem__(self, key):
        """Override getitem to emulate standard wtforms."""
        return self.active_form.__getitem__(key)

    def __contains__(self, item):
        """Override contains to emulate standard wtforms."""
        return self.active_form.__contains__(item)

    def __init__(self, *args, **kwargs):
        """Do all the required setup for managing the forms."""
        super(MultiStepWizard, self).__init__(*args, **kwargs)
        self.name = kwargs.get('session_key', self.__class__.__name__)
        curr_step = session.get(self.name, {}).get('curr_step', 1)
        if 'curr_step' in kwargs:
            curr_step = int(kwargs.pop('curr_step'))
        if curr_step > len(self.__forms__):
            curr_step = 1
        self.step = curr_step
        self.__forms = []
        self._setup_session()
        self._populate_forms()
        invalid_forms_msg = 'Something happened during form population.'
        assert len(self.__forms) == len(self.__forms__), invalid_forms_msg
        assert len(self.__forms) > 0, 'Need at least one form!'
        self.active_form = self.get_active()[1]
        self._setfields()

    def _setfields(self):
        """Dynamically set fields for this particular form step."""
        _, form = self.get_active()
        for name, val in vars(form).items():
            if repr(val).startswith('<UnboundField'):
                setattr(self, name, val)

    def alldata(self, combine_fields=False, flush_after=False):
        """Get the specific forms data."""
        _alldata = dict()
        if self.name in session:
            _alldata = session[self.name].get('data')
            if combine_fields:
                combined = dict()
                for formname, data in _alldata.items():
                    if data is not None:
                        combined.update(data)

                _alldata = combined
        if flush_after:
            self.flush()
        return _alldata

    @property
    def data(self):
        """Get the specific forms data."""
        _, form = self.get_active()
        return form.data

    @property
    def forms(self):
        """Get all forms."""
        return self.__forms

    def _setup_session(self):
        """Setup session placeholders for later use."""
        if self.name not in session:
            session[self.name] = dict(curr_step=self.curr_step, data={f.__name__:None for f in self.__forms__})

    def _populate_forms(self):
        """Populate all forms with existing data for validation.

        This will only be done if the session data exists for a form.
        """
        if len(self.__forms) > 0:
            return
        else:
            for form in self.__forms__:
                data = session[self.name]['data'].get(form.__name__)
                init_form = form(**data) if data is not None else form()
                self.__forms.append(init_form)

            return

    def _update_session_formdata(self, form):
        """Update session data for a given form key."""
        name = form.__class__.__name__
        data = form.data
        session[self.name]['data'][name] = data

    @property
    def active_name(self):
        """Return the nice name of this form class."""
        return self.active_form.__class__.__name__

    def next_step(self):
        """Set the step number in the session to the next value."""
        next_step = session[self.name]['curr_step'] + 1
        self.curr_step = next_step
        if self.name in session:
            session[self.name]['curr_step'] += 1

    @property
    def step(self):
        """Get the current step."""
        if self.name in session:
            return session[self.name]['curr_step']

    @step.setter
    def step(self, step_val):
        """Set the step number in the session."""
        self.curr_step = step_val
        if self.name in session:
            session[self.name]['curr_step'] = step_val

    def validate_on_submit(self, *args, **kwargs):
        """Override validator and setup session updates for persistence."""
        step, form = self.get_active()
        self._update_session_formdata(form)
        if not form.validate_on_submit():
            self.step = step - 1
            return False
        if step - 1 < len(self.__forms):
            self.curr_step += 1
            self.active_form = self.__forms[(self.curr_step - 1)]
            self.next_step()
        elif step - 1 == len(self.__forms):
            self.step = -1
        return True

    @property
    def remaining(self):
        """Get the number of steps remaining."""
        return len(self.__forms[self.curr_step:]) + 1

    @property
    def total_steps(self):
        """Get the number of steps for this form in a (non-zero index)."""
        return len(self.__forms)

    @property
    def steps(self):
        """Get a list of the steps for iterating in views, html, etc."""
        return range(1, self.total_steps + 1)

    def get_active(self):
        """Get active step."""
        form_index = self.curr_step - 1 if self.curr_step > 0 else 0
        return (self.curr_step + 1, self.__forms[form_index])

    def flush(self):
        """Clear data and reset."""
        del session[self.name]

    def is_complete(self):
        """Determine if all forms have been completed."""
        if self.name not in session:
            return False
        completed = self.step == -1
        if completed:
            self.curr_step = 1
        return completed