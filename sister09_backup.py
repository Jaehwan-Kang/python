#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Usage) #./sister09_backup.py [web|db|conf]
#

import sys, os, datetime

# 백업 경로 설정
dbdir = "/backup/db"
confdir = "/backup/conf"
webdir = "/backup/web"

# 호출할 백업 함수
TARGET = sys.argv[1]

# 백업 클래스
class Bakcup:

    date = datetime.date.today()
    rdate = date - datetime.timedelta(weeks=12)

    # 디비 백업 함수 (os 명령어 이용한 mysqldump)
    def dbbackup(self):
        dbhost = ""
        db = ""
        db2 = ""
        dbuser = ""
        dbpasswd = ""

        # SQL DUMP
        os.popen("/mysql/bin/mysqldump -u %s -p%s -h %s %s > %s/%s.%s.sql" % (dbuser, dbpasswd, dbhost, db, dbdir, date, db))
        os.popen("/mysql/bin/mysqldump -u %s -p%s -h %s %s > %s/%s.%s.sql" % (dbuser, dbpasswd, dbhost, db2, dbdir, date, db2))
        # 12 Weeks ago File DELETE
        os.popen("/usr/bin/rm -rf %s/%s.*" % (dbdir, rdate))

    # 웹소스 백업 함수(os 명령어 이용한 tar 압축)
    def webbackup(self):
        target = [ 'baby09', 'sister09', 'thankyoudealer']

        for i in target:
            os.popen("tar jcf %s/%s.%s.bz2 /home/%s --exclude=sess_*" % (webdir, i, date, target))
            os.popen("rm -rf %s/%s.%s.bz2" % (webdir, i, rdate))

    # 설정파일 백업 함수
    def confbackup(self):
        os.popen("tar jcf %s/nginx_%s.bz2 /etc/nginx" % (confdir, date))
        os.popen("tar jcf %s/php_%s.bz2 /etc/php*" % (confdir, date))

        os.popen("/usr/bin/rm -rf %s/nginx_%s.bz2" % (confdir, rdate))
        os.popen("/usr/bin/rm -rf %s/php_%s.bz2" % (confdir, rdate))


# 아규먼트 비교, 백업 호출
if TARGET.upper() == "DB":
    excute = Bakcup()
    excute.dbbackup()

elif TARGET.upper() == "WEB":
    excute = Bakcup()
    excute.webbackup()

elif TARGET.upper() == "CONF":
    excute = Bakcup()
    excute.confbackup()