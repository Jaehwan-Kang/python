import sys, os, datetime
import paramiko
from scp import SCPClient

# 백업 경로 설정
dbdir = "/Backup/DB_DATA"
imgdir = "/Backup/IMAGE_DATA"
webdir = "/Backup/WEB_DATA"

# 아규먼트에 따른 백업 대상 설정
TARGET = sys.argv[1]


# 백업 클래스
class teamboxBakcup:

    # 디비 백업 함수 (os 명령어 이용한 mysqldump)
    def dbbackup(self):
        dbhost = "db.teamboxcloud.com"
        db = "teambox"
        dbuser = "namucloud"
        dbpasswd = "skanzmffkdnem$%"
        date = datetime.date.today()
        os.popen("mysqldump -u %s -p%s -h %s %s > %s/%s.%s.sql" % (dbuser, dbpasswd, dbhost, db, dbdir, date, db))

    # 웹소스 백업 함수(os 명령어 이용한 tar 압축)
    def webbackup(self):
        target = "/home/teambox/public_html"
        date = datetime.date.today()
        os.popen("tar zcf %s/teambox.%s.tgz %s" % (webdir, date, target))

    # 이미지 백업 함수 (paramiko 이용한 scp)
    def imgbackup(self):
        date = datetime.date.today()
        DIR = imgdir + "/" + str(date)
        os.mkdir(DIR)
        os.chdir(DIR)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('img.teamboxcloud.com', username='teambox',password='inity!@#$',port=7777)

        scp = SCPClient(ssh.get_transport())
        scp.get('/home/teambox/public_html/index.html')

        ssh.close()

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