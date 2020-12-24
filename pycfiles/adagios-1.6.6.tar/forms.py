# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/../adagios/status/forms.py
# Compiled at: 2018-05-16 10:07:32
from django import forms
from django.utils.translation import ugettext as _
import adagios.status.utils, adagios.businessprocess

class LiveStatusForm(forms.Form):
    """ This form is used to generate a mk_livestatus query """
    table = forms.ChoiceField()
    columns = forms.MultipleChoiceField()
    filter1 = forms.ChoiceField(required=False)
    filter2 = forms.ChoiceField(required=False)


class RemoveSubProcessForm(forms.Form):
    """ Remove one specific sub process from a business process
    """
    process_name = forms.CharField(max_length=100, required=True)
    process_type = forms.CharField(max_length=100, required=True)

    def __init__(self, instance, *args, **kwargs):
        self.bp = instance
        super(RemoveSubProcessForm, self).__init__(*args, **kwargs)

    def save(self):
        process_name = self.cleaned_data.get('process_name')
        process_type = self.cleaned_data.get('process_type')
        self.bp.remove_process(process_name, process_type)
        self.bp.save()


status_method_choices = map(lambda x: (
 x, x), adagios.businessprocess.BusinessProcess.status_calculation_methods)

class BusinessProcessForm(forms.Form):
    """ Use this form to edit a BusinessProcess """
    name = forms.CharField(max_length=100, required=True, help_text=_('Unique name for this business process.'))
    display_name = forms.CharField(max_length=100, required=False, help_text=_('This is the name that will be displayed to users on this process. Usually it is the name of the system this business group represents.'))
    notes = forms.CharField(max_length=1000, required=False, help_text=_('Here you can put in any description of the business process you are adding. Its a good idea to write down what the business process is about and who to contact in case of downtimes.'))
    status_method = forms.ChoiceField(choices=status_method_choices, help_text=_('Here you can choose which method is used to calculate the global status of this business process'))
    state_0 = forms.CharField(max_length=100, required=False, help_text=_("Human friendly text for this respective state. You can type whatever you want but nagios style exit codes indicate that 0 should be 'ok'"))
    state_1 = forms.CharField(max_length=100, required=False, help_text=_('Typically used to represent warning or performance problems'))
    state_2 = forms.CharField(max_length=100, required=False, help_text=_('Typically used to represent critical status'))
    state_3 = forms.CharField(max_length=100, required=False, help_text=_('Use this when status is unknown'))

    def __init__(self, instance, *args, **kwargs):
        self.bp = instance
        super(BusinessProcessForm, self).__init__(*args, **kwargs)

    def save(self):
        c = self.cleaned_data
        self.bp.data.update(c)
        self.bp.save()

    def remove(self):
        c = self.data
        process_name = c.get('process_name')
        process_type = c.get('process_type')
        if process_type == 'None':
            process_type = None
        self.bp.remove_process(process_name, process_type)
        self.bp.save()
        return

    def clean(self):
        cleaned_data = super(BusinessProcessForm, self).clean()
        new_name = cleaned_data.get('name')
        if new_name and new_name != self.bp.name:
            if new_name in adagios.businessprocess.get_all_process_names():
                raise forms.ValidationError(_('Cannot rename process to %s. Another process with that name already exists') % new_name)
        return cleaned_data

    def delete(self):
        """ Delete this business process """
        self.bp.delete()

    def add_process(self):
        process_name = self.data.get('process_name')
        hostgroup_name = self.data.get('hostgroup_name')
        servicegroup_name = self.data.get('servicegroup_name')
        service_name = self.data.get('service_name')
        if process_name:
            self.bp.add_process(process_name, None)
        if hostgroup_name:
            self.bp.add_process(hostgroup_name, None)
        if servicegroup_name:
            self.bp.add_process(servicegroup_name, None)
        if service_name:
            self.bp.add_process(service_name, None)
        self.bp.save()
        return


choices = ('businessprocess', 'hostgroup', 'servicegroup', 'service', 'host')
process_type_choices = map(lambda x: (x, x), choices)

class AddSubProcess(forms.Form):
    process_type = forms.ChoiceField(choices=process_type_choices)
    process_name = forms.CharField(widget=forms.HiddenInput(attrs={'style': 'width: 300px;'}), max_length=100)
    display_name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=100, required=False, initial='not critical')

    def __init__(self, instance, *args, **kwargs):
        self.bp = instance
        super(AddSubProcess, self).__init__(*args, **kwargs)

    def save(self):
        self.bp.add_process(**self.cleaned_data)
        self.bp.save()


class AddHostgroupForm(forms.Form):
    pass


class AddGraphForm(forms.Form):
    host_name = forms.CharField(max_length=100)
    service_description = forms.CharField(max_length=100, required=False)
    metric_name = forms.CharField(max_length=100, required=True)
    notes = forms.CharField(max_length=100, required=False, help_text=_('Put here a friendly description of the graph'))

    def __init__(self, instance, *args, **kwargs):
        self.bp = instance
        super(AddGraphForm, self).__init__(*args, **kwargs)

    def save(self):
        self.bp.add_pnp_graph(**self.cleaned_data)
        self.bp.save()