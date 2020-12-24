# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/feedinfo.py
# Compiled at: 2018-01-24 00:52:58
import transitfeed

class FeedInfo(transitfeed.GtfsObjectBase):
    """Model and validation for feed_info.txt."""
    _REQUIRED_FIELD_NAMES = [
     'feed_publisher_name', 'feed_publisher_url',
     'feed_lang']
    _FIELD_NAMES = _REQUIRED_FIELD_NAMES + ['feed_start_date', 'feed_end_date',
     'feed_version']
    _DEPRECATED_FIELD_NAMES = [('feed_valid_from', 'feed_start_date'),
     ('feed_valid_until', 'feed_end_date'),
     ('feed_timezone', None)]
    _TABLE_NAME = 'feed_info'

    def __init__(self, field_dict=None):
        self._schedule = None
        if field_dict:
            self.__dict__.update(field_dict)
        return

    def ValidateFeedInfoLang(self, problems):
        return not transitfeed.ValidateLanguageCode(self.feed_lang, 'feed_lang', problems)

    def ValidateFeedInfoPublisherUrl(self, problems):
        return not transitfeed.ValidateURL(self.feed_publisher_url, 'feed_publisher_url', problems)

    def ValidateDates(self, problems):
        start_date_valid = transitfeed.ValidateDate(self.feed_start_date, 'feed_start_date', problems)
        end_date_valid = transitfeed.ValidateDate(self.feed_end_date, 'feed_end_date', problems)
        if start_date_valid and end_date_valid and self.feed_end_date < self.feed_start_date:
            problems.InvalidValue('feed_end_date', self.feed_end_date, 'feed_end_date %s is earlier than feed_start_date "%s"' % (
             self.feed_end_date, self.feed_start_date))

    def ValidateBeforeAdd(self, problems):
        transitfeed.ValidateRequiredFieldsAreNotEmpty(self, self._REQUIRED_FIELD_NAMES, problems)
        self.ValidateFeedInfoLang(problems)
        self.ValidateFeedInfoPublisherUrl(problems)
        self.ValidateDates(problems)
        return True

    def ValidateAfterAdd(self, problems):
        pass

    def AddToSchedule(self, schedule, problems):
        schedule.AddFeedInfoObject(self, problems)