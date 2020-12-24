# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ctstore/init.py
# Compiled at: 2016-08-10 16:47:18
import os
jss = os.path.join('js', 'store')
dirs = [
 jss]
copies = {'.': [
       'model.py'], 
   'css': [
         'custom.css'], 
   'html': [
          'index.html']}
copies[jss] = [
 'config.js', 'data.js']
syms = {'js': [
        'store.js'], 
   'css': [
         'store.css', 'layouts'], 
   'html': [
          'results.html', 'checkout.html']}
syms[jss] = [
 'core.js', 'core', 'pages']
requires = [
 'ctuser']