#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import time
from threading import Thread

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.file_util import ExcelUtil

class JdSearcher(Thread):
    def __init__(self, content, box, flag=False, totalpage=1, interval=3):
        super().__init__()
        self.content = content
        self.box = box
        self.flag = flag

        self.totalpage = totalpage
        self.interval = interval
        self.rootpath = "/Users/zhangwenjie10/PycharmProjects/data_reptile"
        self.outpath = "/Users/zhangwenjie10/PycharmProjects/data_reptile"
        self.excel = ExcelUtil()

    def run(self):
        self.search(self.content, self.box, self.totalpage, self.interval)
        time.sleep(2)
        print('%s say hello' % self.name)

    def stop(self):
        self.browser.quit()

    def search(self, content, box, totalpage=1, interval=3):

        self.browser = webdriver.Chrome(self.rootpath + "/driver/chromedriver")
        self.browser.maximize_window()
        try:
            wait1 = WebDriverWait(self.browser, 300)
            wait = WebDriverWait(self.browser, 2)

            self.browser.get('https://www.jd.com/')  # 打开请求的url
            input = wait1.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#key')))  # 等待搜索输入框加载完成
            self.browser.set_window_size(1000, 500)
            input.send_keys(content)  # 输入框中输入“美食”
            sumbit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > div > button')))
            sumbit.click()
            js = "var q=document.documentElement.scrollTop=10000"

            store_set = set()  # 数据去重
            for j in range(int(totalpage)):
                for n in range(5):
                    self.browser.execute_script(js)
                    time.sleep(1)
                t_selector = Selector(text=self.browser.page_source)
                sku_price = t_selector.xpath(
                    '//div[@id="J_goodsList"]/ul/li/div').extract()
                for i in range(len(sku_price)):
                    try:
                        soup=BeautifulSoup(sku_price[i],'html.parser')
                        imge = soup.find(class_="p-img").a.img
                        price = soup.find(class_="p-price").strong.i.string
                        title = soup.find(class_="p-name p-name-type-2").a.attrs["title"]
                        cmt_count = soup.find(class_="p-commit").strong.a.string
                        cmt_href = soup.find(class_="p-commit").strong.a.attrs["href"]
                        box.insert('', 'end', values=[title, price, cmt_count, cmt_href])
                        time.sleep(int(self.interval))
                    except Exception as e:
                        print(e)
                        continue
                next = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pn-next')))
                next.click()
                time.sleep(int(interval))

        except Exception as e:
            print(e)
        finally:
            self.browser.quit()
            # self.excel.save(outpath+"/"+content+".xls")

# if __name__ == '__main__':

#     content = input("请输入搜索信息： ")
#     totalpage=1
#     interval=3
#     totalpage=input("请输入总共查询的页数： ")
#     interval=input("请输入每次查询间隔时间（秒）： ")
#     outpath=input("请输入输出文件目录：")
#
#
#     index = JdSearcher()
#     index.run()
# #
#     content = index.searchinfo.get()
#     totalpage = index.pagenum.get()
#     interval = index.delayTime.get()
#
#     if content:
#         index.search(content,totalpage,int(interval),outpath)
#     else:
#         print("提示： 未输入搜索信息！！")

