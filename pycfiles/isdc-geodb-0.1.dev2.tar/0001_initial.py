# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dodi/envs/isdc/isdc_modules/isdc_geodb/geodb/migrations/0001_initial.py
# Compiled at: 2018-08-31 03:26:03
from __future__ import unicode_literals
from django.db import migrations, models
import django.contrib.gis.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     (
      b'geodb', b'userfunctions_migration')]
    operations = [
     migrations.CreateModel(name=b'AfgAdmbndaAdm1', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_code', models.IntegerField(null=True, blank=True)),
      (
       b'area', models.FloatField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbnda_adm1', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAdmbndaAdm2', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'unit_type', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_ps', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'test2', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbnda_adm2', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAdmbndaInt', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'name_en_short', models.CharField(max_length=255, blank=True)),
      (
       b'names_ps', models.CharField(max_length=255, blank=True)),
      (
       b'name_prs', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbnda_int', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAdmbndlAdm1', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'fid_afg_admbnda_adm1_50000_agcho', models.IntegerField(null=True, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbndl_adm1', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAdmbndlAdm2', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'unit_type', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_ps', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbndl_adm2', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAdmbndlInt', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_admbndl_int', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAirdrma', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, dim=3, null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'nameshort', models.CharField(max_length=255, blank=True)),
      (
       b'namelong', models.CharField(max_length=255, blank=True)),
      (
       b'city', models.CharField(max_length=255, blank=True)),
      (
       b'icao', models.CharField(max_length=255, blank=True)),
      (
       b'iata', models.CharField(max_length=255, blank=True)),
      (
       b'apttype', models.CharField(max_length=255, blank=True)),
      (
       b'aptclass', models.CharField(max_length=255, blank=True)),
      (
       b'authority', models.CharField(max_length=255, blank=True)),
      (
       b'status', models.CharField(max_length=255, blank=True)),
      (
       b'rwpaved', models.CharField(max_length=255, blank=True)),
      (
       b'rwlengthm', models.IntegerField(null=True, blank=True)),
      (
       b'elevm', models.IntegerField(null=True, blank=True)),
      (
       b'humuse', models.CharField(max_length=255, blank=True)),
      (
       b'humoperate', models.CharField(max_length=255, blank=True)),
      (
       b'locprecisi', models.CharField(max_length=255, blank=True)),
      (
       b'iso3', models.CharField(max_length=255, blank=True)),
      (
       b'lastcheckd', models.DateTimeField(null=True, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'createdate', models.DateTimeField(null=True, blank=True)),
      (
       b'updatedate', models.DateTimeField(null=True, blank=True)),
      (
       b'adjusted_by', models.CharField(max_length=255, blank=True)),
      (
       b'type', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_airdrma', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAirdrmp', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, dim=3, null=True, blank=True)),
      (
       b'nameshort', models.CharField(max_length=255, blank=True)),
      (
       b'namelong', models.CharField(max_length=255, blank=True)),
      (
       b'city', models.CharField(max_length=255, blank=True)),
      (
       b'icao', models.CharField(max_length=255, blank=True)),
      (
       b'iata', models.CharField(max_length=255, blank=True)),
      (
       b'apttype', models.CharField(max_length=255, blank=True)),
      (
       b'aptclass', models.CharField(max_length=255, blank=True)),
      (
       b'authority', models.CharField(max_length=255, blank=True)),
      (
       b'status', models.CharField(max_length=255, blank=True)),
      (
       b'rwpaved', models.CharField(max_length=255, blank=True)),
      (
       b'rwlengthm', models.IntegerField(null=True, blank=True)),
      (
       b'rwlengthf', models.IntegerField(null=True, blank=True)),
      (
       b'elevm', models.IntegerField(null=True, blank=True)),
      (
       b'humuse', models.CharField(max_length=255, blank=True)),
      (
       b'humoperate', models.CharField(max_length=255, blank=True)),
      (
       b'locprecisi', models.CharField(max_length=255, blank=True)),
      (
       b'latitude', models.FloatField(null=True, blank=True)),
      (
       b'longitude', models.FloatField(null=True, blank=True)),
      (
       b'iso3', models.CharField(max_length=255, blank=True)),
      (
       b'country', models.CharField(max_length=255, blank=True)),
      (
       b'lastcheckd', models.DateTimeField(null=True, blank=True)),
      (
       b'remarks', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'createdate', models.DateTimeField(null=True, blank=True)),
      (
       b'updatedate', models.DateTimeField(null=True, blank=True)),
      (
       b'geonameid', models.IntegerField(null=True, blank=True)),
      (
       b'adjusted_by', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.CharField(max_length=20, blank=True)),
      (
       b'dist_code', models.CharField(max_length=20, blank=True))], options={b'db_table': b'afg_airdrmp', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgAvsa', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'avalanche_cat', models.CharField(max_length=255, blank=True)),
      (
       b'avalanche_id', models.IntegerField(null=True, blank=True)),
      (
       b'avalanche_zone', models.CharField(max_length=255, blank=True)),
      (
       b'avalanche_area', models.IntegerField(null=True, blank=True)),
      (
       b'avalanche_lenght_m', models.IntegerField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'sum_area_sqm', models.IntegerField(null=True, blank=True)),
      (
       b'avalanche_pop', models.IntegerField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_avsa', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgBasinLvl4GlofasPoint', fields=[
      (
       b'gid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'value', models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)),
      (
       b'wcmwf_lat', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'wcmwf_lon', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'shape_leng', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'shape_area', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True))], options={b'db_table': b'afg_basin_lvl4_glofas_point', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaAdm1ItsProvc', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_adm1_its_provc', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaAdm1NearestProvc', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_adm1_nearest_provc', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaAdm2NearestDistrictc', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_adm2_nearest_districtc', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaAirdrm', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_airdrm', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaGsmcvr', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'gsm_coverage', models.CharField(max_length=255, blank=True)),
      (
       b'gsm_coverage_population', models.FloatField(null=True, blank=True)),
      (
       b'gsm_coverage_area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_gsmcvr', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaHltfacTier1', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_hltfac_tier1', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaHltfacTier2', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_hltfac_tier2', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaHltfacTier3', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_hltfac_tier3', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCapaHltfacTierall', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=255, blank=True)),
      (
       b'time', models.CharField(max_length=255, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capa_hltfac_tierall', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptAdm1ItsProvcImmap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_adm1_its_provc_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptAdm1NearestProvcImmap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_adm1_nearest_provc_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptAdm2NearestDistrictcImmap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_adm2_nearest_districtc_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptAirdrmImmap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_airdrm_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptGmscvr', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'gsm_coverage', models.CharField(max_length=255, blank=True)),
      (
       b'frequency', models.IntegerField(null=True, blank=True)),
      (
       b'gsm_coverage_population', models.FloatField(null=True, blank=True)),
      (
       b'gsm_coverage_area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_gmscvr', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptHltfacTier1Immap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_hltfac_tier1_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptHltfacTier2Immap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_hltfac_tier2_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptHltfacTier3Immap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_hltfac_tier3_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptHltfacTierallImmap', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'facilities_name', models.CharField(max_length=50, blank=True)),
      (
       b'time', models.CharField(max_length=50, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'sum_area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_capt_hltfac_tierall_immap', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgCaptPpl', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'vil_uid', models.CharField(max_length=50, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'distance_to_road', models.IntegerField(null=True, blank=True)),
      (
       b'time_to_road', models.IntegerField(null=True, blank=True)),
      (
       b'airdrm_id', models.IntegerField(null=True, blank=True)),
      (
       b'airdrm_dist', models.IntegerField(null=True, blank=True)),
      (
       b'airdrm_time', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_provc_vuid', models.CharField(max_length=50, blank=True)),
      (
       b'ppl_provc_dist', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_provc_time', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_provc_its_vuid', models.CharField(max_length=50, blank=True)),
      (
       b'ppl_provc_its_dist', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_provc_its_time', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_distc_vuid', models.CharField(max_length=50, blank=True)),
      (
       b'ppl_distc_dist', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_distc_time', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_distc_its_vuid', models.CharField(max_length=50, blank=True)),
      (
       b'ppl_distc_its_dist', models.IntegerField(null=True, blank=True)),
      (
       b'ppl_distc_its_time', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier1_id', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier1_dist', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier1_time', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier2_id', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier2_dist', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier2_time', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier3_id', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier3_dist', models.IntegerField(null=True, blank=True)),
      (
       b'hltfac_tier3_time', models.IntegerField(null=True, blank=True))], options={b'db_table': b'afg_capt_ppl', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgEqHzda', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'acc_val', models.FloatField(null=True, blank=True)),
      (
       b'valley', models.IntegerField(null=True, blank=True)),
      (
       b'seismic_intensity_and_description', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'data', models.CharField(max_length=255, blank=True)),
      (
       b'population_at_risk', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True)),
      (
       b'seismic_intensity_cat', models.CharField(max_length=255, blank=True))], options={b'db_table': b'afg_eq_hzda', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgEqtUnkPplEqHzd', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'acc_val', models.FloatField(null=True, blank=True)),
      (
       b'seismic_intensity_and_description', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'data', models.CharField(max_length=255, blank=True)),
      (
       b'seismic_intensity_cat', models.CharField(max_length=255, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True))], options={b'db_table': b'afg_eqt_unk_ppl_eq_hzd', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgFaultslUnkCafd', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'shape_leng', models.FloatField(null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'faultid', models.IntegerField(null=True, blank=True)),
      (
       b'type', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'remarks', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_faultsl_unk_cafd', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgFaultslUnkUsgs', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'data', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_faultsl_unk_usgs', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgGeologyTecta', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_geology_tecta', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgHltfac', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'facility_id', models.FloatField(null=True, blank=True)),
      (
       b'vilicode', models.CharField(max_length=50, blank=True)),
      (
       b'facility_name', models.CharField(max_length=255, blank=True)),
      (
       b'facility_name_dari', models.CharField(max_length=255, blank=True)),
      (
       b'facility_name_pashto', models.CharField(max_length=255, blank=True)),
      (
       b'location', models.CharField(max_length=255, blank=True)),
      (
       b'location_dari', models.CharField(max_length=255, blank=True)),
      (
       b'location_pashto', models.CharField(max_length=255, blank=True)),
      (
       b'facilitytype', models.FloatField(null=True, blank=True)),
      (
       b'lat', models.FloatField(null=True, blank=True)),
      (
       b'lon', models.FloatField(null=True, blank=True)),
      (
       b'activestatus', models.CharField(max_length=255, blank=True)),
      (
       b'date_established', models.DateTimeField(null=True, blank=True)),
      (
       b'subimplementer', models.CharField(max_length=255, blank=True)),
      (
       b'locationsource', models.CharField(max_length=255, blank=True)),
      (
       b'moph', models.CharField(max_length=250, blank=True)),
      (
       b'hproreply', models.CharField(max_length=250, blank=True)),
      (
       b'facility_types_description', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=250, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=250, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'hpro_facilitytypes_description', models.CharField(max_length=250, blank=True))], options={b'db_table': b'afg_hltfac', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgIncidentOasis', fields=[
      (
       b'uid', models.IntegerField(serialize=False, primary_key=True, db_column=b'UID')),
      (
       b'xmin', models.FloatField(null=True, db_column=b'XMIN', blank=True)),
      (
       b'xmax', models.FloatField(null=True, db_column=b'XMAX', blank=True)),
      (
       b'ymin', models.FloatField(null=True, db_column=b'YMIN', blank=True)),
      (
       b'ymax', models.FloatField(null=True, db_column=b'YMAX', blank=True)),
      (
       b'id', models.CharField(max_length=255, db_column=b'ID', blank=True)),
      (
       b'name', models.CharField(max_length=255, db_column=b'NAME', blank=True)),
      (
       b'type', models.CharField(max_length=255, db_column=b'TYPE', blank=True)),
      (
       b'target', models.CharField(max_length=255, db_column=b'TARGET', blank=True)),
      (
       b'dead', models.IntegerField(null=True, blank=True)),
      (
       b'affected', models.IntegerField(null=True, blank=True)),
      (
       b'violent', models.IntegerField(null=True, blank=True)),
      (
       b'injured', models.IntegerField(null=True, blank=True)),
      (
       b'incident_date', models.DateField(null=True, blank=True)),
      (
       b'time00', models.CharField(max_length=255, blank=True)),
      (
       b'locdesc', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'town', models.CharField(max_length=255, blank=True)),
      (
       b'district', models.CharField(max_length=255, blank=True)),
      (
       b'province', models.CharField(max_length=255, blank=True)),
      (
       b'description', models.CharField(max_length=255, blank=True)),
      (
       b'scoring', models.IntegerField(null=True, blank=True)),
      (
       b'incident_dateserial', models.BigIntegerField(null=True, blank=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'accumulative_affected', models.IntegerField(null=True, blank=True)),
      (
       b'main_type', models.CharField(max_length=255, blank=True)),
      (
       b'main_target', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True))], options={b'db_table': b'afg_incident_oasis', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgIncidentOasisTemp', fields=[
      (
       b'uid', models.IntegerField(serialize=False, primary_key=True, db_column=b'UID')),
      (
       b'name', models.CharField(max_length=255, db_column=b'NAME', blank=True)),
      (
       b'type', models.CharField(max_length=255, db_column=b'TYPE', blank=True)),
      (
       b'target', models.CharField(max_length=255, db_column=b'TARGET', blank=True)),
      (
       b'dead', models.IntegerField(null=True, blank=True)),
      (
       b'affected', models.IntegerField(null=True, blank=True)),
      (
       b'violent', models.IntegerField(null=True, blank=True)),
      (
       b'injured', models.IntegerField(null=True, blank=True)),
      (
       b'incident_date', models.DateField(null=True, blank=True)),
      (
       b'locdesc', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'town', models.CharField(max_length=255, blank=True)),
      (
       b'district', models.CharField(max_length=255, blank=True)),
      (
       b'province', models.CharField(max_length=255, blank=True)),
      (
       b'description', models.CharField(max_length=255, blank=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True))], options={b'db_table': b'afg_incident_oasis_temp', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgLndcrva', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'lccsuslb', models.CharField(max_length=255, blank=True)),
      (
       b'lccsperc', models.CharField(max_length=255, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'aggcode_simplified', models.CharField(max_length=255, blank=True)),
      (
       b'agg_simplified_description', models.CharField(max_length=255, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'area_buildup_assoc', models.CharField(max_length=255, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'lccs_main_description', models.CharField(max_length=255, blank=True)),
      (
       b'lccs_sub_description', models.CharField(max_length=255, blank=True)),
      (
       b'lccsuslb_simplified', models.CharField(max_length=255, blank=True)),
      (
       b'lccs_aggregated', models.CharField(max_length=255, blank=True)),
      (
       b'aggcode', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_buildings', models.FloatField(null=True, blank=True)),
      (
       b'vuid_population', models.FloatField(null=True, blank=True)),
      (
       b'vuid_pop_per_building', models.FloatField(null=True, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_lndcrva', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgLndcrvaCity', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'osm_id', models.CharField(max_length=255, blank=True)),
      (
       b'code', models.IntegerField(null=True, blank=True)),
      (
       b'fclass', models.CharField(max_length=255, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_lndcrva_city', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgLndcrvaSimplified', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'lccsperc', models.CharField(max_length=255, blank=True)),
      (
       b'aggcode', models.CharField(max_length=255, blank=True)),
      (
       b'aggcode_simplified', models.CharField(max_length=255, blank=True)),
      (
       b'agg_simplified_description', models.CharField(max_length=255, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_population_landscan', models.IntegerField(null=True, blank=True)),
      (
       b'vuid_area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'population_misti', models.IntegerField(null=True, blank=True)),
      (
       b'note', models.CharField(max_length=255, blank=True)),
      (
       b'edited_by', models.CharField(max_length=255, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'unit_type', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_ps', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_lndcrva_simplified', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgLspAffpplp', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'lsi_ku', models.IntegerField(null=True, blank=True)),
      (
       b'ls_s1_wb', models.IntegerField(null=True, blank=True)),
      (
       b'ls_s2_wb', models.IntegerField(null=True, blank=True)),
      (
       b'ls_s3_wb', models.IntegerField(null=True, blank=True)),
      (
       b'lsi_immap', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_lsp_affpplp', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmChelsaBioclim', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.IntegerField(null=True, blank=True)),
      (
       b'bio13', models.IntegerField(null=True, blank=True)),
      (
       b'bio14', models.IntegerField(null=True, blank=True)),
      (
       b'bio15', models.IntegerField(null=True, blank=True)),
      (
       b'bio16', models.IntegerField(null=True, blank=True)),
      (
       b'bio17', models.IntegerField(null=True, blank=True)),
      (
       b'bio18', models.IntegerField(null=True, blank=True)),
      (
       b'bio19', models.IntegerField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_chelsa_bioclim', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc26', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2050_rpc26', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc45', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2050_rpc45', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2050Rpc85', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2050_rpc85', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc26', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2070_rpc26', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc45', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2070_rpc45', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClim1KmWorldclimBioclim2070Rpc85', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'bio1', models.FloatField(null=True, blank=True)),
      (
       b'bio2', models.FloatField(null=True, blank=True)),
      (
       b'bio3', models.FloatField(null=True, blank=True)),
      (
       b'bio4', models.FloatField(null=True, blank=True)),
      (
       b'bio5', models.FloatField(null=True, blank=True)),
      (
       b'bio6', models.FloatField(null=True, blank=True)),
      (
       b'bio7', models.FloatField(null=True, blank=True)),
      (
       b'bio8', models.FloatField(null=True, blank=True)),
      (
       b'bio9', models.FloatField(null=True, blank=True)),
      (
       b'bio10', models.FloatField(null=True, blank=True)),
      (
       b'bio11', models.FloatField(null=True, blank=True)),
      (
       b'bio12', models.FloatField(null=True, blank=True)),
      (
       b'bio13', models.FloatField(null=True, blank=True)),
      (
       b'bio14', models.FloatField(null=True, blank=True)),
      (
       b'bio15', models.FloatField(null=True, blank=True)),
      (
       b'bio16', models.FloatField(null=True, blank=True)),
      (
       b'bio17', models.FloatField(null=True, blank=True)),
      (
       b'bio18', models.FloatField(null=True, blank=True)),
      (
       b'bio19', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_clim_1km_worldclim_bioclim_2070_rpc85', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClimperc1KmChelsaPrec', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'january', models.FloatField(null=True, blank=True)),
      (
       b'february', models.FloatField(null=True, blank=True)),
      (
       b'march', models.FloatField(null=True, blank=True)),
      (
       b'april', models.FloatField(null=True, blank=True)),
      (
       b'may', models.FloatField(null=True, blank=True)),
      (
       b'june', models.FloatField(null=True, blank=True)),
      (
       b'july', models.FloatField(null=True, blank=True)),
      (
       b'august', models.FloatField(null=True, blank=True)),
      (
       b'september', models.FloatField(null=True, blank=True)),
      (
       b'october', models.FloatField(null=True, blank=True)),
      (
       b'november', models.FloatField(null=True, blank=True)),
      (
       b'december', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_climperc_1km_chelsa_prec', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClimtemp1KmChelsaTempavg', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'january', models.FloatField(null=True, blank=True)),
      (
       b'february', models.FloatField(null=True, blank=True)),
      (
       b'march', models.FloatField(null=True, blank=True)),
      (
       b'april', models.FloatField(null=True, blank=True)),
      (
       b'may', models.FloatField(null=True, blank=True)),
      (
       b'june', models.FloatField(null=True, blank=True)),
      (
       b'july', models.FloatField(null=True, blank=True)),
      (
       b'august', models.FloatField(null=True, blank=True)),
      (
       b'september', models.FloatField(null=True, blank=True)),
      (
       b'october', models.FloatField(null=True, blank=True)),
      (
       b'november', models.FloatField(null=True, blank=True)),
      (
       b'december', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_climtemp_1km_chelsa_tempavg', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClimtemp1KmChelsaTempmax', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'january', models.FloatField(null=True, blank=True)),
      (
       b'february', models.FloatField(null=True, blank=True)),
      (
       b'march', models.FloatField(null=True, blank=True)),
      (
       b'april', models.FloatField(null=True, blank=True)),
      (
       b'may', models.FloatField(null=True, blank=True)),
      (
       b'june', models.FloatField(null=True, blank=True)),
      (
       b'july', models.FloatField(null=True, blank=True)),
      (
       b'august', models.FloatField(null=True, blank=True)),
      (
       b'september', models.FloatField(null=True, blank=True)),
      (
       b'october', models.FloatField(null=True, blank=True)),
      (
       b'november', models.FloatField(null=True, blank=True)),
      (
       b'december', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_climtemp_1km_chelsa_tempmax', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgMettClimtemp1KmChelsaTempmin', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=50, blank=True)),
      (
       b'january', models.FloatField(null=True, blank=True)),
      (
       b'february', models.FloatField(null=True, blank=True)),
      (
       b'march', models.FloatField(null=True, blank=True)),
      (
       b'april', models.FloatField(null=True, blank=True)),
      (
       b'may', models.FloatField(null=True, blank=True)),
      (
       b'june', models.FloatField(null=True, blank=True)),
      (
       b'july', models.FloatField(null=True, blank=True)),
      (
       b'august', models.FloatField(null=True, blank=True)),
      (
       b'september', models.FloatField(null=True, blank=True)),
      (
       b'october', models.FloatField(null=True, blank=True)),
      (
       b'november', models.FloatField(null=True, blank=True)),
      (
       b'december', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_mett_climtemp_1km_chelsa_tempmin', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPoiaBuildings', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'osm_id', models.FloatField(null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'type', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_poia_buildings', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPoip', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'osm_id', models.FloatField(null=True, blank=True)),
      (
       b'timestamp', models.CharField(max_length=255, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'type', models.CharField(max_length=255, blank=True)),
      (
       b'category_style', models.CharField(max_length=255, blank=True))], options={b'db_table': b'afg_poip', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPpla', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'vuidnear', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_buildings', models.FloatField(null=True, blank=True)),
      (
       b'vuid_population', models.FloatField(null=True, blank=True)),
      (
       b'vuid_pop_per_building', models.FloatField(null=True, blank=True)),
      (
       b'name_local', models.CharField(max_length=255, blank=True)),
      (
       b'name_alternative_en', models.CharField(max_length=255, blank=True)),
      (
       b'name_local_confidence', models.CharField(max_length=255, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True)),
      (
       b'area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True)),
      (
       b'pplp_point_x', models.FloatField(null=True, blank=True)),
      (
       b'pplp_point_y', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_ppla', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPplaBasin', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'vuidnear', models.CharField(max_length=50, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'area_population', models.FloatField(null=True, blank=True)),
      (
       b'area_buildings', models.FloatField(null=True, blank=True)),
      (
       b'area_sqm', models.IntegerField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_buildings', models.FloatField(null=True, blank=True)),
      (
       b'vuid_population', models.FloatField(null=True, blank=True)),
      (
       b'vuid_pop_per_building', models.FloatField(null=True, blank=True)),
      (
       b'name_local', models.CharField(max_length=255, blank=True)),
      (
       b'name_alternative_en', models.CharField(max_length=255, blank=True)),
      (
       b'name_local_confidence', models.CharField(max_length=255, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True)),
      (
       b'basinmember_id', models.IntegerField(null=True, blank=True))], options={b'db_table': b'afg_ppla_basin', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPplp', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'vil_uid', models.CharField(max_length=255, blank=True)),
      (
       b'cntr_code', models.IntegerField(null=True, blank=True)),
      (
       b'afg_uid', models.CharField(max_length=255, blank=True)),
      (
       b'language_field', models.CharField(max_length=255, db_column=b'language_', blank=True)),
      (
       b'lang_code', models.IntegerField(null=True, blank=True)),
      (
       b'elevation', models.FloatField(null=True, blank=True)),
      (
       b'lat_y', models.FloatField(null=True, blank=True)),
      (
       b'lon_x', models.FloatField(null=True, blank=True)),
      (
       b'note', models.CharField(max_length=255, blank=True)),
      (
       b'edited_by', models.CharField(max_length=255, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code_1', models.IntegerField(null=True, blank=True)),
      (
       b'unit_type', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'dist_na_ps', models.CharField(max_length=255, blank=True)),
      (
       b'reg_unama_na_dar', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_area_sqm', models.FloatField(null=True, blank=True)),
      (
       b'vuidnear', models.CharField(max_length=255, blank=True)),
      (
       b'vuid_buildings', models.FloatField(null=True, blank=True)),
      (
       b'vuid_population', models.FloatField(null=True, blank=True)),
      (
       b'vuid_pop_per_building', models.FloatField(null=True, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'name_local', models.CharField(max_length=255, blank=True)),
      (
       b'name_local_confidence', models.CharField(max_length=255, blank=True)),
      (
       b'name_alternative_en', models.CharField(max_length=255, blank=True))], options={b'db_table': b'afg_pplp', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgPpltDemographics', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'vuidnear', models.CharField(max_length=50, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=100, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=100, blank=True)),
      (
       b'prov_code_field', models.IntegerField(null=True, db_column=b'prov_code_', blank=True)),
      (
       b'partofbuil', models.CharField(max_length=100, blank=True)),
      (
       b'vuid_buildings', models.IntegerField(null=True, blank=True)),
      (
       b'vuid_population', models.IntegerField(null=True, blank=True)),
      (
       b'vuid_male_perc', models.FloatField(null=True, blank=True)),
      (
       b'vuid_female_perc', models.FloatField(null=True, blank=True)),
      (
       b'note', models.CharField(max_length=200, blank=True)),
      (
       b'vuid_pop_per_building', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_0_4', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_5_9', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_10_14', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_15_19', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_20_24', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_25_29', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_30_34', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_35_39', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_40_44', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_45_49', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_50_54', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_55_59', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_60_64', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_65_69', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_70_74', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_75_79', models.FloatField(null=True, blank=True)),
      (
       b'm_perc_yrs_80pls', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_0_4', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_5_9', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_10_14', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_15_19', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_20_24', models.FloatField(null=True, db_column=b'f_perc_yrs__20_24', blank=True)),
      (
       b'f_perc_yrs_25_29', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_30_34', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_35_39', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_40_44', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_45_49', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_50_54', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_55_59', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_60_64', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_65_69', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_70_74', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_75_79', models.FloatField(null=True, blank=True)),
      (
       b'f_perc_yrs_80pls', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_pplt_demographics', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgRafUnkIom', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'no', models.IntegerField(null=True, blank=True)),
      (
       b'incident_date', models.DateTimeField(null=True, blank=True)),
      (
       b'disaster_type', models.CharField(max_length=255, blank=True)),
      (
       b'rafno', models.CharField(max_length=255, blank=True)),
      (
       b'assessment_date', models.DateTimeField(null=True, blank=True)),
      (
       b'msraf_status', models.CharField(max_length=255, blank=True)),
      (
       b'region', models.CharField(max_length=255, blank=True)),
      (
       b'province', models.CharField(max_length=255, blank=True)),
      (
       b'district', models.CharField(max_length=255, blank=True)),
      (
       b'village_or_nahya', models.CharField(max_length=255, blank=True)),
      (
       b'long', models.FloatField(null=True, blank=True)),
      (
       b'lat', models.FloatField(null=True, blank=True)),
      (
       b'numberofhouseholds', models.IntegerField(null=True, blank=True)),
      (
       b'numberoffamilies', models.IntegerField(null=True, blank=True)),
      (
       b'numberofidps', models.IntegerField(null=True, blank=True)),
      (
       b'totalpopulation', models.IntegerField(null=True, blank=True)),
      (
       b'affectedfamilies', models.IntegerField(null=True, blank=True)),
      (
       b'province_1', models.CharField(max_length=255, blank=True)),
      (
       b'district_1', models.CharField(max_length=255, blank=True)),
      (
       b'village', models.CharField(max_length=255, blank=True)),
      (
       b'nodamaged', models.CharField(max_length=255, blank=True)),
      (
       b'moderatelydamaged', models.IntegerField(null=True, blank=True)),
      (
       b'severelydamaged', models.IntegerField(null=True, blank=True)),
      (
       b'completelydestroyed', models.IntegerField(null=True, blank=True)),
      (
       b'affected_individuals', models.IntegerField(null=True, blank=True)),
      (
       b'deaths', models.IntegerField(null=True, blank=True)),
      (
       b'injuried', models.IntegerField(null=True, blank=True)),
      (
       b'missing', models.IntegerField(null=True, blank=True)),
      (
       b'long_1', models.FloatField(null=True, blank=True)),
      (
       b'lat_1', models.FloatField(null=True, blank=True)),
      (
       b'alternativevillagenamemisti', models.CharField(max_length=255, blank=True)),
      (
       b'alternativedistrictname', models.CharField(max_length=255, blank=True)),
      (
       b'misti_vuid', models.CharField(max_length=255, blank=True)),
      (
       b'disastertype', models.CharField(max_length=255, blank=True))], options={b'db_table': b'afg_raf_unk_iom', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgRdsl', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'avg_slope', models.FloatField(null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'source', models.CharField(max_length=255, blank=True)),
      (
       b'speedkmh', models.IntegerField(null=True, blank=True)),
      (
       b'type_update', models.CharField(max_length=255, blank=True)),
      (
       b'adjusted_kmh', models.IntegerField(null=True, blank=True)),
      (
       b'priority_class', models.IntegerField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'bridge', models.CharField(max_length=255, blank=True)),
      (
       b'tunnel', models.CharField(max_length=255, blank=True)),
      (
       b'road_length', models.IntegerField(null=True, blank=True)),
      (
       b'builduparea', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_rdsl', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgRiv', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, blank=True)),
      (
       b'join_count', models.IntegerField(null=True, blank=True)),
      (
       b'join_cou_1', models.IntegerField(null=True, blank=True)),
      (
       b'join_cou_2', models.IntegerField(null=True, blank=True)),
      (
       b'objectid', models.IntegerField(null=True, blank=True)),
      (
       b'arcid', models.IntegerField(null=True, blank=True)),
      (
       b'grid_code', models.IntegerField(null=True, blank=True)),
      (
       b'from_node', models.IntegerField(null=True, blank=True)),
      (
       b'to_node', models.IntegerField(null=True, blank=True)),
      (
       b'shape_leng', models.FloatField(null=True, blank=True)),
      (
       b'idcode', models.IntegerField(null=True, blank=True)),
      (
       b'fnode', models.IntegerField(null=True, blank=True)),
      (
       b'tnode', models.IntegerField(null=True, blank=True)),
      (
       b'strahler', models.IntegerField(null=True, blank=True)),
      (
       b'segment', models.IntegerField(null=True, blank=True)),
      (
       b'shreve', models.IntegerField(null=True, blank=True)),
      (
       b'us_accum', models.FloatField(null=True, blank=True)),
      (
       b'link_type', models.CharField(max_length=255, blank=True)),
      (
       b'riverwidth', models.IntegerField(null=True, blank=True)),
      (
       b'landcover', models.CharField(max_length=255, blank=True)),
      (
       b'vertices', models.IntegerField(null=True, blank=True)),
      (
       b'name', models.CharField(max_length=255, blank=True)),
      (
       b'flooddepth', models.FloatField(null=True, blank=True)),
      (
       b'riverwid_1', models.FloatField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_riv', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgShedaLvl2', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, dim=3, null=True, blank=True)),
      (
       b'basinnumbe', models.IntegerField(null=True, blank=True)),
      (
       b'basinname', models.CharField(max_length=255, blank=True)),
      (
       b'area', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_sheda_lvl2', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgShedaLvl3', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, dim=3, null=True, blank=True)),
      (
       b'basinnumbe', models.IntegerField(null=True, blank=True)),
      (
       b'basinname', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_sheda_lvl3', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgShedaLvl4', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'value', models.FloatField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_sheda_lvl4', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgSnowaAverageExtent', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'aver_cov', models.CharField(max_length=50, blank=True)),
      (
       b'cov_10_oct', models.CharField(max_length=50, blank=True)),
      (
       b'cov_11_nov', models.CharField(max_length=50, blank=True)),
      (
       b'cov_05_may', models.CharField(max_length=50, blank=True)),
      (
       b'cov_03_mar', models.CharField(max_length=50, blank=True)),
      (
       b'cov_04_apr', models.CharField(max_length=50, blank=True)),
      (
       b'cov_08_aug', models.CharField(max_length=50, blank=True)),
      (
       b'cov_12_dec', models.CharField(max_length=50, blank=True)),
      (
       b'cov_02_feb', models.CharField(max_length=50, blank=True)),
      (
       b'cov_01_jan', models.CharField(max_length=50, blank=True)),
      (
       b'cov_07_jul', models.CharField(max_length=50, blank=True)),
      (
       b'cov_06_jun', models.CharField(max_length=50, blank=True)),
      (
       b'cov_09_sep', models.CharField(max_length=50, blank=True)),
      (
       b'source', models.CharField(max_length=250, blank=True)),
      (
       b'author', models.CharField(max_length=250, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'afg_snowa_average_extent', 
        b'managed': True}),
     migrations.CreateModel(name=b'AfgUtilWell', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'serial_number', models.FloatField(null=True, blank=True)),
      (
       b'implementing_agency', models.CharField(max_length=255, blank=True)),
      (
       b'donor_name', models.CharField(max_length=255, blank=True)),
      (
       b'date_visited', models.DateTimeField(null=True, blank=True)),
      (
       b'district_name', models.CharField(max_length=255, blank=True)),
      (
       b'village_name', models.CharField(max_length=255, blank=True)),
      (
       b'care_taker_name', models.CharField(max_length=255, blank=True)),
      (
       b'longitude_degree', models.FloatField(null=True, blank=True)),
      (
       b'latitude_degree', models.FloatField(null=True, blank=True)),
      (
       b'water_point_code', models.FloatField(null=True, blank=True)),
      (
       b'year_implented', models.FloatField(null=True, blank=True)),
      (
       b'ec_micros_cm', models.FloatField(null=True, blank=True)),
      (
       b'ph', models.FloatField(null=True, blank=True)),
      (
       b't_c', models.FloatField(null=True, blank=True)),
      (
       b'beneficiaries_families', models.FloatField(null=True, blank=True)),
      (
       b'well_depth_m', models.FloatField(null=True, blank=True)),
      (
       b'well_diameter_cm', models.FloatField(null=True, blank=True)),
      (
       b'static_water_level_m', models.FloatField(null=True, blank=True)),
      (
       b'type_of_system', models.CharField(max_length=255, blank=True)),
      (
       b'maintenance_system_existing', models.CharField(max_length=255, blank=True)),
      (
       b'maintenance_agreement_signed', models.CharField(max_length=255, blank=True)),
      (
       b'mechanic_valveman_trained', models.CharField(max_length=255, blank=True)),
      (
       b'wage_of_mechanic_valveman_paid', models.CharField(max_length=255, blank=True)),
      (
       b'water_user_group_established', models.CharField(max_length=255, blank=True)),
      (
       b'care_taker_selected_trained', models.CharField(max_length=255, blank=True)),
      (
       b'water_management_committee_established', models.FloatField(null=True, blank=True)),
      (
       b'pipe_scheme_conditions', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_problem', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_working', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_working_with_bucket', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_dry_drawdown', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_collapsed_destroyed', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_plugged_abandoned', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_enclosed', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_concrete_problem', models.CharField(max_length=255, blank=True)),
      (
       b'water_point_pump_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_tap_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_pipeline_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_catchment_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_reservoir_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_solar_pump_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_solar_panel_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_submersible_pump_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_generator_problem', models.CharField(max_length=255, blank=True)),
      (
       b'pipe_scheme_generator_room_problem', models.CharField(max_length=255, blank=True)),
      (
       b'wp_type', models.CharField(max_length=255, blank=True)),
      (
       b'no_maintenance_problem', models.CharField(max_length=255, blank=True)),
      (
       b'community_problem', models.CharField(max_length=255, blank=True)),
      (
       b'mechanic_valveman_problem', models.CharField(max_length=255, blank=True)),
      (
       b'spare_parts_availlability_problem', models.CharField(max_length=255, blank=True)),
      (
       b'original_hp_present', models.CharField(max_length=255, blank=True)),
      (
       b'no_new_hp', models.CharField(max_length=255, blank=True)),
      (
       b'new_hp_from_community', models.CharField(max_length=255, blank=True)),
      (
       b'new_hp_from_ngo_government', models.CharField(max_length=255, blank=True)),
      (
       b'hp_condition', models.CharField(max_length=255, blank=True)),
      (
       b'hp_problem_fixible', models.CharField(max_length=255, blank=True)),
      (
       b'hp_problem_not_fixible', models.CharField(max_length=255, blank=True)),
      (
       b'hp_raising_main_problem', models.CharField(max_length=255, blank=True)),
      (
       b'hp_removed_vandalized', models.CharField(max_length=255, blank=True)),
      (
       b'pump_manufacturer', models.CharField(max_length=255, blank=True)),
      (
       b'pump_code', models.FloatField(null=True, blank=True)),
      (
       b'solar_panel_manufacturer', models.CharField(max_length=255, blank=True)),
      (
       b'pump_type', models.CharField(max_length=255, blank=True)),
      (
       b'flood_risk', models.CharField(max_length=255, blank=True)),
      (
       b'avalanche_risk', models.CharField(max_length=255, blank=True)),
      (
       b'data_source', models.CharField(max_length=255, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'landcover_description', models.CharField(max_length=255, blank=True)),
      (
       b'vuid', models.CharField(max_length=255, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'type_settlement', models.CharField(max_length=255, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True))], options={b'db_table': b'afg_util_well', 
        b'managed': True}),
     migrations.CreateModel(name=b'AndmaOffice', fields=[
      (
       b'gid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'objectid', models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)),
      (
       b'vil_uid', models.CharField(max_length=10, blank=True)),
      (
       b'note', models.CharField(max_length=50, blank=True)),
      (
       b'name_en', models.CharField(max_length=50, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=50, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=50, blank=True)),
      (
       b'dist_na_da', models.CharField(max_length=254, blank=True)),
      (
       b'prov_na_da', models.CharField(max_length=254, blank=True)),
      (
       b'dist_na_ps', models.CharField(max_length=254, blank=True)),
      (
       b'geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True))], options={b'db_table': b'andma_office', 
        b'managed': True}),
     migrations.CreateModel(name=b'basinsummary', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'basin', models.CharField(max_length=255)),
      (
       b'Population', models.FloatField(null=True, blank=True)),
      (
       b'Area', models.FloatField(null=True, blank=True)),
      (
       b'settlements', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area', models.FloatField(null=True, blank=True)),
      (
       b'forest_area', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'settlements_at_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_forecast_pop', models.FloatField(null=True, blank=True))], options={b'db_table': b'basinsummary', 
        b'managed': True}),
     migrations.CreateModel(name=b'CurrentScBasins', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'basin', models.FloatField(null=True, blank=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True))], options={b'db_table': b'current_sc_basins', 
        b'managed': True}),
     migrations.CreateModel(name=b'DistrictAddSummary', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'dist_code', models.CharField(max_length=255)),
      (
       b'hlt_h1', models.FloatField(null=True, blank=True)),
      (
       b'hlt_h2', models.FloatField(null=True, blank=True)),
      (
       b'hlt_h3', models.FloatField(null=True, blank=True)),
      (
       b'hlt_special_hospital', models.FloatField(null=True, blank=True)),
      (
       b'hlt_rehabilitation_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_maternity_home', models.FloatField(null=True, blank=True)),
      (
       b'hlt_drug_addicted_treatment_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_chc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_bhc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_shc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_private_clinic', models.FloatField(null=True, blank=True)),
      (
       b'hlt_malaria_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_mobile_health_team', models.FloatField(null=True, blank=True)),
      (
       b'hlt_other', models.FloatField(null=True, blank=True)),
      (
       b'road_highway', models.FloatField(null=True, blank=True)),
      (
       b'road_primary', models.FloatField(null=True, blank=True)),
      (
       b'road_secondary', models.FloatField(null=True, blank=True)),
      (
       b'road_tertiary', models.FloatField(null=True, blank=True)),
      (
       b'road_residential', models.FloatField(null=True, blank=True)),
      (
       b'road_track', models.FloatField(null=True, blank=True)),
      (
       b'road_path', models.FloatField(null=True, blank=True)),
      (
       b'road_river_crossing', models.FloatField(null=True, blank=True)),
      (
       b'road_bridge', models.FloatField(null=True, blank=True))], options={b'db_table': b'district_add_summary', 
        b'managed': True}),
     migrations.CreateModel(name=b'districtsummary', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'district', models.CharField(max_length=255)),
      (
       b'Population', models.FloatField(null=True, blank=True)),
      (
       b'Area', models.FloatField(null=True, blank=True)),
      (
       b'settlements', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area', models.FloatField(null=True, blank=True)),
      (
       b'forest_area', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'settlements_at_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_pop', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_area', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'total_buildings', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_buildings', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_buildings', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_buildings', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'districtsummary', 
        b'managed': True}),
     migrations.CreateModel(name=b'earthquake_events', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'event_code', models.CharField(max_length=25)),
      (
       b'title', models.CharField(max_length=255)),
      (
       b'dateofevent', models.DateTimeField()),
      (
       b'magnitude', models.FloatField(null=True, blank=True)),
      (
       b'depth', models.FloatField(null=True, blank=True)),
      (
       b'shakemaptimestamp', models.BigIntegerField(null=True, blank=True))], options={b'db_table': b'earthquake_events', 
        b'managed': True}),
     migrations.CreateModel(name=b'earthquake_shakemap', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'event_code', models.CharField(max_length=25, blank=True)),
      (
       b'shakemaptimestamp', models.BigIntegerField(null=True, blank=True)),
      (
       b'grid_value', models.IntegerField(null=True, blank=True))], options={b'db_table': b'earthquake_shakemap', 
        b'managed': True}),
     migrations.CreateModel(name=b'EventdataHistory', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'timestamp', models.DateTimeField(null=True, blank=True)),
      (
       b'api', models.CharField(max_length=255, blank=True)),
      (
       b'eventdata', models.TextField(blank=True))], options={b'db_table': b'eventdata_history', 
        b'managed': True}),
     migrations.CreateModel(name=b'HistoryDrought', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'ogc_fid', models.IntegerField(null=True, blank=True)),
      (
       b'min', models.FloatField(null=True, blank=True)),
      (
       b'mean', models.FloatField(null=True, blank=True)),
      (
       b'max', models.FloatField(null=True, blank=True)),
      (
       b'std', models.FloatField(null=True, blank=True)),
      (
       b'sum', models.FloatField(null=True, blank=True)),
      (
       b'count', models.FloatField(null=True, blank=True)),
      (
       b'basin_id', models.FloatField(null=True, blank=True)),
      (
       b'agg_code', models.CharField(max_length=50, blank=True)),
      (
       b'woy', models.CharField(max_length=50, blank=True))], options={b'db_table': b'history_drought', 
        b'managed': True}),
     migrations.CreateModel(name=b'LandcoverDescription', fields=[
      (
       b'code', models.CharField(max_length=255, blank=True)),
      (
       b'id', models.IntegerField(serialize=False, primary_key=True))], options={b'db_table': b'landcover_description', 
        b'managed': True}),
     migrations.CreateModel(name=b'OasisSettlements', fields=[
      (
       b'gid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'type_settlement', models.CharField(max_length=20, blank=True)),
      (
       b'source', models.CharField(max_length=50, blank=True)),
      (
       b'x', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'y', models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=50, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=50, blank=True)),
      (
       b'un_reg', models.CharField(max_length=50, blank=True)),
      (
       b'isaf_rc', models.CharField(max_length=50, blank=True)),
      (
       b'name_en', models.CharField(max_length=200, blank=True)),
      (
       b'vil_uid', models.IntegerField(null=True, blank=True)),
      (
       b'anso_reg', models.CharField(max_length=50, blank=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True))], options={b'db_table': b'oasis_settlements', 
        b'managed': True}),
     migrations.CreateModel(name=b'ProvinceAddSummary', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'prov_code', models.CharField(max_length=255)),
      (
       b'hlt_h1', models.FloatField(null=True, blank=True)),
      (
       b'hlt_h2', models.FloatField(null=True, blank=True)),
      (
       b'hlt_h3', models.FloatField(null=True, blank=True)),
      (
       b'hlt_special_hospital', models.FloatField(null=True, blank=True)),
      (
       b'hlt_rehabilitation_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_maternity_home', models.FloatField(null=True, blank=True)),
      (
       b'hlt_drug_addicted_treatment_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_chc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_bhc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_shc', models.FloatField(null=True, blank=True)),
      (
       b'hlt_private_clinic', models.FloatField(null=True, blank=True)),
      (
       b'hlt_malaria_center', models.FloatField(null=True, blank=True)),
      (
       b'hlt_mobile_health_team', models.FloatField(null=True, blank=True)),
      (
       b'hlt_other', models.FloatField(null=True, blank=True)),
      (
       b'road_highway', models.FloatField(null=True, blank=True)),
      (
       b'road_primary', models.FloatField(null=True, blank=True)),
      (
       b'road_secondary', models.FloatField(null=True, blank=True)),
      (
       b'road_tertiary', models.FloatField(null=True, blank=True)),
      (
       b'road_residential', models.FloatField(null=True, blank=True)),
      (
       b'road_track', models.FloatField(null=True, blank=True)),
      (
       b'road_path', models.FloatField(null=True, blank=True)),
      (
       b'road_river_crossing', models.FloatField(null=True, blank=True)),
      (
       b'road_bridge', models.FloatField(null=True, blank=True))], options={b'db_table': b'province_add_summary', 
        b'managed': True}),
     migrations.CreateModel(name=b'provincesummary', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'province', models.CharField(max_length=255)),
      (
       b'Population', models.FloatField(null=True, blank=True)),
      (
       b'Area', models.FloatField(null=True, blank=True)),
      (
       b'settlements', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area', models.FloatField(null=True, blank=True)),
      (
       b'forest_area', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_population', models.FloatField(null=True, blank=True)),
      (
       b'settlements_at_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'med_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'low_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_area', models.FloatField(null=True, blank=True)),
      (
       b'water_body_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'water_body_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'barren_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'built_up_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'fruit_trees_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'irrigated_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'permanent_snow_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rainfed_agricultural_land_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'rangeland_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'sandcover_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'vineyards_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'forest_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_population', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'low_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_pop', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_pop_risk', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_area', models.FloatField(null=True, blank=True)),
      (
       b'sand_dunes_area_risk', models.FloatField(null=True, blank=True)),
      (
       b'total_buildings', models.FloatField(null=True, blank=True)),
      (
       b'total_risk_buildings', models.FloatField(null=True, blank=True)),
      (
       b'high_ava_buildings', models.FloatField(null=True, blank=True)),
      (
       b'med_ava_buildings', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_buildings', models.FloatField(null=True, blank=True))], options={b'db_table': b'provincesummary', 
        b'managed': True}),
     migrations.CreateModel(name=b'RefSecurity', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'last_incidentdate', models.DateField(null=True, blank=True)),
      (
       b'last_sync', models.DateField(null=True, blank=True)),
      (
       b'last_entry', models.DateField(null=True, blank=True))], options={b'db_table': b'ref_security', 
        b'managed': True}),
     migrations.CreateModel(name=b'SlopeHospLndcvrNofldNoavaNouxo4KmsqGonogo', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'dist_code', models.IntegerField(null=True, blank=True)),
      (
       b'dist_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_na_en', models.CharField(max_length=255, blank=True)),
      (
       b'prov_code', models.IntegerField(null=True, blank=True)),
      (
       b'area', models.IntegerField(null=True, blank=True)),
      (
       b'buff_dist', models.FloatField(null=True, blank=True)),
      (
       b'orig_fid', models.IntegerField(null=True, blank=True)),
      (
       b'gonogo', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'slope_hosp_lndcvr_nofld_noava_nouxo__4kmsq_gonogo', 
        b'managed': True}),
     migrations.CreateModel(name=b'tempCurrentSC', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True))], options={b'db_table': b'temp_current_sc', 
        b'managed': True}),
     migrations.CreateModel(name=b'villagesummary', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'vuid', models.CharField(max_length=255)),
      (
       b'basin', models.CharField(max_length=255)),
      (
       b'riverflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'riverflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_riverflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_pop', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_verylow_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_low_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_med_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_high_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_veryhigh_area', models.FloatField(null=True, blank=True)),
      (
       b'flashflood_forecast_extreme_area', models.FloatField(null=True, blank=True)),
      (
       b'total_flashflood_forecast_area', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_low_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_med_pop', models.FloatField(null=True, blank=True)),
      (
       b'ava_forecast_high_pop', models.FloatField(null=True, blank=True)),
      (
       b'total_ava_forecast_pop', models.FloatField(null=True, blank=True))], options={b'db_table': b'villagesummary', 
        b'managed': True}),
     migrations.CreateModel(name=b'villagesummaryEQ', fields=[
      (
       b'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'event_code', models.CharField(max_length=20)),
      (
       b'village', models.CharField(max_length=255)),
      (
       b'district', models.CharField(max_length=255)),
      (
       b'pop_shake_weak', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_light', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_moderate', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_strong', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_verystrong', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_severe', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_violent', models.FloatField(null=True, blank=True)),
      (
       b'pop_shake_extreme', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_weak', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_light', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_moderate', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_strong', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_verystrong', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_severe', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_violent', models.FloatField(null=True, blank=True)),
      (
       b'settlement_shake_extreme', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_weak', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_light', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_moderate', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_strong', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_verystrong', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_severe', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_violent', models.FloatField(null=True, blank=True)),
      (
       b'buildings_shake_extreme', models.FloatField(null=True, blank=True))], options={b'db_table': b'villagesummary_eq', 
        b'managed': True}),
     migrations.CreateModel(name=b'WrlAdmbndaInt', fields=[
      (
       b'ogc_fid', models.IntegerField(serialize=False, primary_key=True)),
      (
       b'wkb_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True)),
      (
       b'name_en', models.CharField(max_length=255, blank=True)),
      (
       b'continent', models.CharField(max_length=255, blank=True)),
      (
       b'name_prs', models.CharField(max_length=255, blank=True)),
      (
       b'name_ps', models.CharField(max_length=255, blank=True)),
      (
       b'shape_length', models.FloatField(null=True, blank=True)),
      (
       b'shape_area', models.FloatField(null=True, blank=True))], options={b'db_table': b'wrl_admbnda_int', 
        b'managed': True}),
     migrations.AddField(model_name=b'afgavsa', name=b'basinmember', field=models.ForeignKey(related_name=b'basinmembersava', to=b'geodb.AfgShedaLvl4'))]