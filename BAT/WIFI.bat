@ECHO OFF 
color 17
title WIFI设置程序
:loop
	cls
	echo -----------------
	echo  请选择需要的操作
	echo -----------------
	echo         1.Open WIFI
	echo         2.Close WIFI
	echo         3.Show WIFI
	SET /P ST=      请选择：
	if /I "%ST%"=="1" goto OPEN
	if /I "%ST%"=="2" goto CLOSE
	if /I "%ST%"=="3" goto SHOW
	goto loop
:end
exit

:OPEN
	echo 开始创建WIFI网络，请稍候
	%启用并设定 虚拟WIFI网卡 模式%
	netsh wlan set hostednetwork mode=allow ssid=cqustone key=123456789
	%开启无线网络%
	netsh wlan start hostednetwork
	echo WIFI已打开 &pause
	goto :eof

:CLOSE
	%关闭无线网络%
	netsh wlan stop hostednetwork
	echo WIFI已关闭 &pause
	goto :eof

:SHOW
	%显示无线网络%
	netsh wlan show hostednetwork
	echo WIFI已显示 &pause
	goto :eof

:EXIT
	echo Good bye,See you next time. &pause
	goto :eof