# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\MessageSource.py
# Compiled at: 2005-04-03 02:47:13
__doc__ = '\nXSLT error codes and messages\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft import TranslateMessage as _
POSITION_INFO = _('In stylesheet %s, line %s, column %s:\n%s')
EXPRESSION_POSITION_INFO = _('In stylesheet %s, line %s, column %s in "%s":\n%s')
XSLT_EXPRESSION_POSITION_INFO = _('%s\nThe error occurred in the expression "%s".')
BUILTIN_TEMPLATE_WITH_PARAMS = _('Built-in template invoked with params that will be ignored. This message will only appear once per transform.')
TEMPLATE_CONFLICT_LOCATION = _('In stylesheet %s, line %s, column %s, pattern %s')
DEFAULT_MESSAGE_PREFIX = _('STYLESHEET MESSAGE:\n')
DEFAULT_MESSAGE_SUFFIX = _('\nEND STYLESHEET MESSAGE\n')

class Error:
    __module__ = __name__
    NO_STYLESHEET = 20
    LITERAL_RESULT_MISSING_VERSION = 22
    STYLESHEET_PARSE_ERROR = 23
    SOURCE_PARSE_ERROR = 24
    XSLT_ILLEGAL_ELEMENT = 27
    CIRCULAR_VAR = 29
    DUPLICATE_TOP_LEVEL_VAR = 30
    DUPLICATE_NAMESPACE_ALIAS = 31
    ILLEGAL_ELEMENT_CHILD = 50
    ILLEGAL_TEXT_CHILD_PARSE = 51
    UNDEFINED_PREFIX = 52
    MISSING_REQUIRED_ATTRIBUTE = 70
    ILLEGAL_NULL_NAMESPACE_ATTR = 71
    ILLEGAL_XSL_NAMESPACE_ATTR = 72
    INVALID_ATTR_CHOICE = 73
    INVALID_CHAR_ATTR = 74
    INVALID_NUMBER_ATTR = 75
    INVALID_NS_URIREF_ATTR = 76
    INVALID_ID_ATTR = 77
    INVALID_QNAME_ATTR = 78
    INVALID_NCNAME_ATTR = 79
    INVALID_PREFIX_ATTR = 80
    INVALID_NMTOKEN_ATTR = 81
    QNAME_BUT_NOT_NCNAME = 82
    AVT_SYNTAX = 83
    AVT_EMPTY = 84
    INVALID_AVT = 85
    INVALID_PATTERN = 86
    INVALID_EXPRESSION = 87
    APPLYIMPORTS_WITH_NULL_CURRENT_TEMPLATE = 100
    ILLEGAL_IMPORT = 110
    INCLUDE_NOT_FOUND = 112
    CIRCULAR_INCLUDE = 113
    ILLEGAL_CHOOSE_CHILD = 120
    CHOOSE_REQUIRES_WHEN = 121
    NAMED_TEMPLATE_NOT_FOUND = 131
    MULTIPLE_MATCH_TEMPLATES = 141
    DUPLICATE_NAMED_TEMPLATE = 142
    ATTRIBUTE_ADDED_TOO_LATE = 150
    ATTRIBUTE_ADDED_TO_NON_ELEMENT = 152
    NONTEXT_IN_ATTRIBUTE = 153
    BAD_ATTRIBUTE_NAME = 154
    UNDEFINED_ATTRIBUTE_SET = 160
    INVALID_FOREACH_SELECT = 170
    ILLEGAL_TEXT_CHILD = 200
    ILLEGAL_APPLYTEMPLATE_NODESET = 212
    CIRCULAR_ATTRIBUTE_SET = 222
    ILLEGAL_SHADOWING = 232
    VAR_WITH_CONTENT_AND_SELECT = 233
    STYLESHEET_REQUESTED_TERMINATION = 241
    ILLEGAL_XML_PI = 250
    NONTEXT_IN_PI = 251
    UNKNOWN_OUTPUT_METHOD = 260
    DUPLICATE_DECIMAL_FORMAT = 270
    UNDEFINED_DECIMAL_FORMAT = 271
    ILLEGAL_NUMBER_FORMAT_VALUE = 293
    UNSUPPORTED_NUMBER_LANG_VALUE = 294
    UNSUPPORTED_NUMBER_LETTER_FOR_LANG = 295
    NONTEXT_IN_COMMENT = 310
    FWD_COMPAT_WITHOUT_FALLBACK = 320
    UNKNOWN_EXTENSION_ELEMENT = 321
    DOC_FUNC_EMPTY_NODESET = 1000
    UNKNOWN_NODE_BASE_URI = 1001
    WRONG_ARGUMENT_TYPE = 2001
    INVALID_QNAME_ARGUMENT = 2002
    RESTRICTED_OUTPUT_VIOLATION = 7000


