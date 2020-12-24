# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/pyppeteer/pyppeteer/coverage.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 13968 bytes
"""Coverage module."""
from functools import cmp_to_key
import logging
from typing import Any, Dict, List
from pyppeteer import helper
from pyppeteer.connection import CDPSession
from pyppeteer.errors import PageError
from pyppeteer.execution_context import EVALUATION_SCRIPT_URL
from pyppeteer.helper import debugError
from pyppeteer.util import merge_dict
logger = logging.getLogger(__name__)

class Coverage(object):
    __doc__ = "Coverage class.\n\n    Coverage gathers information about parts of JavaScript and CSS that were\n    used by the page.\n\n    An example of using JavaScript and CSS coverage to get percentage of\n    initially executed code::\n\n        # Enable both JavaScript and CSS coverage\n        await page.coverage.startJSCoverage()\n        await page.coverage.startCSSCoverage()\n\n        # Navigate to page\n        await page.goto('https://example.com')\n        # Disable JS and CSS coverage and get results\n        jsCoverage = await page.coverage.stopJSCoverage()\n        cssCoverage = await page.coverage.stopCSSCoverage()\n        totalBytes = 0\n        usedBytes = 0\n        coverage = jsCoverage + cssCoverage\n        for entry in coverage:\n            totalBytes += len(entry['text'])\n            for range in entry['ranges']:\n                usedBytes += range['end'] - range['start'] - 1\n\n        print('Bytes used: {}%'.format(usedBytes / totalBytes * 100))\n    "

    def __init__(self, client: CDPSession) -> None:
        self._jsCoverage = JSCoverage(client)
        self._cssCoverage = CSSCoverage(client)

    async def startJSCoverage(self, options: Dict=None, **kwargs: Any) -> None:
        """Start JS coverage measurement.

        Available options are:

        * ``resetOnNavigation`` (bool): Whether to reset coverage on every
          navigation. Defaults to ``True``.
        * ``reportAnonymousScript`` (bool): Whether anonymous script generated
          by the page should be reported. Defaults to ``False``.

        .. note::
            Anonymous scripts are ones that don't have an associated url. These
            are scripts that are dynamically created on the page using ``eval``
            of ``new Function``. If ``reportAnonymousScript`` is set to
            ``True``, anonymous scripts will have
            ``__pyppeteer_evaluation_script__`` as their url.
        """
        options = merge_dict(options, kwargs)
        await self._jsCoverage.start(options)

    async def stopJSCoverage(self) -> List:
        """Stop JS coverage measurement and get result.

        Return list of coverage reports for all scripts. Each report includes:

        * ``url`` (str): Script url.
        * ``text`` (str): Script content.
        * ``ranges`` (List[Dict]): Script ranges that were executed. Ranges are
          sorted and non-overlapping.

          * ``start`` (int): A start offset in text, inclusive.
          * ``end`` (int): An end offset in text, exclusive.

        .. note::
           JavaScript coverage doesn't include anonymous scripts by default.
           However, scripts with sourceURLs are reported.
        """
        return await self._jsCoverage.stop()

    async def startCSSCoverage(self, options: Dict=None, **kwargs: Any) -> None:
        """Start CSS coverage measurement.

        Available options are:

        * ``resetOnNavigation`` (bool): Whether to reset coverage on every
          navigation. Defaults to ``True``.
        """
        options = merge_dict(options, kwargs)
        await self._cssCoverage.start(options)

    async def stopCSSCoverage(self) -> List:
        """Stop CSS coverage measurement and get result.

        Return list of coverage reports for all non-anonymous scripts. Each
        report includes:

        * ``url`` (str): StyleSheet url.
        * ``text`` (str): StyleSheet content.
        * ``ranges`` (List[Dict]): StyleSheet ranges that were executed. Ranges
          are sorted and non-overlapping.

          * ``start`` (int): A start offset in text, inclusive.
          * ``end`` (int): An end offset in text, exclusive.

        .. note::
           CSS coverage doesn't include dynamically injected style tags without
           sourceURLs (but currently includes... to be fixed).
        """
        return await self._cssCoverage.stop()


