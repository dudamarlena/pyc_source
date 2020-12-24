# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/api_tasty/auth.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 807 bytes
from tastypie.authentication import ApiKeyAuthentication

class DeveloperApiKeyAuthentication(ApiKeyAuthentication):
    __doc__ = "\n    Extends the build in ApiKeyAuthentication and adds in checking\n    for a user's superuser status.\n    "

    def get_key(self, user, api_key):
        """
        Attempts to find the API key for the user. Uses ``ApiKey`` by default
        In addition this checks if the user is a superuser.
        If the user is not even if he has a key he will still be unauthorized.
        """
        from tastypie.models import ApiKey
        if not user.profile.is_superuser:
            return self._unauthorized()
        try:
            ApiKey.objects.get(user=user, key=api_key)
        except ApiKey.DoesNotExist:
            return self._unauthorized()
        else:
            return True