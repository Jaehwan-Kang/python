import sys, os, datetime
import paramiko
from scp import SCPClient

# BackupDIR
dbdir = "/Backup/DB_DATA"
imgdir = "/Backup/IMAGE_DATA"
webdir = "/Backup/WEB_DATA"

TARGET = sys.argv[1]


## backup class
class teamboxBakcup:

    # db backup function
    def dbbackup(self):
        dbhost = "db.teamboxcloud.com"
        db = "teambox"
        dbuser = "namucloud"
        dbpasswd = "skanzmffkdnem$%"
        date = datetime.date.today()
        os.popen("mysqldump -u %s -p%s -h %s %s > %s/%s.%s.sql" % (dbuser, dbpasswd, dbhost, db, dbdir, date, db))
    # web backup function
    def webbackup(self):
        target = "/home/teambox/public_html"
        date = datetime.date.today()
        os.popen("tar zcf %s/teambox.%s.tgz %s" % (webdir, date, target))
    # image backup function
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

## target backup
if TARGET.upper() == "DB":
    excute = teamboxBakcup()
    excute.dbbackup()

elif TARGET.upper() == "WEB":
    excute = teamboxBakcup()
    excute.webbackup()

elif TARGET.upper() == "IMAGE":
    excute = teamboxBakcup()
    excute.imgbackup()