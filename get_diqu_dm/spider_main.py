# -*- coding: utf-8 -*-
#from mysql_handler import MysqlHandler
from html_downloader import HtmlDownloader
from html_parser import HtmlParser
import traceback


class CodeSpider(object):
    def __init__(self):
        # 实例化其他模块类
        #self.mysql_handler = MysqlHandler()
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
        self.path = "D:\\python_work\\get_diqu_dm\\"
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

    def craw(self):
        try:
            # 记录正在下载、解析的url，便于分析错误
            downloading_url = self.root_url
            html_content = self.html_downloader.download(downloading_url)
            # 第一个参数：需要解析的html代码
            # 第二个参数：用于url拼接的url
            self.province_url_list = self.html_parser.province_parser(html_content, self.split_url)
            #print(self.province_url_list)
            with open(self.path+"shen_daima.txt", "a") as f:
                for province_name, province_url, province_code in self.province_url_list:
                    province_code = province_code+'0000000000'
                    
                    f.write(province_code+"\t"+province_name+"\n")
                    
                    # 第一个参数：1-插入一个省数据；2-市数据；3-区数据；4-乡镇街道数据
                    # 第二个参数：省市区街道名称
                    # 第三个参数：上级的id，注意省没有上级id
                    # 第四个参数：市区街道的行政区划编码
                    #province_id = self.mysql_handler.insert(1, province_name, None, None)
                    
                    # 记录正在下载、解析的url，便于分析错误
                    downloading_url = province_url
                    html_content = self.html_downloader.download(downloading_url)
                    self.city_url_list = self.html_parser.city_parser(html_content, self.split_url)
                    with open(self.path+"other_daima.txt","a") as o:
                        for city_name, city_url, city_code in self.city_url_list:
                            o.write(city_code+"\t"+city_name+"\n")
                            #city_id = self.mysql_handler.insert(2, city_name, province_id, city_code)
                            # 例如直辖市没有下级页面
                            if city_url is None:
                                continue
                            # 记录正在下载、解析的url，便于分析错误
                            
                            downloading_url = city_url
                            html_content = self.html_downloader.download(downloading_url)
                            self.county_url_list = self.html_parser.county_parser(html_content, self.split_url + province_code + "/")
                            for county_name, county_url, county_code in self.county_url_list:
                                o.write(county_code+"\t"+county_name+"\n")
                                #county_id = self.mysql_handler.insert(3, county_name, city_id, county_code)
                                if county_url is None:
                                    continue
                                # 记录正在下载、解析的url，便于分析错误
                                print('To deal with county')
                                downloading_url = county_url
                                html_content = self.html_downloader.download(downloading_url)
                                self.town_url_list = self.html_parser.town_parser(html_content, self.split_url)
                                for town_name, town_url, town_code in self.town_url_list:
                                    # 输出抓取到的乡镇街道的名称、链接（实际不需要）、编号代码
                                    o.write(town_code+"\t"+town_name+"\n")
                                    print(town_name, town_url, town_code)
                                    #self.mysql_handler.insert(4, town_name, county_id, town_code)
            #self.mysql_handler.close()
            f.close()
            o.close()
        except Exception as e:
            print('[ERROR] Craw Field!Url:', downloading_url, 'Info:', e)
            # 利用traceback定位异常
            traceback.print_exc()

if __name__ == '__main__':
    obj_spider = CodeSpider()
    obj_spider.craw()
