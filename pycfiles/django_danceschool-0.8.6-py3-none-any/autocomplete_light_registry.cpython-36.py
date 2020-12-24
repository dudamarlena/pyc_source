# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/autocomplete_light_registry.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 6473 bytes
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q
from dal import autocomplete
from danceschool.core.models import StaffMember, Location
from .models import ExpenseItem, RevenueItem, TransactionParty

def get_method_list():
    """
    Include manual methods by default
    """
    methods = [
     str(_('Cash')), str(_('Check')), str(_('Bank/Debit Card')), str(_('Other'))]
    methods += ExpenseItem.objects.order_by().values_list('paymentMethod', flat=True).distinct()
    methods += RevenueItem.objects.order_by().values_list('paymentMethod', flat=True).distinct()
    methods_list = list(set(methods))
    if None in methods_list:
        methods_list.remove(None)
    return methods_list


class PaymentMethodAutoComplete(autocomplete.Select2ListView):
    __doc__ = '\n    This is the autocomplete view used to indicate payment methods in the\n    Revenue Reporting view.\n    '

    def get_list(self):
        return get_method_list()

    def create(self, text):
        """
        Since this autocomplete is used to create new RevenueItems, and the set of
        RevenueItem paymentMethods is automatically updated in get_method_list(),
        this function does not need to do anything
        """
        return text


class TransactionPartyAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.has_perm('financial.can_autocomplete_transactionparty'):
            return TransactionParty.objects.none()
        else:
            qs = TransactionParty.objects.all()
            if self.q:
                words = self.q.split(' ')
                lastName = words.pop()
                firstName = words.pop() if words else lastName
                qs = qs.filter(Q(name__icontains=(self.q)) | Q(user__first_name__istartswith=firstName) | Q(user__last_name__istartswith=lastName) | Q(staffMember__firstName__istartswith=firstName) | Q(staffMember__lastName__istartswith=lastName) | Q(location__name__icontains=(self.q)))
            return qs

    def get_result_label(self, item):
        if item.location:
            return str(_('%s (Location)')) % item.name
        else:
            if item.staffMember:
                return str(_('%s (Staff Member)')) % item.name
            if item.user:
                return str(_('%s (User)')) % item.name
            return item.name

    def get_selected_result_label(self, item):
        return item.name

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field:
            if q:
                page_obj = context.get('page_obj', None)
                if page_obj is None or page_obj.number == 1:
                    display_create_option = True
        if display_create_option and self.has_add_permission(self.request):
            for s in Location.objects.filter(Q(Q(name__istartswith=q) & Q(transactionparty__isnull=True))):
                create_option += [
                 {'id':'Location_%s' % s.id, 
                  'text':_('Generate from location "%(location)s"') % {'location': s.name}, 
                  'create_id':True}]

            for s in StaffMember.objects.filter(Q((Q(firstName__istartswith=q) | Q(lastName__istartswith=q)) & Q(transactionparty__isnull=True))):
                create_option += [
                 {'id':'StaffMember_%s' % s.id, 
                  'text':_('Generate from staff member "%(staff_member)s"') % {'staff_member': s.fullName}, 
                  'create_id':True}]

            for s in User.objects.filter(Q((Q(first_name__istartswith=q) | Q(last_name__istartswith=q)) & Q(staffmember__isnull=True) & Q(transactionparty__isnull=True))):
                create_option += [
                 {'id':'User_%s' % s.id, 
                  'text':_('Generate from user "%(user)s"') % {'user': s.get_full_name()}, 
                  'create_id':True}]

            create_option += [
             {'id':q, 
              'text':_('Create "%(new_value)s"') % {'new_value': q}, 
              'create_id':True}]
        return create_option

    def create_object(self, text):
        if self.create_field == 'name':
            if text.startswith('Location_'):
                this_id = text[len('Location_'):]
                this_loc = Location.objects.get(id=this_id)
                return self.get_queryset().get_or_create(name=(this_loc.name),
                  location=this_loc)[0]
            else:
                if text.startswith('StaffMember_'):
                    this_id = text[len('StaffMember_'):]
                    this_member = StaffMember.objects.get(id=this_id)
                    return self.get_queryset().get_or_create(name=(this_member.fullName),
                      staffMember=this_member,
                      defaults={'user': getattr(this_member, 'userAccount', None)})[0]
                if text.startswith('User_'):
                    this_id = text[len('User_'):]
                    this_user = User.objects.get(id=this_id)
                    return self.get_queryset().get_or_create(name=(this_user.get_full_name()),
                      user=this_user,
                      defaults={'staffMember': getattr(this_user, 'staffmember', None)})[0]
                return self.get_queryset().get_or_create(name=text,
                  staffMember=None,
                  user=None,
                  location=None)[0]
        else:
            return super(TransactionPartyAutoComplete, self).create_object(text)