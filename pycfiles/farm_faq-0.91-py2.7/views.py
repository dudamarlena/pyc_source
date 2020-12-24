# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/views.py
# Compiled at: 2014-03-27 06:14:42
from django.shortcuts import render
from .models import Category, Question

def index(request):
    """
    This displays the FAQ page.
    """
    categories = Category.objects.all()
    questions = Question.objects.filter(active=True)
    return render(request, 'faq/index.html', {'categories': categories, 'questions': questions})