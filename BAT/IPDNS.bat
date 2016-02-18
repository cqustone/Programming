@ECHO OFF 
color 17
title IP-DNS选择程序
:loop
	cls
	echo --------------------
	echo  请选择要设置的IP地址
	echo --------------------
	echo         1.校园网
	echo         2.公  网
	echo         3.无线网
	echo         4.家庭无线
	SET /P ST=      请选择：
	if /I "%ST%"=="1" goto CAMPUS
	if /I "%ST%"=="2" goto PUBLIC
	if /I "%ST%"=="3" goto WIRELESS
	if /I "%ST%"=="4" goto HOMEWIRE
	goto loop
:end
exit

:CAMPUS
	netsh interface ip set address name="本地连接" source=static addr=172.20.69.222 mask=255.255.255.0 gateway=172.20.69.1
	echo IP地址配置成功
	netsh dnsclient delete dnsservers "本地连接" all
	netsh interface ip add dns "本地连接" 202.202.0.33
	netsh interface ip add dns "本地连接" 202.202.0.34 index=2
	echo DNS服务器配置成功 &pause
	goto :eof

:PUBLIC
	netsh interface ip set address name="本地连接" source=static addr=202.202.76.254 mask=255.255.224.0 gateway=202.202.76.193
	echo IP地址配置成功
	netsh dnsclient delete dnsservers "本地连接" all
	netsh interface ip add dns "本地连接" 202.202.0.33
	netsh interface ip add dns "本地连接" 202.202.0.34 index=2
	echo DNS服务器配置成功 &pause
	goto :eof

:WIRELESS
	netsh interface ip set address name="无线网络连接" source=static addr=172.21.109.222 mask=255.255.255.0 gateway=172.21.109.1
	echo IP地址配置成功
	netsh dnsclient delete dnsservers "无线网络连接" all
	netsh interface ip add dns "无线网络连接" 202.202.0.33
	netsh interface ip add dns "无线网络连接" 202.202.0.34 index=2
	echo DNS服务器配置成功 &pause
	goto :eof

:HOMEWIRE
	netsh interface ip set address name="无线网络连接" source=static addr=192.168.0.168 mask=255.255.255.0 gateway=192.168.0.1
	echo IP地址配置成功
	netsh dnsclient delete dnsservers "无线网络连接" all
	netsh interface ip add dns "无线网络连接" 10.0.1.17
	netsh interface ip add dns "无线网络连接" 10.0.1.20 index=2
	echo DNS服务器配置成功 &pause
	goto :eof

:EXIT
	echo Good bye,See you next time. &pause
	goto :eof