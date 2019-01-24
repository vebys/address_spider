# -*- coding: utf-8 -*-
import pymysql.cursors
class MysqlHandler(object):
    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", passwd="root", db="code_spider", charset="utf8", cursorclass=pymysql.cursors.DictCursor)

    def insert(self,code,name):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('REPLACE INTO diqudaima (code, name) VALUES (%s, %s)' , [code, name])                
            #insert_id = cursor.lastrowid
            self.db.commit()
        except Exception as e:
            raise Exception('MySQL ERROR:', e)
        # 返回存储后的id
        return name+"success"

    #最后需要调用该方法来关闭连接
    def close(self):
        self.db.close()
