# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/grouping/strategies/legacy.py
# Compiled at: 2019-09-04 11:06:02
from __future__ import absolute_import
import re, posixpath
from sentry.grouping.component import GroupingComponent
from sentry.grouping.strategies.base import strategy
from sentry.grouping.strategies.utils import remove_non_stacktrace_variants, has_url_origin
_ruby_anon_func = re.compile('_\\d{2,}')
_filename_version_re = re.compile('(?:\n    v?(?:\\d+\\.)*\\d+|   # version numbers, v1, 1.0.0\n    [a-f0-9]{7,8}|     # short sha\n    [a-f0-9]{32}|      # md5\n    [a-f0-9]{40}       # sha1\n)/', re.X | re.I)
_java_reflect_enhancer_re = re.compile('(sun\\.reflect\\.Generated(?:Serialization)?ConstructorAccessor)\\d+', re.X)
_java_cglib_enhancer_re = re.compile('(\\$\\$[\\w_]+?CGLIB\\$\\$)[a-fA-F0-9]+(_[0-9]+)?', re.X)
_java_assist_enhancer_re = re.compile('(\\$\\$_javassist)(?:_seam)?(?:_[0-9]+)?', re.X)
_clojure_enhancer_re = re.compile('(\\$fn__)\\d+', re.X)
RECURSION_COMPARISON_FIELDS = [
 'abs_path',
 'package',
 'module',
 'filename',
 'function',
 'lineno',
 'colno']

def is_unhashable_module_legacy(frame, platform):
    if platform == 'javascript' and '/' in frame.module and frame.abs_path and frame.abs_path.endswith(frame.module):
        return True
    if platform == 'java' and '$$Lambda$' in frame.module:
        return True
    return False


def is_unhashable_function_legacy(func):
    return func.startswith(('lambda$', '[Anonymous'))


def is_recursion_legacy(frame1, frame2):
    """Returns a boolean indicating whether frames are recursive calls."""
    for field in RECURSION_COMPARISON_FIELDS:
        if getattr(frame1, field, None) != getattr(frame2, field, None):
            return False

    return True


def remove_module_outliers_legacy(module, platform):
    """Remove things that augment the module but really should not."""
    if platform == 'java':
        if module[:35] == 'sun.reflect.GeneratedMethodAccessor':
            return ('sun.reflect.GeneratedMethodAccessor', 'removed reflection marker')
        if module[:44] == 'jdk.internal.reflect.GeneratedMethodAccessor':
            return ('jdk.internal.reflect.GeneratedMethodAccessor', 'removed reflection marker')
        old_module = module
        module = _java_reflect_enhancer_re.sub('\\1<auto>', module)
        module = _java_cglib_enhancer_re.sub('\\1<auto>', module)
        module = _java_assist_enhancer_re.sub('\\1<auto>', module)
        module = _clojure_enhancer_re.sub('\\1<auto>', module)
        if old_module != module:
            return (module, 'removed codegen marker')
    return (
     module, None)


def remove_filename_outliers_legacy(filename, platform):
    """
    Attempt to normalize filenames by removing common platform outliers.

    - Sometimes filename paths contain build numbers
    """
    if platform == 'cocoa':
        return (posixpath.basename(filename), 'stripped to basename')
    else:
        removed = []
        if platform == 'java':
            new_filename = _java_assist_enhancer_re.sub('\\1<auto>', filename)
            if new_filename != filename:
                removed.append('javassist parts')
                filename = new_filename
        new_filename = _filename_version_re.sub('<version>/', filename)
        if new_filename != filename:
            removed.append('version')
            filename = new_filename
        if removed:
            return (filename, 'removed %s' % (' and ').join(removed))
        return (
         filename, None)


def remove_function_outliers_legacy(function):
    """
    Attempt to normalize functions by removing common platform outliers.

    - Ruby generates (random?) integers for various anonymous style functions
      such as in erb and the active_support library.
    - Block functions have metadata that we don't care about.
    """
    if function.startswith('block '):
        return ('block', 'ruby block')
    else:
        new_function = _ruby_anon_func.sub('_<anon>', function)
        if new_function != function:
            return (new_function, 'trimmed integer suffix')
        return (
         new_function, None)


