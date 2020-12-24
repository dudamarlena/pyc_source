# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/model.py
# Compiled at: 2013-04-11 17:47:52
import time, datetime
from camelot.core.orm import Entity
from camelot.admin.entity_admin import EntityAdmin
from sqlalchemy import sql
from sqlalchemy.schema import Column
import sqlalchemy.types, camelot.types
from camelot.core.sql import metadata
from camelot.core.orm import Entity, Field, ManyToOne, OneToMany, ManyToMany, using_options, ColumnProperty
from camelot.admin.action import Action
from camelot.admin.entity_admin import EntityAdmin
from camelot.core.utils import ugettext_lazy as _
from camelot.model.party import Person
from camelot.view import action_steps
from camelot.view.forms import Form, TabForm, WidgetOnlyForm, HBoxForm, Stretch
from camelot.view.controls import delegates
from camelot.view.filters import ComboBoxFilter
from camelot.view.art import ColorScheme
from sqlalchemy.types import Unicode, Date, Integer
from camelot_example.change_rating import ChangeRatingAction
from camelot_example.drag_and_drop import DropAction

def genre_choices(entity_instance):
    """Choices for the possible movie genres"""
    return [
     (None, ''),
     ('action', 'Action'),
     ('animation', 'Animation'),
     ('comedy', 'Comedy'),
     ('drama', 'Drama'),
     ('sci-fi', 'Sci-Fi'),
     ('war', 'War'),
     ('thriller', 'Thriller'),
     ('family', 'Family')]


class BurnToDisk(Action):
    verbose_name = _('Burn to disk')

    def model_run(self, model_context):
        yield action_steps.UpdateProgress(0, 3, _('Formatting disk'))
        time.sleep(0.7)
        yield action_steps.UpdateProgress(1, 3, _('Burning movie'))
        time.sleep(0.7)
        yield action_steps.UpdateProgress(2, 3, _('Finishing'))
        time.sleep(0.5)

    def get_state(self, model_context):
        """Turn the burn to disk button on, only if the title of the
        movie is entered"""
        state = super(BurnToDisk, self).get_state(model_context)
        obj = model_context.get_object()
        if obj and obj.title:
            state.enabled = True
        else:
            state.enabled = False
        return state


class Movie(Entity):
    __tablename__ = 'movies'
    title = Column(sqlalchemy.types.Unicode(60), nullable=False)
    short_description = Column(sqlalchemy.types.Unicode(512))
    releasedate = Column(sqlalchemy.types.Date)
    genre = Column(sqlalchemy.types.Unicode(15))
    rating = Column(camelot.types.Rating())
    director = ManyToOne('Person')
    cast = OneToMany('Cast')
    visitor_reports = OneToMany('VisitorReport', cascade='delete')
    tags = ManyToMany('Tag', tablename='tags_movies__movies_tags', local_colname='tags_id', remote_colname='movies_id')
    cover = Column(camelot.types.Image(upload_to='covers'))
    script = Column(camelot.types.File(upload_to='script'))
    description = Column(camelot.types.RichText)

    @property
    def visitors_chart(self):
        from camelot.container.chartcontainer import BarContainer
        return BarContainer(range(len(self.visitor_reports)), [ vr.visitors for vr in self.visitor_reports ])

    @ColumnProperty
    def total_visitors(self):
        return sql.select([sql.func.sum(VisitorReport.visitors)], VisitorReport.movie_id == self.id)

    bar = 3

    class Admin(EntityAdmin):
        list_display = [
         'cover', 'title', 'releasedate', 'rating']
        lines_per_row = 5
        list_filter = [
         'genre', ComboBoxFilter('director.full_name')]
        list_search = [
         'director.full_name']
        list_actions = [
         ChangeRatingAction()]
        drop_action = DropAction()
        form_display = TabForm([
         (
          'Movie',
          Form([
           HBoxForm([WidgetOnlyForm('cover'), ['title', 'rating', Stretch()]]),
           'short_description',
           'releasedate',
           'director',
           'script',
           'genre',
           'description'], columns=2)),
         (
          'Cast', WidgetOnlyForm('cast')),
         (
          'Visitors', WidgetOnlyForm('visitors_chart')),
         (
          'Tags', WidgetOnlyForm('tags'))])
        form_actions = [
         BurnToDisk()]
        field_attributes = dict(cast=dict(create_inline=True), genre=dict(choices=genre_choices, editable=lambda o: bool(o.title and len(o.title))), releasedate=dict(background_color=lambda o: ColorScheme.orange_1 if o.releasedate and o.releasedate < datetime.date(1920, 1, 1) else None), visitors_chart=dict(delegate=delegates.ChartDelegate), rating=dict(tooltip='<table>\n                                                          <tr><td>1 star</td><td>Not that good</td></tr>\n                                                          <tr><td>2 stars</td><td>Almost good</td></tr>\n                                                          <tr><td>3 stars</td><td>Good</td></tr>\n                                                          <tr><td>4 stars</td><td>Very good</td></tr>\n                                                          <tr><td>5 stars</td><td>Awesome !</td></tr>\n                                                       </table>'), smiley=dict(delegate=delegates.SmileyDelegate), script=dict(remove_original=True))

    def __unicode__(self):
        return self.title or ''


class Cast(Entity):
    __tablename__ = 'cast'
    role = Column(sqlalchemy.types.Unicode(60))
    movie = ManyToOne('Movie', required=True, backref='cast')
    actor = ManyToOne(Person, required=True)

    class Admin(EntityAdmin):
        verbose_name = 'Actor'
        list_display = ['actor', 'role']

    def __unicode__(self):
        if self.actor:
            return self.actor.name
        return ''


class Tag(Entity):
    __tablename__ = 'tags'
    name = Column(sqlalchemy.types.Unicode(60), nullable=False)
    movies = ManyToMany('Movie', tablename='tags_movies__movies_tags', local_colname='movies_id', remote_colname='tags_id')

    def __unicode__(self):
        return self.name

    class Admin(EntityAdmin):
        form_size = (400, 200)
        list_display = ['name']


class VisitorReport(Entity):
    __tablename__ = 'visitor_report'
    date = Column(sqlalchemy.types.Date, nullable=False, default=datetime.date.today)
    visitors = Column(sqlalchemy.types.Integer, nullable=False, default=0)
    movie = ManyToOne('Movie', required=True)

    class Admin(EntityAdmin):
        verbose_name = _('Visitor Report')
        list_display = ['movie', 'date', 'visitors']
        field_attributes = {'visitors': {'minimum': 0}}