# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0001_initial.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion, smart_selects.db_fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'ApplicationOption', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, unique=True, verbose_name=b'选项')),
      (
       b'order_by', models.IntegerField(verbose_name=b'顺序'))], options={b'ordering': [
                    b'order_by'], 
        b'db_table': b'bee_django_crm_application_options'}),
     migrations.CreateModel(name=b'ApplicationQuestion', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, unique=True, verbose_name=b'问题')),
      (
       b'order_by', models.IntegerField(verbose_name=b'顺序')),
      (
       b'input_type', models.IntegerField(choices=[(1, '输入框'), (2, '单选（圆钮）'), (3, '单选（下拉）'), (4, '多选（方钮）')], verbose_name=b'类型'))], options={b'ordering': [
                    b'order_by'], 
        b'db_table': b'bee_django_crm_application_question'}),
     migrations.CreateModel(name=b'City', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, null=True))], options={b'db_table': b'bee_django_crm_city'}),
     migrations.CreateModel(name=b'Contract', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, unique=True, verbose_name=b'合同名称')),
      (
       b'period', models.IntegerField(verbose_name=b'周期')),
      (
       b'duration', models.IntegerField(verbose_name=b'时长')),
      (
       b'price', models.FloatField(verbose_name=b'金额'))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_crm_contract'}),
     migrations.CreateModel(name=b'District', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, null=True)),
      (
       b'city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.City'))], options={b'db_table': b'bee_django_crm_district'}),
     migrations.CreateModel(name=b'Poster', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'is_show', models.BooleanField(default=False, verbose_name=b'是否显示')),
      (
       b'qrcode_width', models.IntegerField(default=0, null=True, verbose_name=b'二维码宽度')),
      (
       b'qrcode_height', models.IntegerField(default=0, null=True, verbose_name=b'二维码高度')),
      (
       b'qrcode_pos_x', models.IntegerField(default=0, null=True, verbose_name=b'二维码x轴坐标')),
      (
       b'qrcode_pos_y', models.IntegerField(default=0, null=True, verbose_name=b'二维码y轴坐标')),
      (
       b'qrcode_color', models.CharField(default=b'#000000', max_length=8, null=True, verbose_name=b'二维码颜色')),
      (
       b'photo', models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(b'media/crm/poster_photo'), upload_to=b''))], options={b'db_table': b'bee_django_crm_poster'}),
     migrations.CreateModel(name=b'PreUser', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'nickname', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'昵称')),
      (
       b'name', models.CharField(max_length=20, verbose_name=b'姓名')),
      (
       b'mobile', models.CharField(max_length=15, unique=True, verbose_name=b'电话')),
      (
       b'gender', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'性别')),
      (
       b'wx', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'微信')),
      (
       b'birthday', models.DateField(blank=True, null=True, verbose_name=b'出生日期')),
      (
       b'level', models.IntegerField(default=1, verbose_name=b'级别')),
      (
       b'grade', models.IntegerField(blank=True, null=True, verbose_name=b'意向')),
      (
       b'address', models.TextField(blank=True, null=True, verbose_name=b'地址')),
      (
       b'job', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'工作')),
      (
       b'email', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'邮箱')),
      (
       b'hobby', models.TextField(blank=True, null=True, verbose_name=b'爱好')),
      (
       b'married', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'婚姻状况')),
      (
       b'children', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'孩子状况')),
      (
       b'job_info', models.TextField(blank=True, null=True, verbose_name=b'工作详情')),
      (
       b'family', models.TextField(blank=True, null=True, verbose_name=b'家庭详情')),
      (
       b'contract_id', models.IntegerField(blank=True, null=True, verbose_name=b'合同')),
      (
       b'fee', models.FloatField(blank=True, null=True, verbose_name=b'缴费金额')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'备注')),
      (
       b'is_add_coin', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'加缦币')),
      (
       b'attended_date', models.DateField(blank=True, null=True, verbose_name=b'入学日期')),
      (
       b'pay_datetime', models.DateField(blank=True, null=True, verbose_name=b'缴费日期')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'applied_at', models.DateTimeField(null=True)),
      (
       b'paid_at', models.DateTimeField(null=True)),
      (
       b'city', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field=b'province', chained_model_field=b'province', null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.City', verbose_name=b'市'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_crm_preuser'}),
     migrations.CreateModel(name=b'PreUserApplication', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'answer', models.TextField()),
      (
       b'preuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_user_applications', to=b'bee_django_crm.PreUser')),
      (
       b'question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.ApplicationQuestion'))], options={b'db_table': b'bee_django_crm_preuser_application'}),
     migrations.CreateModel(name=b'PreUserContract', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'price', models.FloatField(verbose_name=b'实收金额')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'paid_at', models.DateTimeField(verbose_name=b'缴费日期')),
      (
       b'study_at', models.DateTimeField(blank=True, null=True, verbose_name=b'开课日期')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'备注')),
      (
       b'is_checked', models.BooleanField(default=False, verbose_name=b'审核')),
      (
       b'checked_at', models.DateTimeField(null=True)),
      (
       b'after_checked_at', models.DateTimeField(null=True)),
      (
       b'checked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.Contract', verbose_name=b'合同')),
      (
       b'preuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.PreUser'))], options={b'ordering': [
                    b'-paid_at', b'-created_at'], 
        b'db_table': b'bee_django_crm_preuser_contract'}),
     migrations.CreateModel(name=b'PreUserTrack', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'tracked_at', models.DateTimeField(verbose_name=b'联络时间')),
      (
       b'info', models.TextField(verbose_name=b'详情')),
      (
       b'created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_created_by_user', to=settings.AUTH_USER_MODEL)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_track_user', to=b'bee_django_crm.PreUser'))], options={b'db_table': b'bee_django_crm_preuser_track'}),
     migrations.CreateModel(name=b'Province', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, null=True))], options={b'db_table': b'bee_django_crm_province'}),
     migrations.CreateModel(name=b'Source', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=60, verbose_name=b'来源名称')),
      (
       b'reg_name', models.CharField(blank=True, max_length=60, null=True, verbose_name=b'注册页显示名称')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'is_poster', models.BooleanField(default=False, verbose_name=b'是否海报类型')),
      (
       b'is_show', models.BooleanField(default=False, verbose_name=b'编辑时是否显示'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_crm_source'}),
     migrations.AddField(model_name=b'preuser', name=b'province', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.Province', verbose_name=b'省')),
     migrations.AddField(model_name=b'preuser', name=b'referral_user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_crm_referral_user', to=settings.AUTH_USER_MODEL, verbose_name=b'转介人')),
     migrations.AddField(model_name=b'preuser', name=b'source', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.Source', verbose_name=b'来源')),
     migrations.AddField(model_name=b'poster', name=b'source', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.Source')),
     migrations.AddField(model_name=b'city', name=b'province', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.Province')),
     migrations.AddField(model_name=b'applicationoption', name=b'question', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.ApplicationQuestion', verbose_name=b'问题'))]