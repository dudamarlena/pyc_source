# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\tests\test_data_gen.py
# Compiled at: 2012-02-06 09:37:57
import random
__all__ = ['Person']
names = [
 ('Mary', 'F'), ('Marsha', 'F'), ('Max', 'M'),
 ('Joe', 'M'), ('John', 'M'), ('Jacob', 'M'),
 ('Bob', 'M'), ('Billy', 'M'), ('Bobby', 'M'),
 ('Zaphod', 'M'), ('Zack', 'M'), ('Zackary', 'M'),
 ('Trillian', 'F'), ('Tristan', 'F'), ('Trinity', 'F'),
 ('Ford', 'M'), ('Jim', 'M'), ('Jimmy', 'M'),
 ('Arthor', 'M'), ('Andy', 'M'), ('Anna', 'F'),
 ('Jax', 'M'), ('Jason', 'M'), ('Johnathan', 'M'),
 ('Marvin', 'M'), ('Michael', 'M'), ('Mike', 'M'),
 ('Lucy', 'F'), ('Linda', 'F'), ('Lisa', 'F')]

class Person(object):
    """docstring for Person"""

    def __init__(self):
        self.id = int(random.randint(0, len(names) - 1))
        self.name = names[self.id][0]
        self.gender = names[self.id][1]
        self.age = int(random.randint(18, 70))
        self.college = int(random.randint(0, 5))
        self.friends = int(random.randint(1, 500))

    def name(self):
        return self.name

    def gender(self):
        return self.gender

    def age(self):
        return self.age

    def college(self):
        return self.college

    def friends(self):
        return self.friends


if __name__ == '__main__':
    people = [ Person() for a in range(250) ]
    previous = Person()
    for p in people:
        if p.name == previous.name:
            p = Person()
        s = (',').join(str(a) for a in [p.name, p.gender, p.age, p.college, p.friends]) + '\n'
        print p.__dict__
        previous = p

    print 'Done.'