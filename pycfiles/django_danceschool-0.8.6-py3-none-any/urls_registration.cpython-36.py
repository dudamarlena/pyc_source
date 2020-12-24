# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/urls_registration.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 2490 bytes
from django.conf.urls import url
from .views import EventRegistrationSummaryView, EventRegistrationSelectView, RefundProcessingView, RefundConfirmationView, ViewInvoiceView, InvoiceNotificationView
from .classreg import RegistrationOfflineView, ClassRegistrationView, SingleClassRegistrationView, ClassRegistrationReferralView, RegistrationSummaryView, StudentInfoView
from .ajax import processCheckIn
urlpatterns = [
 url('^$', (ClassRegistrationView.as_view()), name='registration'),
 url('^id/(?P<marketing_id>[\\w\\-_]+)/$', (ClassRegistrationReferralView.as_view()), name='registrationWithMarketingId'),
 url('^referral/(?P<voucher_id>[\\w\\-_]+)/$', (ClassRegistrationReferralView.as_view()), name='registrationWithVoucher'),
 url('^event/(?P<uuid>[\\w\\-_]+)/$', (SingleClassRegistrationView.as_view()), name='singleClassRegistration'),
 url('^offline/$', (RegistrationOfflineView.as_view()), name='registrationOffline'),
 url('^getinfo/$', (StudentInfoView.as_view()), name='getStudentInfo'),
 url('^summary/$', (RegistrationSummaryView.as_view()), name='showRegSummary'),
 url('^registrations/$', (EventRegistrationSelectView.as_view()), name='viewregistrations_selectevent'),
 url('^registrations/(?P<event_id>[0-9]+)/$', (EventRegistrationSummaryView.as_view()), name='viewregistrations'),
 url('^registrations/checkin/$', processCheckIn, name='formhandler_checkin'),
 url('^invoice/view/(?P<pk>[0-9a-f-]+)/$', (ViewInvoiceView.as_view()), name='viewInvoice'),
 url('^invoice/notify/(?P<pk>[0-9a-f-]+)/$', (InvoiceNotificationView.as_view()), name='sendInvoiceNotifications'),
 url('^invoice/notify/$', (InvoiceNotificationView.as_view()), name='sendInvoiceNotifications'),
 url('^invoice/refund/confirm/$', (RefundConfirmationView.as_view()), name='refundConfirmation'),
 url('^invoice/refund/(?P<pk>[0-9a-f-]+)/$', (RefundProcessingView.as_view()), name='refundProcessing')]