# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/invoices/listeners.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 618 bytes
from tendenci.apps.profiles.models import Profile

def update_profiles_total_spend(instance, **kwargs):
    """
    adds total to profiles.total_spend if status_detail=='tendered'
    @instance invoices.Invoice object
    """
    if instance.status_detail == 'tendered':
        user = instance.owner or instance.creator
        if not user:
            return
        try:
            profile = Profile.objects.get(user=user)
        except:
            profile = Profile.objects.create_profile(user)

        if not profile:
            return
        profile.total_spend += instance.total
        profile.save()