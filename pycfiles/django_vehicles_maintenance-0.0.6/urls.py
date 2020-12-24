# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\maintenance\django_vehicles_maintenance\maintenance\urls.py
# Compiled at: 2015-01-05 21:15:22
from django.conf.urls import patterns, include, url
from maintenance.main import views
from django.conf import settings
from django.views.generic.simple import direct_to_template
from maintenance.main.forms import *
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('^login/$', views.ingresar), url('^logout/$', views.logoutUser), url('^reporte/(.*)$', views.chassis_maintenanceReportView), url('^CarburetionTankReport/(.*)$', views.carburetion_tank_maintenanceReportView), url('^StorageTankReport/(.*)$', views.storage_tank_maintenanceReportView), url('^RadioReport/(.*)$', views.radio_maintenanceReportView), (
 '^ServicesGroup/New/$', views.services_groupInline_formset), (
 '^ServicesGroup/(?P<id>\\d+)/$', views.services_groupInline_formset), (
 '^ServicesGroup/Delete/(?P<id>\\d+)/$', views.delete_services_group), (
 '^servicesView/$', views.servicesView), (
 '^Service/new/$', views.service_manageView, {}, 'service_new'), (
 '^Service/edit/(?P<id>\\d+)/$', views.service_manageView, {}, 'service_edit'), (
 '^Service/Delete/(?P<id>\\d+)/$', views.delete_service), (
 '^Garages/$', views.garagesView), (
 '^Garage/New/$', views.garage_manageView), (
 '^Garage/(?P<id>\\d+)/$', views.garage_manageView), (
 '^Garage/Delete/(?P<id>\\d+)/$', views.delete_garageView), (
 '^Chassises/$', views.chassisesView), (
 '^Chassis/(?P<id>\\d+)/$', views.chassis_manageView), (
 '^Chassis/New/$', views.chassis_manageView), (
 '^Chassis/Delete/(?P<id>\\d+)/$', views.delete_chassis), (
 '^mantenimientos_chasis/(.*)', views.chassis_maintenanceView), (
 '^ChassisMaintenance/New/(?P<chassis_id>\\d+)/$', views.chassis_maintenace_Inline_formset), (
 '^ChassisMaintenance/(?P<id>\\d+)/(?P<chassis_id>\\d+)/$', views.chassis_maintenace_Inline_formset), (
 '^ChassisMaintenance/delete/(?P<id>\\d+)/(?P<chassis_id>\\d+)/$', views.delete_chassis_maintenance), (
 '^CarburetionTanks/$', views.carburetion_tanksView), (
 '^mantenimientos_TanqueCarburacion/(.*)', views.carburetion_tank_maintenanceView), (
 '^CarburetionTank/New/$', views.carburetion_tank_manageView), (
 '^CarburetionTank/(?P<id>\\d+)/$', views.carburetion_tank_manageView), (
 '^CarburetionTankMaintenace/New/(?P<carburetion_tank_id>\\d+)/$', views.carburetion_tank_maintenance_Inline_formset), (
 '^CarburetionTankMaintenace/(?P<id>\\d+)/(?P<carburetion_tank_id>\\d+)/$', views.carburetion_tank_maintenance_Inline_formset), (
 '^CarburetionTankMaintenace/Delete/(?P<id>\\d+)/(?P<carburetion_tank_id>\\d+)/$', views.delete_carburetion_tank_maintenance), (
 '^CarburetionTank/Delete/(?P<id>\\d+)/$', views.delete_carburetion_tank), (
 '^StorageTanks/$', views.storage_tanksView), (
 '^mantenimientos_TanqueAlmacenamiento/(.*)', views.storage_tank_maintenanceView), (
 '^StorageTankMaintenace/New/(?P<storage_tank_id>\\d+)/$', views.storage_tank_maintenance_Inline_formset), (
 '^StorageTankMaintenace/(?P<id>\\d+)/(?P<storage_tank_id>\\d+)/', views.storage_tank_maintenance_Inline_formset), (
 '^StorageTankMaintenace/Delete/(?P<id>\\d+)/(?P<storage_tank_id>\\d+)/$', views.delete_storage_maintenance), (
 '^StorageTank/Delete/(?P<id>\\d+)/$', views.delete_storage_tank), (
 '^Vehicle/(?P<id>\\d+)/', views.vehicle_manageView), (
 '^Vehicle/New/', views.vehicle_manageView), (
 '^Vehicle/Delete/(?P<id>\\d+)/$', views.delete_vehicle, {}, 'vehicle_delete'), (
 '^VehicleDetails/(.*)', views.vehicle_details), (
 '^$', views.index), (
 '^Radios/$', views.radiosView), (
 '^Radio/new/$', views.radio_manageView, {}, 'radio_new'), (
 '^Radio/edit/(?P<id>\\d+)/$', views.radio_manageView, {}, 'radio_edit'), (
 '^Radio/Delete/(?P<id>\\d+)/$', views.delete_radio), (
 '^RadioMaintenances/(.*)', views.radio_maintenanceView), (
 '^RadioMaintenance/(?P<id>\\d+)/(?P<radio_id>\\d+)/$', views.radio_maintenance_Inline_formset), (
 '^RadioMaintenance/New/(?P<radio_id>\\d+)/$', views.radio_maintenance_Inline_formset), (
 '^RadioMaintenance/Delete/(?P<id>\\d+)/(?P<radio_id>\\d+)/$', views.delete_radio_maintenance), (
 '^TanqueAlmacenamiento/new/$', views.storage_tank_manageView, {}, 'storage_tank_new'), (
 '^TanqueAlmacenamiento/edit/(?P<id>\\d+)/$', views.storage_tank_manageView, {}, 'storage_tank_edit'), (
 '^Chasis/new/$', views.chassis_manageView, {}, 'chassis_new'), (
 '^Chasis/edit/(?P<id>\\d+)/$', views.chassis_manageView, {}, 'chassis_edit'), (
 '^ChasisMaintenanceS/delete/(?P<id>\\d+)/$', views.delete_chassis_maintenanceS, {}, 'delete_chassis_maintenanceS'), (
 '^ServicesGroup/(?P<id>\\d+)/$', views.service_group_inlineView, {}, 'Service_group_inlineView'), url('^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), url('^admin/', include(admin.site.urls)))