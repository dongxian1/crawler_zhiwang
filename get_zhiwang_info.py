# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:23:29 2018

@author: lzy
"""
'''
数据库结构：
id paperid papername author workunit date
'''

from selenium import webdriver
import time
from lxml import etree
from urllib import request
import re
from dbmanager_zhiwang import dbmanager_paper
    

def get_paper(url,paperid):
    req=request.Request(url,headers=header)
    html_page=request.urlopen(req).read().lower().decode('utf-8',errors='ignore')
    html_parse=etree.HTML(html_page)
    ul_list=html_parse.xpath('//div[@class="essaybox"]//ul')
    for ul in ul_list:
        li_list=ul.findall('li')
        for li in li_list:
            try:
                a_list=li.itertext()
                info_temp=''
                for a in a_list:
                    info_temp=info_temp+a.replace(' ','').replace('\r\n','').replace('&nbsp&nbsp','')
                info=info_temp.split('.')
                if(db.judge_exist(info[0])==False):
                    length=len(info)-1
                    if(length<3):
                        deal=info[length]
                        date=re.findall('\d.*',deal)[0]
                        workunit=deal.replace(date,'').replace('年','')
                        info[length]=workunit
                        info.append(date)
                    info.append(str(paperid))
                    if(db.insert_paper_info(tuple(info))==False):
                        return False
            except Exception as arg:
                print(arg)
                return False
    return True


if __name__=="__main__":
    header={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
    db=dbmanager_paper('root','','127.0.0.1','zhiwang')
    while(True):
        status='finish'
        result=db.get_url()
        if(result==[]):
            break
        print(result[2])
        if(get_paper(result[2],result[1])==False):
            status='error'
        status_info=(status,result[0])
        db.set_status(status_info)
        time.sleep(10)
        
