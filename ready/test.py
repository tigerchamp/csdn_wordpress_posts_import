#coding=utf-8
import sys
# import urllib
# import urllib2
# import cookielib
from helper.tools import *
from helper.parse_page import *
from helper.translate import *
from lxml import etree
import json
import random

###
# The process is like this:
# 1. getCurl to get article list and their urls
# 2. Parse_page to get title/content from each url
# 3. Translate Chinese title to pinyin
# 4. Post to WordPress
###

### run log
# 20180109
# 20180609
# 20180701
###
reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(2000)

wp_url = "http://www.zizaicloud.com/wp-json/wp/v2/posts"
wp_url_tags = "http://www.zizaicloud.com/wp-json/wp/v2/tags"
username = "admin"

##### change before submitting #####
password = "" 
##### change before submitting #####


wp_data = {}
wp_headers = {}
old_tags = {}

# todo 先获取所有的 old tags
# res_old_tags = Crawl_helper_tools_url.http_auth_handle_get_tag(wp_url_tags,wp_data)
# if (res_old_tags == "fail"):
# 	print('获取标签失败')
# 	sys.exit()
# decode_res_tags = json.loads(res_old_tags)
# for res_tag in decode_res_tags:
# 	old_tags[res_tag['name']] = res_tag['id']
# print('已经存在的标签列表：')
# print(old_tags)

# url = 'http://cloud.51cto.com/col/384'
url = 'http://other.51cto.com/php/get_category_new_articles_list.php'
root_url = 'http://other.51cto.com/'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : 'http://www.zizaicloud.com'}


def importByCategory(cto_type_id = '', wp_cate_id = ''):

	params = {'page':2, 'type_id':cto_type_id}	# page doesn't work... need to click listmore on the first page to get more articles

	crawl_url = Crawl_helper_tools_url(url,root_url)
	artlist_json = crawl_url.getCurl(url, params, headers)

	#print html
	if artlist_json == '' or artlist_json == 'None':
		print 'REST api get json failed'
		sys.exit()

	# print html

	art_list = json.loads(artlist_json)

	print '==========='
	#print art_list[0][1]['url']

	trans = Baidu_Translation()

	for article in art_list[0]:
		#	html = crawl_url.getCurl(article['url'], {}, headers)
		#	tree = etree.HTML(html)
		#	crawl_url.parse_html_page_count(tree,"//div[@class='wznr']")
		try:
			parse_page = Crawl_helper_parse_page(article['url'])
			title = parse_page.getTitle_soup()
			content = parse_page.getContent_soup()

			print "====== a new article ==========="
			# print article['url']
			# print "===title===="
			# print title
			# print "====content===="
			# print content
		except Exception , e:
			print 'except 内容异常....',e
			continue

		# page_cates = next_page_crawl_url.getCates()

		content = content + "<br><p>此文章转自51CTO 原文网址: <a target=\"_blank\" href=\"" + article['url'] + "\">" + article['url'] + "</a></p><br>"

		wp_data['status'] = "publish"
		wp_data['title'] = title
		wp_data['content'] = content
		wp_data['author'] = 1
		wp_data['categories[0]'] = wp_cate_id

		try:
			slug = trans.GetResult(title)	#Tanslate Chinese title to Pinyin words, this will be used as %post_name% in url
		except Exception as e:
			slug = '*err*'

		if (slug != '*err*'):
			if (len(slug) > 20):
				slug = slug[0: slug.find(' ', 19)]
			wp_data['slug'] = '-'.join(slug.split(' ')) + '-' + str(random.randint(0,999))
			print wp_data['slug']


		# for tag_i in range(len(page_tags)):
		#     print(page_tags[tag_i])
		#     wp_data["tags["+str(tag_i)+"]"] = old_tags[page_tags[tag_i].decode('utf-8')]

		# todo 爬虫 添加至 github
		# todo 源代码 带有 script 在 wp中显示有问题

		#print('===创建文章 参数===')
		
		#print(wp_data['title'])
		res = Crawl_helper_tools_url.http_auth(username, password, wp_url, wp_data, wp_headers)
		if (res == "fail"):
		    print(title + "添加失败")

#51cto_type_ids = {'云资讯':'384', '云趋势':'385', '云应用':'386', '云安全':'387', '云开发':'389', '半月刊':'1733'}
#wp_cate_ids = {'资讯':'10', '技术':'18', '安全':'19'}
cate_mapping = {'384':'10', '385':'10', '386':'10', '387':'19','389':'18', '1733':'10'}

# wp_cate_id = "10"
#cto_type_id = 384	#not used at this moment, just for reminding me to change type_id in params

theMap = cate_mapping.iteritems();

for k, v in theMap:
	importByCategory(k, v)

print 'END'
sys.exit()