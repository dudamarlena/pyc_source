# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/user/workspace/eldermatics/eldermatics/eldermatics/blog/views.py
# Compiled at: 2017-04-27 03:53:39
from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import Blog
from django.db import connection
from category.models import Categories
import datetime, itertools
from django.contrib.sites.shortcuts import get_current_site
import sys
from msg_management.models import Error_Mngmnt
reload(sys)
sys.setdefaultencoding('utf8')

def success_parameter(body, type, status):
    json_obj = {'success': True, 'body': body, 'type': type, 'status': status}
    return json_obj


def failure_parameter(body, type, status):
    json_obj = {'success': False, 'body': body, 'type': type, 'status': status}
    return json_obj


@api_view(['GET'])
def blog_listing_page_v1(request, page_no, blog_limit):
    full_url = ('').join([
     'http://', get_current_site(request).domain, '/uploads/listing_'])
    if request.method == 'GET':
        try:
            all_blog_data = {}
            start_id = int(page_no) * int(blog_limit)
            all_blogs_list = []
            with connection.cursor() as (cursor):
                cursor.execute('SELECT slug, title, modified_date, upload_image, category FROM blog_blog WHERE                               status = 1 AND soft_delete = 1 ORDER BY modified_date DESC LIMIT %s OFFSET %s', (int(blog_limit), start_id))
                row = cursor.fetchall()
            all_blogs = list(row)
            for blog_entry in all_blogs:
                blog_details_dict = {}
                blog_entry = list(blog_entry)
                appended_pic_url = full_url + str(blog_entry[3])
                blog_entry[3] = unicode(appended_pic_url, 'utf-8')
                blog_details_dict['slug'] = blog_entry[0]
                blog_details_dict['name'] = blog_entry[1]
                day = int(blog_entry[2].strftime('%d'))
                if day % 10 == 1:
                    blog_entry[2] = blog_entry[2].strftime('%B %dst, %Y')
                if day % 10 == 2:
                    blog_entry[2] = blog_entry[2].strftime('%B %dnd, %Y')
                if day % 10 == 3:
                    blog_entry[2] = blog_entry[2].strftime('%B %drd, %Y')
                if day % 10 >= 4 or day % 10 == 0:
                    blog_entry[2] = blog_entry[2].strftime('%B %dth, %Y')
                blog_details_dict['created_date'] = blog_entry[2]
                blog_details_dict['image_url'] = blog_entry[3]
                blog_details_dict['category'] = blog_entry[4]
                blog_category_name = Categories.objects.values_list('title').filter(id=blog_entry[4]).order_by('priority')
                blog_details_dict['blog_category_name'] = blog_category_name[0][0]
                all_blogs_list.append(blog_details_dict)

            all_blog_data['blog_listing'] = all_blogs_list
            all_blogs_count = Blog.objects.values_list('id').filter(status=True, soft_delete='1')
            all_blogs_count = len(all_blogs_count)
            all_blog_data['all_blog_count'] = all_blogs_count
            articledetails = {}
            category_ids = Categories.objects.values_list('id', 'title', 'slug').filter(soft_delete='1').order_by('priority')
            if category_ids:
                data_list = []
                for single_id in category_ids:
                    data_json = {}
                    articlenumbers = Blog.objects.values_list('id', 'title').filter(status=True, soft_delete='1', category=str(single_id[0]))
                    if len(articlenumbers) == 0:
                        continue
                    data_json['slug'] = single_id[2]
                    data_json['article_name'] = single_id[1]
                    articledetails[single_id[1]] = str(len(articlenumbers))
                    data_json['article_count'] = articledetails[single_id[1]]
                    data_list.append(data_json)

                all_blog_data['articledetails'] = data_list
            year_month_blog = []
            with connection.cursor() as (cursor):
                cursor.execute('SELECT YEAR AS YEAR, GROUP_CONCAT( DATE_FORMAT( modified_date, "%M" )                             ORDER BY MONTH(modified_date) DESC ) AS published FROM `blog_blog` WHERE soft_delete = 1 AND status = 1 GROUP BY YEAR                             ORDER BY YEAR DESC')
                datewise_data = cursor.fetchall()
            year_month_list = []
            for year in datewise_data:
                month_name_count_list = []
                year_month_json = {}
                year_month_json['year'] = year[0]
                if ',' in year[1]:
                    month_name = year[1].split(',')
                    counter = []
                    for flag in itertools.groupby(month_name):
                        counter.append((flag[0], len(list(flag[1]))))

                    for month in counter:
                        internal_json_data = {}
                        internal_json_data['month_name'] = month[0]
                        internal_json_data['month_count'] = month[1]
                        month_name_count_list.append(internal_json_data)

                    year_month_json['data'] = month_name_count_list
                else:
                    internal_json_data = {}
                    internal_json_data['month_name'] = year[1]
                    internal_json_data['month_count'] = '1'
                    month_name_count_list.append(internal_json_data)
                    year_month_json['data'] = month_name_count_list
                year_month_list.append(year_month_json)
                year_month_blog.append(year)

            all_blog_data['date_wise_data'] = year_month_list
            with connection.cursor() as (cursor):
                cursor.execute('SELECT slug, title, modified_date, upload_image, category,                     did_you_know FROM blog_blog WHERE did_you_know = 1 AND status = 1 AND                     soft_delete = 1 ORDER BY modified_date DESC')
                row = cursor.fetchone()
            if row:
                did_you_know = list(row)
            else:
                did_you_know = []
            did_you_know_json = {}
            if did_you_know:
                did_you_know = list(did_you_know)
                did_you_know[3] = full_url + did_you_know[3]
                did_you_know_json['slug'] = did_you_know[0]
                did_you_know_json['name'] = did_you_know[1]
                did_you_know[2] = did_you_know[2].strftime('%m/%d/%y')
                did_you_know_json['created_date'] = did_you_know[2]
                did_you_know_json['image_url'] = did_you_know[3]
                did_you_know_json['category'] = did_you_know[4]
            else:
                did_you_know = 'No record found.'
            all_blog_data['did_you_know'] = did_you_know_json
            all_blog_data = success_parameter(all_blog_data, {'message': 'Blogs Data Recieved Successfully'}, 200)
        except Exception:
            all_blog_data = {}
            error_msg = Error_Mngmnt.objects.filter(error_code='BlogList')
            error_msg = error_msg[0].error_msg
            all_blog_data = failure_parameter(all_blog_data, {'message': error_msg}, 200)

        return Response(all_blog_data)


