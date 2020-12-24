# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/prerequisites/ajax.py
# Compiled at: 2018-03-26 19:55:31
# Size of source mod 2**32: 2851 bytes
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from braces.views import PermissionRequiredMixin
from danceschool.core.models import Customer, DanceRole
from .models import Requirement, CustomerRequirement

class CustomerRequirementAjaxView(PermissionRequiredMixin, View):
    permission_required = 'prerequisites.add_customerrequirement'

    def post(self, request, *args, **kwargs):
        customerId = request.POST.get('customerId')
        requirementId = request.POST.get('requirementId')
        roleId = request.POST.get('roleId')
        roleEnforced = str(request.POST.get('roleEnforced', ''))
        setMet = str(request.POST.get('setMet', ''))
        roleEnforced = True if roleEnforced.lower() == 'true' else False
        if setMet.lower() == 'true':
            setMet = True
        else:
            if setMet.lower() == 'false':
                setMet = False
            else:
                setMet = None
            try:
                customer = Customer.objects.get(id=customerId)
                req = Requirement.objects.get(id=requirementId)
                role = DanceRole.objects.get(id=roleId) if roleId else None
            except (ValueError, ObjectDoesNotExist):
                return HttpResponseBadRequest(_('Invalid request.'))

            response = {'customerId': customerId, 
             'requirementId': requirementId}
            if setMet is not None:
                if req.roleEnforced and not role:
                    return HttpResponseBadRequest(_('Role must be specified.'))
                cr, created = CustomerRequirement.objects.update_or_create(customer=customer, requirement=req, role=role, defaults={'met': setMet})
                response.update({'setMet': setMet, 
                 'customerRequirementId': cr.id, 
                 'customerRequirementCreated': created})
            else:
                if not (roleEnforced and not role):
                    meets = req.customerMeetsRequirement(customer, danceRole=role)
                    response.update({'customerStatus': meets})
                else:
                    roles = DanceRole.objects.all()
                    response['customerStatus'] = {}
                    for role in roles:
                        meets = req.customerMeetsRequirement(customer, danceRole=role)
                        response['customerStatus'][role.name] = meets

        return JsonResponse(response)