g_errorMessages = {Error.NO_STYLESHEET: _('No stylesheets to process.'), Error.LITERAL_RESULT_MISSING_VERSION: _('Document root element must have a xsl:version attribute.  (see XSLT 1.0 sec. 2.3).'), Error.STYLESHEET_PARSE_ERROR: _('Error parsing stylesheet (%s): %s'), Error.SOURCE_PARSE_ERROR: _('Error parsing source document (%s): %s'), Error.XSLT_ILLEGAL_ELEMENT: _("Illegal element '%s' in XSLT Namespace (see XSLT 1.0 sec. 2.1)."), Error.CIRCULAR_VAR: _('Circular variable reference error (see XSLT 1.0 sec. 11.4) for variable or parameter: (%s, %s)'), Error.DUPLICATE_TOP_LEVEL_VAR: _('Top level variable %s has duplicate definitions with the same import precedence.  (see XSLT 1.0 sec. 11)'), Error.DUPLICATE_NAMESPACE_ALIAS: _('The namespace for "%s" has duplicate namespace aliases defined with the same import precedence.  (see XSLT 1.0 sec. 2.6.2)'), Error.ILLEGAL_ELEMENT_CHILD: _("Illegal child '%s' within element '%s'"), Error.ILLEGAL_TEXT_CHILD_PARSE: _("Illegal literal text %s within element '%s'"), Error.UNDEFINED_PREFIX: _("Undefined namespace prefix '%s'"), Error.MISSING_REQUIRED_ATTRIBUTE: _("Element '%s' missing required attribute '%s'"), Error.ILLEGAL_NULL_NAMESPACE_ATTR: _("Illegal null-namespace attribute '%s' on element '%s'."), Error.ILLEGAL_XSL_NAMESPACE_ATTR: _("Illegal xsl-namespace attribute '%s' on element '%s'."), Error.INVALID_ATTR_CHOICE: _("Illegal attribute value '%s', must be one of '%s'"), Error.INVALID_CHAR_ATTR: _("Invalid char attribute value '%s'"), Error.INVALID_NUMBER_ATTR: _("Invalid number attribute value '%s'"), Error.INVALID_NS_URIREF_ATTR: _("'%s' is not a valid namespace name (see Namespaces in XML erratum NE05)"), Error.INVALID_ID_ATTR: _("Invalid ID attribute value '%s'"), Error.INVALID_QNAME_ATTR: _("Invalid QName attribute value '%s'"), Error.INVALID_NCNAME_ATTR: _("Invalid NCName attribute value '%s'"), Error.INVALID_PREFIX_ATTR: _("Invalid prefix attribute value '%s'"), Error.INVALID_NMTOKEN_ATTR: _("Invalid NMTOKEN attribute value '%s'"), Error.QNAME_BUT_NOT_NCNAME: _("QName allowed but not NCName, '%s' found"), Error.AVT_SYNTAX: _('Unbalanced curly braces ({}) in attribute value template. (see XSLT 1.0 sec. 7.6.2)'), Error.AVT_EMPTY: _('No expression in attribute value template.'), Error.INVALID_AVT: _('Malformed attribute value template: "%s" in the element at %s, line %s, column %s\n  %s'), Error.INVALID_PATTERN: _('Malformed pattern: "%s" in the element at %s, line %s, column %s\n  %s'), Error.INVALID_EXPRESSION: _('Malformed expression: "%s" in the element at %s, line %s, column %s\n  %s'), Error.APPLYIMPORTS_WITH_NULL_CURRENT_TEMPLATE: _('apply-imports used where there is no current template.  (see XSLT Spec)'), Error.ILLEGAL_IMPORT: _('xsl:import is not allowed here (xsl:import must be at top level and precede all other XSLT top-level instructions).  (see XSLT 1.0 sec. 2.6.2)'), Error.INCLUDE_NOT_FOUND: _('Unable to open imported or included stylesheet "%s", using base URI "%s", or all base URIs in the include PATH'), Error.CIRCULAR_INCLUDE: _('Stylesheet %s may not be included or imported more than once (see XSLT 1.0 sec. 2.6)'), Error.ILLEGAL_CHOOSE_CHILD: _('FIXME'), Error.CHOOSE_REQUIRES_WHEN: _('"choose" must have at least one "when" child (see XSLT 1.0 sec. 9.2)'), Error.NAMED_TEMPLATE_NOT_FOUND: _('Named template "%s" invoked but not defined.'), Error.MULTIPLE_MATCH_TEMPLATES: _('Multiple templates matching node %r.  (see XSLT 1.0 sec. 5.5).\nConflicting template locations:\n%s'), Error.DUPLICATE_NAMED_TEMPLATE: _("Named template '%s' already defined with same import precedence"), Error.ATTRIBUTE_ADDED_TOO_LATE: _('Children were added to element before xsl:attribute instantiation. (see XSLT 1.0 sec. 7.1.3)'), Error.ATTRIBUTE_ADDED_TO_NON_ELEMENT: _('xsl:attribute attempted to add attribute to non-element. (see XSLT 1.0 sec. 7.1.3)'), Error.NONTEXT_IN_ATTRIBUTE: _('Nodes other than text nodes created during xsl:attribute instantiation. (see XSLT 1.0 sec. 7.1.3)'), Error.BAD_ATTRIBUTE_NAME: _('An attribute cannot be created with name %s. (see XSLT 1.0 sec. 7.1.3)'), Error.UNDEFINED_ATTRIBUTE_SET: _('Undefined attribute set (%s)'), Error.INVALID_FOREACH_SELECT: _('"select" attribute of "for-each" must evaluate to a node set (see XSLT 1.0 sec. 8)'), Error.ILLEGAL_TEXT_CHILD: _('xsl:text cannot have any child elements" (see XSLT 1.0 sec. 7.2)'), Error.ILLEGAL_APPLYTEMPLATE_NODESET: _('apply-templates must apply to a node-set.'), Error.CIRCULAR_ATTRIBUTE_SET: _("Circular attribute-set error for '%s'. (see XSLT 1.0 sec. 7.1.4)"), Error.ILLEGAL_SHADOWING: _('Illegal shadowing of %s.  An xsl:param or xsl:variable may not shadow another variable not at top level (see XSLT 1.0 sec. 11).'), Error.VAR_WITH_CONTENT_AND_SELECT: _('Illegal binding of of %s.  An xsl:param or xsl:variable may not have both a select attribute and non-empty content. (see XSLT 1.0 sec. 11.2).'), Error.STYLESHEET_REQUESTED_TERMINATION: _('A message instruction in the Stylesheet requested termination of processing:\n%s'), Error.ILLEGAL_XML_PI: _('A processing instruction cannot be used to output an XML or text declaration. (see XSLT 1.0 sec. 7.3)'), Error.NONTEXT_IN_PI: _('Nodes other than text nodes created during xsl:processing-instruction instantiation. (see XSLT 1.0 sec. 7.4)'), Error.UNKNOWN_OUTPUT_METHOD: _('Unknown output method (%s)'), Error.DUPLICATE_DECIMAL_FORMAT: _('Duplicate declaration of decimal-format %s. (XSLT Spec: 12.3)'), Error.UNDEFINED_DECIMAL_FORMAT: _('Undefined decimal-format (%s)'), Error.ILLEGAL_NUMBER_FORMAT_VALUE: _('Value "%s" for "format" attribute of xsl:number is invalid. (see XSLT 1.0 sec. 7.7)'), Error.UNSUPPORTED_NUMBER_LANG_VALUE: _('Language "%s" for alphabetic numbering in xsl:number is unsupported.'), Error.UNSUPPORTED_NUMBER_LETTER_FOR_LANG: _('Value "%s" for "letter-value" attribute of xsl:number is not supported with the language "%s".'), Error.NONTEXT_IN_COMMENT: _('Nodes other than text nodes created during xsl:comment instantiation. (see XSLT 1.0 sec. 7.4)'), Error.FWD_COMPAT_WITHOUT_FALLBACK: _('No xsl:fallback instruction found for element %r processed in forward-compatible mode.'), Error.UNKNOWN_EXTENSION_ELEMENT: _('No implementation for extension element %r, %r'), Error.DOC_FUNC_EMPTY_NODESET: _('Second argument to document(), if given, must be a non-empty node-set. (see XSLT 1.0 sec. 12.1 erratum E14)'), Error.UNKNOWN_NODE_BASE_URI: _('Could not determine base URI of node: %s'), Error.WRONG_ARGUMENT_TYPE: _('A built-in or extension function was called with the wrong type of argument(s).'), Error.INVALID_QNAME_ARGUMENT: _('A built-in or extension function requiring a QName argument was called with this non-QName value: "%s".'), Error.RESTRICTED_OUTPUT_VIOLATION: _('The requested output of element "%s" is forbidden according to output restrictions')}