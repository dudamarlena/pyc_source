# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynk/build.py
# Compiled at: 2019-01-03 04:37:50
"""
Semi-automatically generates a Python binding for the 'nuklear' GUI library,
which is a simple header-only C library with no dependencies.  The binding
makes use of the 'cffi' python package; to use it see the documentation for
'cffi'.
"""
import cffi, re, os, os.path, platform, StringIO

def run_c_preprocessor(header_contents):
    """
    Run a C preprocessor on the given header file contents.
    """
    from pcpp.preprocessor import Preprocessor
    cpp = Preprocessor()
    if platform.system() == 'Windows':
        cpp.define('_MSC_VER')
        cpp.define('__int32 int')
        if platform.architecture()[0] == '64bit':
            cpp.define('_WIN64')
        else:
            cpp.define('WIN32')
            cpp.define('_WIN32')
    else:
        cpp.define('__GNUC__')
        if platform.architecture()[0] == '64bit':
            cpp.define('__x86_64__')
    cpp.parse(header_contents)
    output = StringIO.StringIO()
    cpp.write(output)
    return output.getvalue()


def build_nuklear_defs(preprocessed_text, extra_cdef):
    """
    Preprocess the header file and extract declarations, writing the
    declarations to the given output filename.

    The header contents is preprocessed and then a number of transformations
    are applied to remove problematic constructs - mostly compile-time arithmetic
    in enum declarations.
    """
    print 'Evaluating << expressions...'
    shift_expr = '\\(1 << \\(([0-9]+)\\)\\)'

    def evaluate_shift(match):
        return str(1 << int(match.group(1)))

    preprocessed_text = re.sub(shift_expr, evaluate_shift, preprocessed_text)
    print 'Evaluating | expressions...'
    val_expr = '(nk|NK)_[a-zA-Z0-9_]+'
    or_expr = '%s( *\\| *%s)+' % (val_expr, val_expr)

    def lookup_value(value_name):
        ret = 0
        assignment = re.search('%s *= *([^\n,]*)' % value_name, preprocessed_text)
        if assignment:
            value = assignment.group(1)
            if re.match(or_expr, value) or re.match(val_expr, value):
                ret = evaluate_or(value)
            else:
                ret = int(value, 0)
        else:
            raise Exception("Cannot find definition for value '%s'" % value_name)
        return ret

    def evaluate_or(expression_text):
        values = map(lambda x: lookup_value(x.strip()), expression_text.split('|'))
        return reduce(lambda x, y: x | y, values)

    def replace_or(match):
        return str(evaluate_or(match.group(0)))

    preprocessed_text = re.sub(or_expr, replace_or, preprocessed_text)
    print 'Stubbing nk_table...'
    preprocessed_text = re.sub('(struct nk_table {.*?;)[^;]*?sizeof\\(.*?};', lambda x: x.group(1) + '\n    ...;\n};', preprocessed_text, count=0, flags=re.MULTILINE | re.DOTALL)
    print "Removing duplicate 'nk_draw_list_clear' declaration..."
    preprocessed_text = re.sub('extern void nk_draw_list_clear\\(struct nk_draw_list \\*list\\);', '', preprocessed_text)
    return preprocessed_text + extra_cdef


def maker():
    """ Make the ffibuilder object by parsing the nuklear header. """
    nuklear_header_filename = 'nuklear/nuklear.h'
    cached_preprocessed_header_filename = 'nuklear_preprocessed.h'
    nuklear_overview_filename = 'nuklear/demo/overview.c'
    opts = '\n    #define NK_INCLUDE_DEFAULT_ALLOCATOR\n    #define NK_INCLUDE_VERTEX_BUFFER_OUTPUT\n    #define NK_INCLUDE_FONT_BAKING\n    #define NK_INCLUDE_STANDARD_VARARGS\n    '
    header = opts + open(nuklear_header_filename, 'rU').read()
    source = '\n    #define NK_IMPLEMENTATION\n    ' + header
    extra_cdef = '\n    void pynk_overview(struct nk_context *ctx);\n    extern "Python" {\n        float pynk_text_width_callback(nk_handle handle, float height, const char *text, int len);\n        void pynk_query_font_glyph_callback(nk_handle handle, float font_height,\n                                            struct nk_user_font_glyph *glyph,\n                                            nk_rune codepoint, nk_rune next_codepoint);\n    }\n    '
    overview_source = open(nuklear_overview_filename, 'rU').read()
    source += '\n    #define UNUSED(a) (void)a\n    #define MIN(a,b) ((a) < (b) ? (a) : (b))\n    #define MAX(a,b) ((a) < (b) ? (b) : (a))\n    #define LEN(a) (sizeof(a)/sizeof(a)[0])\n    '
    source += overview_source
    source += '\n    void pynk_overview(struct nk_context *ctx) {\n        overview(ctx);\n    }\n    '
    header_only_options = '\n    #define NK_STATIC_ASSERT(X) \n\n    '
    preprocessed_text = None
    if os.path.exists(cached_preprocessed_header_filename):
        print
        print '***************************************************************'
        print 'NOTE: Using cached preprocessed header from', cached_preprocessed_header_filename
        print '      Any changes to the header will not have been propagated.'
        print '***************************************************************'
        print
        preprocessed_text = open(cached_preprocessed_header_filename, 'rU').read()
    else:
        print 'Preprocessing header...'
        preprocessed_text = run_c_preprocessor(header_only_options + header)
        open(cached_preprocessed_header_filename, 'w').write(preprocessed_text)
    defs = build_nuklear_defs(preprocessed_text, extra_cdef)
    print 'Creating ffi builder...'
    ffibuilder = cffi.FFI()
    ffibuilder.cdef(defs)
    ffibuilder.set_source('_nuklear', source, libraries=[])
    return ffibuilder


if __name__ == '__main__':
    ffibuilder = maker()
    ffibuilder.compile(verbose=True)