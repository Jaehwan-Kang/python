# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='mysql')
cur = conn.cursor()
cur.execute("show status like 'Threads_connected'")

for row in cur:
    if row > sys.argv[1] and row < sys.argv[2]:
    print("Warning Connections %s" % row)
    sys.exit(1)
elif row > sys.argv[2]:
    print("Critical Connectios %s" % row)
    sys.exit(2)
else:
    print("O.K Connections %s" % row)

cur.close()
conn.close()

