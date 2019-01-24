# -*- coding: utf-8 -*-
from mysql_handler import MysqlHandler
from html_downloader import HtmlDownloader
from html_parser import HtmlParser
import traceback
import time


class CodeSpider(object):
    def __init__(self):
        # 实例化其他模块类
        self.mysql_handler = MysqlHandler()
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
        # 爬取起点url
        self.root_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
        # 用于后续url的拼接
        self.split_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'
        # 省页面列表
        self.province_url_list = []
        # 市页面列表
        self.city_url_list = []
        # 区页面列表
        self.county_url_list = []
        # 乡镇、街道页面列表
        self.town_url_list = []
        self.last_log_path = "d:\\log.txt"

    def craw(self):
        try:
            # 记录正在下载、解析的url，便于分析错误
            downloading_url = self.root_url
            html_content = self.html_downloader.download(downloading_url)
            # 第一个参数：需要解析的html代码
            # 第二个参数：用于url拼接的url
            self.province_url_list = self.html_parser.province_parser(html_content, self.split_url)
            #print(self.province_url_list)
            pro = self.province_url_list
            #print(self.province_url_list[0][0])
            with open(self.last_log_path , "r") as r:
                last_log = r.read()
            #print(last_log)
            if last_log != "":
                last_log_index = pro.index(tuple(last_log.split(';')))
                #print("inde:"+str(last_log_index))
                for i in range(last_log_index):
                    del self.province_url_list[0]
                    
                print("删除已下载元素后还剩余："+str(len(self.province_url_list))+"共计：31")
                #print(self.province_url_list)
                #exit()
            #else:
            #  print("下载开始，共计:"+str(len(pro))
            #print(last_log_index)
            #exit()
            for province_name, province_url, province_code in self.province_url_list:
                #print(province_code)
                #记录最后一个下载
                last_record = (province_name, province_url, province_code)
                #print(last_record)
                with open(self.last_log_path, "w") as l:
                    #last_name = province_name.encode('utf8')
                    l.write(last_record[0]+";"+last_record[1]+";"+last_record[2])
                #exit()
                province_id = self.mysql_handler.insert(province_code+'0000000000', province_name)     
                #print(province_id)
                # 记录正在下载、解析的url，便于分析错误
                downloading_url = province_url
                html_content = self.html_downloader.download(downloading_url)
                self.city_url_list = self.html_parser.city_parser(html_content, self.split_url)
                for city_name, city_url, city_code in self.city_url_list:
                    city_id = self.mysql_handler.insert(city_code, city_name)
                    # 例如直辖市没有下级页面
                    if city_url is None:
                        continue
                    # 记录正在下载、解析的url，便于分析错误
                    downloading_url = city_url
                    html_content = self.html_downloader.download(downloading_url)
                    self.county_url_list = self.html_parser.county_parser(html_content, self.split_url + province_code + "/")
                    for county_name, county_url, county_code in self.county_url_list:
                        county_id = self.mysql_handler.insert(county_code, county_name)
                        if county_url is None:
                            continue
                        # 记录正在下载、解析的url，便于分析错误
                        downloading_url = county_url
                        html_content = self.html_downloader.download(downloading_url)
                        self.town_url_list = self.html_parser.town_parser(html_content, self.split_url)
                        for town_name, town_url, town_code in self.town_url_list:
                            # 输出抓取到的乡镇街道的名称、链接（实际不需要）、编号代码
                            print(town_name, town_url, town_code)
                            self.mysql_handler.insert(town_code, town_name)
            self.mysql_handler.close()
        except Exception as e:
            print('[ERROR] Craw Field!Url:', downloading_url, 'Info:', e)
            # 利用traceback定位异常
            traceback.print_exc()
            time.sleep(60)            
            return self.craw()

if __name__ == '__main__':
    obj_spider = CodeSpider()
    obj_spider.craw()
