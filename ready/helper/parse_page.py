#coding=utf-8

from tools import *
from lxml import etree
from bs4 import BeautifulSoup

class Crawl_helper_parse_page:

    url = ''
    html = ''
    title = ''
    tag = []
    content = ''

    def __init__(self,url):
        self.url = url

    def getText(self,elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def getTitle(self,url = '',data = {},headers = {}):
        print 'in function getTitle'
        print url
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)

        self.html = response
        # print(response)
        print 'start etree 2'
        tree = etree.HTML(self.html)
        xpath_title = '//*[@id="article_details"]/div[1]/h1/span/a'
        print 'start etree 3'
        node = tree.xpath(xpath_title)[0]
        print '文章标题是： '
        print self.getText(node)

        xpath_content = '//*[@id="article_content"]'
        node_content = tree.xpath(xpath_content)[0]
        print '文章内容是： '
        print self.getText(node_content)


        print node
        print node.itertext()
        print self.getText(node)
        print node.text
        print node.tag
        print node.attrib
        print node.getchildren()
        print '========'
        for i in node.getchildren():
            print i.text
            print i.tag
            print i.attrib
            print self.getText(i)
            print '++++++'
        sys.exit()
        return  'title'
        pass


    def getTitle_soup(self,url = '',data = {},headers = {}):
        print url
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        title = soup.find("div","wznr").h2.string
        # print(title)

        if (title):
            return  title
        else:
            return "title not found!"

    def getTag(self,url = '',data = {},headers = {}):
        return ['tag1','tag2']
        pass

    def getTag_soup(self,url = '',data = {},headers = {}):
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        res_tags = []

        try:
            tags = soup.find("span","link_categories").contents
        except Exception , e:
            return []

        #print(tags)
        for tag_content in tags:
            if (tag_content.name == "a") and (tag_content.string != ""):
                res_tags.append(tag_content.string)

        #res_tags.append('from csdn')
        return  res_tags

    def getContent(self,url = '',data = {},headers = {}):
        return 'content'
        pass

    def parseContent(self, content = ''):
        constr = str(content)
        pos = constr.find("<br/>\n<p")
        if ( pos >= 0):
            #print pos
            constr = constr[pos + 6:]

        # Check which one is in front, trim from that one 
        list1 = []

        pos = constr.find("<p>【编辑推荐】")
        if (pos > 0): list1.append(pos)
        pos = constr.find("<p>【参会报名】")
        if (pos > 0): list1.append(pos)
        pos = constr.find("<p>【51CTO")
        if (pos > 0): list1.append(pos)
        pos = constr.find("<a class=\"dzdz\"")
        if (pos > 0): list1.append(pos)

        if (list1):
            pos = min(list1)
        else:
            pos = -1

        # pos2 = constr.find("<p>【参会报名】")
        # if (pos1 > 0 and pos2 > 0):
        #     pos = (pos1 > pos2 and pos2 or pos1)
        # elif (pos1 == -1 and pos2 == -1):
        #     pos = -1
        # else:
        #      pos = (pos1 > pos2 and pos1 or pos2)
           
        if (pos > 0):
            #print pos
            constr = constr[0 : pos - 1]
        return constr

    def getContent_soup(self,url = '',data = {},headers = {}):
        if (self.html):
            response = self.html
        else:
            if (url):
                response = Crawl_helper_tools_url.getCurl(url,data,headers)
            else:
                response = Crawl_helper_tools_url.getCurl(self.url,data,headers)
        if(response == 'fail'):
            return 'FAIL'

        self.html = response
        soup = BeautifulSoup(self.html,"lxml")
        contents = soup.find("div","zwnr")

        if (contents):
            return  self.parseContent(contents)
        else:
            return "content not found!"



