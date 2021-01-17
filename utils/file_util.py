#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xlrd as xlrd
import xlwt

class ExcelUtil():

    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('sheet1')

    def writeExcel(self,row,col,content):
        # 创建一个worksheet
        # 写入excel  参数对应 行, 列, 值
        self.worksheet.write(row,col, content)

    def save(self,name):
        #保存
        self.workbook.save(name)

    def loadExcel(self,filename):

        # 打开excel文件,获取工作簿对象
        wb = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_name('sheet1')
        return sheet