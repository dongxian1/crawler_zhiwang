# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 07:52:53 2018

@author: lzy
"""

import mysql.connector.pooling
import mysql.connector.connection


class dbmanager_paper:
    
    def __init__(self,username,password,IP_address,database):
        try:
            dbconfig = {
              "user":       username,
              "password":   password,
              "host":       IP_address,
              "port":       3306,
              "database":   database,
              "charset":    "utf8"
            }
            self.conpool=mysql.connector.pooling.MySQLConnectionPool(pool_size=10,**dbconfig)
        except Exception as arg:
            print(arg)
    
    def set_status(self,status_info):
        sql='update rzhiwang set status="%s" where id=%s'%status_info
        con=self.conpool.get_connection()
        cursor=con.cursor()
        try:
            cursor.execute(sql)
            con.commit()
        except Exception as Arg:
            con.rollback()
            print(Arg)
        finally:
            if con:
                con.close()
            if cursor:
                cursor.close()  
    
    def get_url(self):
        sql='select * from rzhiwang where status="new" limit 1'
        con=self.conpool.get_connection()
        cursor=con.cursor()
        cursor.execute(sql)
        result=cursor.fetchone()
        cursor.close()
        con.close()
        return result
    
    def insert_info(self,insert_papaer_info_list,insert_paper_url0,insert_paper_url1,insert_paper_url2):
        insert_zhiwang_url_sql='insert into zhiwang_url (paperid,name,author,date,reference,src_url) values(%s,"%s","%s","%s","%s","%s")'%insert_papaer_info_list
        insert_rzhiwang_sql='insert into rzhiwang (paperid,papername,indexs,status) values(%s,"%s","%s","%s")'
        con=self.conpool.get_connection()
        cursor=con.cursor()
        try:
           cursor.execute(insert_zhiwang_url_sql)
           for url0 in insert_paper_url0:
               cursor.execute(insert_rzhiwang_sql%(insert_papaer_info_list[0],url0,str(0),"new"))
           for url1 in insert_paper_url1:
               cursor.execute(insert_rzhiwang_sql%(insert_papaer_info_list[0],url1,str(1),"new"))
           for url2 in insert_paper_url2:
               cursor.execute(insert_rzhiwang_sql%(insert_papaer_info_list[0],url2,str(2),"new")) 
           con.commit()
        except Exception as arg:
            print(arg)
            con.rollback()
            return False
        finally:
            if con:
                con.close()
            if cursor:
                cursor.close()
        return True     
      
    def insert_paper_info(self,info):
        sql='insert into zhiwang_info (papername,author,workunit,date,paperid) values("%s","%s","%s","%s",%s)'%info
        con=self.conpool.get_connection()
        cursor=con.cursor()
        try:
            cursor.execute(sql)
            con.commit()
        except Exception as arg:
            print(arg)
            con.rollback()
            return False
        finally:
            if con:
                con.close()
            if cursor:
                cursor.close() 
        return True
    
    def judge_exist(self,papername):
        sql='select papername from zhiwang_info where papername="%s"'%papername
        con=self.conpool.get_connection()
        cursor=con.cursor()
        try:
            cursor.execute(sql)
            result=cursor.fetchone()
            if result==None:
                return False
        except Exception as arg:
            print(arg)
        finally:
            if con:
                con.close()
            if cursor:
                cursor.close()
        return True