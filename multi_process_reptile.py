# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 17:13:25 2018

@author: Administrator
"""

###玩玩爬取武汉链家二手房两房信息
import requests
import bs4
import json
from multiprocessing import Pool
from multiprocessing import Process
import threading

def get_url():
    url=[]
    url1='https://wh.lianjia.com/ershoufang/l2/'
    url.append(url1)
    page=[x for x in range(2,101)]
    for i in page:
        url.append('https://wh.lianjia.com/ershoufang/pg'+str(i)+'l2/')
    return url


###获取信息
def get_infor(url):
    response = requests.get(url)
    soup=bs4.BeautifulSoup(response.text,'lxml')
    ##地址和房源名称信息
    titles=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.title > a')
    ##位置
    locations=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.flood > div > a')
    ###小区信息
    addresses=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.address > div > a')
    ##房子信息
    houseinfoes=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.address > div')
    ##楼层##
    positioninfoes=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.flood > div')
    ##单价###
    prices=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.priceInfo > div.unitPrice > span')
    ##总价###
    totals=soup.select('body > div.content > div.leftContent > ul > li > div.info.clear > div.priceInfo > div.totalPrice > span')
    ##整理信息##
    for location,address,houseinfo,positioninfo,price,total in zip(locations,addresses,houseinfoes,positioninfoes,prices,totals):
        data={
            '位置':location.get_text(),
            "小区":address.get_text(),
            '房源信息':houseinfo.get_text(),
            '楼层年代':positioninfo.get_text(),
            "单价":price.get_text()[2:],
            "总价":total.get_text()+'万'
        }
#        print(data)
        write_to_file(data)

###写入txt文件中##
def write_to_file(content):
    with open('C:\\Users\\Administrator\\Desktop\\house_information.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n' +'\n')

##获取全部房源信息并保存到txt##
def main():
    urls=get_url()
    for url in urls:
        get_infor(url)
if __name__=='__main__':
    ###多进程
    p=Process(target=main)
    p.start()
    p.join()
    print('Process Completed')
    ###进程池
    # p=Pool(5)
    # for i in range(5):
    #     p.apply_async(main)
    # print(u'信息获取完成')
    ###多线程
    # t=threading.Thread(target=main)
    # t.start()
    # t.join()
    # print('信息获取完成')

        