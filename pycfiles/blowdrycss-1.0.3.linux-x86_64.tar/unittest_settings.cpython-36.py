# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/unittest_settings.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 9704 bytes
"""
**Parameters:**

| markdown_directory (*string*) -- Generally used for development purposes only.

| project_directory (*string) -- Path to your project directory

| css_directory (*string*) -- Path to your projects CSS directory

| docs_directory (*string*) -- Path to Sphinx docs.

| file_types = (*tuple of strings*) -- All file types/extensions to search for in the defined project_directory
  that contain encoded class selectors.

| timing_enabled (*bool*) -- Run performance timer

| markdown_docs (*bool*) -- Generate a markdown files that provides a quick syntax and clashing alias reference.

| html_docs (*bool*) -- Generate a html file that provides a quick syntax and clashing alias reference.

| rst_docs (*bool*) -- Generate a sphinx rst file that provides a quick syntax and clashing alias reference.

| human_readable (*bool*) -- Generate a standard human readable css file.

| minify (*bool*) -- Generate a minified version of the css file.

| media_queries_enabled (*bool*) -- Generate breakpoint and scaling media queries.

| use_em (*bool*) -- A ``pixels`` to ``em`` unit conversion flag. True enables unit conversion.
  False disables unit conversions meaning any pixel value remains unchanged.

| base (*int*) -- Base used for unit conversion (typically set to 16). The pixel value will be divided by
  ``base`` during unit conversion.

| xxsmall (*tuple of floats*) -- (0px, upper limit in pixels)

| xsmall (*tuple of floats*) -- (xxsmall upper limit + 1px, upper limit in pixels)

| small (*tuple of floats*) -- (xsmall upper limit + 1px, upper limit in pixels)

| medium (*tuple of floats*) -- (small upper limit + 1px, upper limit in pixels)

| large (*tuple of floats*) -- (medium upper limit + 1px, upper limit in pixels)

| xlarge (*tuple of floats*) -- (large upper limit + 1px, upper limit in pixels)

| xxlarge (*tuple of floats*) -- (xlarge upper limit + 1px, upper limit in pixels)

| giant (*tuple of floats*) -- (xxlarge upper limit + 1px, upper limit in pixels)

| xgiant (*tuple of floats*) -- (giant upper limit + 1px, upper limit in pixels)

| xxgiant (*tuple of floats*) -- (xgiant upper limit + 1px, 1E+6) [Technically the upper limit is infinity,
  but CSS does not permit it.]

**cssutils Patch:**

``cssutils`` does not currently support CSS 3 Units.  The patch in this file allows length units of
``q``, ``ch``, ``rem``, ``vw``, ``vh``, ``vmin``, and ``vmax``. It also allows angle units of ``turn``.

"""
from __future__ import absolute_import, division, unicode_literals
from builtins import round
from os import getcwd, path
from string import digits
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from cssutils import profile
__project__ = 'blowdrycss'
cwd = getcwd()
if cwd.endswith('unit_tests'):
    markdown_directory = path.join(cwd, 'test_markdown')
    project_directory = path.join(cwd, 'test_examplesite')
    css_directory = path.join(project_directory, 'test_css')
    docs_directory = path.join(cwd, 'test_docs')
else:
    markdown_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_markdown')
    project_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_examplesite')
    css_directory = path.join(project_directory, 'test_css')
    docs_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_docs')
logging_enabled = False
logging_level = DEBUG
log_to_console = True
log_to_file = True
log_directory = path.join(cwd, 'log')
log_file_name = 'blowdrycss.log'
one_mega_byte = 1048576
log_file_size = 4 * one_mega_byte
log_backup_count = 1
file_types = ('*.html', )
timing_enabled = True
markdown_docs = True
html_docs = True
rst_docs = True
human_readable = True
minify = True
media_queries_enabled = True
use_em = True
base = 16

def px_to_em(pixels):
    """ Convert a numeric value from px to em using ``settings.base`` as the unit conversion factor.

    **Rules:**

    - ``pixels`` shall only contain [0-9.-].
    - Inputs that contain any other value are simply passed through unchanged.
    - Default ``base`` is 16 meaning ``16px = 1rem``

    **Note:** Does not check the ``property_name`` or ``use_em`` values.  Rather, it blindly converts
    whatever input is provided.  The calling method is expected to know what it is doing.

    Rounds float to a maximum of 4 decimal places.

    :type pixels: str, int, float
    :param pixels: A numeric value with the units stripped.
    :return: (str)

        - If the input is convertible return the converted number as a string with the units ``em``
          appended to the end.
        - If the input is not convertible return the unprocessed input.

    >>> from settings.blowdrycss_settings import px_to_em
    >>> # settings.use_em = True
    >>> px_to_em(pixels='-16.0')
    -1em
    >>> # settings.use_em = False
    >>> px_to_em(pixels='42px')
    42px
    >>> # Invalid input passes through.
    >>> px_to_em(pixels='invalid')
    invalid

    """
    if set(str(pixels)) <= set(digits + '-.'):
        em = float(pixels) / float(base)
        em = round(em, 4)
        em = str(em) + 'em'
        return em
    else:
        return pixels


xxsmall = (
 px_to_em(0), px_to_em(120))
xsmall = (px_to_em(121), px_to_em(240))
small = (px_to_em(241), px_to_em(480))
medium = (px_to_em(481), px_to_em(720))
large = (px_to_em(721), px_to_em(1024))
xlarge = (px_to_em(1025), px_to_em(1366))
xxlarge = (px_to_em(1367), px_to_em(1920))
giant = (px_to_em(1921), px_to_em(2560))
xgiant = (px_to_em(2561), px_to_em(2800))
xxgiant = (px_to_em(2801), px_to_em(1000000))
custom_property_alias_dict = {'background':{
  'bg-'}, 
 'background-color':{
  'bgc-', 'bg-c-', 'bg-color-'}, 
 'color':{
  'c-'}, 
 'font-size':{
  'fsize-', 'f-size-'}, 
 'font-weight':{
  'fweight-', 'f-weight-'}, 
 'height':{
  'h-'}, 
 'margin':{
  'm-'}, 
 'margin-top':{
  'm-top-'}, 
 'margin-bottom':{
  'm-bot-'}, 
 'padding':{
  'p-', 'pad-'}, 
 'padding-top':{
  'p-top-'}, 
 'position':{
  'pos-'}, 
 'text-align':{
  'talign-', 't-align-'}, 
 'vertical-align':{
  'valign-', 'v-align-'}, 
 'width':{
  'w-'}}
profile._MACROS['length'] = '0|{num}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['positivelength'] = '0|{positivenum}(em|ex|px|in|cm|mm|pt|pc|q|ch|rem|vw|vh|vmin|vmax)'
profile._MACROS['angle'] = '0|{num}(deg|grad|rad|turn)'
profile._resetProperties()