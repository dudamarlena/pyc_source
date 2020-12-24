# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/examples/sqla/app2.py
# Compiled at: 2016-06-26 14:14:34
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))

    def __unicode__(self):
        return self.desc


class Tyre(db.Model):
    __tablename__ = 'tyres'
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), primary_key=True)
    tyre_id = db.Column(db.Integer, primary_key=True)
    car = db.relationship('Car', backref='tyres')
    desc = db.Column(db.String(50))


class CarAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'desc']


class TyreAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['car', 'tyre_id', 'desc']


admin = admin.Admin(app, name='Example: SQLAlchemy2', template_mode='bootstrap3')
admin.add_view(CarAdmin(Car, db.session))
admin.add_view(TyreAdmin(Tyre, db.session))
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)