@strategy(id='single-exception:legacy', interfaces=['singleexception'], variants=['!system', 'app'])
def single_exception_legacy(exception, config, **meta):
    type_component = GroupingComponent(id='type', values=[exception.type] if exception.type else [], contributes=False)
    value_component = GroupingComponent(id='value', values=[exception.value] if exception.value else [], contributes=False)
    stacktrace_component = GroupingComponent(id='stacktrace')
    if exception.stacktrace is not None:
        stacktrace_component = config.get_grouping_component(exception.stacktrace, **meta)
        if stacktrace_component.contributes:
            if exception.type:
                type_component.update(contributes=True)
                if exception.value:
                    value_component.update(hint='stacktrace and type take precedence')
            elif exception.value:
                value_component.update(hint='stacktrace takes precedence')
    if not stacktrace_component.contributes:
        if exception.type:
            type_component.update(contributes=True)
        if exception.value:
            value_component.update(contributes=True)
    return GroupingComponent(id='exception', values=[stacktrace_component, type_component, value_component])


@strategy(id='chained-exception:legacy', interfaces=['exception'], variants=['!system', 'app'], score=2000)
def chained_exception_legacy(chained_exception, config, **meta):
    exceptions = chained_exception.exceptions()
    if len(exceptions) == 1:
        return config.get_grouping_component(exceptions[0], **meta)
    else:
        any_stacktraces = False
        values = []
        for exception in exceptions:
            exception_component = config.get_grouping_component(exception, **meta)
            stacktrace_component = exception_component.get_subcomponent('stacktrace')
            if stacktrace_component is not None and stacktrace_component.contributes:
                any_stacktraces = True
            values.append(exception_component)

        if any_stacktraces:
            for value in values:
                stacktrace_component = value.get_subcomponent('stacktrace')
                if stacktrace_component is None or not stacktrace_component.contributes:
                    value.update(contributes=False, hint='exception has no stacktrace')

        return GroupingComponent(id='chained-exception', values=values)


@chained_exception_legacy.variant_processor
def chained_exception_legacy_variant_processor(variants, config, **meta):
    return remove_non_stacktrace_variants(variants)


@strategy(id='frame:legacy', interfaces=['frame'], variants=['!system', 'app'])
def frame_legacy(frame, event, **meta):
    platform = frame.platform or event.platform
    contributes = None
    hint = None
    func = frame.raw_function or frame.function
    filename_component = GroupingComponent(id='filename')
    if frame.filename == '<anonymous>':
        filename_component.update(contributes=False, values=[frame.filename], hint='anonymous filename discarded')
    elif frame.filename == '[native code]':
        contributes = False
        hint = 'native code indicated by filename'
    elif frame.filename:
        if has_url_origin(frame.abs_path):
            filename_component.update(contributes=False, values=[frame.filename], hint='ignored because filename is a URL')
        elif frame.filename.startswith('Caused by: '):
            filename_component.update(values=[
             frame.filename], contributes=False, hint='ignored because invalid')
        else:
            hashable_filename, hashable_filename_hint = remove_filename_outliers_legacy(frame.filename, platform)
            filename_component.update(values=[hashable_filename], hint=hashable_filename_hint)
    module_component = GroupingComponent(id='module')
    if frame.module:
        if is_unhashable_module_legacy(frame, platform):
            module_component.update(values=[
             GroupingComponent(id='salt', values=['<module>'], hint='normalized generated module name')], hint='ignored module')
        else:
            module_name, module_hint = remove_module_outliers_legacy(frame.module, platform)
            module_component.update(values=[module_name], hint=module_hint)
        if frame.filename:
            filename_component.update(values=[
             frame.filename], contributes=False, hint='module takes precedence')
    context_line_component = GroupingComponent(id='context-line')
    if frame.context_line is not None:
        if len(frame.context_line) > 120:
            context_line_component.update(hint='discarded because line too long')
        elif has_url_origin(frame.abs_path) and not func:
            context_line_component.update(hint='discarded because from URL origin')
        else:
            context_line_component.update(values=[frame.context_line])
    symbol_component = GroupingComponent(id='symbol')
    function_component = GroupingComponent(id='function')
    lineno_component = GroupingComponent(id='lineno')
    if not context_line_component.contributes and (module_component.contributes or filename_component.contributes):
        if frame.symbol:
            symbol_component.update(values=[frame.symbol])
            if func:
                function_component.update(contributes=False, values=[func], hint='symbol takes precedence')
            if frame.lineno:
                lineno_component.update(contributes=False, values=[frame.lineno], hint='symbol takes precedence')
        elif func:
            if is_unhashable_function_legacy(func):
                function_component.update(values=[
                 GroupingComponent(id='salt', values=['<function>'], hint='normalized lambda function name')])
            else:
                function, function_hint = remove_function_outliers_legacy(func)
                function_component.update(values=[function], hint=function_hint)
            if frame.lineno:
                lineno_component.update(contributes=False, values=[frame.lineno], hint='function takes precedence')
        elif frame.lineno:
            lineno_component.update(values=[frame.lineno])
    else:
        if context_line_component.contributes:
            fallback_hint = 'is not used if context-line is available'
        else:
            fallback_hint = 'is not used if module or filename are available'
        if frame.symbol:
            symbol_component.update(contributes=False, values=[
             frame.symbol], hint='symbol ' + fallback_hint)
        if func:
            function_component.update(contributes=False, values=[
             func], hint='function name ' + fallback_hint)
        if frame.lineno:
            lineno_component.update(contributes=False, values=[
             frame.lineno], hint='line number ' + fallback_hint)
    return GroupingComponent(id='frame', values=[
     module_component,
     filename_component,
     context_line_component,
     symbol_component,
     function_component,
     lineno_component], contributes=contributes, hint=hint)