@api_view(['GET'])
def blog_category_listing_page_v1(request, article_slug, start_page, blog_limit):
    if request.method == 'GET':
        try:
            blog_category_id = Categories.objects.values_list('id').filter(slug=article_slug)
            article_id = blog_category_id[0][0]
            full_url = ('').join([
             'http://', get_current_site(request).domain, '/uploads/listing_'])
            category_blog_data = {}
            start_page = int(start_page) * int(blog_limit)
            category_blogs = []
            with connection.cursor() as (cursor):
                cursor.execute('SELECT slug, title, modified_date, upload_image, category                               FROM blog_blog WHERE category = %s AND status = 1 AND soft_delete = 1                                ORDER BY modified_date DESC                               LIMIT %s OFFSET %s ', (article_id, int(blog_limit), start_page))
                row = cursor.fetchall()
            blog_category_name = Categories.objects.values_list('title').filter(id=article_id).order_by('priority')
            category_blog_data['blog_category_name'] = blog_category_name[0][0]
            blogcategorylisting = list(row)
            blogcategory_count = len(blogcategorylisting)
            for items in blogcategorylisting:
                row = Blog.objects.values_list('id').filter(category=article_id, status=1, soft_delete=1)
                blogcategory_count = len(row)
                category_blog_data['blog_listing_count'] = blogcategory_count
                if blogcategory_count == 0:
                    continue
                blog_details_dict = {}
                items = list(items)
                appended_pic_url = full_url + str(items[3])
                items[3] = unicode(appended_pic_url, 'utf-8')
                blog_details_dict['slug'] = items[0]
                blog_details_dict['name'] = items[1]
                day = int(items[2].strftime('%d'))
                if day % 10 == 1:
                    items[2] = items[2].strftime('%B %dst, %Y')
                if day % 10 == 2:
                    items[2] = items[2].strftime('%B %dnd, %Y')
                if day % 10 == 3:
                    items[2] = items[2].strftime('%B %drd, %Y')
                if day % 10 >= 4 or day % 10 == 0:
                    items[2] = items[2].strftime('%B %dth, %Y')
                blog_details_dict['created_date'] = items[2]
                blog_details_dict['image_url'] = items[3]
                blog_details_dict['category'] = items[4]
                category_blogs.append(blog_details_dict)

            category_blog_data['blog_listing'] = category_blogs
            with connection.cursor() as (cursor):
                cursor.execute('SELECT slug, title, modified_date, upload_image, category,                     did_you_know FROM blog_blog WHERE did_you_know = 1 AND status = 1 AND                     soft_delete = 1 ORDER BY modified_date DESC')
                row = cursor.fetchone()
            if row:
                did_you_know = list(row)
            else:
                did_you_know = []
            did_you_know_json = {}
            if did_you_know:
                did_you_know = list(did_you_know)
                did_you_know[3] = full_url + did_you_know[3]
                did_you_know_json['slug'] = did_you_know[0]
                did_you_know_json['name'] = did_you_know[1]
                did_you_know[2] = did_you_know[2].strftime('%m/%d/%y')
                did_you_know_json['created_date'] = did_you_know[2]
                did_you_know_json['image_url'] = did_you_know[3]
                did_you_know_json['category'] = did_you_know[4]
            else:
                did_you_know_json = 'No record found.'
            category_blog_data['did_you_know'] = did_you_know_json
            category_blog_data = success_parameter(category_blog_data, {'message': 'Blogs Data Recieved Successfully'}, 200)
        except Exception:
            category_blog_data = {}
            error_msg = Error_Mngmnt.objects.filter(error_code='BlogCategory')
            error_msg = error_msg[0].error_msg
            category_blog_data = failure_parameter(category_blog_data, {'message': error_msg}, 200)

        return Response(category_blog_data)


