# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/forms.py
# Compiled at: 2018-04-26 09:36:24
# Size of source mod 2**32: 6787 bytes
from __future__ import unicode_literals
from hashlib import md5
from six.moves.urllib.parse import urlencode
import six
from django import forms
from robokassa.conf import LOGIN, PASSWORD1, PASSWORD2, TEST_MODE, STRICT_CHECK, FORM_TARGET, EXTRA_PARAMS
from robokassa.models import SuccessNotification

class BaseRobokassaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseRobokassaForm, self).__init__(*args, **kwargs)
        for key in EXTRA_PARAMS:
            self.fields['shp' + key] = forms.CharField(required=False)
            if 'initial' in kwargs:
                self.fields[('shp' + key)].initial = kwargs['initial'].get(key, 'None')

    def _append_extra_part(self, standard_part, value_func):
        extra_part = ':'.join(['%s=%s' % ('shp' + key, value_func('shp' + key)) for key in EXTRA_PARAMS])
        if extra_part:
            return ':'.join([standard_part, extra_part])
        return standard_part

    def extra_params(self):
        extra = {}
        for param in EXTRA_PARAMS:
            if 'shp' + param in self.cleaned_data:
                extra[param] = self.cleaned_data[('shp' + param)]

        return extra

    def _get_signature(self):
        return md5(self._get_signature_string().encode('utf-8')).hexdigest().upper()

    def _get_signature_string(self):
        raise NotImplementedError


class RobokassaForm(BaseRobokassaForm):
    MrchLogin = forms.CharField(max_length=20, initial=LOGIN)
    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2, required=False)
    InvId = forms.IntegerField(min_value=0, required=False)
    Desc = forms.CharField(max_length=100, required=False)
    SignatureValue = forms.CharField(max_length=32)
    IncCurrLabel = forms.CharField(max_length=10, required=False)
    Email = forms.CharField(max_length=100, required=False)
    Culture = forms.CharField(max_length=10, required=False)
    target = FORM_TARGET

    def __init__(self, *args, **kwargs):
        super(RobokassaForm, self).__init__(*args, **kwargs)
        if TEST_MODE is True:
            self.fields['isTest'] = forms.BooleanField(required=False)
            self.fields['isTest'].initial = 1
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        self.fields['SignatureValue'].initial = self._get_signature()

    def get_redirect_url(self):
        """ Получить URL с GET-параметрами, соответствующими значениям полей в
        форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
        ручной отправке формы методом GET.
        """

        def _initial(name, field):
            val = self.initial.get(name, field.initial)
            if not val:
                return val
            return six.text_type(val).encode('1251')

        fields = [(name, _initial(name, field)) for name, field in list(self.fields.items()) if _initial(name, field)]
        params = urlencode(fields)
        return self.target + '?' + params

    def _get_signature_string(self):

        def _val(name):
            value = self.initial[name] if name in self.initial else self.fields[name].initial
            if value is None:
                return ''
            return six.text_type(value)

        standard_part = ':'.join([_val('MrchLogin'), _val('OutSum'), _val('InvId'), PASSWORD1])
        return self._append_extra_part(standard_part, _val)


class ResultURLForm(BaseRobokassaForm):
    __doc__ = 'Форма для приема результатов и проверки контрольной суммы'
    OutSum = forms.CharField(max_length=15)
    InvId = forms.IntegerField(min_value=0)
    SignatureValue = forms.CharField(max_length=32)

    def clean(self):
        try:
            signature = self.cleaned_data['SignatureValue'].upper()
            if signature != self._get_signature():
                raise forms.ValidationError('Ошибка в контрольной сумме')
        except KeyError:
            raise forms.ValidationError('Пришли не все необходимые параметры')

        return self.cleaned_data

    def _get_signature_string(self):
        _val = lambda name: six.text_type(self.cleaned_data[name])
        standard_part = ':'.join([_val('OutSum'), _val('InvId'), PASSWORD2])
        return self._append_extra_part(standard_part, _val)


class _RedirectPageForm(ResultURLForm):
    __doc__ = 'Форма для проверки контрольной суммы на странице Success'
    Culture = forms.CharField(max_length=10)

    def _get_signature_string(self):
        _val = lambda name: six.text_type(self.cleaned_data[name])
        standard_part = ':'.join([_val('OutSum'), _val('InvId'), PASSWORD1])
        return self._append_extra_part(standard_part, _val)


class SuccessRedirectForm(_RedirectPageForm):
    __doc__ = 'Форма для обработки страницы Success с дополнительной защитой. Она\n    проверяет, что ROBOKASSA предварительно уведомила систему о платеже,\n    отправив запрос на ResultURL.'

    def clean(self):
        data = super(SuccessRedirectForm, self).clean()
        if STRICT_CHECK:
            if not SuccessNotification.objects.filter(InvId=data['InvId']):
                raise forms.ValidationError('От ROBOKASSA не было предварительного уведомления')
        return data


class FailRedirectForm(BaseRobokassaForm):
    __doc__ = 'Форма приема результатов для перенаправления на страницу Fail'
    OutSum = forms.CharField(max_length=15)
    InvId = forms.IntegerField(min_value=0)
    Culture = forms.CharField(max_length=10)