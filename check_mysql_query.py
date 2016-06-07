# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='information_schema')

cur = conn.cursor()

result = cur.execute("show status like 'Threads_connected'")

print(result[1])
#for row in cur:
#    print(row[1])

cur.close()
conn.close()