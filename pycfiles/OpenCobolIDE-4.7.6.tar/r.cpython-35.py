# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/r.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 23755 bytes
"""
    pygments.lexers.r
    ~~~~~~~~~~~~~~~~~

    Lexers for the R/S languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, words, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
__all__ = [
 'RConsoleLexer', 'SLexer', 'RdLexer']
line_re = re.compile('.*?\n')

class RConsoleLexer(Lexer):
    __doc__ = '\n    For R console transcripts or R CMD BATCH output files.\n    '
    name = 'RConsole'
    aliases = ['rconsole', 'rout']
    filenames = ['*.Rout']

    def get_tokens_unprocessed(self, text):
        slexer = SLexer(**self.options)
        current_code_block = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('>') or line.startswith('+'):
                insertions.append((len(current_code_block),
                 [
                  (
                   0, Generic.Prompt, line[:2])]))
                current_code_block += line[2:]
            else:
                if current_code_block:
                    for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                        yield item

                    current_code_block = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)

        if current_code_block:
            for item in do_insertions(insertions, slexer.get_tokens_unprocessed(current_code_block)):
                yield item


class SLexer(RegexLexer):
    __doc__ = '\n    For S, S-plus, and R source code.\n\n    .. versionadded:: 0.10\n    '
    name = 'S'
    aliases = ['splus', 's', 'r']
    filenames = ['*.S', '*.R', '.Rhistory', '.Rprofile', '.Renviron']
    mimetypes = ['text/S-plus', 'text/S', 'text/x-r-source', 'text/x-r',
     'text/x-R', 'text/x-r-history', 'text/x-r-profile']
    builtins_base = ('Arg', 'Conj', 'Cstack_info', 'Encoding', 'FALSE', 'Filter', 'Find',
                     'I', 'ISOdate', 'ISOdatetime', 'Im', 'Inf', 'La.svd', 'Map',
                     'Math.Date', 'Math.POSIXt', 'Math.data.frame', 'Math.difftime',
                     'Math.factor', 'Mod', 'NA_character_', 'NA_complex_', 'NA_real_',
                     'NCOL', 'NROW', 'NULLNA_integer_', 'NaN', 'Negate', 'NextMethod',
                     'Ops.Date', 'Ops.POSIXt', 'Ops.data.frame', 'Ops.difftime',
                     'Ops.factor', 'Ops.numeric_version', 'Ops.ordered', 'Position',
                     'R.Version', 'R.home', 'R.version', 'R.version.string', 'RNGkind',
                     'RNGversion', 'R_system_version', 'Re', 'Recall', 'Reduce',
                     'Summary.Date', 'Summary.POSIXct', 'Summary.POSIXlt', 'Summary.data.frame',
                     'Summary.difftime', 'Summary.factor', 'Summary.numeric_version',
                     'Summary.ordered', 'Sys.Date', 'Sys.chmod', 'Sys.getenv', 'Sys.getlocale',
                     'Sys.getpid', 'Sys.glob', 'Sys.info', 'Sys.localeconv', 'Sys.readlink',
                     'Sys.setFileTime', 'Sys.setenv', 'Sys.setlocale', 'Sys.sleep',
                     'Sys.time', 'Sys.timezone', 'Sys.umask', 'Sys.unsetenv', 'Sys.which',
                     'TRUE', 'UseMethod', 'Vectorize', 'abbreviate', 'abs', 'acos',
                     'acosh', 'addNA', 'addTaskCallback', 'agrep', 'alist', 'all',
                     'all.equal', 'all.equal.POSIXct', 'all.equal.character', 'all.equal.default',
                     'all.equal.factor', 'all.equal.formula', 'all.equal.language',
                     'all.equal.list', 'all.equal.numeric', 'all.equal.raw', 'all.names',
                     'all.vars', 'any', 'anyDuplicated', 'anyDuplicated.array', 'anyDuplicated.data.frame',
                     'anyDuplicated.default', 'anyDuplicated.matrix', 'aperm', 'aperm.default',
                     'aperm.table', 'append', 'apply', 'args', 'arrayInd', 'as.Date',
                     'as.Date.POSIXct', 'as.Date.POSIXlt', 'as.Date.character', 'as.Date.date',
                     'as.Date.dates', 'as.Date.default', 'as.Date.factor', 'as.Date.numeric',
                     'as.POSIXct', 'as.POSIXct.Date', 'as.POSIXct.POSIXlt', 'as.POSIXct.date',
                     'as.POSIXct.dates', 'as.POSIXct.default', 'as.POSIXct.numeric',
                     'as.POSIXlt', 'as.POSIXlt.Date', 'as.POSIXlt.POSIXct', 'as.POSIXlt.character',
                     'as.POSIXlt.date', 'as.POSIXlt.dates', 'as.POSIXlt.default',
                     'as.POSIXlt.factor', 'as.POSIXlt.numeric', 'as.array', 'as.array.default',
                     'as.call', 'as.character', 'as.character.Date', 'as.character.POSIXt',
                     'as.character.condition', 'as.character.default', 'as.character.error',
                     'as.character.factor', 'as.character.hexmode', 'as.character.numeric_version',
                     'as.character.octmode', 'as.character.srcref', 'as.complex',
                     'as.data.frame', 'as.data.frame.AsIs', 'as.data.frame.Date',
                     'as.data.frame.POSIXct', 'as.data.frame.POSIXlt', 'as.data.frame.array',
                     'as.data.frame.character', 'as.data.frame.complex', 'as.data.frame.data.frame',
                     'as.data.frame.default', 'as.data.frame.difftime', 'as.data.frame.factor',
                     'as.data.frame.integer', 'as.data.frame.list', 'as.data.frame.logical',
                     'as.data.frame.matrix', 'as.data.frame.model.matrix', 'as.data.frame.numeric',
                     'as.data.frame.numeric_version', 'as.data.frame.ordered', 'as.data.frame.raw',
                     'as.data.frame.table', 'as.data.frame.ts', 'as.data.frame.vector',
                     'as.difftime', 'as.double', 'as.double.POSIXlt', 'as.double.difftime',
                     'as.environment', 'as.expression', 'as.expression.default',
                     'as.factor', 'as.function', 'as.function.default', 'as.hexmode',
                     'as.integer', 'as.list', 'as.list.Date', 'as.list.POSIXct',
                     'as.list.data.frame', 'as.list.default', 'as.list.environment',
                     'as.list.factor', 'as.list.function', 'as.list.numeric_version',
                     'as.logical', 'as.logical.factor', 'as.matrix', 'as.matrix.POSIXlt',
                     'as.matrix.data.frame', 'as.matrix.default', 'as.matrix.noquote',
                     'as.name', 'as.null', 'as.null.default', 'as.numeric', 'as.numeric_version',
                     'as.octmode', 'as.ordered', 'as.package_version', 'as.pairlist',
                     'as.qr', 'as.raw', 'as.single', 'as.single.default', 'as.symbol',
                     'as.table', 'as.table.default', 'as.vector', 'as.vector.factor',
                     'asNamespace', 'asS3', 'asS4', 'asin', 'asinh', 'assign', 'atan',
                     'atan2', 'atanh', 'attachNamespace', 'attr', 'attr.all.equal',
                     'attributes', 'autoload', 'autoloader', 'backsolve', 'baseenv',
                     'basename', 'besselI', 'besselJ', 'besselK', 'besselY', 'beta',
                     'bindingIsActive', 'bindingIsLocked', 'bindtextdomain', 'bitwAnd',
                     'bitwNot', 'bitwOr', 'bitwShiftL', 'bitwShiftR', 'bitwXor',
                     'body', 'bquote', 'browser', 'browserCondition', 'browserSetDebug',
                     'browserText', 'builtins', 'by', 'by.data.frame', 'by.default',
                     'bzfile', 'c.Date', 'c.POSIXct', 'c.POSIXlt', 'c.noquote', 'c.numeric_version',
                     'call', 'callCC', 'capabilities', 'casefold', 'cat', 'category',
                     'cbind', 'cbind.data.frame', 'ceiling', 'char.expand', 'charToRaw',
                     'charmatch', 'chartr', 'check_tzones', 'chol', 'chol.default',
                     'chol2inv', 'choose', 'class', 'clearPushBack', 'close', 'close.connection',
                     'close.srcfile', 'close.srcfilealias', 'closeAllConnections',
                     'col', 'colMeans', 'colSums', 'colnames', 'commandArgs', 'comment',
                     'computeRestarts', 'conditionCall', 'conditionCall.condition',
                     'conditionMessage', 'conditionMessage.condition', 'conflicts',
                     'contributors', 'cos', 'cosh', 'crossprod', 'cummax', 'cummin',
                     'cumprod', 'cumsum', 'cut', 'cut.Date', 'cut.POSIXt', 'cut.default',
                     'dQuote', 'data.class', 'data.matrix', 'date', 'debug', 'debugonce',
                     'default.stringsAsFactors', 'delayedAssign', 'deparse', 'det',
                     'determinant', 'determinant.matrix', 'dget', 'diag', 'diff',
                     'diff.Date', 'diff.POSIXt', 'diff.default', 'difftime', 'digamma',
                     'dim', 'dim.data.frame', 'dimnames', 'dimnames.data.frame',
                     'dir', 'dir.create', 'dirname', 'do.call', 'dput', 'drop', 'droplevels',
                     'droplevels.data.frame', 'droplevels.factor', 'dump', 'duplicated',
                     'duplicated.POSIXlt', 'duplicated.array', 'duplicated.data.frame',
                     'duplicated.default', 'duplicated.matrix', 'duplicated.numeric_version',
                     'dyn.load', 'dyn.unload', 'eapply', 'eigen', 'else', 'emptyenv',
                     'enc2native', 'enc2utf8', 'encodeString', 'enquote', 'env.profile',
                     'environment', 'environmentIsLocked', 'environmentName', 'eval',
                     'eval.parent', 'evalq', 'exists', 'exp', 'expand.grid', 'expm1',
                     'expression', 'factor', 'factorial', 'fifo', 'file', 'file.access',
                     'file.append', 'file.choose', 'file.copy', 'file.create', 'file.exists',
                     'file.info', 'file.link', 'file.path', 'file.remove', 'file.rename',
                     'file.show', 'file.symlink', 'find.package', 'findInterval',
                     'findPackageEnv', 'findRestart', 'floor', 'flush', 'flush.connection',
                     'force', 'formals', 'format', 'format.AsIs', 'format.Date',
                     'format.POSIXct', 'format.POSIXlt', 'format.data.frame', 'format.default',
                     'format.difftime', 'format.factor', 'format.hexmode', 'format.info',
                     'format.libraryIQR', 'format.numeric_version', 'format.octmode',
                     'format.packageInfo', 'format.pval', 'format.summaryDefault',
                     'formatC', 'formatDL', 'forwardsolve', 'gamma', 'gc', 'gc.time',
                     'gcinfo', 'gctorture', 'gctorture2', 'get', 'getAllConnections',
                     'getCallingDLL', 'getCallingDLLe', 'getConnection', 'getDLLRegisteredRoutines',
                     'getDLLRegisteredRoutines.DLLInfo', 'getDLLRegisteredRoutines.character',
                     'getElement', 'getExportedValue', 'getHook', 'getLoadedDLLs',
                     'getNamespace', 'getNamespaceExports', 'getNamespaceImports',
                     'getNamespaceInfo', 'getNamespaceName', 'getNamespaceUsers',
                     'getNamespaceVersion', 'getNativeSymbolInfo', 'getOption', 'getRversion',
                     'getSrcLines', 'getTaskCallbackNames', 'geterrmessage', 'gettext',
                     'gettextf', 'getwd', 'gl', 'globalenv', 'gregexpr', 'grep',
                     'grepRaw', 'grepl', 'gsub', 'gzcon', 'gzfile', 'head', 'iconv',
                     'iconvlist', 'icuSetCollate', 'identical', 'identity', 'ifelse',
                     'importIntoEnv', 'in', 'inherits', 'intToBits', 'intToUtf8',
                     'interaction', 'interactive', 'intersect', 'inverse.rle', 'invisible',
                     'invokeRestart', 'invokeRestartInteractively', 'is.R', 'is.array',
                     'is.atomic', 'is.call', 'is.character', 'is.complex', 'is.data.frame',
                     'is.double', 'is.element', 'is.environment', 'is.expression',
                     'is.factor', 'is.finite', 'is.function', 'is.infinite', 'is.integer',
                     'is.language', 'is.list', 'is.loaded', 'is.logical', 'is.matrix',
                     'is.na', 'is.na.POSIXlt', 'is.na.data.frame', 'is.na.numeric_version',
                     'is.name', 'is.nan', 'is.null', 'is.numeric', 'is.numeric.Date',
                     'is.numeric.POSIXt', 'is.numeric.difftime', 'is.numeric_version',
                     'is.object', 'is.ordered', 'is.package_version', 'is.pairlist',
                     'is.primitive', 'is.qr', 'is.raw', 'is.recursive', 'is.single',
                     'is.symbol', 'is.table', 'is.unsorted', 'is.vector', 'isBaseNamespace',
                     'isIncomplete', 'isNamespace', 'isOpen', 'isRestart', 'isS4',
                     'isSeekable', 'isSymmetric', 'isSymmetric.matrix', 'isTRUE',
                     'isatty', 'isdebugged', 'jitter', 'julian', 'julian.Date', 'julian.POSIXt',
                     'kappa', 'kappa.default', 'kappa.lm', 'kappa.qr', 'kronecker',
                     'l10n_info', 'labels', 'labels.default', 'lapply', 'lazyLoad',
                     'lazyLoadDBexec', 'lazyLoadDBfetch', 'lbeta', 'lchoose', 'length',
                     'length.POSIXlt', 'letters', 'levels', 'levels.default', 'lfactorial',
                     'lgamma', 'library.dynam', 'library.dynam.unload', 'licence',
                     'license', 'list.dirs', 'list.files', 'list2env', 'load', 'loadNamespace',
                     'loadedNamespaces', 'loadingNamespaceInfo', 'local', 'lockBinding',
                     'lockEnvironment', 'log', 'log10', 'log1p', 'log2', 'logb',
                     'lower.tri', 'ls', 'make.names', 'make.unique', 'makeActiveBinding',
                     'mapply', 'margin.table', 'mat.or.vec', 'match', 'match.arg',
                     'match.call', 'match.fun', 'max', 'max.col', 'mean', 'mean.Date',
                     'mean.POSIXct', 'mean.POSIXlt', 'mean.default', 'mean.difftime',
                     'mem.limits', 'memCompress', 'memDecompress', 'memory.profile',
                     'merge', 'merge.data.frame', 'merge.default', 'message', 'mget',
                     'min', 'missing', 'mode', 'month.abb', 'month.name', 'months',
                     'months.Date', 'months.POSIXt', 'months.abb', 'months.nameletters',
                     'names', 'names.POSIXlt', 'namespaceExport', 'namespaceImport',
                     'namespaceImportClasses', 'namespaceImportFrom', 'namespaceImportMethods',
                     'nargs', 'nchar', 'ncol', 'new.env', 'ngettext', 'nlevels',
                     'noquote', 'norm', 'normalizePath', 'nrow', 'numeric_version',
                     'nzchar', 'objects', 'oldClass', 'on.exit', 'open', 'open.connection',
                     'open.srcfile', 'open.srcfilealias', 'open.srcfilecopy', 'options',
                     'order', 'ordered', 'outer', 'packBits', 'packageEvent', 'packageHasNamespace',
                     'packageStartupMessage', 'package_version', 'pairlist', 'parent.env',
                     'parent.frame', 'parse', 'parseNamespaceFile', 'paste', 'paste0',
                     'path.expand', 'path.package', 'pipe', 'pmatch', 'pmax', 'pmax.int',
                     'pmin', 'pmin.int', 'polyroot', 'pos.to.env', 'pretty', 'pretty.default',
                     'prettyNum', 'print', 'print.AsIs', 'print.DLLInfo', 'print.DLLInfoList',
                     'print.DLLRegisteredRoutines', 'print.Date', 'print.NativeRoutineList',
                     'print.POSIXct', 'print.POSIXlt', 'print.by', 'print.condition',
                     'print.connection', 'print.data.frame', 'print.default', 'print.difftime',
                     'print.factor', 'print.function', 'print.hexmode', 'print.libraryIQR',
                     'print.listof', 'print.noquote', 'print.numeric_version', 'print.octmode',
                     'print.packageInfo', 'print.proc_time', 'print.restart', 'print.rle',
                     'print.simple.list', 'print.srcfile', 'print.srcref', 'print.summary.table',
                     'print.summaryDefault', 'print.table', 'print.warnings', 'prmatrix',
                     'proc.time', 'prod', 'prop.table', 'provideDimnames', 'psigamma',
                     'pushBack', 'pushBackLength', 'q', 'qr', 'qr.Q', 'qr.R', 'qr.X',
                     'qr.coef', 'qr.default', 'qr.fitted', 'qr.qty', 'qr.qy', 'qr.resid',
                     'qr.solve', 'quarters', 'quarters.Date', 'quarters.POSIXt',
                     'quit', 'quote', 'range', 'range.default', 'rank', 'rapply',
                     'raw', 'rawConnection', 'rawConnectionValue', 'rawShift', 'rawToBits',
                     'rawToChar', 'rbind', 'rbind.data.frame', 'rcond', 'read.dcf',
                     'readBin', 'readChar', 'readLines', 'readRDS', 'readRenviron',
                     'readline', 'reg.finalizer', 'regexec', 'regexpr', 'registerS3method',
                     'registerS3methods', 'regmatches', 'remove', 'removeTaskCallback',
                     'rep', 'rep.Date', 'rep.POSIXct', 'rep.POSIXlt', 'rep.factor',
                     'rep.int', 'rep.numeric_version', 'rep_len', 'replace', 'replicate',
                     'requireNamespace', 'restartDescription', 'restartFormals',
                     'retracemem', 'rev', 'rev.default', 'rle', 'rm', 'round', 'round.Date',
                     'round.POSIXt', 'row', 'row.names', 'row.names.data.frame',
                     'row.names.default', 'rowMeans', 'rowSums', 'rownames', 'rowsum',
                     'rowsum.data.frame', 'rowsum.default', 'sQuote', 'sample', 'sample.int',
                     'sapply', 'save', 'save.image', 'saveRDS', 'scale', 'scale.default',
                     'scan', 'search', 'searchpaths', 'seek', 'seek.connection',
                     'seq', 'seq.Date', 'seq.POSIXt', 'seq.default', 'seq.int', 'seq_along',
                     'seq_len', 'sequence', 'serialize', 'set.seed', 'setHook', 'setNamespaceInfo',
                     'setSessionTimeLimit', 'setTimeLimit', 'setdiff', 'setequal',
                     'setwd', 'shQuote', 'showConnections', 'sign', 'signalCondition',
                     'signif', 'simpleCondition', 'simpleError', 'simpleMessage',
                     'simpleWarning', 'simplify2array', 'sin', 'single', 'sinh',
                     'sink', 'sink.number', 'slice.index', 'socketConnection', 'socketSelect',
                     'solve', 'solve.default', 'solve.qr', 'sort', 'sort.POSIXlt',
                     'sort.default', 'sort.int', 'sort.list', 'split', 'split.Date',
                     'split.POSIXct', 'split.data.frame', 'split.default', 'sprintf',
                     'sqrt', 'srcfile', 'srcfilealias', 'srcfilecopy', 'srcref',
                     'standardGeneric', 'stderr', 'stdin', 'stdout', 'stop', 'stopifnot',
                     'storage.mode', 'strftime', 'strptime', 'strsplit', 'strtoi',
                     'strtrim', 'structure', 'strwrap', 'sub', 'subset', 'subset.data.frame',
                     'subset.default', 'subset.matrix', 'substitute', 'substr', 'substring',
                     'sum', 'summary', 'summary.Date', 'summary.POSIXct', 'summary.POSIXlt',
                     'summary.connection', 'summary.data.frame', 'summary.default',
                     'summary.factor', 'summary.matrix', 'summary.proc_time', 'summary.srcfile',
                     'summary.srcref', 'summary.table', 'suppressMessages', 'suppressPackageStartupMessages',
                     'suppressWarnings', 'svd', 'sweep', 'sys.call', 'sys.calls',
                     'sys.frame', 'sys.frames', 'sys.function', 'sys.load.image',
                     'sys.nframe', 'sys.on.exit', 'sys.parent', 'sys.parents', 'sys.save.image',
                     'sys.source', 'sys.status', 'system', 'system.file', 'system.time',
                     'system2', 't', 't.data.frame', 't.default', 'table', 'tabulate',
                     'tail', 'tan', 'tanh', 'tapply', 'taskCallbackManager', 'tcrossprod',
                     'tempdir', 'tempfile', 'testPlatformEquivalence', 'textConnection',
                     'textConnectionValue', 'toString', 'toString.default', 'tolower',
                     'topenv', 'toupper', 'trace', 'traceback', 'tracemem', 'tracingState',
                     'transform', 'transform.data.frame', 'transform.default', 'trigamma',
                     'trunc', 'trunc.Date', 'trunc.POSIXt', 'truncate', 'truncate.connection',
                     'try', 'tryCatch', 'typeof', 'unclass', 'undebug', 'union',
                     'unique', 'unique.POSIXlt', 'unique.array', 'unique.data.frame',
                     'unique.default', 'unique.matrix', 'unique.numeric_version',
                     'units', 'units.difftime', 'unix.time', 'unlink', 'unlist',
                     'unloadNamespace', 'unlockBinding', 'unname', 'unserialize',
                     'unsplit', 'untrace', 'untracemem', 'unz', 'upper.tri', 'url',
                     'utf8ToInt', 'vapply', 'version', 'warning', 'warnings', 'weekdays',
                     'weekdays.Date', 'weekdays.POSIXt', 'which', 'which.max', 'which.min',
                     'with', 'with.default', 'withCallingHandlers', 'withRestarts',
                     'withVisible', 'within', 'within.data.frame', 'within.list',
                     'write', 'write.dcf', 'writeBin', 'writeChar', 'writeLines',
                     'xor', 'xor.hexmode', 'xor.octmode', 'xpdrows.data.frame', 'xtfrm',
                     'xtfrm.AsIs', 'xtfrm.Date', 'xtfrm.POSIXct', 'xtfrm.POSIXlt',
                     'xtfrm.Surv', 'xtfrm.default', 'xtfrm.difftime', 'xtfrm.factor',
                     'xtfrm.numeric_version', 'xzfile', 'zapsmall')
    tokens = {'comments': [
                  (
                   '#.*$', Comment.Single)], 
     
     'valid_name': [
                    (
                     '[a-zA-Z][\\w.]*', Text),
                    (
                     '\\.[a-zA-Z_][\\w.]*', Text)], 
     
     'punctuation': [
                     (
                      '\\[{1,2}|\\]{1,2}|\\(|\\)|;|,', Punctuation)], 
     
     'keywords': [
                  (
                   words(builtins_base, suffix='(?![\\w. =])'),
                   Keyword.Pseudo),
                  (
                   '(if|else|for|while|repeat|in|next|break|return|switch|function)(?![\\w.])',
                   Keyword.Reserved),
                  (
                   '(array|category|character|complex|double|function|integer|list|logical|matrix|numeric|vector|data.frame|c)(?![\\w.])',
                   Keyword.Type),
                  (
                   '(library|require|attach|detach|source)(?![\\w.])',
                   Keyword.Namespace)], 
     
     'operators': [
                   (
                    '<<?-|->>?|-|==|<=|>=|<|>|&&?|!=|\\|\\|?|\\?', Operator),
                   (
                    '\\*|\\+|\\^|/|!|%[^%]*%|=|~|\\$|@|:{1,3}', Operator)], 
     
     'builtin_symbols': [
                         (
                          '(NULL|NA(_(integer|real|complex|character)_)?|letters|LETTERS|Inf|TRUE|FALSE|NaN|pi|\\.\\.(\\.|[0-9]+))(?![\\w.])',
                          Keyword.Constant),
                         (
                          '(T|F)\\b', Name.Builtin.Pseudo)], 
     
     'numbers': [
                 (
                  '0[xX][a-fA-F0-9]+([pP][0-9]+)?[Li]?', Number.Hex),
                 (
                  '[+-]?([0-9]+(\\.[0-9]+)?|\\.[0-9]+|\\.)([eE][+-]?[0-9]+)?[Li]?',
                  Number)], 
     
     'statements': [
                    include('comments'),
                    (
                     '\\s+', Text),
                    (
                     '`.*?`', String.Backtick),
                    (
                     "\\'", String, 'string_squote'),
                    (
                     '\\"', String, 'string_dquote'),
                    include('builtin_symbols'),
                    include('numbers'),
                    include('keywords'),
                    include('punctuation'),
                    include('operators'),
                    include('valid_name')], 
     
     'root': [
              include('statements'),
              (
               '\\{|\\}', Punctuation),
              (
               '.', Text)], 
     
     'string_squote': [
                       (
                        "([^\\'\\\\]|\\\\.)*\\'", String, '#pop')], 
     
     'string_dquote': [
                       (
                        '([^"\\\\]|\\\\.)*"', String, '#pop')]}

    def analyse_text(text):
        if re.search('[a-z0-9_\\])\\s]<-(?!-)', text):
            return 0.11


class RdLexer(RegexLexer):
    __doc__ = '\n    Pygments Lexer for R documentation (Rd) files\n\n    This is a very minimal implementation, highlighting little more\n    than the macros. A description of Rd syntax is found in `Writing R\n    Extensions <http://cran.r-project.org/doc/manuals/R-exts.html>`_\n    and `Parsing Rd files <developer.r-project.org/parseRd.pdf>`_.\n\n    .. versionadded:: 1.6\n    '
    name = 'Rd'
    aliases = ['rd']
    filenames = ['*.Rd']
    mimetypes = ['text/x-r-doc']
    tokens = {'root': [
              (
               '\\\\[\\\\{}%]', String.Escape),
              (
               '%.*$', Comment),
              (
               '\\\\(?:cr|l?dots|R|tab)\\b', Keyword.Constant),
              (
               '\\\\[a-zA-Z]+\\b', Keyword),
              (
               '^\\s*#(?:ifn?def|endif).*\\b', Comment.Preproc),
              (
               '[{}]', Name.Builtin),
              (
               '[^\\\\%\\n{}]+', Text),
              (
               '.', Text)]}