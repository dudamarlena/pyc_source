# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taxydromikilib/taxydromikilib.py
# Compiled at: 2017-09-25 10:10:06
"""
Main module file

Put your classes here
"""
from __future__ import unicode_literals
from requests import Session
from bs4 import BeautifulSoup as Bfs
import time, logging
__author__ = b'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = b'plaintext'
__date__ = b'25-09-2017'
LOGGER_BASENAME = b'taxydromikilib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class TrackingState(object):

    def __init__(self, data):
        self._data = data

    def _get_data(self, class_name):
        try:
            value = self._data.find(b'div', {b'class': class_name}).contents[1]
        except Exception:
            value = None

        return value

    @property
    def status(self):
        return self._get_data(b'checkpoint-status')

    @property
    def location(self):
        return self._get_data(b'checkpoint-location')

    @property
    def date(self):
        return self._get_data(b'checkpoint-date')

    @property
    def time(self):
        return self._get_data(b'checkpoint-time')

    @property
    def is_final(self):
        return b'tracking-delivery last' in unicode(self._data)


class Taxydromiki(object):

    def __init__(self):
        self._base_url = b'https://www.taxydromiki.com'
        self._headers = {b'User-Agent': b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', b'Accept-Language': b'en-US,en;q=0.5', 
           b'Accept-Encoding': b'gzip, deflate, br', 
           b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        self._session = None
        return

    def _initialize(self):
        self._session = Session()
        headers = self._headers.copy()
        headers.update({b'Upgrade-Insecure-Requests': b'1', b'cache-contol': b'max-age=0'})
        url = (b'{base}/track').format(base=self._base_url)
        response = self._session.get(url, headers=headers)
        form_build_id, theme_token = self._get_tokens(response)
        self._perform_ajax_blocks_call()
        return (form_build_id, theme_token)

    @staticmethod
    def _get_tokens(response):
        soup = Bfs(response.text, b'html.parser')
        form = soup.find(b'form', {b'id': b'custom-geniki-tracking-page-form'})
        form_build_id = form.find(b'input', {b'name': b'form_build_id'}).attrs.get(b'value')
        index = response.text.find(b'theme_token')
        theme_token = response.text[index:index + 80].split(b'"')[1]
        return (form_build_id, theme_token)

    def _perform_ajax_blocks_call(self):
        url = (b'{base}/ajaxblocks').format(base=self._base_url)
        headers = self._headers.copy()
        headers.update({b'Accept': b'application/json, text/javascript, */*; q=0.01', b'X-Requested-With': b'XMLHttpRequest', 
           b'Referer': (b'{base}/track').format(base=self._base_url)})
        payload = {b'_': str(int(time.time() * 1000)), b'blocks': b'custom-custom_time_date', 
           b'path': b'track', 
           b'nocache': b'1'}
        response = self._session.get(url, headers=headers, params=payload)
        return response.ok

    def search(self, tracking_number):
        form_build_id, theme_token = self._initialize()
        url = (b'{base}/system/ajax').format(base=self._base_url)
        headers = self._headers.copy()
        headers.update({b'Host': b'www.taxydromiki.com', b'Accept': b'application/json, text/javascript, */*; q=0.01', 
           b'Content-Type': b'application/x-www-form-urlencoded', 
           b'X-Requested-With': b'XMLHttpRequest', 
           b'Referer': (b'{base}/track').format(base=self._base_url), 
           b'Origin': self._base_url})
        payload = {b'_triggering_element_name': b'op', b'_triggering_element_value': b'Αναζήτηση', 
           b'ajax_html_ids[]': [
                              b'mp-pusher',
                              b'mp-menu',
                              b'block-custom-custom-time-date',
                              b'block-custom-custom_time_date-ajax-content',
                              b'block-custom-custom-account-menu',
                              b'block-lang-dropdown-language-content',
                              b'lang_dropdown_form_language_content',
                              b'lang-dropdown-select-language_content',
                              b'trigger',
                              b'block-system-main-menu',
                              b'block-custom-geniki-tracking-form',
                              b'custom-geniki-tracking-form',
                              b'edit-tracking-number--2',
                              b'edit-submit--3',
                              b'block-block-10',
                              b'main-content',
                              b'custom-geniki-tracking-page-form',
                              b'edit-tracking-searchbox',
                              b'edit-tracking-number',
                              b'edit-submit',
                              b'tracking-result',
                              b'block-menu-block-1',
                              b'block-user-login',
                              b'user-login-form',
                              b'edit-name',
                              b'edit-pass',
                              b'edit-actions',
                              b'edit-submit--4',
                              b'block-block-3',
                              b'block-block-4',
                              b'block-block-9',
                              b'block-block-2',
                              b'block-menu-menu-footer-menu',
                              b'block-menu-menu-footer-second',
                              b'block-block-8'], 
           b'ajax_page_state[css][modules/node/node.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/ckeditor/css/ckeditor.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/ctools/css/ctools.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/date/date_api/date.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/date/date_popup/themes/datepicker.1.7.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/lang_dropdown/lang_dropdown.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/logintoboggan/logintoboggan.css]': b'1', 
           b'ajax_page_state[css][sites/all/modules/views/css/views.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/field/field.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/search/search.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.base.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.menus.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.messages.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/system/system.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/user/user.base.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/omega/omega/omega/css/modules/user/user.theme.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/after.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.hacks.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.no-query.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.normalize.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.print.css]': b'1', 
           b'ajax_page_state[css][sites/all/themes/taxydromiki/css/taxydromiki.styles.css]': b'1', 
           b'ajax_page_state[js][0]': b'1', 
           b'ajax_page_state[js][misc/ajax.js]': b'1', 
           b'ajax_page_state[js][misc/drupal.js]': b'1', 
           b'ajax_page_state[js][misc/form.js]': b'1', 
           b'ajax_page_state[js][misc/jquery.cookie.js]': b'1', 
           b'ajax_page_state[js][misc/jquery.js]': b'1', 
           b'ajax_page_state[js][misc/jquery.once.js]': b'1', 
           b'ajax_page_state[js][misc/progress.js]': b'1', 
           b'ajax_page_state[js][public://languages/el_j43hC-GL4y98fNlJzVRM9SL0SKGIvZ5zF9vHNPqFpS8.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/ajaxblocks/ajaxblocks.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/browserclass/browserclass.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/clientside_validation/clientside_validation.ie8.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/clientside_validation/clientside_validation.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/clientside_validation/jquery-validate/jquery.validate.min.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/clientside_validation/jquery.form.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/custom/custom_geniki/custom_geniki.tracking.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/google_analytics/googleanalytics.js]': b'1', 
           b'ajax_page_state[js][sites/all/modules/lang_dropdown/lang_dropdown.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/omega/omega/omega/js/no-js.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/classie.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.hoverIntent.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.uniform.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/jquery.wookmark.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/mlpushmenu.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/modernizr.custom.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/taxydromiki.behaviors.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/js/taxydromiki.responsive.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/libraries/html5shiv/html5shiv-printshiv.min.js]': b'1', 
           b'ajax_page_state[js][sites/all/themes/taxydromiki/libraries/html5shiv/html5shiv.min.js]': b'1', 
           b'ajax_page_state[theme]': b'taxydromiki', 
           b'ajax_page_state[theme_token]': theme_token, 
           b'form_build_id': form_build_id, 
           b'form_id': b'custom_geniki_tracking_page_form', 
           b'tracking_number': tracking_number}
        response = self._session.post(url, headers=headers, data=payload)
        response_data = next((entry for entry in response.json() if entry.get(b'command') == b'insert'), None)
        soup = Bfs(response_data.get(b'data'), b'html.parser')
        entries = soup.find_all(b'div', {b'class': b'tracking-checkpoint'})
        return [ TrackingState(entry) for entry in entries ]