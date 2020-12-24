# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/configuration/sources/derivative.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 3601 bytes
from satella.coding.algos import merge_dicts
from satella.exceptions import ConfigurationError
from .base import BaseSource
__all__ = [
 'AlternativeSource', 'OptionalSource', 'MergingSource']

class AlternativeSource(BaseSource):
    __doc__ = '\n    If first source of configuration fails with ConfigurationError, use the next one instead, ad\n    nauseam.\n    '
    __slots__ = ('sources', )

    def __init__(self, *sources):
        super().__init__()
        self.sources = sources

    def __repr__(self) -> str:
        return 'AlternativeSource(%s)' % (repr(self.sources),)

    def provide(self) -> dict:
        """
        :raises ConfigurationError: when backup fails too
        """
        for source in self.sources:
            try:
                s = source.provide()
                assert isinstance(s, dict), 'provide() returned a non-dict'
                return s
            except ConfigurationError:
                pass

        else:
            raise ConfigurationError('all sources failed!')


class OptionalSource(AlternativeSource):
    __doc__ = '\n     This will substitute for empty dict if underlying config would fail.\n\n     Apply this to your sources if you expect that they will fail.\n\n     Use as\n\n     >>> OptionalSource(SomeOtherSource1)\n     '

    def __init__(self, source):
        super().__init__(source, BaseSource())

    def __repr__(self) -> str:
        return 'OptionalSource(%s)' % repr(self.sources[0])


class MergingSource(BaseSource):
    __doc__ = "\n    Source that merges configuration from a bunch of sources. The configuration has to be a\n    dictionary!!\n\n    :param sources: Sources to examine. Source later in queue will override earlier's entries, so\n        take care.\n    :param on_fail: how to behave when a source fails\n    :param fail_if_no_sources_are_correct: even if on_fail == MergingSource.SILENT,\n        if all sources fail, this will fail as well. Of course this makes sense only if on_fail ==\n        MergingSource.SILENT\n    "
    RAISE = 0
    SILENT = 1
    __slots__ = ('sources', 'on_fail', 'fail_if_no_sources_are_correct')

    def __init__(self, *sources, on_fail=RAISE, fail_if_no_sources_are_correct=True):
        super().__init__()
        self.sources = sources
        self.on_fail = on_fail
        self.fail_if_no_sources_are_correct = fail_if_no_sources_are_correct

    def provide(self) -> dict:
        cfg = {}
        correct_sources = 0
        for source in self.sources:
            try:
                p = source.provide()
                correct_sources += 1
            except ConfigurationError as e:
                try:
                    if self.on_fail == MergingSource.RAISE:
                        raise e
                    else:
                        if self.on_fail == MergingSource.SILENT:
                            p = {}
                        else:
                            raise ConfigurationError('Invalid on_fail parameter %s' % (self.on_fail,))
                finally:
                    e = None
                    del e

            assert isinstance(p, dict), 'what was provided by the config was not a dict'
            cfg = merge_dicts(cfg, p)
            assert isinstance(cfg, dict), 'what merge_dicts returned wasnt a dict'

        if correct_sources == 0:
            if self.sources:
                if self.fail_if_no_sources_are_correct:
                    raise ConfigurationError('No source was able to load the configuration')
        return cfg

    def __repr__(self) -> str:
        return '<MergingSource %s>' % (repr(self.sources),)