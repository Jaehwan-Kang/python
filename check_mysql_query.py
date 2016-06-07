# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='information_schema')
cur = conn.cursor()
result = cur.execute("show status like 'Threads_connected'")
cur.close()
conn.close()

if result > sys.argv[1] and result < sys.argv[2]:
    print("Warning Connections %s" % result)
    sys.exit(1)
elif result > sys.argv[2]:
    print("Critical Connectios %s" % result)
    sys.exit(2)
else:
    print("O.K Connections %s" % result)