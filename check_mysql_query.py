# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql, sys

conn = pymysql.connect(host=sys.argv[1], port=3306, user=sys.argv[2], passwd=sys.argv[3], db='information_schema')
cur = conn.cursor()
cur.execute("select count(ID) from PROCESSLIST")

for row in cur:
    if int(row[1]) >= int(sys.argv[4]) and int(row[1]) < int(sys.argv[5]):
        print("Warning Connections %s" % int(row[1]))
        cur.close()
        conn.close()
        sys.exit(1)
    elif int(row[1]) >= int(sys.argv[5]):
        print("Critical Connectios %s" % row[1])
        cur.close()
        conn.close()
        sys.exit(2)
    else:
        print("O.K Connections %s" % row[1])
        cur.close()
        conn.close()
        sys.exit(0)
