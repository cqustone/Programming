#!/usr/bin/env python
# -*- coding: utf-8 -*-
#writer by cqustone
#Create time:2016-01-02
#用法: Python Capture.py ExcelName.xls 
#输入：Excel文件名（N行三列 编号+名称+网址）
#输出：对每行数据进行处理，将结果写入单独的工作表中
#例如：查询指定学生的各科成绩并将结果输出到个人成绩单
#说明：用作参数的文件，每条信息单独一行(包含表头等信息)
#说明：Sheet1为源数据，Sheet2为结果模板，Sheet3等为输出结果
#参考：http://anyoneking.com/archives/283

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
	reason = "1.网站无备案信息，且服务器架设在"
	result = xlwt.Workbook()	###生成新的Excel###
	template = data.sheets()[1]		###获取模板
	keyword = data.sheets()[0]		###获取源数据
	nsheets = len(data.sheets())	###获取表数量
	nrows = keyword.nrows			###获取行数量
	###先复制源数据及模板
	copy_sheet(keyword,result.add_sheet("目录"))
	copy_sheet(template,result.add_sheet("模板"))
	for i in range(1,nrows):
		row = keyword.row_values(i)
		num = row[0]					###获取编号EX:8.
		name = row[1]					###获取名称EX:百度
		index = row[2]					###获取索引
		url = "http://www." + index		###获取索引(必须加http否则出错)
		sheetname = str(int(num)) + "." + str(name)##EX:8.百度
		try:
			newsheet = result.add_sheet(sheetname, cell_overwrite_ok=True)	
			copy_sheet(template,newsheet)		###复制模板内容
			city = NetFun.dm_server(index)		###查询数据并写入
			newsheet.write(1,1,name)	
			newsheet.write(1,3,url)	
			newsheet.write(2,5,city)	
			newsheet.write(4,1,reason + city + "。")
			###准备截图并保存
			picname = "1." + str(int(num)) + " " + str(name) + ".png"	##EX:1.8 百度.png
			NetFun.capture(url,picname)
			print("  " + str(i) + "/" + str(nrows-1) + " (" + name + "<>" + index + ") is finished." )
		except Exception as e:
			print (e)
			print("  " + str(i) + "/" + str(nrows-1) + " (" + name + "<>" + index + ") is wrong." )
			continue
	result.save(filename)			
	print ("  It's done! See you!")