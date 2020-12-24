# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/rating/widgets.py
# Compiled at: 2008-06-02 11:18:03
from tw.api import Widget, JSLink, CSSLink, js_callback
from tw import jquery
__all__ = ['Rating']
rating_css = CSSLink(modname=__name__, filename='static/ratings.css')
rating_js = JSLink(modname=__name__, filename='static/jquery.rating.js', css=[
 rating_css], javascript=[
 jquery.packed])

class Rating(Widget):
    params = [
     'action', 'average_text', 'label_text', 'submit_text', 'on_click']
    css_class = 'rating'
    default = 0
    average_text = 'Average Rating:'
    label_text = 'Rate Me!'
    template = '<form class="${css_class}" title="${average_text} ${value}" \n      action="${action}" id="${id}">\n    <label for="${id}_select" class="avg">${label_text}</label>\n    <select id="${id}_select">\n        <option value="0">0</option>\n        <option value="1">1</option>\n        <option value="2">2</option>\n        <option value="3">3</option>\n        <option value="4">4</option>\n        <option value="5">5</option>\n    </select>\n    <input type="button" value="${submit_text}">\n</form>'
    javascript = [
     rating_js]
    include_dynamic_js_calls = True
    on_click = ''

    def update_params(self, d):
        super(Rating, self).update_params(d)
        self.add_call(jquery.function(js_callback(jquery.function('#' + d.id).rating())))