@api_view(['GET'])
def blog_date_listing_page_v1(request, blogyear, blogmonth, start_page, blog_limit):
    if request.method == 'GET':
        try:
            full_url = ('').join([
             'http://', get_current_site(request).domain, '/uploads/listing_'])
            date_blog_data = {}
            start_page = int(start_page) * int(blog_limit)
            date_blogs = []
            month_number = datetime.datetime.strptime(blogmonth, '%B')
            month_number = month_number.month
            with connection.cursor() as (cursor):
                cursor.execute('SELECT id, title, modified_date, upload_image, category, slug FROM blog_blog WHERE soft_delete=1 AND                               status=1 AND MONTH(`modified_date`) ="%s" AND YEAR(`modified_date`) ="%s" ORDER BY                               modified_date DESC LIMIT %s OFFSET %s', (month_number, int(blogyear), int(blog_limit), start_page))
                blogdatelisting = cursor.fetchall()
            blogdatelisting = list(blogdatelisting)
            blogdatelisting_count = len(blogdatelisting)
            for items in blogdatelisting:
                blog_details_dict = {}
                items = list(items)
                appended_pic_url = full_url + str(items[3])
                items[3] = unicode(appended_pic_url, 'utf-8')
                blog_details_dict['id'] = items[0]
                blog_details_dict['name'] = items[1]
                day = int(items[2].strftime('%d'))
                if day % 10 == 1:
                    items[2] = items[2].strftime('%B %dst, %Y')
                if day % 10 == 2:
                    items[2] = items[2].strftime('%B %dnd, %Y')
                if day % 10 == 3:
                    items[2] = items[2].strftime('%B %drd, %Y')
                if day % 10 >= 4 or day % 10 == 0:
                    items[2] = items[2].strftime('%B %dth, %Y')
                blog_details_dict['created_date'] = items[2]
                blog_details_dict['image_url'] = items[3]
                blog_details_dict['category'] = items[4]
                blog_details_dict['slug'] = items[5]
                blog_category_name = Categories.objects.values_list('title').filter(id=items[4], soft_delete=1).order_by('priority')
                blog_details_dict['blog_category_name'] = blog_category_name[0][0]
                date_blogs.append(blog_details_dict)

            date_blog_data['blog_listing'] = date_blogs
            with connection.cursor() as (cursor):
                cursor.execute('SELECT id FROM blog_blog WHERE soft_delete=1 AND                               status=1 AND MONTH(`modified_date`) ="%s"                               AND YEAR(`modified_date`) ="%s" ORDER BY modified_date DESC', (month_number, int(blogyear)))
                row = cursor.fetchall()
            blogdatelisting_count = len(row)
            date_blog_data['blog_listing_count'] = blogdatelisting_count
            with connection.cursor() as (cursor):
                cursor.execute('SELECT id, title, modified_date, upload_image, category, slug                     did_you_know FROM blog_blog WHERE did_you_know = 1 AND status = 1 AND                     soft_delete = 1 ORDER BY modified_date DESC')
                row = cursor.fetchone()
            try:
                did_you_know = list(row)
                did_you_know_json = {}
                did_you_know = list(did_you_know)
                did_you_know[3] = full_url + did_you_know[3]
                did_you_know_json['id'] = did_you_know[0]
                did_you_know_json['name'] = did_you_know[1]
                did_you_know[2] = did_you_know[2].strftime('%m/%d/%y')
                did_you_know_json['created_date'] = did_you_know[2]
                did_you_know_json['image_url'] = did_you_know[3]
                did_you_know_json['category'] = did_you_know[4]
                did_you_know_json['slug'] = did_you_know[5]
            except Exception:
                did_you_know_json = 'No record found.'

            date_blog_data['did_you_know'] = did_you_know_json
            date_blog_data = success_parameter(date_blog_data, {'message': 'Blogs Data Recieved Successfully'}, 200)
        except Exception:
            date_blog_data = {}
            error_msg = Error_Mngmnt.objects.filter(error_code='BlogDate')
            error_msg = error_msg[0].error_msg
            date_blog_data = failure_parameter(date_blog_data, {'message': error_msg}, 200)

        return Response(date_blog_data)


