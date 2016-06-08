# -*- coding: utf-8 -*-
import paramiko, sys, pymysql

def MysqlQuery():
	conn = pymysql.client(host='localhsot', port=3306, user='root', password='cy.admin.156', db='mysql')
	cur = conn.cursor()
	cur.execute("show status like 'Threads_connected'")

	for row in cur:
		if row[1] >= sys.argv[1] and row[1] < sys.argv[2]:
			print("Warning Connections %s" % row[1])
        	cur.close()
        	conn.close()
		elif row[1] >= sys.argv[2]:
        	print("Critical Connectios %s" % row[1])
        	cur.close()
        	conn.close()
        else:
        	print("O.K Connections %s" % row[1])
        	cur.close()
        	conn.close()

def SSHConnection(host, port, user="guest", passwd="guest"):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, port, username=user, password=passwd)

	session = ssh.get_transport().open_session()
	session.get_pty()

	return ssh, session

ssh, session = SSHConnection('211.61.155.156', 22, "cyebiz", "Cyebiz2014admin")
session.MysqlQuery()

#session.exec_command("/usr/local/mysql/bin/mysql -h localhost -u root -pcy.admin.156 -e \"show status like 'Threads_connected'\"")

print(session.recv(1024))

session.close()
ssh.close()
