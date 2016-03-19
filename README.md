Programming
===========
编程开发学习研究、学习笔记等  


BAT批处理
------------
 - WIFI.bat：WIFI设置程序  
 - IPDNS.bat：IP-DNS选择程序  
 - Directory.bat：目录选择程序  


Python Study
------------
####批量对网页截屏——Capture.py  
> - 用法: Python Capture.py ExcelName.xls   
> - 输入：Excel文件名（N行三列 编号+名称+网址）  
> - 输出：对每行数据进行处理，将结果写入单独的工作表中  
> - 说明：用作参数的文件，每条信息单独一行(包含表头等信息)  
> - 说明：Sheet1为源数据，Sheet2为结果模板，Sheet3等为输出结果  
> - Capture >> ForNews：对每行数据进行处理，将结果写入同一工作表中  

####批量查询网站归属地——ChkSite.py  
> - 用法: python ChkSite.py 8.8.8.8   
> - 用法: python ChkSite.py www.baidu.com  
> - 用法: python ChkSite.py ip.txt city.txt  
> - 用法: python ChkSite.py dm.txt ip.txt city.txt  


Django Study
------------
####Django静态文件解析  
> - (settings.py)STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]   
> - (urls.py)urlpatterns += staticfiles_urlpatterns() 必须放在最后一行   
> - (Template){% load staticfiles %} <link href="{% static "css/Style.css" %}" />  

####Django截屏操作  
> - Phantomjs执行capture.js截屏  
> - Selenium Webdriver对象browser截屏  
