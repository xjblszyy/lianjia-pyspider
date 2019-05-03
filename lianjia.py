#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-27 10:25:03
# Project: lianjia


from itertools import islice
import re
from six import itervalues

from pyspider.libs.base_handler import *
import pymysql
from fake_useragent import UserAgent


# 设置代理
def get_proxy():
    return requests.get('http://localhost:5010/get/').text

# mysql 连接实例对象
class SQL():
    def __new__(cls):
    # 返回同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(SQL, cls).__new__(cls)
        return cls.instance
    
    #数据库初始化
    def __init__(self):
        #数据库连接相关信息
        self.hosts = '127.0.0.1'  
        self.username = 'root'
        self.password = '123456'
        self.database = 'lianjia'
        self.port = 3306
        self.connection = False
        try:
            self.conn = pymysql.connect(host=self.hosts,user=self.username,passwd=self.password,db= self.database,port=self.port,charset='utf8')
            self.cursor = self.conn.cursor()
            self.connection = True
        except Exception as e:
            print("Cannot Connect To Mysql!/n", e)

    def escape(self,string):
        return '%s' % string
    
    #插入数据到数据库   
    def insert(self, tablename=None, pk=None, **values):

        if self.connection: 
            tablename = self.escape(tablename)  
            _keys = ",".join(self.escape(k) for k in values)
            _values = ",".join(['%s',]*len(values))
            sql_query = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE house_id= (%s)" % (tablename,_keys,_values, pk)
            try:
                self.cursor.execute(sql_query,list(itervalues(values)))      
                self.conn.commit()
                return True
            except Exception as e:
                print("An Error Occured: ", e)
                return False


class Handler(BaseHandler):
    
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Host": "www.lianjia.com",
        "Referer": "https://www.lianjia.com/city/",
    }

    crawl_config = {
        # "headers": headers,
        # "proxy": get_proxy(),
    }

    @every(minutes=24 * 60)
    def on_start(self):  # 开始爬取的城市地址
        self.crawl('https://www.lianjia.com/city/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):  # 获取城市列表
        for each in response.doc('.city_list a[href^="http"]').items():
            url = each.attr.href
            print("{0}:{1}".format(each.text(), url))
            self.crawl(url+"ershoufang/", callback=self.city_page)

    @config(priority=2)
    def city_page(self, response):  # 进入城市房子信息，爬取区域信息
        content = response.doc('.position a[href^="http"]').items()  # 这是一个生成器，用islice做切片功能，去除第一个a链接，第一条是所有区域的房子，可以切片过滤这条内容
        for each in islice(content, 0, None):  
            print("{0}:{1}".format(each.text(), each.attr.href))
            self.crawl(each.attr.href, callback=self.area_page)
    
    @config(priority=3)
    def area_page(self, response):  # 选择区域后进去房子列表
        total_count = response.doc('.total span').text()  # 搜索到的房子的总计数量,分页是每页30条数据
        page = int(int(total_count)/30)
        if page >= 100:
            page = 100
        for pg in range(page):
            url = response.url + "pg{}/".format(pg+1)  # 每页的url
            self.crawl(url, callback=self.pagination_page)
        
    @config(priority=4)
    def pagination_page(self, response):  # 每页的信息
        content = response.doc('.title a[href^="http"]').items()
        for each in content:
            # print(each.attr.href)  # 房子的链接地址
            id = each.attr.href.split("/")[-1].split(".")[0]  # 房子的唯一id
            self.crawl(each.attr.href, callback=self.info_page)
            
    @config(priority=4)
    def info_page(self, response):  # 房子的详细信息
        re_data = {}
        # 数据
        url = response.url
        id = int(url.split("/")[-1].split(".")[0])
        title = response.doc('.main').text()
        house_price = response.doc('.price .total').text() + "万元"
        house_area = response.doc('.area .mainInfo').text()
        house_type = response.doc('.room .mainInfo').text()
        house_floor = response.doc('.room .subInfo').text()
        house_diretion = response.doc('.type .mainInfo').text()
        house_describle = response.doc('.content .title .sub').text()
        house_address = response.doc('.areaName .info').text().replace("\xa0", " ")
        house_man_name = response.doc('.brokerName .name').text()
        number = response.doc('.phone').text()
        house_man_numbers = re.findall('\d+', number)
        house_man_number = 0
        for i in house_man_numbers:
            if i.startswith("400"):   
                house_man_number = i
                
        # 图片
        images_list = []
        images = response.doc('.smallpic li').items()
        for image in images:
            images_list.append(image.attr["data-src"])

        re_data["house_id"] = str(id)
        re_data["title"] = title
        re_data["house_price"] = house_price
        re_data["house_area"] = house_area
        re_data["house_type"] = house_type
        re_data["house_floor"] = house_floor
        re_data["house_diretion"] = house_diretion
        re_data["house_describle"] = house_describle
        re_data["house_address"] = house_address
        re_data["house_man_name"] = house_man_name
        re_data["house_man_number"] = house_man_number
        re_data["images"] = images_list
        return re_data
    
    def on_result(self, data):
        cnn = SQL()
        id = data["house_id"]
        images = data.pop("images")
        # 保存房屋信息
        cnn.insert("home_house", id, **data)
        
        # 保存图片
        for i in images:
            image_data = {}
            image_data["pic"] = i
            image_data["house_id"] = id
            cnn.insert("home_picture", id, **image_data)
            