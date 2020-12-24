# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/examples/sqla-hybrid_property/app.py
# Compiled at: 2016-06-26 14:14:34
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.filters import IntGreaterFilter
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_db_2.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Screen(db.Model):
    __tablename__ = 'screen'
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    @hybrid_property
    def number_of_pixels(self):
        return self.width * self.height


class ScreenAdmin(sqla.ModelView):
    """ Flask-admin can not automatically find a hybrid_property yet. You will
        need to manually define the column in list_view/filters/sorting/etc."""
    list_columns = [
     'id', 'width', 'height', 'number_of_pixels']
    column_sortable_list = ['id', 'width', 'height', 'number_of_pixels']
    column_filters = [
     IntGreaterFilter(Screen.number_of_pixels, 'Number of Pixels')]


admin = admin.Admin(app, name='Example: SQLAlchemy2', template_mode='bootstrap3')
admin.add_view(ScreenAdmin(Screen, db.session))
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)