@strategy(id='stacktrace:legacy', interfaces=['stacktrace'], variants=['!system', 'app'], score=1800)
def stacktrace_legacy(stacktrace, config, variant, **meta):
    frames = stacktrace.frames
    contributes = None
    hint = None
    all_frames_considered_in_app = False
    if len(frames) == 1 and not frames[0].function and frames[0].is_url():
        contributes = False
        hint = 'ignored single frame stack'
    else:
        if variant == 'app':
            total_frames = len(frames)
            in_app_count = sum((1 if f.in_app else 0) for f in frames)
            if in_app_count == 0:
                in_app_count = total_frames
                all_frames_considered_in_app = True
            if total_frames > 0 and in_app_count / float(total_frames) < 0.1:
                contributes = False
                hint = 'less than 10% of frames are in-app'
        values = []
        prev_frame = None
        frames_for_filtering = []
        for frame in frames:
            frame_component = config.get_grouping_component(frame, variant=variant, **meta)
            if variant == 'app' and not frame.in_app and not all_frames_considered_in_app:
                frame_component.update(contributes=False, hint='non app frame')
            elif prev_frame is not None and is_recursion_legacy(frame, prev_frame):
                frame_component.update(contributes=False, hint='ignored due to recursion')
            elif variant == 'app' and not frame.in_app and all_frames_considered_in_app:
                frame_component.update(hint='frame considered in-app because no frame is in-app')
            values.append(frame_component)
            frames_for_filtering.append(frame.get_raw_data())
            prev_frame = frame

    rv = config.enhancements.assemble_stacktrace_component(values, frames_for_filtering, meta['event'].platform)
    rv.update(contributes=contributes, hint=hint)
    return rv


@strategy(id='threads:legacy', interfaces=['threads'], variants=['!system', 'app'], score=1900)
def threads_legacy(threads_interface, config, **meta):
    thread_count = len(threads_interface.values)
    if thread_count != 1:
        return GroupingComponent(id='threads', contributes=False, hint='ignored because contains %d threads' % thread_count)
    stacktrace = threads_interface.values[0].get('stacktrace')
    if not stacktrace:
        return GroupingComponent(id='threads', contributes=False, hint='thread has no stacktrace')
    return GroupingComponent(id='threads', values=[config.get_grouping_component(stacktrace, **meta)])