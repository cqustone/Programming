@ECHO OFF 
color 17
title WIFI���ó���
:loop
	cls
	echo -----------------
	echo  ��ѡ����Ҫ�Ĳ���
	echo -----------------
	echo         1.Open WIFI
	echo         2.Close WIFI
	echo         3.Show WIFI
	SET /P ST=      ��ѡ��
	if /I "%ST%"=="1" goto OPEN
	if /I "%ST%"=="2" goto CLOSE
	if /I "%ST%"=="3" goto SHOW
	goto loop
:end
exit

:OPEN
	echo ��ʼ����WIFI���磬���Ժ�
	%���ò��趨 ����WIFI���� ģʽ%
	netsh wlan set hostednetwork mode=allow ssid=cqustone key=123456789
	%������������%
	netsh wlan start hostednetwork
	echo WIFI�Ѵ� &pause
	goto :eof

:CLOSE
	%�ر���������%
	netsh wlan stop hostednetwork
	echo WIFI�ѹر� &pause
	goto :eof

:SHOW
	%��ʾ��������%
	netsh wlan show hostednetwork
	echo WIFI����ʾ &pause
	goto :eof

:EXIT
	echo Good bye,See you next time. &pause
	goto :eof