# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gaufung/WorkSpace/SimpleWebFramework/example/urls.py
# Compiled at: 2017-09-21 07:47:57
import random
from tindo import view, ctx, route
from tindo import redirect

@view('index.html')
@route('/')
def index():
    session = ctx.response.session
    session.number = random.randint(1, 100)
    session.times = 2
    return dict()


@view('register.html')
@route('/register', methods=['GET', 'POST'])
def register():
    i = ctx.request.input(firstname=None, lastname=None)
    firstname = i.get('firstname')
    lastname = i.get('lastname')
    if firstname is None and lastname is None:
        return dict(register=True)
    else:
        return dict(firstname=firstname, lastname=lastname)
        return


@view('name.html')
@route('/user/<username>')
def user(name):
    return dict(name=name)


@view('comment.html')
@route('/user/<name>/<group>')
def comment(name, group):
    return dict(name=name, group=group)


@view('session.html')
@route('/session')
def session():
    sess = ctx.response.session
    return dict(name=sess.name)


@view('game.html')
@route('/game', methods=['GET', 'POST'])
def game():
    i = ctx.request.input(number=None)
    times = ctx.response.session.times
    number = ctx.response.session.number
    guess_number = i.get('number')
    if guess_number is not None:
        try:
            guess_number = int(guess_number)
        except ValueError as e:
            return dict(status='Invalid guess')

        if times:
            times -= 1
            ctx.response.session.times = times
            guess_number = int(guess_number)
            if guess_number > number:
                return dict(success=False, status='Too Big', times=times)
            if guess_number < number:
                return dict(success=False, status='Too Small', times=times)
            return dict(success=True)
        else:
            redirect('/')
    else:
        return dict(times=times, status='')
    return