class JSCoverage(object):
    __doc__ = 'JavaScript Coverage class.'

    def __init__(self, client: CDPSession) -> None:
        self._client = client
        self._enabled = False
        self._scriptURLs = dict()
        self._scriptSources = dict()
        self._eventListeners = list()
        self._resetOnNavigation = False

    async def start(self, options: Dict=None, **kwargs: Any) -> None:
        """Start coverage measurement."""
        options = merge_dict(options, kwargs)
        if self._enabled:
            raise PageError('JSCoverage is always enabled.')
        self._resetOnNavigation = True if 'resetOnNavigation' not in options else bool(options['resetOnNavigation'])
        self._reportAnonymousScript = bool(options.get('reportAnonymousScript'))
        self._enabled = True
        self._scriptURLs.clear()
        self._scriptSources.clear()
        self._eventListeners = [
         helper.addEventListener(self._client, 'Debugger.scriptParsed', lambda e: self._client._loop.create_task(self._onScriptParsed(e))),
         helper.addEventListener(self._client, 'Runtime.executionContextsCleared', self._onExecutionContextsCleared)]
        await self._client.send('Profiler.enable')
        await self._client.send('Profiler.startPreciseCoverage', {'callCount':False, 
         'detailed':True})
        await self._client.send('Debugger.enable')
        await self._client.send('Debugger.setSkipAllPauses', {'skip': True})

    def _onExecutionContextsCleared(self, event: Dict) -> None:
        if not self._resetOnNavigation:
            return
        self._scriptURLs.clear()
        self._scriptSources.clear()

    async def _onScriptParsed(self, event: Dict) -> None:
        if event.get('url') == EVALUATION_SCRIPT_URL:
            return
            if not event.get('url'):
                if not self._reportAnonymousScript:
                    return
            scriptId = event.get('scriptId')
            url = event.get('url')
            if not url:
                if self._reportAnonymousScript:
                    url = f"debugger://VM{scriptId}"
        else:
            try:
                response = await self._client.send('Debugger.getScriptSource', {'scriptId': scriptId})
                self._scriptURLs[scriptId] = url
                self._scriptSources[scriptId] = response.get('scriptSource')
            except Exception as e:
                try:
                    debugError(logger, e)
                finally:
                    e = None
                    del e

    async def stop(self) -> List:
        """Stop coverage measurement and return results."""
        if not self._enabled:
            raise PageError('JSCoverage is not enabled.')
        self._enabled = False
        result = await self._client.send('Profiler.takePreciseCoverage')
        await self._client.send('Profiler.stopPreciseCoverage')
        await self._client.send('Profiler.disable')
        await self._client.send('Debugger.disable')
        helper.removeEventListeners(self._eventListeners)
        coverage = []
        for entry in result.get('result', []):
            url = self._scriptURLs.get(entry.get('scriptId'))
            text = self._scriptSources.get(entry.get('scriptId'))
            if not text is None:
                if url is None:
                    continue
                flattenRanges = []
                for func in entry.get('functions', []):
                    flattenRanges.extend(func.get('ranges', []))

                ranges = convertToDisjointRanges(flattenRanges)
                coverage.append({'url':url,  'ranges':ranges,  'text':text})

        return coverage


