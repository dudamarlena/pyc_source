# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/templatetags/bee_django_course_simple_filter.py
# Compiled at: 2019-11-06 03:10:54
__author__ = 'zhangyue'
from django import template
from bee_django_course_simple.models import UserQuestion, Question
register = template.Library()

@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


@register.simple_tag
def get_user_answer_option_id(user, question_id):
    option = get_user_answer_option(user, question_id)
    if option:
        return option.id
    else:
        return
        return


@register.simple_tag
def get_user_answer_option(user, question_id):
    question = Question.objects.get(id=question_id)
    try:
        user_question = UserQuestion.objects.get(question=question, user_part__user_section__user_course__user=user)
        answer_option = user_question.answer_option
        return answer_option
    except:
        return

    return