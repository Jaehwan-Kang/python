#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, datetime, pysftp

# 백업 경로 설정
dbdir = "/Backup/DB_DATA"
imgdir = "/Backup/IMAGE_DATA"
webdir = "/Backup/WEB_DATA"

# 호출할 백업 함수
TARGET = sys.argv[1]

# 백업 클래스
class teamboxBakcup:

    # 디비 백업 함수 (os 명령어 이용한 mysqldump)
    def dbbackup(self):
        dbhost = ""
        db = ""
        dbuser = ""
        dbpasswd = ""
        date = datetime.date.today()
        os.popen("/usr/local/mysql/bin/mysqldump -u %s -p%s -h %s %s > %s/%s.%s.sql" % (dbuser, dbpasswd, dbhost, db, dbdir, date, db))

    # 웹소스 백업 함수(os 명령어 이용한 tar 압축)
    def webbackup(self):
        target = "/home/teambox/public_html"
        date = datetime.date.today()
        os.popen("tar zcf %s/teambox.%s.tgz %s" % (webdir, date, target))

    # 이미지 백업 함수 (pysftp)
    def imgbackup(self):
        date = datetime.date.today()
        DIR = imgdir + "/" + str(date) + "/"
        os.mkdir(DIR)

        with pysftp.Connection('host', username="", password="", port=) as sftp:
            with sftp.cd('/home/teambox/'):
                #sftp.get('/home/teambox/public_html')

                sftp.get_r('public_html', DIR, preserve_mtime=True,)
        sftp.close()

# 아규먼트 비교, 백업 호출
if TARGET.upper() == "DB":
    excute = teamboxBakcup()
    excute.dbbackup()

elif TARGET.upper() == "WEB":
    excute = teamboxBakcup()
    excute.webbackup()

elif TARGET.upper() == "IMAGE":
    excute = teamboxBakcup()
    excute.imgbackup()