class CSSCoverage(object):
    __doc__ = 'CSS Coverage class.'

    def __init__(self, client: CDPSession) -> None:
        self._client = client
        self._enabled = False
        self._stylesheetURLs = dict()
        self._stylesheetSources = dict()
        self._eventListeners = []
        self._resetOnNavigation = False

    async def start(self, options: Dict=None, **kwargs: Any) -> None:
        """Start coverage measurement."""
        options = merge_dict(options, kwargs)
        if self._enabled:
            raise PageError('CSSCoverage is already enabled.')
        self._resetOnNavigation = True if 'resetOnNavigation' not in options else bool(options['resetOnNavigation'])
        self._enabled = True
        self._stylesheetURLs.clear()
        self._stylesheetSources.clear()
        self._eventListeners = [
         helper.addEventListener(self._client, 'CSS.styleSheetAdded', lambda e: self._client._loop.create_task(self._onStyleSheet(e))),
         helper.addEventListener(self._client, 'Runtime.executionContextsCleared', self._onExecutionContextsCleared)]
        await self._client.send('DOM.enable')
        await self._client.send('CSS.enable')
        await self._client.send('CSS.startRuleUsageTracking')

    def _onExecutionContextsCleared(self, event: Dict) -> None:
        if not self._resetOnNavigation:
            return
        self._stylesheetURLs.clear()
        self._stylesheetSources.clear()

    async def _onStyleSheet(self, event: Dict) -> None:
        header = event.get('header', {})
        if not header.get('sourceURL'):
            return
        try:
            response = await self._client.send('CSS.getStyleSheetText', {'styleSheetId': header['styleSheetId']})
            self._stylesheetURLs[header['styleSheetId']] = header['sourceURL']
            self._stylesheetSources[header['styleSheetId']] = response['text']
        except Exception as e:
            try:
                debugError(logger, e)
            finally:
                e = None
                del e

    async def stop(self) -> List:
        """Stop coverage measurement and return results."""
        if not self._enabled:
            raise PageError('CSSCoverage is not enabled.')
        self._enabled = False
        result = await self._client.send('CSS.stopRuleUsageTracking')
        await self._client.send('CSS.disable')
        await self._client.send('DOM.disable')
        helper.removeEventListeners(self._eventListeners)
        styleSheetIdToCoverage = {}
        for entry in result['ruleUsage']:
            ranges = styleSheetIdToCoverage.get(entry['styleSheetId'])
            if not ranges:
                ranges = []
                styleSheetIdToCoverage[entry['styleSheetId']] = ranges
            ranges.append({'startOffset':entry['startOffset'], 
             'endOffset':entry['endOffset'], 
             'count':1 if entry['used'] else 0})

        coverage = []
        for styleSheetId in self._stylesheetURLs:
            url = self._stylesheetURLs.get(styleSheetId)
            text = self._stylesheetSources.get(styleSheetId)
            ranges = convertToDisjointRanges(styleSheetIdToCoverage.get(styleSheetId, []))
            coverage.append({'url':url,  'ranges':ranges,  'text':text})

        return coverage


def convertToDisjointRanges(nestedRanges: List[Any]) -> List[Any]:
    """Convert ranges."""
    points = []
    for nested_range in nestedRanges:
        points.append({'offset':nested_range['startOffset'],  'type':0,  'range':nested_range})
        points.append({'offset':nested_range['endOffset'],  'type':1,  'range':nested_range})

    def _sort_func(a: Dict, b: Dict) -> int:
        if a['offset'] != b['offset']:
            return a['offset'] - b['offset']
        if a['type'] != b['type']:
            return b['type'] - a['type']
        aLength = a['range']['endOffset'] - a['range']['startOffset']
        bLength = b['range']['endOffset'] - b['range']['startOffset']
        if a['type'] == 0:
            return bLength - aLength
        return aLength - bLength

    points.sort(key=(cmp_to_key(_sort_func)))
    hitCountStack = []
    results = []
    lastOffset = 0
    for point in points:
        if hitCountStack:
            if lastOffset < point['offset']:
                if hitCountStack[(len(hitCountStack) - 1)] > 0:
                    lastResult = results[(-1)] if results else None
                    if lastResult and lastResult['end'] == lastOffset:
                        lastResult['end'] = point['offset']
                    else:
                        results.append({'start':lastOffset,  'end':point['offset']})
        lastOffset = point['offset']
        if point['type'] == 0:
            hitCountStack.append(point['range']['count'])
        else:
            hitCountStack.pop()

    return [range for range in results if range['end'] - range['start'] > 1]