#!/usr/bin/env python
# -*- coding: utf-8 -*-
#查询网站/IP地址/归属地信息（批量查询、单个查询）
#writer by cqustone
#Create time:2015-12-02
#用法: python ChkSite.py dm.txt ip.txt city.txt（输入三个文件：域名 > IP / 归属地） 
#用法: python ChkSite.py ip.txt city.txt       （输入两个文件：IP > 归属地） 
#用法: python ChkSite.py www.baidu.com        （输入网站域名/网址）
#用法: python ChkSite.py 8.8.8.8               （输入IP地址）
#说明：用作参数的文件，每条网址、IP地址单独一行

import signal
import urllib
import json
import sys,os,re
import socket
import urllib.parse
import urllib.request

def handler(signum, frame):
	sys.exit(0)
signal.signal(signal.SIGINT, handler)

#定义IP与域名正则及通用URL(查询接口地址)
re_ip = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
url = "http://ip.taobao.com/service/getIpInfo.php?ip="

#查找IP地址
def ip_location(ip):
	data = urllib.request.urlopen(url + ip).read().decode()
	datadict=json.loads(data) 
	for oneinfo in datadict:
		if "code" == oneinfo:
			if datadict[oneinfo] == 0:
				return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
#查找网址
def dm_server(netadd):	##过滤网址前缀(正确|错误)
	netadd = netadd.lower().replace('http://','').replace('https://','')
	netadd = netadd.replace('http:/','').replace('https:/','')
	netadd = netadd.replace(r'http:\\','').replace(r'https:\\','')
	netadd = netadd.replace('http:\\','').replace('https:\\','')
	netadd = netadd.replace(r'http:','').replace(r'https:','')
	netadd = netadd.replace(r'http//','').replace(r'https//','')
	netadd = netadd.replace(r'http/','').replace(r'https/','')
	netadd = netadd.replace(r'http\\','').replace(r'https\\','')		
	netadd = netadd.replace('http\\','').replace('https\\','')		
	addstr = netadd.strip().split('/')	
	addstr = addstr[0]
	try:
		result = socket.gethostbyname(addstr)
	except:
		www = 'www'
		nPos = addstr.find(www)
		if nPos == -1:
			addstr = 'www.' + addstr
		try:
			result = socket.gethostbyname(addstr)
		except:
			result = "0.0.0.0"
	return result

if len(sys.argv) <= 1 :		####未输入参数
	print ("")
	print ("  Please input at least one parameter!")
	print ("  EX: 8.8.8.8")
	print ("  EX: www.baidu.com")
	print ("  EX: ip.txt city.txt")
	print ("  EX: dm.txt ip.txt city.txt")
	sys.exit(0)
elif len(sys.argv) <= 2 :	####输入1个参数（IP / 网址）
	if os.path.isfile(sys.argv[1]):		###该参数为文件
		print ("")
		print ("  When you want to enter one parameter")
		print ("  The parameter must be ip or domain")
		print ("  The parameter cann't be filename")
		sys.exit(0)
	else:								###该参数不为文件
		ipordomain = sys.argv[1]
		if re_ip.match(ipordomain):				##该参数为IP地址
			city_address = ip_location(ipordomain)
			print ("")
			print ("  IP:  " + ipordomain + "  <>  归属地:  " + city_address)
		#elif (re_domain.match(ipordomain)):		
		else:									##该参数为网址 
			ip_address = dm_server(ipordomain)
			city_address = ip_location(ip_address)
			print ("")
			print ("  网址:  " + ipordomain)
			print ("  IP:  " + ip_address + "  <>  归属地:  " + city_address)
		#else:
			# print ("  Make sure the parameter fits the format.")
			# print ("  EX: 8.8.8.8")
			# print ("  EX: www.baidu.com")
			# sys.exit(0)
elif len(sys.argv) <= 3 :  	####输入2个参数（批量查询IP地址的归属地）
	print ("")
	print ("  When you want to enter two parameters")
	print ("  Make sure the first parameter is the filename of ipaddress")
	print ("  The program is converting")
	print ("  Please wait ……")
	ipfile = open(sys.argv[1],'r')
	cityfile = open(sys.argv[2], 'w+')
	for line in ipfile.readlines():
		if re_ip.match(line):
			city_address = ip_location(line)
		else:
			city_address = 'IP Format Error'
		cityfile.write(city_address)
		cityfile.write('\n')
	ipfile.close()
	cityfile.close()
else:						#####输入3个参数（批量查询网址对应的IP地址及归属地）
	print ("")
	print ("  When you want to enter three or more parameters")
	print ("  Make sure the first parameter is the filename of netaddress") 
	print ("  The program is converting")
	print ("  Please wait ……")
	dmfile = open(sys.argv[1],'r')
	ipfile = open(sys.argv[2], 'w+')
	cityfile = open(sys.argv[3], 'w+')
	for line in dmfile.readlines():
		#if re_domain.match(line):
		ip_address = dm_server(line)	    	
		ipfile.write(ip_address)
		ipfile.write('\n')
		city_address = ip_location(ip_address)
		cityfile.write(city_address)
		cityfile.write('\n')
	dmfile.close()
	ipfile.close()
	cityfile.close()
print ("  It's done! See you!")