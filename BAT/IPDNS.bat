@ECHO OFF 
color 17
title IP-DNSѡ�����
:loop
	cls
	echo --------------------
	echo  ��ѡ��Ҫ���õ�IP��ַ
	echo --------------------
	echo         1.У԰��
	echo         2.��  ��
	echo         3.������
	echo         4.��ͥ����
	SET /P ST=      ��ѡ��
	if /I "%ST%"=="1" goto CAMPUS
	if /I "%ST%"=="2" goto PUBLIC
	if /I "%ST%"=="3" goto WIRELESS
	if /I "%ST%"=="4" goto HOMEWIRE
	goto loop
:end
exit

:CAMPUS
	netsh interface ip set address name="��������" source=static addr=172.20.69.222 mask=255.255.255.0 gateway=172.20.69.1
	echo IP��ַ���óɹ�
	netsh dnsclient delete dnsservers "��������" all
	netsh interface ip add dns "��������" 202.202.0.33
	netsh interface ip add dns "��������" 202.202.0.34 index=2
	echo DNS���������óɹ� &pause
	goto :eof

:PUBLIC
	netsh interface ip set address name="��������" source=static addr=202.202.76.254 mask=255.255.224.0 gateway=202.202.76.193
	echo IP��ַ���óɹ�
	netsh dnsclient delete dnsservers "��������" all
	netsh interface ip add dns "��������" 202.202.0.33
	netsh interface ip add dns "��������" 202.202.0.34 index=2
	echo DNS���������óɹ� &pause
	goto :eof

:WIRELESS
	netsh interface ip set address name="������������" source=static addr=172.21.109.222 mask=255.255.255.0 gateway=172.21.109.1
	echo IP��ַ���óɹ�
	netsh dnsclient delete dnsservers "������������" all
	netsh interface ip add dns "������������" 202.202.0.33
	netsh interface ip add dns "������������" 202.202.0.34 index=2
	echo DNS���������óɹ� &pause
	goto :eof

:HOMEWIRE
	netsh interface ip set address name="������������" source=static addr=192.168.0.168 mask=255.255.255.0 gateway=192.168.0.1
	echo IP��ַ���óɹ�
	netsh dnsclient delete dnsservers "������������" all
	netsh interface ip add dns "������������" 10.0.1.17
	netsh interface ip add dns "������������" 10.0.1.20 index=2
	echo DNS���������óɹ� &pause
	goto :eof

:EXIT
	echo Good bye,See you next time. &pause
	goto :eof