# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth2/utils/googletotp/googletotp.py
# Compiled at: 2019-04-02 03:10:22
# Size of source mod 2**32: 2540 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import datetime, time
from django_google_auth2.utils.googleutils import googleutils
from django_google_auth2.utils.googleotp.googleotp import OTP

class TOTP(OTP):

    def __init__(self, *args, **kwargs):
        self.interval = kwargs.pop('interval', 30)
        (super(TOTP, self).__init__)(*args, **kwargs)

    def at(self, for_time, counter_offset=0):
        """
        Accepts either a Unix timestamp integer or a Time object.
        Time objects will be adjusted to UTC automatically
        @param [Time/Integer] time the time to generate an OTP for
        @param [Integer] counter_offset an amount of ticks to add to the time counter
        """
        if not isinstance(for_time, datetime.datetime):
            for_time = datetime.datetime.fromtimestamp(int(for_time))
        return self.generate_otp(self.timecode(for_time) + counter_offset)

    def now(self):
        """
        Generate the current time OTP
        @return [Integer] the OTP as an integer
        """
        return self.generate_otp(self.timecode(datetime.datetime.now()))

    def verify(self, otp, for_time=None, valid_window=0):
        """
        Verifies the OTP passed in against the current time OTP
        @param [String/Integer] otp the OTP to check against
        @param [Integer] valid_window extends the validity to this many counter ticks before and after the current one
        """
        if for_time is None:
            for_time = datetime.datetime.now()
        if valid_window:
            for i in range(-valid_window, valid_window + 1):
                if googleutils.strings_equal(str(otp), str(self.at(for_time, i))):
                    return True

            return False
        else:
            return googleutils.strings_equal(str(otp), str(self.at(for_time)))

    def provisioning_uri(self, name, issuer_name=None):
        """
        Returns the provisioning URI for the OTP
        This can then be encoded in a QR Code and used
        to provision the Google Authenticator app
        @param [String] name of the account
        @return [String] provisioning uri
        """
        return googleutils.build_uri((self.secret), name, issuer_name=issuer_name)

    def timecode(self, for_time):
        i = time.mktime(for_time.timetuple())
        return int(i / self.interval)