# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/tag_matcher.py
# Compiled at: 2014-11-03 07:16:44
# Size of source mod 2**32: 7547 bytes


class TagMatcher(object):
    __doc__ = 'Abstract base class that defines the TagMatcher protocol.'

    def should_run_with(self, tags):
        """Determines if a feature/scenario with these tags should run or not.

        :param tags:    List of scenario/feature tags to check.
        :return: True,  if scenario/feature should run.
        :return: False, if scenario/feature should be excluded from the run-set.
        """
        return not self.should_exclude_with(tags)

    def should_exclude_with(self, tags):
        """Determines if a feature/scenario with these tags should be excluded
        from the run-set.

        :param tags:    List of scenario/feature tags to check.
        :return: True, if scenario/feature should be excluded from the run-set.
        :return: False, if scenario/feature should run.
        """
        raise NotImplementedError


class OnlyWithCategoryTagMatcher(TagMatcher):
    __doc__ = '\n    Provides a tag matcher that allows to determine if feature/scenario\n    should run or should be excluded from the run-set (at runtime).\n\n    EXAMPLE:\n    --------\n\n    Run some scenarios only when runtime conditions are met:\n\n      * Run scenario Alice only on Windows OS\n      * Run scenario Bob only on MACOSX\n\n    .. code-block:: gherkin\n\n        # -- FILE: features/alice.feature\n        # TAG SCHEMA: @only.with_{category}.{current_value}\n        Feature:\n\n          @only.with_os=win32\n          Scenario: Alice (Run only on Windows)\n            Given I do something\n            ...\n\n          @only.with_os=darwin\n          Scenario: Bob (Run only on MACOSX)\n            Given I do something else\n            ...\n\n\n    .. code-block:: python\n\n        # -- FILE: features/environment.py\n        from behave.tag_matcher import OnlyWithCategoryTagMatcher\n        import sys\n\n        # -- MATCHES TAGS: @only.with_{category}=* = @only.with_os=*\n        active_tag_matcher = OnlyWithCategoryTagMatcher("os", sys.platform)\n\n        def before_scenario(context, scenario):\n            if active_tag_matcher.should_exclude_with(scenario.effective_tags):\n                scenario.mark_skipped()   #< LATE-EXCLUDE from run-set.\n    '
    tag_prefix = 'only.with_'
    value_separator = '='

    def __init__(self, category, value, tag_prefix=None, value_sep=None):
        super(OnlyWithCategoryTagMatcher, self).__init__()
        self.active_tag = self.make_category_tag(category, value, tag_prefix, value_sep)
        self.category_tag_prefix = self.make_category_tag(category, None, tag_prefix, value_sep)

    def should_exclude_with(self, tags):
        category_tags = self.select_category_tags(tags)
        if category_tags and self.active_tag not in category_tags:
            return True
        return False

    def select_category_tags(self, tags):
        return [tag for tag in tags if tag.startswith(self.category_tag_prefix)]

    @classmethod
    def make_category_tag(cls, category, value=None, tag_prefix=None, value_sep=None):
        if tag_prefix is None:
            tag_prefix = cls.tag_prefix
        if value_sep is None:
            value_sep = cls.value_separator
        value = value or ''
        return '%s%s%s%s' % (tag_prefix, category, value_sep, value)


class OnlyWithAnyCategoryTagMatcher(TagMatcher):
    __doc__ = '\n    Provides a tag matcher that matches any category that follows the\n    "@only.with_" tag schema and determines if it should run or\n    should be excluded from the run-set (at runtime).\n\n    TAG SCHEMA: @only.with_{category}.{value}\n\n    .. seealso:: OnlyWithCategoryTagMatcher\n\n    EXAMPLE:\n    --------\n\n    Run some scenarios only when runtime conditions are met:\n\n      * Run scenario Alice only on Windows OS\n      * Run scenario Bob only with browser Chrome\n\n    .. code-block:: gherkin\n\n        # -- FILE: features/alice.feature\n        # TAG SCHEMA: @only.with_{category}={current_value}\n        Feature:\n\n          @only.with_os=win32\n          Scenario: Alice (Run only on Windows)\n            Given I do something\n            ...\n\n          @only.with_browser=chrome\n          Scenario: Bob (Run only with Web-Browser Chrome)\n            Given I do something else\n            ...\n\n\n    .. code-block:: python\n\n        # -- FILE: features/environment.py\n        from behave.tag_matcher import OnlyWithAnyCategoryTagMatcher\n        import sys\n\n        # -- MATCHES ANY TAGS: @only.with_{category}={value}\n        # NOTE: category_value_provider provides active category values.\n        category_value_provider = {\n            "browser": os.environ.get("BEHAVE_BROWSER", "chrome"),\n            "os":      sys.platform,\n        }\n        active_tag_matcher = OnlyWithAnyCategoryTagMatcher(category_value_provider)\n\n        def before_scenario(context, scenario):\n            if active_tag_matcher.should_exclude_with(scenario.effective_tags):\n                scenario.mark_skipped()   #< LATE-EXCLUDE from run-set.\n    '

    def __init__(self, category_value_provider, tag_prefix=None, value_sep=None):
        if value_sep is None:
            value_sep = OnlyWithCategoryTagMatcher.value_separator
        self.category_value_provider = category_value_provider
        self.tag_prefix = tag_prefix or OnlyWithCategoryTagMatcher.tag_prefix
        self.value_separator = value_sep

    def should_exclude_with(self, tags):
        exclude_decision_map = {}
        for category_tag in self.select_category_tags(tags):
            category, value = self.parse_category_tag(category_tag)
            active_value = self.category_value_provider.get(category, None)
            if active_value is None:
                continue
            elif active_value == value:
                exclude_decision_map[category] = False
            elif category not in exclude_decision_map:
                exclude_decision_map[category] = True
                continue

        return any(exclude_decision_map.values())

    def select_category_tags(self, tags):
        return [tag for tag in tags if tag.startswith(self.tag_prefix)]

    def parse_category_tag(self, tag):
        assert tag and tag.startswith(self.tag_prefix)
        category_value = tag[len(self.tag_prefix):]
        if self.value_separator in category_value:
            category, value = category_value.split(self.value_separator, 1)
        else:
            category = category_value
            value = None
        return (
         category, value)


class PredicateTagMatcher(TagMatcher):

    def __init__(self, exclude_function):
        assert callable(exclude_function)
        super(PredicateTagMatcher, self).__init__()
        self.predicate = exclude_function

    def should_exclude_with(self, tags):
        return self.predicate(tags)


class CompositeTagMatcher(TagMatcher):
    __doc__ = 'Provides a composite tag matcher.'

    def __init__(self, tag_matchers=None):
        super(CompositeTagMatcher, self).__init__()
        self.tag_matchers = tag_matchers or []

    def should_exclude_with(self, tags):
        for tag_matcher in self.tag_matchers:
            if tag_matcher.should_exclude_with(tags):
                return True

        return False