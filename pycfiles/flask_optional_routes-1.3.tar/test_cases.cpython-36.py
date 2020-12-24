# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuvok/Desktop/projects/packages/flask_optional_routes/flask_optional_routes/tests/test_cases.py
# Compiled at: 2018-03-04 11:08:14
# Size of source mod 2**32: 493 bytes
TEST_CASES = [
 (
  '/',
  {
   '/'}),
 (
  '/a',
  {
   '/a'}),
 (
  '/a/',
  {
   '/a/'}),
 (
  '/a?',
  {
   '', '/a'}),
 (
  '/a?/',
  {
   '/', '/a/'}),
 (
  '/a/b/c/d',
  {
   '/a/b/c/d'}),
 (
  '/a/b?/c/d?',
  {
   '/a/c', '/a/b/c', '/a/c/d', '/a/b/c/d'}),
 (
  '/a/b?/c/d?/',
  {
   '/a/c/', '/a/b/c/', '/a/c/d/', '/a/b/c/d/'})]