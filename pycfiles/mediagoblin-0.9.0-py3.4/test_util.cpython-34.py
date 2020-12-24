# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_util.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 6632 bytes
try:
    import mock
except ImportError:
    import unittest.mock as mock

import email, pytest, smtplib, pkg_resources, six
from mediagoblin.tests.tools import get_app
from mediagoblin.tools import common, url, translate, mail, text, testing
testing._activate_testing()

def _import_component_testing_method(silly_string):
    return "'%s' is the silliest string I've ever seen" % silly_string


def test_import_component():
    imported_func = common.import_component('mediagoblin.tests.test_util:_import_component_testing_method')
    result = imported_func('hooobaladoobala')
    expected = "'hooobaladoobala' is the silliest string I've ever seen"
    assert result == expected


def test_send_email():
    mail._clear_test_inboxes()
    mail.send_email('sender@mediagoblin.example.org', [
     'amanda@example.org', 'akila@example.org'], 'Testing is so much fun!', 'HAYYY GUYS!\n\nI hope you like unit tests JUST AS MUCH AS I DO!')
    assert len(mail.EMAIL_TEST_INBOX) == 1
    message = mail.EMAIL_TEST_INBOX.pop()
    assert message['From'] == 'sender@mediagoblin.example.org'
    assert message['To'] == 'amanda@example.org, akila@example.org'
    assert message['Subject'] == 'Testing is so much fun!'
    assert message.get_payload(decode=True) == b'HAYYY GUYS!\n\nI hope you like unit tests JUST AS MUCH AS I DO!'
    assert len(mail.EMAIL_TEST_MBOX_INBOX) == 1
    mbox_dict = mail.EMAIL_TEST_MBOX_INBOX.pop()
    assert mbox_dict['from'] == 'sender@mediagoblin.example.org'
    assert mbox_dict['to'] == ['amanda@example.org', 'akila@example.org']
    mbox_message = email.message_from_string(mbox_dict['message'])
    assert mbox_message['From'] == 'sender@mediagoblin.example.org'
    assert mbox_message['To'] == 'amanda@example.org, akila@example.org'
    assert mbox_message['Subject'] == 'Testing is so much fun!'
    assert mbox_message.get_payload(decode=True) == b'HAYYY GUYS!\n\nI hope you like unit tests JUST AS MUCH AS I DO!'


@pytest.fixture()
def starttls_enabled_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests', 'starttls_config.ini'))


def test_email_force_starttls(starttls_enabled_app):
    common.TESTS_ENABLED = False
    SMTP = lambda *args**args: mail.FakeMhost()
    with mock.patch('smtplib.SMTP', SMTP):
        with pytest.raises(smtplib.SMTPException):
            mail.send_email(from_addr='notices@my.test.instance.com', to_addrs='someone@someplace.com', subject='Testing is so much fun!', message_body='Ohai ^_^')


def test_slugify():
    assert url.slugify('a walk in the park') == 'a-walk-in-the-park'
    assert url.slugify('A Walk in the Park') == 'a-walk-in-the-park'
    assert url.slugify('a  walk in the park') == 'a-walk-in-the-park'
    assert url.slugify('a walk in-the-park') == 'a-walk-in-the-park'
    assert url.slugify('a w@lk in the park?') == 'a-w-lk-in-the-park'
    assert url.slugify('a walk in the parć') == 'a-walk-in-the-parc'
    assert url.slugify('àBçďëf') == 'abcdef'
    assert url.slugify('прогулка в парке') == 'progulka-v-parke'
    assert url.slugify('공원에서 산책') == 'gongweoneseo-sancaeg'


def test_locale_to_lower_upper():
    """
    Test cc.i18n.util.locale_to_lower_upper()
    """
    assert translate.locale_to_lower_upper('en') == 'en'
    assert translate.locale_to_lower_upper('en_US') == 'en_US'
    assert translate.locale_to_lower_upper('en-us') == 'en_US'
    assert translate.locale_to_lower_upper('en-US') == 'en_US'
    assert translate.locale_to_lower_upper('en_us') == 'en_US'


def test_locale_to_lower_lower():
    """
    Test cc.i18n.util.locale_to_lower_lower()
    """
    assert translate.locale_to_lower_lower('en') == 'en'
    assert translate.locale_to_lower_lower('en_US') == 'en-us'
    assert translate.locale_to_lower_lower('en-us') == 'en-us'
    assert translate.locale_to_lower_lower('en-US') == 'en-us'
    assert translate.locale_to_lower_lower('en_us') == 'en-us'


def test_gettext_lazy_proxy():
    from mediagoblin.tools.translate import lazy_pass_to_ugettext as _
    from mediagoblin.tools.translate import pass_to_ugettext, set_thread_locale
    proxy = _('Password')
    orig = 'Password'
    set_thread_locale('es')
    p1 = six.text_type(proxy)
    p1_should = pass_to_ugettext(orig)
    assert p1_should != orig, 'Test useless, string not translated'
    assert p1 == p1_should
    set_thread_locale('sv')
    p2 = six.text_type(proxy)
    p2_should = pass_to_ugettext(orig)
    assert p2_should != orig, 'Test broken, string not translated'
    assert p2 == p2_should
    assert p1_should != p2_should, 'Test broken, same translated string'
    assert p1 != p2


def test_html_cleaner():
    result = text.clean_html('<p>Hi everybody! <img src="http://example.org/huge-purple-barney.png" /></p>\n<p>:)</p>')
    assert result == '<div><p>Hi everybody! </p>\n<p>:)</p></div>'
    result = text.clean_html('<p><a href="javascript:nasty_surprise">innocent link!</a></p>')
    assert result == '<p><a href="">innocent link!</a></p>'