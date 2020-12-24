# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zhihu\url.py
# Compiled at: 2017-07-25 02:12:32
# Size of source mod 2**32: 3500 bytes
"""
通用ＵＲＬ类,知乎官方ＵＲＬ接口地址
"""
import time

class URL(object):
    host = 'https://www.zhihu.com'
    zhuanlan_host = 'https://zhuanlan.zhihu.com'

    @classmethod
    def email_login(cls):
        return cls.host + '/login/email'

    @classmethod
    def phone_login(cls):
        return cls.host + '/login/phone_num'

    @classmethod
    def message(cls):
        return cls.host + '/api/v4/messages'

    @classmethod
    def captcha(cls, _type='login'):
        return cls.host + '/captcha.gif?r={timestamp}&type={type}'.format(timestamp=(str(int(time.time() * 1000))), type=_type)

    @classmethod
    def index(cls):
        return cls.host + ''

    @classmethod
    def profile(cls, user_slug):
        return cls.host + '/api/v4/members/{user_slug}'.format(user_slug=user_slug)

    @classmethod
    def follow_people(cls, user_slug):
        return cls.host + '/api/v4/members/{user_slug}/followers'.format(user_slug=user_slug)

    @classmethod
    def vote_up(cls, answer_id):
        return cls.host + '/api/v4/answers/{id}/voters'.format(id=answer_id)

    vote_down = vote_neutral = vote_up

    @classmethod
    def thank(cls, answer_id):
        return cls.host + '/api/v4/answers/{id}/thankers'.format(id=answer_id)

    thank_cancel = thank

    @classmethod
    def nothelp(cls, answer_id):
        return cls.host + '/api/v4/answers/{id}/unhelpers'.format(id=answer_id)

    nothelp_cancel = nothelp

    @classmethod
    def follow_question(cls, question_id):
        return cls.host + '/api/v4/questions/{id}/followers'.format(id=question_id)

    unfollow_question = follow_question

    @classmethod
    def column(cls, slug):
        return 'https://zhuanlan.zhihu.com/api/columns/{slug}'.format(slug=slug)

    @classmethod
    def column_index(cls, slug):
        return cls.zhuanlan_host + '/{slug}'.format(slug=slug)

    @classmethod
    def column_followers(cls, slug):
        return cls.zhuanlan_host + '/api/columns/{slug}/followers'.format(slug=slug)

    @classmethod
    def follow_column(cls, slug):
        return cls.zhuanlan_host + '/api/columns/{slug}/follow'.format(slug=slug)

    unfollow_column = follow_column

    @classmethod
    def register_sms_code(cls):
        return cls.host + '/send_register_verification_code/sms'

    @classmethod
    def register_validate(cls):
        return cls.host + '/register/phone_num/validation'

    @classmethod
    def register(cls):
        return cls.host + '/register/phone_num'

    @classmethod
    def followers(cls, user_slug):
        return cls.host + '/api/v4/members/{slug}/followers?include=data[*].answer_count,gender,follower_count,badge[?(type=best_answerer)].topics'.format(slug=user_slug)