@api_view(['GET'])
def blog_detail_v1(request, blog_slug):
    id_current_article = blog_slug
    if request.method == 'GET':
        try:
            blog_detail_page = {}
            full_url = ('').join([
             'http://', get_current_site(request).domain, '/uploads/'])
            blogcategorylisting = Blog.objects.values_list('id', 'title', 'modified_date', 'location', 'short_description', 'author', 'image_credit', 'category', 'description', 'upload_image', 'meta_title', 'meta_keywords', 'meta_description', 'image_title', 'alt_text', 'og_title', 'og_description', 'og_url', 'meta_robot', 'canonical_url', 'slug').filter(slug=blog_slug, status=True, soft_delete='1')
            items = blogcategorylisting[0]
            blog_details_dict = {}
            items = list(items)
            appended_pic_url = full_url + str(items[9])
            items[9] = unicode(appended_pic_url, 'utf-8')
            blog_details_dict['id'] = items[0]
            id_current_article = items[0]
            blog_details_dict['name'] = items[1]
            day = int(items[2].strftime('%d'))
            if day % 10 == 1:
                items[2] = items[2].strftime('%B %dst, %Y')
            if day % 10 == 2:
                items[2] = items[2].strftime('%B %dnd, %Y')
            if day % 10 == 3:
                items[2] = items[2].strftime('%B %drd, %Y')
            if day % 10 >= 4 or day % 10 == 0:
                items[2] = items[2].strftime('%B %dth, %Y')
            category_name = Categories.objects.values_list('title', 'id').filter(id=items[7], soft_delete='1').order_by('priority')
            category_id = category_name[0][1]
            blog_details_dict['created_date'] = items[2]
            blog_details_dict['location'] = items[3]
            blog_details_dict['short_description'] = items[4]
            blog_details_dict['author'] = items[5]
            blog_details_dict['image_credit'] = items[6]
            blog_details_dict['category'] = category_name[0][0]
            blog_details_dict['description'] = items[8]
            blog_details_dict['image_url'] = items[9]
            blog_details_dict['meta_title'] = items[10]
            blog_details_dict['meta_keywords'] = items[11]
            blog_details_dict['meta_description'] = items[12]
            blog_details_dict['image_title'] = items[13]
            blog_details_dict['alt_text'] = items[14]
            blog_details_dict['og_title'] = items[15]
            blog_details_dict['og_description'] = items[16]
            blog_details_dict['og_url'] = items[17]
            blog_details_dict['meta_robot'] = items[18]
            if '1' in items[18]:
                blog_details_dict['allow_indexing_page'] = True
            else:
                blog_details_dict['allow_indexing_page'] = False
            if '2' in items[18]:
                blog_details_dict['allow_links_on_page\u2028'] = True
            else:
                blog_details_dict['allow_links_on_page\u2028'] = False
            if '3' in items[18]:
                blog_details_dict['prevent_indexing_page\u2028'] = True
            else:
                blog_details_dict['prevent_indexing_page\u2028'] = False
            if '4' in items[18]:
                blog_details_dict['prevent_links_on_page\u2028'] = True
            else:
                blog_details_dict['prevent_links_on_page\u2028'] = False
            blog_details_dict['canonical_url'] = items[19]
            blog_details_dict['slug'] = items[20]
            blog_detail_page['blog_detail'] = blog_details_dict
            full_url = ('').join([
             'http://', get_current_site(request).domain, '/uploads/listing_'])
            with connection.cursor() as (cursor):
                cursor.execute('SELECT slug, title, modified_date, upload_image, category,                 did_you_know FROM blog_blog WHERE did_you_know = 1 AND status = 1 AND                 soft_delete = 1 ORDER BY modified_date DESC')
                row = cursor.fetchone()
            if row:
                did_you_know = list(row)
            else:
                did_you_know = []
            did_you_know_json = {}
            if did_you_know:
                did_you_know = list(did_you_know)
                did_you_know[3] = full_url + did_you_know[3]
                did_you_know_json['slug'] = did_you_know[0]
                did_you_know_json['name'] = did_you_know[1]
                did_you_know[2] = did_you_know[2].strftime('%m/%d/%y')
                did_you_know_json['created_date'] = did_you_know[2]
                did_you_know_json['image_url'] = did_you_know[3]
                did_you_know_json['category'] = did_you_know[4]
            else:
                did_you_know_json = 'No record found.'
            blog_detail_page['did_you_know'] = did_you_know_json
            articledetails = {}
            category_ids = Categories.objects.values_list('id', 'title', 'slug').filter(soft_delete='1').order_by('priority')
            if category_ids:
                data_list = []
                for item in category_ids:
                    data_json = {}
                    articlenumbers = Blog.objects.values_list('slug', 'title').filter(status=True, soft_delete='1', category=str(item[0]))
                    if len(articlenumbers) == 0:
                        continue
                    data_json['slug'] = item[2]
                    data_json['article_name'] = item[1]
                    articledetails[item[1]] = str(len(articlenumbers))
                    data_json['article_count'] = articledetails[item[1]]
                    data_list.append(data_json)

                blog_detail_page['articledetails'] = data_list
            year_month_blog = []
            with connection.cursor() as (cursor):
                cursor.execute('SELECT YEAR AS YEAR, GROUP_CONCAT( DATE_FORMAT( modified_date, "%M" )                             ORDER BY MONTH(modified_date) DESC ) AS published FROM `blog_blog` WHERE soft_delete = 1 AND status = 1 GROUP BY YEAR                             ORDER BY YEAR DESC')
                row = cursor.fetchall()
            year_month_list = []
            for item in row:
                month_name_count_list = []
                year_month_json = {}
                year_month_json['year'] = item[0]
                if ',' in item[1]:
                    month_name = item[1].split(',')
                    counter = []
                    for g in itertools.groupby(month_name):
                        counter.append((g[0], len(list(g[1]))))

                    for i in counter:
                        internal_json_data = {}
                        internal_json_data['month_name'] = i[0]
                        internal_json_data['month_count'] = i[1]
                        month_name_count_list.append(internal_json_data)

                    year_month_json['data'] = month_name_count_list
                else:
                    internal_json_data = {}
                    internal_json_data['month_name'] = item[1]
                    internal_json_data['month_count'] = '1'
                    month_name_count_list.append(internal_json_data)
                    year_month_json['data'] = month_name_count_list
                year_month_list.append(year_month_json)
                year_month_blog.append(item)

            blog_data = Blog.objects.values_list('slug', 'title', 'short_description', 'description', 'upload_image').filter(category=category_id, soft_delete=1, status=1)
            next_one = {}
            previous_one = {}
            if len(blog_data) is 1:
                blog_data = list(blog_data[0])
                next_one['slug'] = blog_data[0]
                next_one['title'] = blog_data[1]
                next_one['short_description'] = blog_data[2]
                next_one['description'] = blog_data[3]
                blog_data[4] = full_url + blog_data[4]
                next_one['image'] = blog_data[4]
                blog_detail_page['next_one'] = next_one
                blog_detail_page['previous_one'] = next_one
            elif len(blog_data) is 2:
                blog_data = Blog.objects.values_list('slug', 'title', 'short_description', 'description', 'upload_image').filter(category=category_id, soft_delete=1, status=1).exclude(id=id_current_article)
                blog_data = list(blog_data[0])
                next_one['slug'] = blog_data[0]
                next_one['title'] = blog_data[1]
                next_one['short_description'] = blog_data[2]
                next_one['description'] = blog_data[3]
                blog_data[4] = full_url + blog_data[4]
                next_one['image'] = blog_data[4]
                blog_detail_page['next_one'] = next_one
                blog_detail_page['previous_one'] = next_one
            elif len(blog_data) > 2:
                with connection.cursor() as (cursor):
                    cursor.execute('SELECT slug, title, short_description, description, upload_image                                FROM blog_blog WHERE soft_delete=1 AND                                               status=1 AND id < %s AND                                category = (select category from blog_blog where id = %s )                                ORDER BY id DESC', (int(id_current_article), int(id_current_article)))
                    row = cursor.fetchall()
                all_blogs = list(row)
                ifSmallestID = len(all_blogs)
                if ifSmallestID < 1:
                    with connection.cursor() as (cursor):
                        cursor.execute(('SELECT slug, title, short_description, description, upload_image                                    FROM blog_blog WHERE soft_delete=1 AND                                                   status=1 AND id = (SELECT MAX(id) FROM blog_blog WHERE                                     soft_delete = 1 AND status = 1 AND category = (select category from blog_blog where id = {0}))                                    ORDER BY id DESC').format(str(id_current_article)))
                        row = cursor.fetchall()
                    all_blogs = list(row[0])
                else:
                    all_blogs = list(all_blogs[0])
                previous_one['slug'] = all_blogs[0]
                previous_one['title'] = all_blogs[1]
                previous_one['short_description'] = all_blogs[2]
                previous_one['description'] = all_blogs[3]
                all_blogs[4] = full_url + all_blogs[4]
                previous_one['image'] = all_blogs[4]
                blog_detail_page['previous_one'] = previous_one
                with connection.cursor() as (cursor):
                    cursor.execute('SELECT slug, title, short_description, description, upload_image                                FROM blog_blog WHERE soft_delete=1 AND                                               status=1 AND id > %s AND                                category = (select category from blog_blog where id = %s )                                ORDER BY id ASC', (int(id_current_article), int(id_current_article)))
                    row = cursor.fetchall()
                all_blogs = list(row)
                ifSmallestID = len(all_blogs)
                if ifSmallestID < 1:
                    with connection.cursor() as (cursor):
                        cursor.execute(('SELECT slug, title, short_description, description, upload_image                                    FROM blog_blog WHERE soft_delete=1 AND                                                   status=1 AND id = (SELECT MIN(id) FROM blog_blog WHERE                                     soft_delete=1 AND status=1 AND category = (select category from blog_blog where id = {0}))                                    ORDER BY id ASC').format(str(id_current_article)))
                        row = cursor.fetchall()
                    all_blogs = list(row[0])
                else:
                    all_blogs = list(all_blogs[0])
                next_one['slug'] = all_blogs[0]
                next_one['title'] = all_blogs[1]
                next_one['short_description'] = all_blogs[2]
                next_one['description'] = all_blogs[3]
                all_blogs[4] = full_url + all_blogs[4]
                next_one['image'] = all_blogs[4]
                blog_detail_page['next_one'] = next_one
            blog_detail_page['date_wise_data'] = year_month_list
            blog_detail_page = success_parameter(blog_detail_page, {'message': 'Blogs Data Recieved Successfully'}, 200)
        except Exception:
            blog_detail_page = {}
            error_msg = Error_Mngmnt.objects.filter(error_code='BlogDetail')
            error_msg = error_msg[0].error_msg
            blog_detail_page = failure_parameter(blog_detail_page, {'message': error_msg}, 200)

        return Response(blog_detail_page)