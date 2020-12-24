# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/stats.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 1806 bytes
from django.http import JsonResponse
from django.db.models import Count, Q, Case, When, IntegerField
from django.contrib.admin.views.decorators import staff_member_required
from collections import Counter
from danceschool.core.models import Registration
from danceschool.core.utils.requests import getDateTimeFromGet
from .models import Voucher

@staff_member_required
def popularVouchersJSON(request):
    startDate = getDateTimeFromGet(request, 'startDate')
    endDate = getDateTimeFromGet(request, 'endDate')
    timeLimit = Q(voucheruse__creationDate__isnull=False)
    if startDate:
        timeLimit = timeLimit & Q(voucheruse__creationDate__gte=startDate)
    if endDate:
        timeLimit = timeLimit & Q(voucheruse__creationDate__lte=endDate)
    uses = list(Voucher.objects.annotate(counter=(Count(Case(When(timeLimit, then=1),
      output_field=(IntegerField()))))).filter(counter__gt=0).values('name', 'counter', 'voucherId').order_by('-counter')[:10])
    return JsonResponse(uses, safe=False)


@staff_member_required
def voucherFrequencyJSON(request):
    startDate = getDateTimeFromGet(request, 'startDate')
    endDate = getDateTimeFromGet(request, 'endDate')
    timeLimit = Q()
    if startDate:
        timeLimit = timeLimit & Q(dateTime__gte=startDate)
    if endDate:
        timeLimit = timeLimit & Q(dateTime__lte=endDate)
    vouchers_counter_sorted = sorted(Counter(Registration.objects.filter(timeLimit).annotate(vouchers_applied=(Count('voucheruse'))).values_list('vouchers_applied', flat=True)).items())
    results_list = [{'vouchers':x[0],  'count':x[1]} for x in vouchers_counter_sorted]
    return JsonResponse(results_list, safe=False)