用python3写的爬虫，从国家统计局爬取地区地址
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/
主文件：spiker_main.py或spider_main_sql.py
有两种存储数据方式
1、爬取胡保存到mysql数据中，使用前需要先建立数据库和表（主文件：spider_main_sql.py）
2、保存到记事本文件，（主文件：spider_main.py）

用到如下包：
bs4
re
urllib.request
urllib.error
requests
random
time
traceback
