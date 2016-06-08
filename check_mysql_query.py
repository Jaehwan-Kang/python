# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql, sys

conn = pymysql.connect(host=sys.argv[1], port=3306, user=sys.argv[2], passwd=sys.argv[3], db='mysql')
cur = conn.cursor()
cur.execute("show status like 'Threads_connected'")

for row in cur:
    if row[1] >= sys.argv[4] and row[1] < sys.argv[5]:
        print("Warning Connections %s" % row[1])
        cur.close()
        conn.close()
        sys.exit(1)
    elif row[1] >= sys.argv[5]:
        print(type(row[1]))
        print(type(sys.argv[5]))
        print("Critical Connectios %s" % row[1])
        cur.close()
        conn.close()
        sys.exit(2)
    else:
        print("O.K Connections %s" % row[1])
        cur.close()
        conn.close()
        sys.exit(0)
