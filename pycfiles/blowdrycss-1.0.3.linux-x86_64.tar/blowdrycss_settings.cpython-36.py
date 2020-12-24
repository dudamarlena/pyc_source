# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/blowdrycss_settings.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 10925 bytes
"""
**Usage Notes:**

The first time ``blowdrycss`` is run it auto-builds ``blowdrycss_settings.py`` via ``__init__.py``.
This makes it easy to find and customize related settings.

**Why such a long name? -- blowdrycss_settings.py**

Popular web frameworks such as django and flask already auto-generate a settings file called ``settings.py``.
The longer more specific name is used to prevent naming conflicts, and increase clarity.

**Parameters:**

| markdown_directory (*string*) -- Generally used for development purposes and github documentation.

| project_directory (*string*) -- Path to recursively search for all defined ``file_types``.

| css_directory (*string*) -- Path where the projects CSS files are located.

| docs_directory (*string*) -- Path where Sphinx docs are located (requires sphinx to be installed and run).

| output_file_name (*string*) -- Name of the generated output file contain DRY CSS definitions.

| output_extension (*string*) -- File extension of the generated output file. Must begin with '.'

| file_types = (*tuple of strings*) -- All file types/extensions to search for in the defined project_directory
  that contain encoded class selectors.

  *Example format:* ::

    ('*.html', )

| timing_enabled (*bool*) -- Run performance timer to see the performance of ``blowdrycss``.

| markdown_docs (*bool*) -- Generate a markdown files that provides a quick syntax and clashing alias reference.
  Normally set to False except when posting to github.

| html_docs (*bool*) -- Generate a html file that provides a quick syntax and clashing alias reference.

| rst_docs (*bool*) -- Generate a sphinx rst file that provides a quick syntax and clashing alias reference.

| human_readable (*bool*) -- Generate a standard human readable css file. This file is named ``blowdry.css`` by
  default.

| minify (*bool*) -- Generate a minified version of the css file. This file is named ``blowdry.min.css`` by default.

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

**Custom Alias Syntax:**

| custom_property_alias_dict (*dict*) -- Contains customized shorthand encodings for a CSS property name.
  e.g. ``'c-'`` is an alias for ``'color'``. This saves on typing.

| These encoded class selectors can be used inside of Web project files matching ``file_type``.
  They can be customized to your liking.

| For more details about how to create custom aliases head on over to :doc:`advancedtopics`.

**cssutils Patch:**

``cssutils`` does not currently support all CSS 3 Units.  The patch in this file allows length units of
``q``, ``ch``, ``rem``, ``vw``, ``vh``, ``vmin``, and ``vmax``. It also allows angle units of ``turn``.

"""
from __future__ import absolute_import, division, unicode_literals
from builtins import round
from os import chdir, getcwd, path
from string import digits
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from cssutils import profile
__author__ = 'chad nelson'
__project__ = 'blowdrycss'
original_directory = getcwd()
chg = path.join('..')
chdir(chg)
cwd = getcwd()
markdown_directory = cwd
project_directory = path.join(cwd, 'examplesite')
css_directory = path.join(project_directory, 'css')
docs_directory = path.join(cwd, 'docs')
chdir(original_directory)
output_file_name = 'blowdry'
output_extension = '.css'
logging_enabled = True
logging_level = INFO
log_to_console = False
log_to_file = True
log_directory = path.join(cwd, 'log')
log_file_name = 'blowdrycss.log'
one_mega_byte = 1048576
log_file_size = 4 * one_mega_byte
log_backup_count = 1
file_types = ('*.html', )
time_limit = 1800
auto_generate = True
hide_css_errors = True
timing_enabled = True
markdown_docs = False
html_docs = True
rst_docs = False
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

    >>> from blowdrycss_settings import px_to_em
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