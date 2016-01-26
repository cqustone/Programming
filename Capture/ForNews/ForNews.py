#!/usr/bin/env python
# -*- coding: utf-8 -*-
#writer by cqustone
#Create time:2016-01-02
#用法: Python NewsInfo.py ExcelName.xls 
#输入：Excel文件名（Sheet2为结果模板 Sheet3为输出结果）
#输入：Excel文件名（Sheet1为源数据，N行三列：编号+文章名称+文章网址）
#输入：Excel文件名（Sheet1为源数据，每条信息单独一行，包含表头等信息）
#输出：对每行数据进行处理，将结果写入单独的工作表中
#例如：报社发稿费需统计发布的文章，并将文章截图保存
#说明：输入文件的网址中必须加http://前缀，否则出错

import signal
import sys,os,re
import xdrlib,xlrd,xlwt
import NetFun
import urllib
import socket
import urllib.parse
import urllib.request

def handler(signum, frame):
	sys.exit(0)
signal.signal(signal.SIGINT, handler)

####复制工作表（仅限内容）
def copy_sheet(template,newsheet): 	
	numRow = template.nrows
	numCol = template.ncols 
	for i in range(numRow):
		row = template.row_values(i) 
		for j in range(numCol): 
			value = row[j] 
			newsheet.write(i, j, value)

if len(sys.argv) <= 1 :		####未输入参数
	print ("")
	print ("  Please input the filename!")
	print ("  EX: ExcelName | ExcelName.xls")
	sys.exit(0)
else:						####输入了参数
	filename = sys.argv[1]
	try:
		data = xlrd.open_workbook(filename)
	except Exception as e:
		print (e)
		sys.exit(0)
	print ("")
	print ("  It's working,please wait.")
	result = xlwt.Workbook()	###生成新的Excel###
	template = data.sheets()[1]		###获取模板
	keyword = data.sheets()[0]		###获取源数据
	nrows = keyword.nrows			###获取行数量
	###先复制源数据及模板
	copy_sheet(keyword,result.add_sheet("目录"))
	copy_sheet(template,result.add_sheet("模板"))
	newsheet = result.add_sheet("结果", cell_overwrite_ok=True)	
	copy_sheet(template,newsheet)		###复制模板内容
	for i in range(1,nrows):
		row = keyword.row_values(i)
		num = row[0]					###获取编号EX:8
		name = row[1]					###获取名称EX:百度
		url = row[2]					###获取网址EX:http://www.baidu.com
		sheetname = str(int(num)) + "." + str(name)##EX:8.百度
		try:
			###查询数据并写入（本示例为查询归属地 其他信息自行修改）
			city = NetFun.dm_server(url)
			newsheet.write(i,0,num)	
			newsheet.write(i,1,name)	
			newsheet.write(i,2,url)	
			newsheet.write(i,3,city)	
			###准备截图并保存
			picname = str(int(num)) + "." + str(name) + ".png"	##EX:8.百度.png
			NetFun.capture(url,picname)
			newsheet.write(i,4,"OK")
			print("  " + str(i) + "/" + str(nrows-1) + " ( " + name + "<>" + url + " ) is finished." )
		except Exception as e:
			newsheet.write(i,4,"Wrong")
			print (e)
			print("  " + str(i) + "/" + str(nrows-1) + " ( " + name + "<>" + url + " ) is wrong." )
			continue
	result.save(filename)
	print ("  It's done! See you!")