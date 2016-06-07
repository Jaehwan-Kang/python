# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='information_schema')

cur = conn.cursor()

cur.execute("show status like 'Threads_connected'")

for row in cur:
    print(row[0])

cur.close()
conn.close()