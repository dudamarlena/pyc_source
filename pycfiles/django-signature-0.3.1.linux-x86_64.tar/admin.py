# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cyberj/src/python/vtenv2.6/lib/python2.6/site-packages/signature/admin.py
# Compiled at: 2011-06-14 07:22:27
from django.contrib import admin
from models import Key, CertificateRequest, Signature, Certificate

class KeyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Key, KeyAdmin)

class CertificateRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(CertificateRequest, CertificateRequestAdmin)

class SignatureAdmin(admin.ModelAdmin):
    pass


admin.site.register(Signature, SignatureAdmin)

class CertificateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Certificate, CertificateAdmin)