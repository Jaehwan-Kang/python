# /usr/bin/python
# -*- coding: utf-8 -*-

# Load Modules
import pymysql, sys

# Mysql Query Setting
conn = pymysql.connect(host=sys.argv[1], port=3306, user=sys.argv[2], passwd=sys.argv[3], db='mysql')
cur = conn.cursor()
cur.execute("show status like 'Threads_connected'")

# Check Mysql Connections
for row in cur:
    if int(row[1]) >= int(sys.argv[4]) and int(row[1]) < int(sys.argv[5]):
        print("Warning %s Connections" % int(row[1]))
        cur.close()
        conn.close()
        sys.exit(1)
    elif int(row[1]) >= int(sys.argv[5]):
        print("Critical %s Connectios" % int(row[1]))
        cur.close()
        conn.close()
        sys.exit(2)
    else:
        print("O.K %s Connections" % int(row[1]))
        cur.close()
        conn.close()
        sys.exit(0)
