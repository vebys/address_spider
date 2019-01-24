# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import requests
import time
import random



class HtmlDownloader(object):
    
  
    def download(self, url):
        if url is None:
            raise Exception('url is None')
        
        header_s =['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',  
                       'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',  
                       'IE 9.0User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',  
                       'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',  
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',  
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',  
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',  
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',  
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',  
                       'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',  
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',  
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36']  
        header_ra = {'User-Agent':random.sample(header_s, 1)[0]}
        # 输出当前进行下载的url
        print("正在下载："+url)
        # 伪装浏览器下载页面
        r = requests.get(url, headers = header_ra , timeout=60)
        r.encoding = "gbk"
        try:
            if r.status_code != 200:
                print('下载错误码：'+r.status_code)
                time.sleep(15)
                return self.download(url)
            else:
                return r.text
            
        except Exception as e:
            print("程序错误信息："+e)
            print("程序出错，当前错误代码"+r.status_code)
            time.sleep(30)
            return self.download(url)

