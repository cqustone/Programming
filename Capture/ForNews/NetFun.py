#!/usr/bin/env python
# -*- coding: utf-8 -*-
#writer by cqustone
#Create time:2016-01-02
#查询网站归属地信息
#网页截图并保存


import signal
import urllib
import json
import sys,os,re
import subprocess
import time
import socket
import urllib.parse
import urllib.request
from selenium import webdriver

#定义IP与域名正则及通用URL(查询接口地址)
re_ip = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
url = "http://ip.taobao.com/service/getIpInfo.php?ip="
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#查找IP地址
def ip_location(ip):
	data = urllib.request.urlopen(url + ip).read().decode()
	datadict=json.loads(data) 
	for oneinfo in datadict:
		if "code" == oneinfo:
			if datadict[oneinfo] == 0:
				return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"]
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
	return ip_location(result)

#截图并保存  命令行执行未能截图保存，必须HTTP服务中执行？
def capture_http(url,picname,foldername):  
		name = os.path.join(BASE_DIR, foldername + '\\%s.png' %picname) 
		command = "phantomjs capture.js %s %s" %(url,name)
		subprocess.Popen(command, shell=True)
# 网页截屏函数   from selenium import webdriver
# 需安装Firefox浏览器，单任务运行
def capture(url,picname):
	browser = webdriver.Firefox()	### Get local session of firefox
	browser.set_window_size(1200, 700)
	browser.get(url)
	browser.execute_script("""
		(function () {
          var y = 0;
          var step = 200;
          window.scroll(0, 0); 
          function f() {
            if (y < document.body.scrollHeight) {
              y += step;
              window.scroll(0, y);
              setTimeout(f, 100);
            } else {
              window.scroll(0, 0);
              document.title += "scroll-done";
            }
          } 
          setTimeout(f, 1000);
        })();
        """)

	for i in range(60):
		if "scroll-done" in browser.title:
			break
	time.sleep(6) 
	browser.save_screenshot(picname)
	browser.quit()		###close()