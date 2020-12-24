# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/plants/geography.py
# Compiled at: 2016-10-03 09:39:22
from operator import itemgetter
import gtk
from sqlalchemy import select, Column, Unicode, String, Integer, ForeignKey
from sqlalchemy.orm import object_session, relation, backref
import bauble.db as db

def get_species_in_geography(geo):
    """
    Return all the Species that have distribution in geo
    """
    session = object_session(geo)
    if not session:
        ValueError('get_species_in_geography(): geography is not in a session')
    from bauble.plugins.plants.species_model import SpeciesDistribution, Species
    geo_table = geo.__table__
    master_ids = set([geo.id])

    def get_geography_children(parent_id):
        stmt = select([geo_table.c.id], geo_table.c.parent_id == parent_id)
        kids = [ r[0] for r in db.engine.execute(stmt).fetchall() ]
        for kid in kids:
            grand_kids = get_geography_children(kid)
            master_ids.update(grand_kids)

        return kids

    geokids = get_geography_children(geo.id)
    master_ids.update(geokids)
    q = session.query(Species).join(SpeciesDistribution).filter(SpeciesDistribution.geography_id.in_(master_ids))
    return list(q)


class GeographyMenu(gtk.Menu):

    def __init__(self, callback):
        super(GeographyMenu, self).__init__()
        geography_table = Geography.__table__
        geos = select([geography_table.c.id, geography_table.c.name,
         geography_table.c.parent_id]).execute().fetchall()
        geos_hash = {}
        for geo_id, name, parent_id in geos:
            try:
                geos_hash[parent_id].append((geo_id, name))
            except KeyError:
                geos_hash[parent_id] = [
                 (
                  geo_id, name)]

        for kids in geos_hash.values():
            kids.sort(key=itemgetter(1))

        def get_kids(pid):
            try:
                return geos_hash[pid]
            except KeyError:
                return []

        def has_kids(pid):
            try:
                return len(geos_hash[pid]) > 0
            except KeyError:
                return False

        def build_menu(geo_id, name):
            item = gtk.MenuItem(name)
            if not has_kids(geo_id):
                if item.get_submenu() is None:
                    item.connect('activate', callback, geo_id)
                return item
            kids_added = False
            submenu = gtk.Menu()
            kids = get_kids(geo_id)
            if len(kids) > 0:
                kids_added = True
            for kid_id, kid_name in kids:
                submenu.append(build_menu(kid_id, kid_name))

            if kids_added:
                sel_item = gtk.MenuItem(name)
                submenu.insert(sel_item, 0)
                submenu.insert(gtk.SeparatorMenuItem(), 1)
                item.set_submenu(submenu)
                sel_item.connect('activate', callback, geo_id)
            else:
                item.connect('activate', callback, geo_id)
            return item

        def populate():
            """
            add geography value to the menu, any top level items that don't
            have any kids are appended to the bottom of the menu
            """
            if not geos_hash:
                return
            else:
                no_kids = []
                for geo_id, geo_name in geos_hash[None]:
                    if geo_id not in geos_hash.keys():
                        no_kids.append((geo_id, geo_name))
                    else:
                        self.append(build_menu(geo_id, geo_name))

                for geo_id, geo_name in sorted(no_kids):
                    self.append(build_menu(geo_id, geo_name))

                self.show_all()
                return

        import gobject
        gobject.idle_add(populate)


class Geography(db.Base):
    """
    Represents a geography unit.

    :Table name: geography

    :Columns:
        *name*:

        *tdwg_code*:

        *iso_code*:

        *parent_id*:

    :Properties:
        *children*:

    :Constraints:
    """
    __tablename__ = 'geography'
    name = Column(Unicode(255), nullable=False)
    tdwg_code = Column(String(6))
    iso_code = Column(String(7))
    parent_id = Column(Integer, ForeignKey('geography.id'))

    def __str__(self):
        return self.name


Geography.children = relation(Geography, primaryjoin=Geography.parent_id == Geography.id, cascade='all', backref=backref('parent', remote_side=[
 Geography.__table__.c.id]), order_by=[
 Geography.name])