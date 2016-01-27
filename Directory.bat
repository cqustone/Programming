@ECHO OFF 
color 17
title 目录选择程序
:loop
	cls
	echo ----------------------
	echo  请选择你要进入的目录
	echo ----------------------
	echo         1.WWW
	echo         2.Django
	echo         3.Python
	echo         4.Node.js
	echo         5.Express
	echo         6.GitHub
	set/p n=      请选择：
	if %n%==1 goto WWW
	if %n%==2 goto DJANGO
	if %n%==3 goto PYTHON
	if %n%==4 goto NODEJS
	if %n%==5 goto Express
	if %n%==6 goto GitHub
	goto loop
:end
exit

:WWW
	cmd /k cd /d C:\AppServ\WWW
:DJANGO
	cmd /k cd /d C:\AppServ\Django
	@ECHO Python manage.py runserver 8081  #运行django环境
:PYTHON
	cmd /k cd /d C:\AppServ\Python
	@ECHO python Chk_site.py 8.8.8.8 | python Chk_site.py www.g.cn | python Chk_site.py filename
:NODEJS
	cmd /k cd /d C:\AppServ\Nodejs
:Express
	cmd /k cd /d C:\AppServ\Express
:GitHub
	cmd /k cd /d C:\AppServ\GitHub