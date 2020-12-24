# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/__main__.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 5165 bytes
import click, geopandas as gpd
from os import path
import osmnx as ox, numpy as np
from . import crossings, intersections, io, validators
from .opensidewalks import make_links
USEFUL_TAGS_PATH = [
 'access', 'area', 'bridge', 'est_width', 'highway',
 'landuse', 'lanes', 'oneway', 'maxspeed', 'name', 'ref',
 'service', 'tunnel', 'width', 'layer']
ox.utils.config(cache_folder=path.join(path.dirname(__file__), '../cache'), useful_tags_path=USEFUL_TAGS_PATH, use_cache=True)

@click.group()
def crossify():
    pass


@crossify.command()
@click.argument('sidewalks_in')
@click.argument('outfile')
def from_file(sidewalks_in, outfile):
    sidewalks = io.read_sidewalks(sidewalks_in)
    core(sidewalks, outfile)


@crossify.command()
@click.argument('west')
@click.argument('south')
@click.argument('east')
@click.argument('north')
@click.argument('outfile')
@click.option('--opensidewalks', is_flag=True)
def osm_bbox(west, south, east, north, outfile, opensidewalks):
    sidewalks = io.fetch_sidewalks(west, south, east, north)
    core(sidewalks, outfile, opensidewalks=opensidewalks)


def core(sidewalks, outfile, opensidewalks=False):
    click.echo('Fetching street network from OpenStreetMap...', nl=False)
    G_streets = io.fetch_street_graph(sidewalks)
    click.echo('Done')
    sidewalks_u = ox.projection.project_gdf(sidewalks)
    click.echo('Generating street graph...', nl=False)
    G_streets_u = ox.projection.project_graph(G_streets)
    for u, v, k, l in G_streets_u.edges(keys=True, data='layer', default=0):
        layer = validators.transform_layer(l)
        G_streets_u.edges[(u, v, k)]['layer'] = layer

    click.echo('Done')
    click.echo('Extracting geospatial data from street graph...', nl=False)
    G_undirected_u = ox.save_load.get_undirected(G_streets_u)
    streets = ox.save_load.graph_to_gdfs(G_undirected_u, nodes=False, edges=True)
    streets.crs = sidewalks_u.crs
    click.echo('Done')
    click.echo('Isolating street intersections...', nl=False)
    ixns = intersections.group_intersections(G_streets_u)
    click.echo('Done')
    click.echo('Drawing crossings...', nl=False)
    validators.standardize_layer(sidewalks_u)
    st_crossings = crossings.make_crossings(ixns, sidewalks_u)
    if st_crossings is None:
        click.echo('Failed to make any crossings!')
        return
    if 'layer' in sidewalks_u.columns:
        keep_cols = [
         'geometry', 'layer']
    else:
        keep_cols = [
         'geometry']
    st_crossings = gpd.GeoDataFrame(st_crossings[keep_cols])
    st_crossings.crs = sidewalks_u.crs
    click.echo('Done')
    st_crossings['highway'] = 'footway'
    st_crossings['footway'] = 'crossing'
    click.echo('Writing to file...', nl=False)
    if opensidewalks:
        st_crossings, sw_links = make_links(st_crossings, offset=1)
        st_crossings['layer'] = st_crossings['layer'].replace(0, np.nan)
        sw_links['layer'] = sw_links['layer'].replace(0, np.nan)
        base, ext = path.splitext(outfile)
        sw_links_outfile = '{}_links{}'.format(base, ext)
        io.write_sidewalk_links(sw_links, sw_links_outfile)
    io.write_crossings(st_crossings, outfile)
    click.echo('Done')


if __name__ == '__main__':
    crossify()