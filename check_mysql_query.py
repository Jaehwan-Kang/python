# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='information_schema')

cur = conn.cursor()

cur.execute("show status like 'Threads_connected'")

print(cur[1])

cur.close()
conn.close()