# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 21:55:13 2018

@author: lzy
"""

import xlwt
import mysql.connector.pooling
import mysql.connector.connection


def create_mysql_conPool(user,password,host,database):
    dbconfig = {
          "user":       user,
          "password":   password,
          "host":       host,
          "port":       3306,
          "database":   database,
          "charset":    "utf8"
        }
    conpool=mysql.connector.pooling.MySQLConnectionPool(pool_name='image',pool_size=10,**dbconfig)
    return conpool

def get_reference(paperid):
    sql="select * from zhiwang_info where paperid=%s"%paperid
    con=conpool.get_connection()
    cursor=con.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    con.close()
    return result

def get_paper_info(index):
    sql="select * from zhiwang_url where paperid=%s"%index
    con=conpool.get_connection()
    cursor=con.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    con.close()
    return result   

def insert_author_info():
    table.write(row,0,str(paperid))
    table.write(row,1,str(result[2])+"("+str(result[4])+")")
    table.write(row,2,str(result[3]))

def insert_reference():
    table.write(row,5,str(result[3]))
    table.write(row,6,str(result[4]))
    table.write(row,7,str(result[5]))

if __name__=="__main__":
    conpool=create_mysql_conPool('root','Ll41655184165518','localhost','zhiwang')
    Excel=xlwt.Workbook()
    table = Excel.add_sheet('table', cell_overwrite_ok=True)
    paperid=0
    row=0
    while(True):
        result=get_paper_info(paperid)
        if result==None:
            break
        insert_author_info()    
        table.write(row,3,str(result[5]))
        table.write(row,4,str(result[6]))
        row=row+1
        result_list=get_reference(str(result[1]))
        for result in result_list:
            insert_author_info()
            insert_reference()
            row=row+1
        paperid=paperid+1
    Excel.save('zhiwang.xlsx')
        
        
    