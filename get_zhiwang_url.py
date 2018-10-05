# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 21:40:10 2018

@author: lzy
"""
'''
主要数据库结构：
主键、论文号、论文名称、论文作者、发表时间、被引用、插入多个url
关系库
主键、外键、引证url、index、状态
'''


from selenium import webdriver
import time
from lxml import etree
from urllib import request
from dbmanager_zhiwang import dbmanager_paper

def get_paper(page,index):
    html_parse=etree.HTML(page)
    ul=html_parse.xpath('//div[@class="essayBox"]/ul')[index]
    li_list=ul.findall('li')
    for li in li_list:
        a_list=li.findall('a')
        for index in range(0,len(a_list)):
            print(a_list[index].text)
            if index==0:
                print(a_list[index].tail)   

def get_cookie():
    driver.get('http://kns.cnki.net/kns/brief/default_result.aspx')
    time.sleep(5)
    driver.find_element_by_name('txt_1_value1').send_keys('体育学刊')     
    driver.find_element_by_xpath('//select[@id="txt_1_sel"]//option[@value="LY$%=|"]').click()      
    driver.find_element_by_id('btnSearch').click()    
    time.sleep(5)
      
    

#缺少paperid
def get_url(num):
    elements=driver.find_elements_by_xpath('//table[@class="GridTableContent"]//tr[@bgcolor]')
    for element in elements:
        try:
            a=element.find_element_by_xpath('td/a[@class="fz14"]')
            print(a.get_attribute('href'))
            paper_info=element.text.replace('\n',' ').split(' ')
            paper_title=paper_info[1]
            index=2
            author=''
            while('体育学刊' not in paper_info[index]):
                author=author+paper_info[index]
                index=index+1
            date=paper_info[index+1]
            reference=paper_info[index+3]
            insert_info=(str(num),paper_title,author,date,reference,a.get_attribute('href'))      
            a.click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            time.sleep(5)
            i=0
            while(i<5):
                i=i+1
                if(etree.HTML(driver.page_source).xpath('//div[@class="yzwx"]/a')!=[]):
                    break
            #不存在引证论文
            url0_list=[]
            url1_list=[]
            url2_list=[]
            if(i!=5):
                html_parse=etree.HTML(driver.page_source)
                url=driver.find_element_by_xpath('//div[@class="yzwx"]/a').get_attribute('href')
                if(url!=None):          
                    print(url)             
                    driver.get(url)
                    html_parse=etree.HTML(driver.page_source)
                    a0_list=html_parse.xpath('//span[@id="CJFQ"]//a')
                    a1_list=html_parse.xpath('//span[@id="CDFD"]//a')
                    a2_list=html_parse.xpath('//span[@id="CMFD"]//a')
                    for a in a0_list:     
                        url0_list.append(a.attrib['href'])
                    
                    for a in a1_list:
                        url1_list.append(a.attrib['href'])
                    
                    for a in a2_list:
                        url2_list.append(a.attrib['href'])     
            db.insert_info(insert_info,url0_list,url1_list,url2_list) 
            num=num+1            

        except Exception as arg:
            print (arg)
        driver.close()
        driver.switch_to_window(windows[0])
        time.sleep(5)
    return num


if __name__=="__main__":
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values' :
            {
            'notifications' : 2
             }
    }
    options.add_experimental_option('prefs',prefs)
    driver = webdriver.Chrome(chrome_options = options)
    driver.maximize_window()
    get_cookie()
    db=dbmanager_paper('root','12345','127.0.0.1','zhiwang')
    num=0
    now_page=1
    driver.get('http://kns.cnki.net/kns/brief/brief.aspx?ctl=4a7fde68-1a44-4852-8b23-1a70aeb4cf8b&dest=%E5%88%86%E7%BB%84%EF%BC%9A%E5%8F%91%E8%A1%A8%E5%B9%B4%E5%BA%A6%20%E6%98%AF%202003&action=5&dbPrefix=SCDB&PageName=ASP.brief_default_result_aspx&Param=%e5%b9%b4+%3d+%272003%27&SortType=(FFD%2c%27RANK%27)+desc&ShowHistory=1&isinEn=1')

    while(now_page<16):
        num=get_url(num)
        a_list=driver.find_elements_by_xpath('//div[@class="TitleLeftCell"]//a')
        for a in a_list:
            if(a.text=='下一页'):
                a.click()
                break
        now_page=now_page+1
        time.sleep(5)