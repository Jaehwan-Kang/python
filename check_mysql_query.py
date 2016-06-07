# /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql

conn = pymysql.connect(host='db.sumradio.com', port=3306, user='root', passwd='cy.admin.235', db='content')

cur = conn.cursor()

cur.execute("SELECT * FROM `information_schema`.`PROCESSLIST` LIMIT 1000")

for row in cur:
    print(row[0])

cur.close()
conn.close()